import os
import shutil
import sys
from concurrent import futures
from functools import lru_cache
from typing import Optional

import requests
from dependency_injector.wiring import inject, Provide
from loguru import logger
from tqdm import tqdm

from novelsave.client.cli.helpers.source import get_source_gateway
from novelsave.containers import Application
from novelsave.core.dtos import ChapterDTO
from novelsave.core.entities.novel import Novel
from novelsave.core.services import (
    BasePathService,
    BaseNovelService,
    BaseAssetService,
    BaseFileService,
)
from novelsave.core.services.source import BaseSourceGateway
from novelsave.exceptions import ContentUpdateFailedException, NSError
from novelsave.exceptions import CookieBrowserNotSupportedException
from novelsave.settings import TQDM_CONFIG
from novelsave.utils.adapters import DTOAdapter
from novelsave.utils.helpers import url_helper, string_helper


def set_cookies(source_gateway: BaseSourceGateway, browser: Optional[str]):
    """sets the cookies in source gateway, process skipped if browser is none"""
    if browser is None:
        return

    try:
        source_gateway.use_cookies_from_browser(browser)
    except CookieBrowserNotSupportedException:
        logger.error(f"Extracting cookies from '{browser=}' not supported.")
        sys.exit(1)

    logger.info(f"Extracted and applied cookies from '{browser}'.")


def retrieve_novel_info(source_gateway: BaseSourceGateway, url: str, browser: str):
    set_cookies(source_gateway, browser)

    logger.info(f"Retrieving novel information from {url}…")
    try:
        output = source_gateway.novel_by_url(url)
    except requests.ConnectionError:
        raise NSError(
            "Connection terminated unexpectedly; Make sure you are connected to the internet."
        )

    return output


@inject
def create_novel(
    url: str,
    browser: Optional[str],
    novel_service: BaseNovelService = Provide[Application.services.novel_service],
    path_service: BasePathService = Provide[Application.services.path_service],
) -> Novel:
    """
    retrieve information about the novel from webpage and insert novel into database.
    this includes chapter list and metadata.
    """
    source_gateway = get_source_gateway(url)
    novel_dto = retrieve_novel_info(source_gateway, url, browser)

    novel = novel_service.insert_novel(novel_dto)
    try:
        novel_service.add_url(novel, url)
    except ValueError as e:
        logger.debug("(ERROR) " + str(e))

    novel_service.insert_chapters(novel, novel_dto.volumes)
    novel_service.insert_metadata(novel, novel_dto.metadata)

    chapters = [c for v in novel_dto.volumes for c in v.chapters]
    logger.info(
        f"Added new novel with values: id={novel.id} title='{novel.title}' chapters={len(chapters)}."
    )

    data_dir = path_service.novel_data_path(novel)
    if data_dir.exists():
        logger.debug(
            f"Removing existing data in novel data dir: {{data.dir}}/{path_service.relative_to_data_dir(data_dir)}."
        )
        shutil.rmtree(data_dir)

    return novel


@inject
def update_novel(
    novel: Novel,
    browser: Optional[str],
    novel_service: BaseNovelService = Provide[Application.services.novel_service],
):
    url = novel_service.get_primary_url(novel)
    logger.debug(f"Acquired primary novel url: {url}.")

    source_gateway = get_source_gateway(url)
    novel_dto = retrieve_novel_info(source_gateway, url, browser)

    novel_service.update_novel(novel, novel_dto)
    novel_service.update_chapters(novel, novel_dto.volumes)
    novel_service.update_metadata(novel, novel_dto.metadata)

    chapters = [c for v in novel_dto.volumes for c in v.chapters]
    logger.info(
        f"Novel updated using new values: id={novel.id} title='{novel.title}' chapters={len(chapters)}"
    )
    return novel


@inject
def download_thumbnail(
    novel: Novel,
    force: bool = False,
    novel_service: BaseNovelService = Provide[Application.services.novel_service],
    file_service: BaseFileService = Provide[Application.services.file_service],
    path_service: BasePathService = Provide[Application.services.path_service],
):
    thumbnail_path = path_service.thumbnail_path(novel)
    novel_service.set_thumbnail_asset(
        novel, path_service.relative_to_data_dir(thumbnail_path)
    )

    if not force and thumbnail_path.exists() and thumbnail_path.is_file():
        logger.info("Skipped thumbnail download since file already exists.")
        return

    logger.debug(f"Attempting to download thumbnail from {novel.thumbnail_url}.")
    try:
        response = requests.get(novel.thumbnail_url)
    except requests.ConnectionError:
        raise NSError(
            "Connection terminated unexpectedly; Make sure you are connected to the internet."
        )

    if not response.ok:
        logger.error(
            f"Encountered an error during thumbnail download: {response.status_code} {response.reason}."
        )
        return

    thumbnail_path.parent.mkdir(parents=True, exist_ok=True)
    file_service.write_bytes(thumbnail_path, response.content)

    size = string_helper.format_bytes(len(response.content))
    logger.info(
        f"Downloaded and saved thumbnail image to {novel.thumbnail_path} ({size})."
    )


@inject
def download_chapters(
    novel: Novel,
    limit: Optional[int],
    threads: Optional[int],
    novel_service: BaseNovelService = Provide[Application.services.novel_service],
    asset_service: BaseAssetService = Provide[Application.services.asset_service],
    dto_adapter: DTOAdapter = Provide[Application.adapters.dto_adapter],
):
    chapters = novel_service.get_pending_chapters(novel, limit)
    if not chapters:
        logger.info("Skipped chapter download as none are pending.")
        return

    url = novel_service.get_primary_url(novel)
    logger.debug(f"Acquired primary novel url: {url}.")

    source_gateway = get_source_gateway(url)
    thread_count = (
        min(threads, os.cpu_count()) if threads is not None else os.cpu_count()
    )

    def download(dto: ChapterDTO):
        try:
            return source_gateway.update_chapter_content(dto)
        except Exception as exc:
            raise ContentUpdateFailedException(dto, exc)

    logger.info(
        f"Downloading {len(chapters)} pending chapters with {thread_count} threads…"
    )
    successes = 0
    with tqdm(total=len(chapters), **TQDM_CONFIG) as pbar:
        with futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
            download_futures = [
                executor.submit(download, dto_adapter.chapter_to_dto(c))
                for c in chapters
            ]

            for future in futures.as_completed(download_futures):
                try:
                    chapter_dto = future.result()
                    chapter_dto.content = asset_service.collect_assets(
                        novel, chapter_dto
                    )
                    novel_service.update_content(chapter_dto)

                    logger.debug(
                        f"Chapter content downloaded: '{chapter_dto.title}' ({chapter_dto.index})"
                    )
                    successes += 1
                except ContentUpdateFailedException as e:
                    logger.error(
                        f"An error occurred during content download: {type(e.exception)}."
                    )
                    logger.debug(
                        "An error occurred during content download: {}",
                        type(e.exception),
                    )

                pbar.update(1)

    logger.info(
        f"Chapters download complete, {successes} succeeded, with {len(chapters) - successes} errors."
    )


@inject
def download_assets(
    novel: Novel,
    asset_service: BaseAssetService = Provide[Application.services.asset_service],
    file_service: BaseFileService = Provide[Application.services.file_service],
    path_service: BasePathService = Provide[Application.services.path_service],
):
    pending = asset_service.pending_assets(novel)
    if not pending:
        logger.info("Skipped assets download as none are pending.")
        return

    logger.info(f"Downloading pending assets (count={len(pending)}).")
    for asset in tqdm(pending, **TQDM_CONFIG):
        response = requests.get(asset.url)
        if not response.ok:
            logger.error(f"Error during asset download: {asset.url} ({asset.id}).")
            continue

        file = path_service.asset_path(novel, asset)
        file.parent.mkdir(parents=True, exist_ok=True)

        file_service.write_bytes(file, response.content)

        asset.path = str(path_service.relative_to_data_dir(file))
        asset_service.update_asset_path(asset)

        logger.debug(f"Asset downloaded and saved: {asset.url} ({asset.id}).")

    logger.info("Assets download complete.")


@lru_cache(maxsize=1)
@inject
def get_novel(
    id_or_url: str,
    silent: bool = False,
    novel_service: BaseNovelService = Provide[Application.services.novel_service],
) -> Novel:
    """retrieve novel is it exists in the database otherwise return none

    :raises ValueError: if novel does not exist
    """

    is_url = url_helper.is_url(id_or_url)
    if is_url:
        novel = novel_service.get_novel_by_url(id_or_url)
    else:
        try:
            novel = novel_service.get_novel_by_id(int(id_or_url))
        except ValueError:
            logger.error(f"Value provided is neither a url or an id: {id_or_url}.")
            sys.exit(1)

    if not novel:
        quote = "'" if is_url else ""
        msg = f"Novel not found: {quote}{id_or_url}{quote}."

        logger.info(msg)
        raise ValueError(msg)

    if not silent:
        logger.info(f"Acquired '{novel.title}' ({novel.id}) from database.")

    return novel


@inject
def get_or_create_novel(
    id_or_url: str,
) -> Novel:
    """retrieve specified novel from database or web-crawl and create the novel"""
    novel = get_novel(id_or_url)

    if novel is None:
        if not id_or_url.startswith("http"):
            sys.exit(1)

        novel = create_novel(id_or_url)

    return novel

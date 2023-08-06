from functools import lru_cache
from typing import List

import novelsave_sources
import requests
from novelsave_sources import (
    novel_source_types,
    locate_novel_source,
    locate_metadata_source,
    UnknownSourceException,
)

from .meta_source_gateway import MetaSourceGateway
from .source_gateway import SourceGateway
from ...core.services.source import BaseSourceService
from ...exceptions import SourceNotFoundException
from ...utils.adapters import SourceAdapter


class SourceService(BaseSourceService):
    def __init__(self, source_adapter: SourceAdapter):
        self.source_adapter = source_adapter

    @property
    def current_version(self) -> str:
        return novelsave_sources.__version__

    def get_latest_version(self) -> str:
        response = requests.get("https://pypi.org/pypi/novelsave-sources/json")
        if not response.ok:
            raise ConnectionError(
                f"Response received was not valid: GET {response.url} - {response.status_code} {response.reason}"
            )

        data = response.json()
        versions = sorted(
            (v for v in data["releases"].keys() if "a" not in v), reverse=True
        )
        return versions[0]

    @lru_cache(1)
    def source_from_url(self, url: str) -> SourceGateway:
        try:
            return SourceGateway(
                locate_novel_source(url)(), source_adapter=self.source_adapter
            )
        except UnknownSourceException:
            raise SourceNotFoundException(url)

    @lru_cache(1)
    def meta_source_from_url(self, url: str) -> MetaSourceGateway:
        try:
            return MetaSourceGateway(
                locate_metadata_source(url)(), source_adapter=self.source_adapter
            )
        except UnknownSourceException:
            raise SourceNotFoundException(url)

    def get_novel_sources(self) -> List[SourceGateway]:
        return [
            SourceGateway(source_type(), source_adapter=self.source_adapter)
            for source_type in novel_source_types()
        ]

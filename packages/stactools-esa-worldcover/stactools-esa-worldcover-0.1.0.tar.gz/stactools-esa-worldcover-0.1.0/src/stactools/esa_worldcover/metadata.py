import os
from typing import Any, Dict, Optional

import rasterio
import shapely
from pystac import Asset, MediaType
from pystac.extensions.projection import AssetProjectionExtension
from pystac.utils import make_absolute_href, str_to_datetime
from stactools.core.io import ReadHrefModifier

from stactools.esa_worldcover.constants import ASSET_PROPS


class Metadata():

    def __init__(self,
                 href: str,
                 read_href_modifier: Optional[ReadHrefModifier] = None):
        if read_href_modifier:
            modified_href = read_href_modifier(href)
        else:
            modified_href = href
        with rasterio.open(modified_href) as dataset:
            self.bbox = dataset.bounds
            self.transform = list(dataset.transform)[0:6]
            self.shape = dataset.shape
            self.tags = dataset.tags()

        self.href = href
        self.asset_type()

    def asset_type(self) -> None:
        filename = os.path.basename(self.href)
        self.root, _ = os.path.splitext(filename)
        self.type = self.root.split("_")[-1].lower()

    @property
    def item_id(self) -> str:
        return "_".join(self.root.split("_")[:-1])

    @property
    def geometry(self) -> Dict[str, Any]:
        return shapely.geometry.mapping(shapely.geometry.box(*self.bbox))

    @property
    def tile(self) -> str:
        return self.tags["product_tile"]

    @property
    def asset(self) -> Asset:
        asset = Asset(href=make_absolute_href(self.href))
        asset.roles = ASSET_PROPS[self.type]["roles"]
        asset.title = ASSET_PROPS[self.type]["title"]
        asset.description = ASSET_PROPS[self.type]["description"]
        asset.media_type = MediaType.COG

        extra_fields = {"raster:bands": ASSET_PROPS[self.type]["bands"]}
        if self.type == "map":
            extra_fields["classification:classes"] = ASSET_PROPS[
                self.type]["classes"]
        asset.extra_fields = extra_fields

        proj = AssetProjectionExtension.ext(asset)
        proj.transform = self.transform
        proj.shape = self.shape

        asset.common_metadata.created = str_to_datetime(
            self.tags["creation_time"])

        return asset

    @staticmethod
    def quality_href(map_href: str) -> str:
        base_href = "_".join(map_href.split("_")[:-1])
        return f"{base_href}_InputQuality.tif"

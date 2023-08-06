"""
Dashboard Enums and Models are from:
https://e360-dashboard-service-dev.internal.imsglobal.com/wrapper/documents
"""


from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator
from pydantic.fields import ModelField


class BaseDashboardModel(BaseModel):
    @validator("*")
    def _handle_datetime_as_str(value: Any, field: ModelField) -> Any:
        if field.type_ == datetime and value:
            return str(value)
        return value


class DashboardStatus(str, Enum):
    UNLOCKED = "unlocked"
    LOCKED = "locked"


class TileType(str, Enum):
    STATIC_TEXT = "staticText"
    IMAGE = "image"
    CODELIST_SUMMARY = "codelistSummary"
    DOCUMENT = "document"
    COHORT_DETAILS = "cohortDetails"
    LINK = "link"
    COHORT_GENDER_BREAKDOWN = "cohortGenderBreakdown"
    COHORT_AGE_BREAKDOWN = "cohortAgeBreakdown"
    COHORT_GENDER_AGE_BREAKDOWN = "cohortGenderAgeBreakdown"
    STACK_EVENT_DISTRIBUTION = "stackEventDistribution"
    COHORT_GEOGRAPHIC_BREAKDOWN = "cohortGeographicBreakdown"
    ANALYTIC = "analytic"
    VISUALISATION_PREVIEW = "visualisationPreview"
    SUBHEADING = "subheading"
    COHORT_PREVIEW_DETAILS = "cohortPreviewDetails"
    COHORT_PREVIEW_GENDER_BREAKDOWN = "cohortPreviewGenderBreakdown"
    COHORT_PREVIEW_AGE_BREAKDOWN = "cohortPreviewAgeBreakdown"
    COHORT_PREVIEW_GENDER_AGE_BREAKDOWN = "cohortPreviewGenderAgeBreakdown"
    COHORT_PREVIEW_EVENT_DISTRIBUTION = "cohortPreviewEventDistribution"
    COHORT_PREVIEW_GEOGRAPHIC_BREAKDOWN = "cohortPreviewGeographicBreakdown"


class TileConfigurationModel(BaseDashboardModel):
    title: Optional[str] = None
    show_title: Optional[bool] = Field(alias="showTitle")
    colour_theme: Optional[str] = Field(alias="colourTheme")
    show_border: Optional[bool] = Field(alias="showBorder")


class TileModel(BaseDashboardModel):
    internal_id: Optional[int] = Field(alias="internalId", default=0)
    tile_index: Optional[int] = Field(alias="tileIndex", default=0)
    asset_id: Optional[UUID] = Field(alias="assetId")
    width: Optional[int] = 0
    height: Optional[int] = 0
    x: Optional[int] = 0
    y: Optional[int] = 0
    version: Optional[int] = None
    tile_type: Optional[TileType] = Field(
        alias="tileType", default=TileType.STATIC_TEXT
    )
    tile_configuration: Optional[TileConfigurationModel] = Field(
        alias="tileConfiguration"
    )
    breakdown_configuration: Optional[Dict[str, Any]] = Field(
        alias="breakdownConfiguration"
    )


class DashboardModel(BaseDashboardModel):
    dashboard_status: Optional[DashboardStatus] = Field(
        alias="dashboardStatus", default=DashboardStatus.UNLOCKED
    )
    tiles: Optional[List[TileModel]] = Field(default_factory=list)
    id: Optional[int] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None


class ErrorMessageModel(BaseDashboardModel):
    message: Optional[str] = None
    error_code: Optional[str] = Field(alias="errorCode")
    details: Optional[List[str]] = Field(default_factory=list)


class TabModel(BaseDashboardModel):
    internal_id: Optional[int] = Field(alias="internalId")
    tab_index: Optional[int] = Field(alias="tabIndex", default=0)
    title: Optional[str] = None
    tiles: Optional[List[TileModel]] = Field(default_factory=list)


class TabbedDashboardModel(BaseDashboardModel):
    """Dashboard with tabs for v2 endpoint"""

    dashboard_status: Optional[DashboardStatus] = Field(
        alias="dashboardStatus", default=DashboardStatus.UNLOCKED
    )
    tabs: Optional[List[TabModel]] = Field(default_factory=list)
    id: Optional[int] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None


class VisualisationPublishRequestModel(BaseDashboardModel):
    visualisation_resource_id: Optional[UUID] = Field(alias="visualisationResourceId")
    title: Optional[str] = None
    version: Optional[int] = None


class PublishedDashboardRequestModel(BaseDashboardModel):
    original_dashboard_id: Optional[int] = Field(alias="originalDashboardId")
    id: Optional[UUID] = None
    name: Optional[str] = None
    type: Optional[str] = None
    visualizations: Optional[Dict[str, VisualisationPublishRequestModel]] = None
    asset_data: Optional[Dict[str, Any]] = Field(alias="assetData")
    is_preview: Optional[bool] = Field(alias="isPreview")


class PublishedTileModel(BaseDashboardModel):
    version: Optional[int] = None
    tile_index: Optional[int] = Field(alias="tileIndex")
    asset_id: Optional[UUID] = Field(alias="assetId")
    width: Optional[int] = None
    height: Optional[int] = None
    x: Optional[int] = None
    y: Optional[int] = None
    tile_type: Optional[TileType] = Field(
        alias="tileType", default=TileType.STATIC_TEXT
    )
    tile_configuration: Optional[TileConfigurationModel] = Field(
        alias="tileConfiguration"
    )
    breakdown_configuration: Optional[Dict[str, Any]] = Field(
        alias="breakdownConfiguration"
    )


class PublishedTabModel(BaseDashboardModel):
    tab_index: Optional[int] = Field(alias="tabIndex")
    title: Optional[str] = None
    tiles: Optional[List[PublishedTileModel]] = Field(default_factory=list)


class PublishedTabModelDashboardModel(BaseDashboardModel):
    dashboard_status: Optional[DashboardStatus] = Field(
        alias="dashboardStatus", default=DashboardStatus.UNLOCKED
    )
    tabs: Optional[List[PublishedTabModel]] = Field(default_factory=list)
    id: Optional[int] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None


class DashboardUserModel(BaseDashboardModel):
    email: Optional[str] = None
    access_token: Optional[str] = Field(alias="accessToken")
    create_date: Optional[datetime] = Field(alias="createDate")


class DashboardUserStatisticsEntryModel(BaseDashboardModel):
    viewed_date: Optional[datetime] = Field(alias="viewedDate")
    ip: Optional[str] = None
    access_token: Optional[str] = Field(alias="accessToken")


class DashboardUserStatisticsModel(BaseDashboardModel):
    viewed: Optional[int] = None
    last_viewed: Optional[datetime] = Field(alias="lastViewed")
    history: Optional[List[DashboardUserStatisticsEntryModel]] = Field(
        default_factory=list
    )


class PublishedDashboardModel(BaseDashboardModel):
    dashboard: Optional[PublishedTabModelDashboardModel] = None
    users: Optional[Dict[str, DashboardUserModel]] = None
    statistics: Optional[Dict[str, DashboardUserStatisticsModel]] = None
    name: Optional[str] = None
    type: Optional[str] = None
    asset_data: Optional[Dict[str, Any]] = Field(alias="assetData")
    version: Optional[int] = None
    is_preview: Optional[bool] = Field(alias="isPreview")
    id: Optional[UUID] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None


class DashboardUserViewModel(BaseDashboardModel):
    email: Optional[str] = None
    ip: Optional[str] = None
    access_token: Optional[str] = Field(alias="accessToken")


class TileTypeModel(BaseDashboardModel):
    name: Optional[str] = None
    description: Optional[str] = None
    minimum_height: Optional[int] = Field(alias="minimumHeight")
    maximum_height: Optional[int] = Field(alias="maximumHeight")
    minimum_width: Optional[int] = Field(alias="minimumWidth")
    maximum_width: Optional[int] = Field(alias="maximumWidth")
    default_height: Optional[int] = Field(alias="defaultHeight")
    default_width: Optional[int] = Field(alias="defaultWidth")
    asset_type: Optional[str] = Field(alias="assetType")
    id: Optional[TileType] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None

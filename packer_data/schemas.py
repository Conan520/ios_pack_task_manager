from typing import List, Optional, Dict

from pydantic import BaseModel, constr


class InfoItem(BaseModel):
    path: str
    branch: str
    commit_id: Optional[str]


class EngineInfo(BaseModel):
    EngineInfoItems: List[InfoItem]


class ProjectInfo(BaseModel):
    ContentDefaultInfo: InfoItem
    PluginsInfo: List[InfoItem]
    SelfInfo: InfoItem


class ShellProjectInfo(BaseModel):
    ProjectsInfo: List[ProjectInfo]


class IOSPluginsInfo(BaseModel):
    id: Optional[int]
    ip: constr(max_length=20)
    cicd_tag: Optional[constr(max_length=50)]
    engine_info: Optional[Dict]
    projects_info: Optional[Dict]

    class Config:
        orm_mode = True


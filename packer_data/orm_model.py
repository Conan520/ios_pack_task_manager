from typing import Optional, Dict

from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class IOSPluginsInfoTable(Base):
    __tablename__ = "ios_plugins_info"
    id: Optional[int] = Column(Integer, primary_key=True)
    ip: str = Column(String(20))
    cicd_tag: Optional[str] = Column(String(50))
    engine_info = Column(JSON)
    projects_info = Column(JSON)

    def __init__(self, *, id: Optional[int] = None, ip: str, cicd_tag: str, engine_info: Dict, projects_info: Dict):
        if id is not None:
            self.id = id
        self.ip = ip
        self.cicd_tag = cicd_tag
        self.engine_info = engine_info
        self.projects_info = projects_info

    def __repr__(self):
        return f"{__class__.__name__}(id={self.id!r}, name={self.cicd_tag!r}, " \
               f"engine_info={self.engine_info!r}, plugins_info={self.projects_info!r})"




from sqlalchemy import Column, String, UUID, ForeignKey, Integer
from .database import Base

class AnalysisResult(Base):
    __tablename__ = 'analysis'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    content = Column(String)
    hash = Column(String(64))
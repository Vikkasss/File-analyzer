from sqlalchemy import Column, String, UUID
from .database import Base

class File(Base):
    __tablename__ = 'files'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String)
    hash = Column(String(64))
    location = Column(String)
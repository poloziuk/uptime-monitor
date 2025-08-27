from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class CheckResult(Base):
    __tablename__ = "checks"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    status = Column(Boolean, nullable=False)
    response_time = Column(Integer)  # мс
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)


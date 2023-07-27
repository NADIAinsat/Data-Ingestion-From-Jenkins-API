from jenkins_api import jenkinsAPI
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship
import database_connection

server = jenkinsAPI.server
session = database_connection.session
engine = database_connection.engine

# Create the base class for declarative models
Base = declarative_base()


# Define the Job model
class Job(Base):
    __tablename__ = 'job'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    running = Column(String)
    enabled = Column(String)
    lastBuild = Column(String)
    queued = Column(String)
    Insert_Date = Column(DateTime, default=func.now())


# Define the Build model
class Build(Base):
    __tablename__ = 'builds'
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('job.id'))
    # to access the related objects from either side of the relationship.
    # job = relationship("Job", back_populates="builds")
    build = Column(String)
    number = Column(String)
    description = Column(String)
    timestamp = Column(DateTime(timezone=True))
    url = Column(String)
    duration = Column(String)
    status = Column(String)
    running = Column(String)
    upstream_job_name = Column(String)
    Insert_Date = Column(DateTime(timezone=True), default=func.now())


# Create the tables
Base.metadata.create_all(engine)

# Close the session
session.close()

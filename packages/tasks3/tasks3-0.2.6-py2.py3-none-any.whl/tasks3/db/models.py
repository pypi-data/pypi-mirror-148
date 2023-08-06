"""Task database model"""
import uuid

from sqlalchemy import (
    CheckConstraint,
    Column,
    Integer,
    JSON,
    Unicode,
    UnicodeText,
    String,
)
from sqlalchemy.ext.declarative import as_declarative, declared_attr

UUID_LENGTH = 6


@as_declarative()
class Base:
    """Declarative base class for SQLAlchemy models"""

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(
        String(length=UUID_LENGTH),
        primary_key=True,
        default=lambda: str(uuid.uuid4())[:UUID_LENGTH],
    )


class Task(Base):
    """
    Task Model

    SQLAlchemy declarative model for the tasks3 database containing tasks.

    Attributes:
        id: Unique ID for the task.
        title: Title of the task.
        urgency: Urgency level[0-4] of the task.
        importance: Importance level[0-4] of the task.
        tags: Set of tags to apply to the task.
        folder: Anchor this task to a particular directory or file.
        description: Description of the task.
    """

    title = Column(Unicode, nullable=False)
    urgency = Column(Integer, nullable=False)
    importance = Column(Integer, nullable=False)
    tags = Column(JSON, nullable=False)
    folder = Column(Unicode, nullable=True)
    description = Column(UnicodeText, nullable=True)

    __table_args__ = (
        CheckConstraint(0 <= urgency, "Urgency interval check"),
        CheckConstraint(urgency <= 4, "Urgency interval check"),
        CheckConstraint(0 <= importance, "Importance interval check"),
        CheckConstraint(importance <= 4, "Importance interval check"),
    )

    def to_dict(self) -> dict:
        return dict(
            id=self.id,
            title=self.title,
            urgency=self.urgency,
            importance=self.importance,
            tags=self.tags,
            folder=self.folder,
            description=self.description,
        )

    def __repr__(self) -> str:
        return f"<Task{self.to_dict().__repr__()}>"

from datetime import datetime
from enum import StrEnum
from django.db import models

# Create your models here.

from abc import ABC, abstractmethod


class BaseEnitity(ABC):

    @abstractmethod
    def validate(self):
        pass

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items()}


class Team(StrEnum):
    BACKEND = "backend"
    FRONTEND = "frontend"
    QA = "qa"
    DEVOPS = "devops"


class Reporter(BaseEnitity):

    def __init__(self, id: int, name: str, email: str, team: str):
        self.id = id
        self.name = name
        self.email = email
        self.team = team

    def validate(self):
        if not self.name:
            raise ValueError("Name cannot be empty")
        if "@" not in self.email:
            raise ValueError("Invalid email")
        if self.team not in Team:
            allowed = ", ".join(t.value for t in Team)
            error = f"Invalid team '{self.team}'. Allowed values: {allowed}"
            raise ValueError(error)
        self.team = Team(self.team)


class Status(StrEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class Priority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Issue(BaseEnitity):

    def __init__(
        self,
        id: int,
        title: str,
        description: str,
        status: str,
        prioirty: str,
        reporter_id: int,
        created_at: str | None = None,
    ):
        self.created_at = created_at or datetime.now().isoformat()
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = prioirty
        self.reporter_id = reporter_id

    def validate(self):
        if not self.title:
            raise ValueError("Title cannot be empty")
        if not self.description:
            raise ValueError("Description cannot be empty")
        if self.status not in Status:
            allowed = ", ".join(s.value for s in Status)
            raise ValueError(
                f"Invalid status '{self.status}'. Allowed values: {allowed}"
            )
        if self.priority not in Priority:
            allowed = ", ".join(p.value for p in Priority)
            raise ValueError(
                f"Invalid priority '{self.priority}'. Allowed values: {allowed}"
            )
        if not isinstance(self.reporter_id, int) or self.reporter_id <= 0:
            raise ValueError("reporter_id must be a positive integer")
        self.status = Status(self.status)
        self.priority = Priority(self.priority)

    def describe(self):
        return f"{self.title} [{self.priority}]"


class CriticalIssue(Issue):

    def describe(self):
        return f"[URGENT] {self.title} - needs immediate attention"


class LowPriorityIssue(Issue):

    def describe(self):
        return f"{self.title} - low priority, handle when free"

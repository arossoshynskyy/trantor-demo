import json
from uuid import uuid4
from datetime import datetime
from dataclasses import dataclass


class Event:
    def __post_init__(self):
        self.event_type =  self.__class__.__name__
        self.id = str(uuid4())
        self.created_at = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z')

    def to_json(self):
        return json.dumps(vars(self))

@dataclass
class DeploymentCreatedEvent(Event):
    deployment_id: str


@dataclass
class DeploymentFailedEvent(Event):
    deployment_id: str
    reason: str

@dataclass
class DeploymentSuccessEvent(Event):
    deployment_id: str

@dataclass
class PackagingFailedEvent(Event):
    deployment_id: str
    reason: str

@dataclass
class PackagingSuccessEvent(Event):
    deployment_id: str
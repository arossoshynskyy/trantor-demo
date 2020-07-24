import logging

from tinydb import Query

from app import steps
from app.events.router import EventRouter
from app.events.event_bus import put_event
from app.events.events import DeploymentCreatedEvent
from app import event_handler
from app.db import get_db

logger = logging.getLogger(__name__)


router = EventRouter()


def get_deployments():
    return get_db().search(Query().document_id.exists())

def get_deployment(deployment_id):
    return get_db().get(deployment_id)

def create_deployment(body):
    """ save deploymen to db, create DeploymentCreatedEvent """

    deployment_id = get_db().insert(body)
    logger.debug(f"Created new deployment {deployment_id}")

    put_event(DeploymentCreatedEvent(deployment_id))
    
    return get_db().get(deployment_id)

def delete_deployment(deployment_id):
    get_db().remove(deployment_id)

def handle_event(body):
    event_handler.handle_event(body)

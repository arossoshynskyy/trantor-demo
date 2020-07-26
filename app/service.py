import logging

from tinydb import Query

from app.steps import (
    package,
    deploy,
)
from app.db import get_db
from app.events.event_bus import put_event
from app.events.events import (
    DeploymentCreatedEvent,
    DeploymentFailedEvent,
    DeploymentSuccessEvent,
    PackagingFailedEvent,
    PackagingSuccessEvent,
)
from app.notifications import (
    notify_deployment_success, 
    notify_deployment_failed,
)

logger = logging.getLogger(__name__)


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

def handle_deployment_created(body):
    """ New deployment created, call package step """
    try:
        deployment = get_db().get(body["deployment_id"])
        package(deployment)
        
        put_event(PackagingSuccessEvent(body["deployment_id"]))
    except:
        put_event(PackagingFailedEvent(body["deployment_id"]))

def handle_packaging_success(body):
    """ Packaging successful, start deployment step"""
    try:
        deployment = get_db().get(body["deployment_id"])
        deploy(deployment)

        put_event(DeploymentSuccessEvent(body["deployment_id"]))
    except:
        put_event(DeploymentFailedEvent(body["deployment_id"]))

def handle_packaging_failed(body):
    """ Notify user on slack about packaging failure """
    notify_deployment_failed()

def handle_deployment_success(body):
    """ Deployment successful notify slack user and tech-release"""
    notify_deployment_success()

def handle_deployment_failed(body):
    """ Notify user on slack about deployment failure """
    notify_deployment_failed()
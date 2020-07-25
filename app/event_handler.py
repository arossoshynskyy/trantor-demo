from app.db import get_db
from app.events.router import EventRouter
from app.steps import deploy, package
from app.events.event_bus import put_event
from app.events.events import (
    DeploymentFailedEvent,
    DeploymentSuccessEvent,
    PackagingFailedEvent,
    PackagingSuccessEvent,
)
from app.notifications import (
    notify_deployment_success, 
    notify_deployment_failed,
)

router = EventRouter()

def handle_event(body):
    router.handle(body)

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
    notify_packaging_failed()

def handle_deployment_success(body):
    """ Deployment successful notify slack user and tech-release"""
    notify_deployment_success()

def handle_deployment_failed(body):
    """ Notify user on slack about deployment failure """
    notify_deployment_failed()

router.register_handler("DeploymentCreatedEvent", handle_deployment_created)
router.register_handler("PackagingSuccessEvent", handle_packaging_success)
router.register_handler("PackagingFailedEvent", handle_packaging_failed)
router.register_handler("DeploymentFailedvent", handle_deployment_failed)
router.register_handler("DeploymentSuccessEvent", handle_deployment_success)

import logging

from app.events import router
from app import service

logger = logging.getLogger(__name__)


def get_deployments():
    return service.get_deployments()

def get_deployment(deployment_id):
    return service.get_deployment(deployment_id)

def create_deployment(body):
    return service.create_deployment(body)

def delete_deployment(deployment_id):
    service.delete_deployment(deployment_id)


def handle_event(body):
    router.handle(body)

@router.event_handler("DeploymentCreatedEvent")
def handle_deployment_created(body):
    service.handle_deployment_created(body)

@router.event_handler("PackagingSuccessEvent")
def handle_packaging_success(body):
    service.handle_packaging_success(body)

@router.event_handler("PackagingFailedEvent")
def handle_packaging_failed(body):
    service.handle_packaging_failed(body)

@router.event_handler("DeploymentFailedEvent")
def handle_deployment_failed(body):
    service.handle_deployment_failed(body)

@router.event_handler("DeploymentSuccessEvent")
def handle_deployment_success(body):
    service.handle_deployment_success(body)
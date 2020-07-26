import logging

from app.events.router import EventRouter
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


router = EventRouter()
router.register_handler("DeploymentCreatedEvent", service.handle_deployment_created)
router.register_handler("PackagingSuccessEvent", service.handle_packaging_success)
router.register_handler("PackagingFailedEvent", service.handle_packaging_failed)
router.register_handler("DeploymentFailedvent", service.handle_deployment_failed)
router.register_handler("DeploymentSuccessEvent", service.handle_deployment_success)

def handle_event(body):
    router.handle(body)

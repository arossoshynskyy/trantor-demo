from datetime import datetime

import boto3
import settings

from app.events.exceptions import EventDeliveryError


def put_event(event):
    response = boto3.client("events").put_events(
        Entries=[
            {
                'Time': datetime.now(),
                'Source': settings.EVENT_SOURCE,
                'Resources': [],
                'DetailType': event.event_type,
                'Detail': event.to_json(),
                'EventBusName': settings.TRANTOR_EVENT_BUS
            },
        ]
    )

    if response["FailedEntryCount"] > 0:
        raise EventDeliveryError(response["FailedEntryCount"], settings.TRANTOR_EVENT_BUS)

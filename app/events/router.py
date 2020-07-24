from app.events.exceptions import EventRoutingError


class EventRouter:
    handlers = {}
    
    def register_handler(self, event_type, func):
        self.handlers[event_type] = func

    def handle(self, event):
        handler = self.handlers.get(event.event_type)

        if not handler:
            raise EventRoutingError(event.event_type)

        handler(event)
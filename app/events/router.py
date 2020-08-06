from app.events.exceptions import EventRoutingError


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class EventRouter(metaclass=Singleton):
    handlers = {}
    
    def register_handler(self, event_type, func):
        self.handlers[event_type] = func

    def event_handler(self, event_type):
        def wrapper(func):
            self.register_handler(event_type, func)
            return func
        return wrapper

    def handle(self, event):
        handler = self.handlers.get(event.event_type)

        if not handler:
            raise EventRoutingError(event.event_type)

        handler(event)


router = EventRouter()
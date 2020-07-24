class EventRoutingError(Exception):
    def __init__(self, event_type):
        self.event_type = event_type
        super().__init__(f"No handler registered for {self.event_type}")

class EventDeliveryError(Exception):
    def __init__(self, failed_delivery_count, event_bus):
        self.failed_delivery_count = failed_delivery_count
        self.event_bus = event_bus
        super().__init__(f"Failed to deliver {self.failed_delivery_count} events to {self.event_bus}")

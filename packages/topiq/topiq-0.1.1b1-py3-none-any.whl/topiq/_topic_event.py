from threading import Event


class _TopicEvent(Event):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def async_wait(self):
        self.wait()


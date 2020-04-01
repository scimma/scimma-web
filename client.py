from confluent_kafka import Consumer, Producer
from confluent_kafka.admin import AdminClient


class ScimmaClientWrapper:
    def __init__(self, *args, **opts):
        self.consumer = Consumer(opts)
        self.producer = Producer(opts)
        self.admin_client = AdminClient(opts)

    def topics(self):
        return [topic_name for topic_name, topic_metadata in self.admin_client.list_topics().topics.items()]
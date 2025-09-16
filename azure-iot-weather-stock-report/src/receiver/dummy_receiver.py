"""
DummyReceiver: subscribes to a Service Bus Topic subscription and prints each summary.
"""
from __future__ import annotations
from dataclasses import dataclass
from ..servicebus.sb_client import ServiceBusTopicClient

@dataclass
class DummyReceiver:
    sb_conn_str: str
    topic: str
    subscription: str

    def run(self) -> None:
        client = ServiceBusTopicClient(self.sb_conn_str, self.topic, self.subscription)

        def on_msg(d):
            summary = d.get("summary") or d
            print(summary)

        client.receive_forever(on_msg)

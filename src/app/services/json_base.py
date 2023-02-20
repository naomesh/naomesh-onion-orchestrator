import json
import time
import uuid
from typing import Any, Dict, Tuple, Union

PROTOCOL_VERSION = "tomodachi-json-base--1.0.0"


class JsonBase(object):
    @classmethod
    async def build_message(
        cls, service: Any, topic: str, data: Any, **kwargs: Any
    ) -> str:
        data_encoding = "raw"

        message = {
            "service": {
                "name": getattr(service, "name", None),
                "uuid": getattr(service, "uuid", None),
            },
            "metadata": {
                "message_uuid": f'{getattr(service, "uuid", "")}.{str(uuid.uuid4())}',  # noqa: E501
                "protocol_version": PROTOCOL_VERSION,
                "compatible_protocol_versions": ["json_base-wip"],
                "timestamp": time.time(),
                "topic": topic,
                "data_encoding": data_encoding,
            },
            **data,
        }
        return json.dumps(message)

    @classmethod
    async def parse_message(
        cls, payload: str, **kwargs: Any
    ) -> Union[Dict, Tuple]:
        message = json.loads(payload)

        message_uuid = message.get("metadata", {}).get("message_uuid")
        timestamp = message.get("metadata", {}).get("timestamp")

        return (
            {
                **message,
                "service": {
                    "name": message.get("service", {}).get("name"),
                    "uuid": message.get("service", {}).get("uuid"),
                },
                "metadata": {
                    "message_uuid": message.get("metadata", {}).get(
                        "message_uuid"
                    ),
                    "protocol_version": message.get("metadata", {}).get(
                        "protocol_version"
                    ),
                    "timestamp": message.get("metadata", {}).get("timestamp"),
                    "topic": message.get("metadata", {}).get("topic"),
                    "data_encoding": message.get("metadata", {}).get(
                        "data_encoding"
                    ),
                },
            },
            message_uuid,
            timestamp,
        )


__all__ = [
    "PROTOCOL_VERSION",
    "JsonBase",
]

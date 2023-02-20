# flake8: noqa

# Simon: Yet another monkey patching for changing the topic
# Internals of tomadochi
# Basically, all this file does is to change the exchange type by grabbing the current one in the service class

import asyncio
import logging
from typing import Any, Callable, Dict, Optional

import aioamqp
from tomodachi.helpers.execution_context import set_execution_context
from tomodachi.options import Options
from tomodachi.transport.amqp import (
    AmqpException,
    AmqpExclusiveQueueLockedException,
    AmqpTooManyConsumersException,
    AmqpTransport,
)


@classmethod
async def subscribe(cls, obj: Any, context: Dict) -> Optional[Callable]:
    if context.get("_amqp_subscribed"):
        return None
    context["_amqp_subscribed"] = True

    set_execution_context(
        {
            "amqp_enabled": True,
            "amqp_current_tasks": 0,
            "amqp_total_tasks": 0,
            "aioamqp_version": aioamqp.__version__,
        }
    )

    cls.channel = None
    channel = await cls.connect(obj, context)
    options: Options = cls.options(context)
    await channel.basic_qos(
        prefetch_count=options.amqp.qos.queue_prefetch_count,
        prefetch_size=0,
        connection_global=False,
    )
    await channel.basic_qos(
        prefetch_count=options.amqp.qos.global_prefetch_count,
        prefetch_size=0,
        connection_global=True,
    )

    async def _subscribe() -> None:
        async def declare_queue(
            routing_key: str,
            func: Callable,
            exchange_name: str = "",
            exchange_type: str = obj.exchange_type,
            queue_name: Optional[str] = None,
            passive: bool = False,
            durable: bool = True,
            exclusive: bool = False,
            auto_delete: bool = False,
            competing_consumer: Optional[bool] = None,
        ) -> Optional[str]:
            try:
                if exchange_name and exchange_name != "amq.topic":
                    await channel.exchange_declare(
                        exchange_name=exchange_name,
                        type_name=exchange_type,
                        passive=False,
                        durable=True,
                        auto_delete=False,
                    )
            except aioamqp.exceptions.ChannelClosed as e:
                error_message = e.args[1]
                if e.args[0] == 403 and exchange_name.startswith("amq."):
                    logging.getLogger("transport.amqp").warning(
                        'Unable to declare exchange [amqp] "{}", starts with reserved "amq." ({})'.format(
                            exchange_name, error_message
                        )
                    )
                    raise
                elif e.args[0] == 507 or e.args[0] == 406:
                    logging.getLogger("transport.amqp").warning(
                        'Unable to change type of existing exchange [amqp] "{}" ({})'.format(
                            exchange_name, error_message
                        )
                    )
                    raise
                else:
                    logging.getLogger("transport.amqp").warning(
                        'Unable to declare exchange [amqp] "{}" ({})'.format(
                            exchange_name, error_message
                        )
                    )
                    raise

            if queue_name and competing_consumer is None:
                competing_consumer = True

            _uuid = obj.uuid
            max_consumers = 1 if not competing_consumer else None

            if queue_name is None:
                queue_name = cls.get_queue_name(
                    cls.encode_routing_key(routing_key),
                    func.__name__,
                    _uuid,
                    competing_consumer,
                    context,
                )
            else:
                queue_name = cls.prefix_queue_name(queue_name, context)

            amqp_arguments = {}
            ttl = options.amqp.queue_ttl
            if ttl:
                amqp_arguments["x-expires"] = int(ttl * 1000)

            try:
                data = await channel.queue_declare(
                    queue_name,
                    passive=passive,
                    durable=durable,
                    exclusive=exclusive,
                    auto_delete=auto_delete,
                    arguments=amqp_arguments,
                )
                if (
                    max_consumers is not None
                    and data.get("consumer_count", 0) >= max_consumers
                ):
                    logging.getLogger("transport.amqp").warning(
                        'Max consumers ({}) for queue [amqp] "{}" has been reached'.format(
                            max_consumers, queue_name
                        )
                    )
                    raise AmqpTooManyConsumersException(
                        "Max consumers for this queue has been reached"
                    )
            except aioamqp.exceptions.ChannelClosed as e:
                if e.args[0] == 405:
                    raise AmqpExclusiveQueueLockedException(str(e)) from e
                raise AmqpException(str(e)) from e

            await channel.queue_bind(
                queue_name,
                exchange_name or "amq.topic",
                cls.encode_routing_key(
                    cls.get_routing_key(routing_key, context)
                ),
            )

            return queue_name

        def callback(routing_key: str, handler: Callable) -> Callable:
            async def _callback(
                self: Any, body: bytes, envelope: Any, properties: Any
            ) -> None:
                # await channel.basic_reject(delivery_tag, requeue=True)
                await asyncio.shield(
                    handler(
                        body.decode(),
                        envelope.delivery_tag,
                        routing_key,
                        # envelope,
                        # properties,
                    )
                )

            return _callback

        for (
            routing_key,
            exchange_name,
            competing,
            queue_name,
            func,
            handler,
        ) in context.get("_amqp_subscribers", []):
            queue_name = await declare_queue(
                routing_key,
                func,
                exchange_name=exchange_name,
                competing_consumer=competing,
                queue_name=queue_name,
            )
            await channel.basic_consume(
                callback(routing_key, handler), queue_name=queue_name
            )

    return _subscribe


# flake8: noqa
AmqpTransport.subscribe = subscribe  # type: ignore


@classmethod
async def client_ack(cls, delivery_tag) -> Optional[Callable]:
    await cls.channel.basic_client_ack(delivery_tag)


AmqpTransport.client_ack = client_ack  # type: ignore

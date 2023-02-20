import tomodachi

from app.core.config import env

global_options = tomodachi.Options(
    amqp=tomodachi.Options.AMQP(
        host=env("NAOMESH_AMQP_BROKER_ADDRESS"),
        port=env("NAOMESH_AMQP_BROKER_PORT"),
        login=env("NAOMESH_AMQP_BROKER_USERNAME"),
        password=env("NAOMESH_AMQP_BROKER_PASSWORD"),
    )
)

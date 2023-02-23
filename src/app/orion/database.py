from prefect.orion.database.alembic_commands import alembic_upgrade
from prefect.orion.database.dependencies import provide_database_interface
from prefect.utilities.asyncutils import run_sync_in_worker_thread


async def upgrade_database():
    db = provide_database_interface()
    await db.engine()

    await run_sync_in_worker_thread(
        alembic_upgrade, revision="head", dry_run=False
    )

from typing import Dict
from app.core.config import env

import prefect.settings
from prefect.cli._utilities import exit_with_error

PREFECT_PREFIX: str = "PREFECT_"


def apply_prefect_config_settings():
    """This function apply the prefect
    settings from the environment variables"""
    prefect_config: Dict[str | prefect.settings.Setting, str] = {
        key: val
        for key, val in env.ENVIRON.items()
        if key.startswith(PREFECT_PREFIX)
    }
    for key in prefect_config:
        if key not in prefect.settings.SETTING_VARIABLES:
            exit_with_error(f"Unknown setting name {key!r}.")
    prefect.settings.update_current_profile(prefect_config)

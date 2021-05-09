from typing import Dict

from db_helper_manager.commands import Commands
from sqlalchemy import create_engine


class DBConfig:
    """Provides configuration data for connecting to the database."""

    dsn_format = "{DIALECT}://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"

    def __init__(self, db_config: Dict):
        self.dsn_default = self.dsn_format.format(**db_config)

    @property
    def default_db_engine(self) -> "Engine":
        return create_engine(self.dsn_default)


class DBManager(DBConfig, Commands):
    """Manages access to the database."""

    def __init__(self, db_config):
        super().__init__(db_config)

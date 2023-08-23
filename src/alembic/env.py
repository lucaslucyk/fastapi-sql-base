import os
import sys
from alembic import context
from sqlalchemy import engine_from_config, pool

sys.path.append(os.getcwd())
from conf.config import settings
from db.base import Base


config = context.config
target_metadata = Base.metadata


def get_db_url() -> str:
    return settings.SQLALCHEMY_DATABASE_URI.replace('+aiosqlite', '')


def run_migrations_offline():

    # url = get_url()
    url = settings.DB_MIGRATIONS_URI
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    # configuration["sqlalchemy.url"] = get_url()
    configuration["sqlalchemy.url"] = settings.DB_MIGRATIONS_URI
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

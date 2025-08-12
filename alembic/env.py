from logging.config import fileConfig
import os

from alembic import context
from sqlalchemy import engine_from_config, pool

# --- Load DATABASE_URL from env/.env ---
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

config = context.config

# If using %(DATABASE_URL)s in alembic.ini, inject the real value here
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise RuntimeError(
        "DATABASE_URL not set. Export it or put it in a .env file."
    )
config.set_main_option("sqlalchemy.url", db_url)

# --- Logging from alembic.ini ---
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Point Alembic to your metadata ---
# Adjust this import to your project's actual Base location
from app.core.database import Base

# IMPORTANT: import models so autogenerate can see them
# Import all db_models to ensure Alembic sees all tables
from app.auth.db_models import User  # noqa: F401
from app.presentation.db_models import Presentation, PresentationImage  # noqa: F401
from app.logo.db_models import Logo  # noqa: F401
from app.document_generation.db_models import (  # noqa: F401
    BusinessProposal, PartnershipAgreement, NDA, 
    Contract, TermsOfService, PrivacyPolicy
)
from app.short_video.db_models import ShortVideo  # noqa: F401

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,          # detect column type changes
        compare_server_default=True # detect server_default changes
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

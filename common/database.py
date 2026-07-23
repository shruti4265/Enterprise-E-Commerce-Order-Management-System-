"""
database.py
============
Common SQLAlchemy database connection module for the Enterprise
E-Commerce Order Management System.

Every team member imports from THIS file — never create a second engine
or a second declarative Base. Sharing one Base and one engine is what
lets SQLAlchemy resolve relationships across everyone's models
(customers <-> addresses <-> orders <-> products <-> inventory, etc.).

What each member does in their own module file (e.g. customer_models.py):

    from common.database import Base
    from sqlalchemy import Column, Integer, String
    from sqlalchemy.orm import relationship

    class Customer(Base):
        __tablename__ = "customers"
        customer_id = Column(Integer, primary_key=True)
        name = Column(String(100), nullable=False)
        addresses = relationship("Address", back_populates="customer")

To get a database session inside any function (recommended way, via the
context manager — commits automatically, rolls back on error, always
closes the session):

    from common.database import get_db_session

    def register_customer(name, email):
        with get_db_session() as session:
            customer = Customer(name=name, email=email)
            session.add(customer)
        # committed automatically here; session is closed too

To create every table that has been defined anywhere in the project
(run this once, after all model files have been imported at least once):

    from common.database import init_db
    init_db()

Configuration
-------------
By default this uses a local SQLite file (ecommerce_oms.db) so anyone
on the team can run the project immediately with zero setup. To point
at a real database (e.g. MySQL/PostgreSQL for production), just set the
DATABASE_URL environment variable before running the app, for example:

    export DATABASE_URL="postgresql+psycopg2://user:pass@localhost:5432/ecommerce_oms"
    export DATABASE_URL="mysql+pymysql://user:pass@localhost:3306/ecommerce_oms"

No code changes are needed for that switch.
"""

import os
from contextlib import contextmanager

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker

from common.logger import get_logger

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# Connection configuration
# ---------------------------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///ecommerce_oms.db")

# `check_same_thread` is only needed for SQLite (allows use across threads,
# e.g. if the project later gets a Flask/FastAPI front end).
_connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=_connect_args,
    echo=False,          # set True temporarily if you want to see raw SQL
    future=True,
)

# Enforce foreign key constraints in SQLite (off by default in SQLite).
if DATABASE_URL.startswith("sqlite"):
    @event.listens_for(Engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

# Session factory — every part of the app should get sessions through
# get_db_session() below rather than calling SessionLocal() directly,
# so commit/rollback/close is handled consistently everywhere.
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# Shared declarative base. ALL models (Customer, Product, Order, ...)
# must inherit from this same Base so relationships and init_db() work
# across every member's module.
Base = declarative_base()


@contextmanager
def get_db_session():
    """
    Context manager that yields a SQLAlchemy session and guarantees it is
    committed on success, rolled back on error, and always closed.

    Example
    -------
        with get_db_session() as session:
            product = session.query(Product).filter_by(product_id=1).first()
            product.stock -= 1
        # auto-committed here
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        logger.error("Database transaction failed and was rolled back.", exc_info=True)
        raise
    except Exception:
        session.rollback()
        logger.error("Unexpected error during DB session; rolled back.", exc_info=True)
        raise
    finally:
        session.close()


def get_engine():
    """Return the shared SQLAlchemy engine (rarely needed directly)."""
    return engine


def init_db():
    """
    Create all tables for every model that has been imported and
    registered against `Base` so far.

    IMPORTANT: each member's model file must be imported at least once
    before calling this (e.g. import customer_models, product_models,
    inventory_models, cart_order_models, payment_models) so that
    SQLAlchemy knows about their tables. A good pattern is to import
    all model modules once inside main.py before calling init_db().
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified successfully (%s).", DATABASE_URL)
    except SQLAlchemyError:
        logger.error("Failed to initialize database tables.", exc_info=True)
        raise


def drop_all_tables():
    """
    Drop every table known to Base. Useful for resetting a dev/test
    database. Never call this against a production database.
    """
    try:
        Base.metadata.drop_all(bind=engine)
        logger.warning("All tables dropped from database (%s).", DATABASE_URL)
    except SQLAlchemyError:
        logger.error("Failed to drop database tables.", exc_info=True)
        raise


if __name__ == "__main__":
    # Quick self-test: run `python database.py` to confirm the connection
    # and table-creation logic work before anyone builds models on top.
    init_db()
    with get_db_session() as db_session:
        logger.info("Test session opened and closed cleanly: %s", db_session.is_active)
    print(f"Connected to: {DATABASE_URL}")
    print(f"Engine ready: {engine}")
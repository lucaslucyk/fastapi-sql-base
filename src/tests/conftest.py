# built-in
import sys
from pathlib import Path
from typing import Generator

# fastapi
from fastapi.testclient import TestClient

# third
#import pytest
from pytest import fixture
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)

# folders to path
TEST_URL = Path(__file__).resolve().parent
BASE_URL = TEST_URL.parent
sys.path.append(str(BASE_URL))


# own
from db import Base
from main import app
from api.dependencies import get_db
from core.config import settings


# async sqlite session
async_engine = create_async_engine(
    settings.TEST_DB_URI,
    future=True,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# async test db session
async def override_get_db() -> Generator:
    async with TestingSessionLocal() as db_session:
        yield db_session

# override database dependency
app.dependency_overrides[get_db] = override_get_db

        
@app.on_event("startup")
async def startup_event():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        
@app.on_event("shutdown")
async def shutdown_event():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as client:
        yield client
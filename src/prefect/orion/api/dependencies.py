"""
Utilities for injecting FastAPI dependencies.
"""

from prefect.orion.database.dependencies import provide_database_interface
from contextlib import asynccontextmanager
from prefect.orion.utilities.server import response_scoped_dependency
from fastapi import Request, Depends


def test():
    return "foo"


@response_scoped_dependency
async def get_session(request: Request, foo=Depends(test)):
    """
    Dependency-injected database session.
    The context manager will automatically handle commits,
    rollbacks, and closing the connection.
    """
    # we cant directly inject into FastAPI dependencies because
    # they are converted to async_generator objects
    db = provide_database_interface()

    # load engine with API timeout setting
    session_factory = await db.session_factory()
    async with session_factory() as session:
        async with session.begin():
            yield session
    print("Exiting session context")

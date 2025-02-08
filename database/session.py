from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)

from config import config


class SessionManager:
    def __init__(
        self,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url=config.db.construct_url(),
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        """
        Dispose of the database engine.

        :return: None
        """
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Get an asynchronous session for database operations.

        :return: An asynchronous generator yielding an AsyncSession.
        """
        async with self.session_factory() as session:
            yield session


session_manager = SessionManager(
    echo=config.db.echo,
    echo_pool=config.db.echo_pool,
    pool_size=config.db.pool_size,
    max_overflow=config.db.max_overflow,
)

"""Compatibility entry point for Render and local deployments."""

from app.main import main


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

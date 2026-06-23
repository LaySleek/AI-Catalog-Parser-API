import asyncio
from typing import Any, TypeVar
from collections.abc import Coroutine
from concurrent.futures import ThreadPoolExecutor

T = TypeVar("T")


def run_async(coroutine: Coroutine[Any, Any, T]) -> T:

    try:
        asyncio.get_running_loop()

    except RuntimeError:
        return asyncio.run(coroutine)

    with ThreadPoolExecutor(max_workers=1) as executor:
        return executor.submit(asyncio.run, coroutine).result()

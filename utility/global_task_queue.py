from typing import Dict
import asyncio

task_queue: Dict[str, asyncio.Future] = {}

import asyncio

from asynchronous_sample.repository.asynchronous_sample_repository import AsynchronousSampleRepository
from utility.global_task_queue import task_queue


class AsynchronousSampleRepositoryImpl(AsynchronousSampleRepository):
    async def heavyOperation(self, userToken: str, data: str) -> str:
        print(f"Start heavy operation for {userToken}")

        await asyncio.sleep(300)

        print(f"End heavy operation for {userToken}")
        return "Success"

    async def checkTaskResult(self, userToken: str) -> tuple[str, str | None]:
        task = task_queue.get(userToken)

        if task is None:
            return "NOT_FOUND", None
        elif not task.done():
            return "PROCESSING", None
        else:
            try:
                return "DONE", task.result()
            except Exception as e:
                return "FAILED", str(e)

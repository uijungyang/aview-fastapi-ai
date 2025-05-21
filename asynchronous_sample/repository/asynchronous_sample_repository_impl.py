import asyncio

from asynchronous_sample.repository.asynchronous_sample_repository import AsynchronousSampleRepository


class AsynchronousSampleRepositoryImpl(AsynchronousSampleRepository):
    async def heavyOperation(self, userToken: str, data: str) -> str:
        print(f"Start heavy operation for {userToken}")

        await asyncio.sleep(300)

        print(f"End heavy operation for {userToken}")
        return "Success"
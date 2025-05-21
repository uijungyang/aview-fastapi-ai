from fastapi import APIRouter, Depends, status, BackgroundTasks
from fastapi.responses import JSONResponse

from asynchronous_sample.controller.request_form.async_sample_request_form import AsyncSampleRequestForm
from asynchronous_sample.service.asynchronous_sample_service_impl import AsynchronousSampleServiceImpl

asynchronousSampleRouter = APIRouter()

async def injectAsynchronousSampleService() -> AsynchronousSampleServiceImpl:
    return AsynchronousSampleServiceImpl()


@asynchronousSampleRouter.post("/async-sample-request")
async def requestAsyncSample(asyncSampleRequestForm: AsyncSampleRequestForm,
                             background_tasks: BackgroundTasks,
                             asynchronousSampleService: AsynchronousSampleServiceImpl = Depends(injectAsynchronousSampleService)):
    print(f"controller -> requestAsyncSample(): asyncSampleRequestForm: {asyncSampleRequestForm.dict()}")

    request = asyncSampleRequestForm.toRequest()
    background_tasks.add_task(asynchronousSampleService.generateHeavyOperation, request)

    return JSONResponse(content=True, status_code=status.HTTP_200_OK)
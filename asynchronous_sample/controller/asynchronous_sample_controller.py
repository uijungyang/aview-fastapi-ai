from fastapi import APIRouter, Depends, status, BackgroundTasks
from fastapi.responses import JSONResponse

from asynchronous_sample.controller.request_form.async_sample_check_request_form import AsyncSampleCheckRequestForm
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

@asynchronousSampleRouter.post("/check-async-sample")
async def getAsyncSampleResult(asyncSampleCheckRequestForm: AsyncSampleCheckRequestForm,
                               asynchronousSampleService: AsynchronousSampleServiceImpl = Depends(injectAsynchronousSampleService)):

    status, result = await asynchronousSampleService.checkAsyncSampleResult(asyncSampleCheckRequestForm.toRequest())

    if status == "NOT_FOUND":
        return JSONResponse(content={"status": status}, status_code=404)
    elif status == "PROCESSING":
        return JSONResponse(content={"status": status}, status_code=200)
    elif status == "DONE":
        return JSONResponse(content={"status": status, "result": result}, status_code=200)
    elif status == "FAILED":
        return JSONResponse(content={"status": status, "error": result}, status_code=500)

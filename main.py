import uvicorn

from fastapi import FastAPI, APIRouter

from prometheus_fastapi_instrumentator import Instrumentator

from services.scheduling import scheduler
from api import mailing_router, recipient_router
import settings


tags_metadata = [
    {
        "name": "recipients",
        "description": "Operations with mailing recipients"
    },
    {
        "name": "mailings",
        "description": "Operations with mailings"
    }
]

app = FastAPI(
    title='Mailing Service',
    openapi_tags=tags_metadata
)
Instrumentator().instrument(app).expose(app)

main_api_router = APIRouter()

main_api_router.include_router(
    recipient_router,
    prefix='/recipients',
    tags=['recipients']
)
main_api_router.include_router(
    mailing_router,
    prefix='/mailings',
    tags=['mailings']
)

app.include_router(main_api_router)


@app.on_event("startup")
async def startup_event():
    scheduler.start()


if __name__ == '__main__':
    uvicorn.run(
        app,
        host='127.0.0.1',
        port=settings.APP_PORT,
    )


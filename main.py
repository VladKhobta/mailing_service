import uvicorn

from fastapi import FastAPI, APIRouter

from services.scheduling import scheduler

from api import mailing_router, recipient_router

import settings


app = FastAPI(title='Mailing Service')

main_api_router = APIRouter()

main_api_router.include_router(
    recipient_router,
    prefix='/recipient',
    tags=['recipient']
)
main_api_router.include_router(
    mailing_router,
    prefix='/mailing',
    tags=['mailing']
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


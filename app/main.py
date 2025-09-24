from fastapi import FastAPI
from .database import engine, Base
from .controllers import message_controller
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app= FastAPI(title='Messages API')

Base.metadata.create_all(bind=engine)

app.include_router(message_controller.router)

@app.exception_handler(RequestValidationError)
async def exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={
            'status': 'error',
            'error': {
                "code": "INVALID_FORMAT",
                "message": "Formato de mensaje inválido",
                "details": exc.errors()[0]['msg']
            }
        }
    )
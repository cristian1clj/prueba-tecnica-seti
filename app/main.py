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
    error = exc.errors()[0]
    custom_details = []

    error_type = error['type']
    field = error['loc'][1]
    if error_type == 'missing':
        details = f'El campo {field} es obligatorio'
    elif error_type == 'string_type':
        details = f'El campo {field} debe ser un string'
    elif error_type == 'datetime':
        details = f'El campo {field} debe ser un datetime'
    else:
        details = error['msg']
    
    return JSONResponse(
        status_code=400,
        content={
            'status': 'error',
            'error': {
                "code": "INVALID_FORMAT",
                "message": "Formato de mensaje inválido",
                "details": details
            }
        }
    )
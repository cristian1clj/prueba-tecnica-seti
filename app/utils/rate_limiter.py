from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import time

requests = {}

def rate_limiter(request: Request, max_requests: int = 5, time_range: int = 60):
    host = request.client.host
    now = time.time()
    time_start = now - time_range
    
    if host not in requests or not requests[host]:
        requests[host] = []
    
    requests[host] = [t for t in requests[host] if t > time_start]
    
    if len(requests[host]) >= max_requests:
        return JSONResponse(
            status_code=429,
            content={
                "status": "error",
                "error": {
                    "code": "TOO_MANY_REQUESTS",
                    "message": "Demasiadas peticiones",
                    "details": f"Has excedido el límite de {max_requests} solicitudes en {time_range} segundos."
                }
            }
        )

    requests[host].append(now)
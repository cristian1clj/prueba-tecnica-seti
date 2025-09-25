from fastapi import Request, HTTPException
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
        raise HTTPException(status_code=429, detail="Se han realizado muchas peticiones")

    requests[host].append(now)
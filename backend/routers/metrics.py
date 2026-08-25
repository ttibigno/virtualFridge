from prometheus_client import Counter, Histogram, Gauge
import time
from fastapi import FastAPI, Request, Response


http_requests_total = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "path", "status"]
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "path", "status"]
)

fridge_additions = Counter(
    "fridge_additions_total", 
    "Total number of fridge additions"
)

things = Gauge(
    "number_of_things",
    "Number of things in the fridge"
)

def setup_metrics(app: FastAPI):
    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next):
        start = time.perf_counter()

        response = await call_next(request)

        duration = time.perf_counter() - start

        http_requests_total.labels(
            method=request.method,
            status=str(response.status_code),
            path= request.url.path
        ).inc()

        http_request_duration_seconds.labels(
            method=request.method,
            status = str(response.status_code),
            path = request.url.path
        ).observe(duration)

        return response

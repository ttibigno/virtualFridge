from prometheus_client import Counter, Histogram, Gauge
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
import time
import structlog

structlog.configure(processors = [structlog.processors.TimeStamper(fmt="iso"), structlog.stdlib.add_log_level, structlog.processors.JSONRenderer()])
logger = structlog.getLogger()


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

def setup_observability(app: FastAPI):
    @app.middleware("http")
    async def httpMiddleware(request: Request, call_next):
        startTime = time.perf_counter()
        response = await call_next(request)
        reqDuration = time.perf_counter() - startTime

        if (request.url.path != "/metrics/"):
            route = request.scope.get("route") #Prendiamo la route per togliere tutti gli endpoint a ids
            path = route.path if route else request.url.path
            http_requests_total.labels(
                method=request.method,
                status=str(response.status_code),
                path= path
            ).inc()
    
            http_request_duration_seconds.labels(
                method=request.method,
                status = str(response.status_code),
                path = path
            ).observe(reqDuration)

            logger.info(
                "httpRequest",
                method = request.method,
                path = path,
                statusCode = response.status_code,
                duration = reqDuration
            )
            
        return response

    @app.exception_handler(SQLAlchemyError)
    async def exceptionMiddleware(request: Request, exception: SQLAlchemyError):
        logger.error(
            "databaseError",
            method = request.method,
            path = request.url.path,
            error = type(exception).__name__
        )

        return JSONResponse(status_code=500, content={"detail": "Database error"})
            
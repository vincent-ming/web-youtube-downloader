import logging
import time
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse

import config
import services
from exceptions import WYDApiError
from models import DownloadRequest

app = FastAPI()

config.log_init()


@app.exception_handler(WYDApiError)
async def api_exception_handler(req: DownloadRequest, exc: WYDApiError):
    logging.error(f'Error occur, {exc}')
    return JSONResponse(status_code=500, content={'detail': f'{exc.message}'})


@app.exception_handler(Exception)
async def exception_handler(req: DownloadRequest, exc: Exception):
    logging.error(exc, exc_info=True)
    return JSONResponse(status_code=500, content={'detail': 'Service is unavailable'})


@app.middleware('http')
async def record_request(req: Request, call_next):
    client = req.client
    logging.info(f'Receive request from {client.host}:{client.port}')
    start_time = time.perf_counter()
    response = await call_next(req)
    elapse_time = time.perf_counter() - start_time
    logging.info(f'Request completed. Elapsed time: {elapse_time:.3f} secs')
    return response


@app.post("/download_music")
async def download_music(req: DownloadRequest):
    logging.info(f'Download start. request: {req}')
    file_path = services.generate_music(req)
    file_name = Path(file_path).name
    return FileResponse(file_path, filename=file_name)

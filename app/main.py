import logging
import os.path
import time

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse

import logConfig
import services
from exceptions import WYDApiError
from models import DownloadInfo

app = FastAPI()

logConfig.init()


@app.exception_handler(WYDApiError)
async def api_exception_handler(info: DownloadInfo, exc: WYDApiError):
    logging.error(exc, exc_info=True)
    return JSONResponse(status_code=500, content={'detail': f'{exc.message}'})


@app.exception_handler(Exception)
async def exception_handler(info: DownloadInfo, exc: Exception):
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


@app.post("/download")
async def download_music(info: DownloadInfo):
    logging.info(f'Download start. info: {info}')
    file_path = services.download(info)
    filename = os.path.basename(file_path)
    return FileResponse(file_path, filename=filename)

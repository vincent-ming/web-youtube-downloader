import logging
import os.path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse

from app import services, logConfig
from app.exceptions import WYDApiError
from app.models import DownloadInfo

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


@app.post("/download")
async def download_music(info: DownloadInfo, req: Request):
    client = req.client
    logging.info(f'{client.host}:{client.port} download start. Req: {info}')
    file_path = services.download(info)
    filename = os.path.basename(file_path)
    return FileResponse(file_path, filename=filename)



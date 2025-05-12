import os.path

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse

from app import services
from app.exceptions import WYDApiError
from app.models import DownloadRequest

app = FastAPI()


@app.exception_handler(WYDApiError)
async def api_exception_handler(request: DownloadRequest, exc: WYDApiError):
    return JSONResponse(status_code=500, content={'detail': f'{exc.message}'})


@app.exception_handler(Exception)
async def exception_handler(request: DownloadRequest, exc: Exception):
    return JSONResponse(status_code=500, content={'detail': 'Service is unavailable'})


@app.post("/download")
async def download_music(request: DownloadRequest):
    file_path = services.download(request)
    filename = os.path.basename(file_path)
    return FileResponse(file_path, filename=filename)



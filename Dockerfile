FROM python-ffmpeg-base:3.12

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--app-dir", "./app", "--host", "0.0.0.0", "--port", "9000"]
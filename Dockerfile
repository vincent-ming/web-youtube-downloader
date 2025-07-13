FROM python-ffmpeg-base:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--app-dir", "./app", "--host", "0.0.0.0", "--port", "9000"]
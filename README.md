pip install -r requirements.txt

apt-get install -y ffmpeg libavcodec-extra

uvicorn main:app --app-dir .\app --host 0.0.0.0 --port 9000
FROM python:3.11
WORKDIR /the/workdir/path
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y ffmpeg
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
FROM python:3.10-slim

WORKDIR /app
COPY . /app

# Install all system dependencies for OpenCV, zbar and MySQL client
RUN apt-get update && apt-get install -y \
    libzbar0 \
    libzbar-dev \
    default-libmysqlclient-dev \
    pkg-config \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install \
        opencv-contrib-python \
        numpy \
        Pillow \
        mysqlclient \
        pyzbar

EXPOSE 5000

CMD ["python", "main_app.py"]

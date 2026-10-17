FROM ubuntu:22.04

# Prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir \
    scikit-learn==1.4.1.post1 \
    joblib \
    pandas \
    numpy \
    flask

COPY . /app

EXPOSE 5000

CMD ["python3", "app.py"]

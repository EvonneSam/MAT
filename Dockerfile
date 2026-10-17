FROM ubuntu:22.04

# Prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Added python3-flask to the list
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-pandas \
    python3-sklearn \
    python3-joblib \
    python3-flask \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

EXPOSE 5000

CMD ["python3", "app.py"]


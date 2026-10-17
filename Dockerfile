FROM ubuntu:22.04

# Prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install pre-compiled python, pandas, scikit-learn, and joblib directly via apt
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-pandas \
    python3-sklearn \
    python3-joblib \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

EXPOSE 5000

CMD ["python3", "app.py"]


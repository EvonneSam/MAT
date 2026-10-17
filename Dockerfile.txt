FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir flask pandas scikit-learn joblib
EXPOSE 5000
CMD ["python", "app.py"]

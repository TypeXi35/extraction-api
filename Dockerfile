FROM python:3.13.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["flask", "--app", "app", "--debug","run", "--host=0.0.0.0", "--port=5000"]
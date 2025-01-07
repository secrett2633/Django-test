import multiprocessing
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.core.settings")

# Uvicorn ASGI worker 사용
worker_class = "uvicorn.workers.UvicornWorker"

bind = "0.0.0.0:8000"
timeout = 60
max_requests = 2000
max_requests_jitter = 50
workers = multiprocessing.cpu_count() * 2
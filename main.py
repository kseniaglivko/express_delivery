"""Модуль запуска программы."""
import uvicorn
from app import app

if __name__ == "__main__":
    uvicorn.run(app, host="192.168.1.126", port=8000)

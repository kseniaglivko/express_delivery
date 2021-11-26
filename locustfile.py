"""Locust-файл со сценариями обращения по запросам."""
from locust import HttpUser, task, between
import rstr
from random import choice


class ExpressDeliveryUser(HttpUser):
    """Класс для пользовательского поведения."""

    wait_time = between(2, 9)

    @task
    def check_index_page(self) -> None:
        """Сценарий входа на приветственную страницу."""
        self.client.get("/")

    @task(1)
    def check_create_delivery(self) -> None:
        """Проверка post-запроса."""
        sample_id = rstr.xeger(r"^[a-z0-9]{2,5}$")
        sample_status = choice(["to_do", "in_progress", "done"])
        data = {
            "id": sample_id,
            "status": sample_status,
        }
        self.client.post("/deliveries", json=data)

    @task(2)
    def check_fetch_db(self) -> None:
        """Проверка get-запроса."""
        self.client.get("/deliveries")

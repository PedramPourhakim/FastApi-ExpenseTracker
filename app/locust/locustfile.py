from locust import HttpUser, task, between
import logging

logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class QuickStartUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        response = self.client.post("/api/v1/users/login?lang=fa", json=
        {"username": "shemuel1226",
         "password": "123456"
         })
        # logger.info(f"Response :  {response.content}")
        access_token = response.json()["access_token"]
        self.client.headers = {"Authorization": f"Bearer {access_token}"}


    @task
    def expenses_list(self):
        self.client.get("/api/v1/expenses?limit=50&offset=0")

    @task
    def people_list(self):
        self.client.get("/api/v1/people/people")

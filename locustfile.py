from locust import HttpUser, task, constant
import random

class User(HttpUser):
    wait_time = constant(0) 
    host = "http://localhost:8000"

    @task
    def create(self):
        uid = random.randint(1, 100000000)
        self.client.post("/api/v1/users/fast", json={
            "username": f"u{uid}",
            "email": f"u{uid}@mail.com",
            "full_name": "Test User",
            "password": "pwd",
            "biography": "bio"
        })
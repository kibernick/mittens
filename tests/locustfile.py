import random
import string
import os

from flask import json
from locust import HttpLocust, TaskSet, task

TENANT_API_KEY = os.environ.get("TENANT_API_KEY") or "sk_test_123455678"
sys_random = random.SystemRandom()


def random_str(size=None, chars=string.ascii_uppercase + string.digits):
    _size = sys_random.randint(1, 200) or size
    return "".join(sys_random.choice(chars) for _ in range(_size))


class TenantBehavior(TaskSet):
    @task(10)
    def create_error_log(self):
        self.client.post(
            "/api/v1/logs", json={"content": random_str()}, headers={"Authorization": f"Basic {TENANT_API_KEY}"}
        )

    @task(1)
    def get_error_logs(self):
        self.client.get("/api/v1/logs", headers={"Authorization": f"Basic {TENANT_API_KEY}"})


class WebsiteUser(HttpLocust):
    task_set = TenantBehavior
    min_wait = 5000
    max_wait = 9000

import asyncio
import random
import re
import threading
import math
from datetime import date
from typing import List

import aiohttp
import requests


class OdooSession:
    session_id = None
    user_id = None
    employee_id = None
    project_task_map = {}

    def __init__(self, base_url, user, password):
        self.base_url = base_url
        self.user = user
        self.password = password
        self.__login()

    def __login(self):
        # Get login page
        url = self.base_url
        response = requests.get(url)

        # Get session_id and csrf
        self.session_id = get_session_id(response)
        csrf = get_csrf(response.text)

        # Login
        url = f"{self.base_url}/web/login"

        payload = {"csrf_token": csrf, "login": self.user, "password": self.password}
        response = requests.post(url, data=payload, headers=self.__headers())

        # Set session_id, user_id and employee_id after login
        self.session_id = get_session_id(response)
        self.user_id = get_user_id(response)
        self.employee_id = self.__get_employee_id()

    def get_data(self, model: str, fields: List[str] = ["name", "id"], domain=[]):
        url = f"{self.base_url}/web/dataset/search_read"
        payload = self.__build_get_data_payload(model, fields, domain)
        response = requests.post(url, json=payload, headers=self.__headers())

        return response.json().get("result", {}).get("records", {})

    async def get_data_async(
        self,
        session: aiohttp.ClientSession,
        model="project.project",
        fields=["name", "id"],
        domain=[],
    ):
        url = f"{self.base_url}/web/dataset/search_read"
        payload = self.__build_get_data_payload(model, fields, domain)
        async with session.post(url, json=payload, headers=self.__headers()) as post:
            response = await post.json()
            return response.get("result", {}).get("records", {})

    def __build_get_data_payload(self, model, fields, domain):
        return {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "model": model,
                "domain": domain,
                "fields": fields,
                "limit": 200,
            },
            "id": random.randint(0, 100000),
        }

    async def get_tasks_for_projects(self, projects):
        result = {}
        async with aiohttp.ClientSession() as session:
            t = []
            for project in projects:
                id = project.get("id")

                t.append(
                    asyncio.ensure_future(
                        self.get_data_async(
                            session, "project.task", domain=[["project_id", "=", id]]
                        )
                    )
                )

            tasks = await asyncio.gather(*t)

            for i, project in enumerate(projects):
                name = normalize(project.get("name"))
                id = project.get("id")
                result[name] = {"id": id, "tasks": []}
                for task in tasks[i]:
                    task_id = task.get("id")
                    task_name = task.get(("name"))
                    result[name]["tasks"].append({task_name: task_id})
        return result

    def __call_kw(self, method, model, args):
        url = f"{self.base_url}/web/dataset/call_kw/{method}"
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": {
                "args": args,
                "model": model,
                "method": method,
                "kwargs": {},
            },
            "id": random.randint(0, 100000),
        }
        response = requests.post(url, json=payload, headers=self.__headers())
        return response.json()

    def create_data(self, model, args):
        return self.__call_kw("create", model, args)

    def update_data(self, model, args):
        return self.__call_kw("write", model, args)

    def unlink_data(self, model, args):
        return self.__call_kw("unlink", model, args)

    async def get_projects_with_tasks(self):
        projects = self.get_data("project.project")
        return await self.get_tasks_for_projects(projects)

    def __get_employee_id(self):
        user = self.get_data(
            "hr.employee.public", fields=["id"], domain=[["user_id", "=", self.user_id]]
        )
        return user[0]["id"]

    def __headers(self):
        return {"Cookie": f"session_id={self.session_id}; fileToken=dummy"}


def get_session_id(response):
    cookies = requests.utils.dict_from_cookiejar(response.cookies)

    return cookies.get("session_id", "")


def get_user_id(response):
    return int(re.search(r'"user_id":\s+\[(\d+)\]', response.text)[1])


def get_csrf(html):
    csrf_match = re.search(r'csrf_token"\svalue="(.*)?"', html)

    return csrf_match[1]


def threader(func, list, *args):
    splitted = split_list(list, 4)
    result = {}
    threads = [
        threading.Thread(target=func, args=(splitted[i], result, *args))
        for i in range(4)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return result


def split_list(list, parts=1):
    length = len(list)
    return [list[i * length // parts : (i + 1) * length // parts] for i in range(parts)]


def normalize(str):
    return re.sub(r"\s+", " ", str.strip())


def seconds_to_hours(seconds):
    hours = seconds / 3600
    return math.ceil(hours * 4) / 4

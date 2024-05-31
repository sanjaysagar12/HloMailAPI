import asyncio


async def main():
    workflow_data = [
        {
            "tag": "login",
            "method": "POST",
            "url": "http://localhost:8000/login",
            "headers": {},
            "body": {
                "email": "sanjaysagarlearn@gmail.com",
                "password": "12345",
            },
            "cookies": {},
        },
        {
            "tag": "profile",
            "method": "POST",
            "url": "http://localhost:8000/profile",
            "headers": {
                "token": "1qwsdfe32were34ew",
            },
            "body": {},
            "cookies": {},
        },
        {
            "tag": "history",
            "method": "POST",
            "url": "http://localhost:8000/history",
            "headers": {
                "token": "iqdo3do2o3n90231kl",
            },
            "body": {},
            "cookies": {},
        },
    ]

    # Example automation data (commented out as they will be provided externally)
    automation_data = {
        "login": {
            "1qwsdfe32were34ew": ["(token)", "profile"],
            "iqdo3do2o3n90231kl": ["(token)", "history"],
        },
    }
    from WorkFlow import WorkFlow

    workflow = WorkFlow()
    data = await workflow.execute(workflow_data, automation_data)
    print(data)


if __name__ == "__main__":
    asyncio.run(main())

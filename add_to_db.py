import os
import dotenv
import asyncio

from bot.database.db_setup import Database

dotenv.load_dotenv()
DATABASE_URI = os.getenv("MONGODB_URI")

db_service = Database(DATABASE_URI)
users_collection = db_service.db["users"]

email_list = []


async def add_user(email: str):
    print(f"Adding user: {email}")
    payload = {"email": email, "username": ""}

    await users_collection.insert_one(payload)


def get_email_list():
    with open("email_list.txt", "r") as file:
        for line in file:
            email = line.strip()
            if email:
                email_list.append(email)


if __name__ == "__main__":
    get_email_list()
    loop = asyncio.get_event_loop()
    tasks = [add_user(email) for email in email_list]
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()

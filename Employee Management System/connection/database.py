from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

empURI = os.getenv("MONGO_URI")
dbName="projectManagement"

client = AsyncIOMotorClient(empURI)
db = client[dbName]

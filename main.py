import os
from typing import Optional, List

from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated

from bson import ObjectId
import asyncio
from pymongo import AsyncMongoClient
from pymongo import ReturnDocument

# Weather API Key
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.weatherapi.com/v1"

app = FastAPI(
    title="Weather Information API",
    summary="A simple application to fetch information from Weather Information API",
)
@app.get("/")
def read_root():
    return {"Hello": "World"}


def weather_query():
    pass

def main():
    pass

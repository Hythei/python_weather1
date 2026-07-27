import os
from typing import Optional, List

import pymongo
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
client = AsyncMongoClient(os.getenv("MONGODB_URL"), server_api=pymongo.server_api.ServerApi(version="1", strict=True,deprecation_errors=True))
db = client.weather_test1
weather_collection = db.get_collection("weather_information")

PyObjectId = Annotated[str, BeforeValidator(str)]


class WeatherInformationModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    location: str = Field(alias="location")
    temperature: float = Field(alias="temperature")
    date: str = Field(alias="date")
    match_prediction: bool = Field(alias="match_prediction")
    model_config = ConfigDict(from_attributes=True)

class WeatherInformation(BaseModel):
    weather_information: List[WeatherInformationModel]

@app.get(
    "/weather_information",
    response_description="Get all weather information",
    response_model=WeatherInformation,
    response_model_by_alias=True,
)

async def get_weather_information():
    return WeatherInformation(weather_information=await weather_collection.find({}).to_list(None))
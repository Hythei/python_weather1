import os
from datetime import datetime
from typing import Optional, List
from dotenv import load_dotenv

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

load_dotenv()

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
    location: str
    temperature: float
    date: datetime
    match_prediction: bool

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

class UpdateWeatherInformationModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    location: Optional[str] = None
    temperature: Optional[float] = None
    date: Optional[datetime] = None
    match_prediction: Optional[bool] = None
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class WeatherInformation(BaseModel):
    weather_information: List[WeatherInformationModel]

@app.get(
    "/weather_information",
    response_description="Get all weather information",
    response_model=WeatherInformation,
    response_model_by_alias=True,
)
async def get_weather_information():
    return WeatherInformation(weather_information=await weather_collection.find({}).to_list(length=None))

@app.post(
    "/weather_information",
    response_description="Add a new weather information",
    response_model=WeatherInformationModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=True,
)
async def add_weather_information(weather_information: WeatherInformationModel = Body(...)):
    new_weather_information =  weather_information.model_dump()
    result = await weather_collection.insert_one(new_weather_information)
    new_weather_information["_id"] = result.inserted_id
    return new_weather_information

@app.put(
    "/weather_information/{id}",
    response_description="Update a weather information",
    response_model=WeatherInformationModel,
    response_model_by_alias=True,
)
async def update_weather_information(
    id: str,
    weather_information: UpdateWeatherInformationModel = Body(...),
):
    update_data = {
        k: v
        for k, v in weather_information.model_dump(exclude={"id"}).items()
        if v is not None
    }

    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid weather information id",
        )

    existing_weather_information = await weather_collection.find_one(
        {"_id": ObjectId(id)}
    )

    if existing_weather_information is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weather information not found",
        )

    if not update_data:
        return existing_weather_information
        update_result = await weather_collection.find_one_and_update(
            {"_id": ObjectId(weather_information["id"])},
            {"$set": weather_information},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Weather information not found")
    if (existing_weather_information := await weather_collection.find_one({"_id": ObjectId(weather_information["id"])})) is not None:
        return existing_weather_information
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Weather information not found")

import os
from datetime import datetime
from typing import Optional, List
from dotenv import load_dotenv
import requests

import pymongo
from fastapi import FastAPI, Body, HTTPException, Query, status
from fastapi.responses import Response
from pydantic import ConfigDict, BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId
from pymongo import AsyncMongoClient
from pymongo import ReturnDocument

from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# Weather API Key
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.weatherapi.com/v1"

app = FastAPI(
    title="Weather Information API",
    summary="A simple application to fetch information from Weather Information API",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



client = AsyncMongoClient(os.getenv("MONGODB_URL"), server_api=pymongo.server_api.ServerApi(version="1", strict=True,deprecation_errors=True))
db = client.weather_test1
weather_collection = db.get_collection("weather_information")

PyObjectId = Annotated[str, BeforeValidator(str)]


class WeatherDocumentModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    location: str
    temperature: float
    date: datetime
    match_prediction: bool

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

class UpdateWeatherDocumentModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    location: Optional[str] = None
    temperature: Optional[float] = None
    date: Optional[datetime] = None
    match_prediction: Optional[bool] = None
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

class WeatherDocuments(BaseModel):
    weather_information: List[WeatherDocumentModel]

def fetchWeatherFromAPI(location: str) -> dict:
    weatherApiParams = {
        "key": API_KEY,
        "q": location,
        "aqi": "no"
    }
    response = requests.get(f"{BASE_URL}/current.json", params=weatherApiParams)
    if not response.ok:
        try:
            error = response.json().get("error", {})
            msg = error.get("message", "Failed to fetch weather data from WeatherAPI")
        except Exception:
            msg = "Failed to fetch weather data from WeatherAPI"
        raise HTTPException(
            status_code=response.status_code if response.status_code in (400, 404) else status.HTTP_502_BAD_GATEWAY,
            detail=msg,
        )
    return response.json()

@app.get(
    "/weather_information/fetch",
    response_description="Get the location's weather information from WeatherAPI and save to database",
    response_model=WeatherDocumentModel,
    response_model_by_alias=True,
)
async def fetch_weather_information(location: str = Query(...)):
    data = fetchWeatherFromAPI(location)
    current = data["current"]
    location_data = data["location"]
    # Dictionary that will be sent to MongoDB
    data_model = {
        "location": location_data['name'],
        "temperature": current['temp_c'],
        "date": datetime.now(),
        "match_prediction": True
    }
    result = await weather_collection.insert_one(data_model)
    data_model["_id"] = result.inserted_id
    return data_model

@app.get(
    "/weather_information",
    response_description="Get all weather information",
    response_model=WeatherDocuments,
    response_model_by_alias=True,
)
async def get_weather_information():
    weather_Documents = list(await weather_collection.find({}).to_list(length=None))
    return {"weather_information": weather_Documents}

@app.post(
    "/weather_information",
    response_description="Add a new weather information",
    response_model=WeatherDocumentModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=True,
)
async def add_weather_information(weather_information: WeatherDocumentModel = Body(...)):
    new_weather_information =  weather_information.model_dump()
    result = await weather_collection.insert_one(new_weather_information)
    new_weather_information["_id"] = result.inserted_id
    return new_weather_information

@app.put(
    "/weather_information/{id}",
    response_description="Update a weather information",
    response_model=WeatherDocumentModel,
    response_model_by_alias=True,
)
async def update_weather_information(
    id: str,
    weather_information: UpdateWeatherDocumentModel = Body(...),
):
    update_data = weather_information.model_dump(
            exclude={"id"},
            exclude_unset=True,
            exclude_none=True,
        )

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
        {"_id": ObjectId(id)},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER,
    )

    if update_result is not None:
        return update_result

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Weather information not found",
    )

@app.delete("/weather_information/{id}",
            response_description="Delete a weather information",
            response_model=WeatherDocumentModel, )
async def delete_weather_information(id: str):
    delete_result = await weather_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Weather information {id} not found")
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List,
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/ping")
def ping():
    return "pong"

cars_db = {}

class Characteristic(BaseModel):
    max_speed: int
    max_fuel_capacity: int

class Car(BaseModel):
    identifier: str
    brand: str
    model: str
    characteristics: Characteristic

@app.post("/cars", status_code=201)
def cars(carss: List[Car]):
    for car in carss:
        cars_db[car.identifier] = car
    return {"message": f"{len(carss)} cars."}

@app.get("/cars")
def get_cars():
    return list(cars_db.values())

@app.get("/cars/{id}")
def get_cars(id: str):
    car = cars_db.get(id)
    if not car:
        raise HTTPException(status_code=404, detail=f"la voiture comportant '{id}' n'est pas trouvé.")
    return car

@app.put("/cars/{id}/characteristics")
def update_characteristics(id: str, characteristics: CharacteristicUpdate):
    car = cars_db.get(id)
    if not car:
        raise HTTPException(status_code=404, detail=f"la voiture comportant  '{id}' n'est pas trouvé.")
    car.characteristics = characteristics
    cars_db[id] = car
    return car


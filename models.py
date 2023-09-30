from pydantic import BaseModel
from typing import List, Dict

class Meal(BaseModel):
    id: int
    food: str
    price: str
    color: str
    consistency: str

class NutrientValues(BaseModel):
    energy: float
    carbohydrate: float
    protein: float
    fat: float
    fiber: float

class DayMenu(BaseModel):
    status: str
    day: int
    menu: List[Meal]
    total_nutrient_values: NutrientValues

class WeeklyMenu(BaseModel):
    week: int
    menus: List[DayMenu]

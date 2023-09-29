from pydantic import BaseModel
from typing import List, Dict

class Meal(BaseModel):
    ID: int
    Yemek: str
    Fiyat: str
    Renk: str
    Kivam: str

class NutrientValues(BaseModel):
    Enerji: float
    Karbonhidrat: float
    Protein: float
    Yağ: float
    Lif: float

class DayMenu(BaseModel):
    Status: str
    Day: int
    Gun_Menu: List[Meal]
    Toplam_Besin_Degerleri: NutrientValues

class WeeklyMenu(BaseModel):
    Hafta: int
    Menuler: List[DayMenu]

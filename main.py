from fastapi import FastAPI
import diet_planning
from fastapi.middleware.cors import CORSMiddleware
from typing import List 
from models import WeeklyMenu
app = FastAPI()

# ["*"],
origins = ["*"]
# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World from Shahmirzali!"}
    

@app.get("/get_data_from_csv", response_model=List[WeeklyMenu])
def get_data_from_csv():
    # user_age: int, user_gender: str, week: int
    data = diet_planning.get_diet_menu()
    if not isinstance(data, list):
        return {"error": "Invalid data format. Expected a list of dictionaries."}
    return data





# @app.get("/get_data_from_csv",response_model=models.WeeklyMenu)
# def get_data_from_csv(user_age: int, user_gender: str):
#     # Get the data from diet_planning module
#     data = diet_planning_2.get_diet_menu()

    # # Check if data is in the desired format (list of dictionaries)
    # if not isinstance(data, list):
    #     return {"error": "Invalid data format. Expected a list of dictionaries."}

    # # Convert the data (list of dictionaries) to a JSON string with double quotes
    # json_string = json.dumps(data, ensure_ascii=False, cls=CustomJSONEncoder)

    # # Parse the JSON string back to a Python object (list of dictionaries)
    # parsed_data = json.loads(json_string)

#     return data

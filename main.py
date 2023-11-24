from fastapi import FastAPI
import diet_planning
from fastapi.middleware.cors import CORSMiddleware
from typing import List 
from models import WeeklyMenu


from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
import os

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

# pip install google-auth
# pip install google-auth-httplib2
# pip install google-auth-oauthlib
# pip install requests
@app.get("/")
async def root():
    return {"message": f"Hello Shahmirzali"}

@app.get("/app")
async def deep_link():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Your Website Title</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <script type="text/javascript">
            window.onload = function() {
                var isAndroid = /android/i.test(navigator.userAgent);
                var isiOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
                if (isAndroid) {
                    window.location.href = 'https://play.google.com/store/apps/details?id=com.google.android.youtube';
                } else if (isiOS) {
                    window.location.href = 'https://apps.apple.com/app/youtube-watch-listen-stream/id544007664';
                }
            }
        </script>
    </head>
    <body>
        <h1>AppLink Test</h1>
        <p>This is an example of a website that redirects users to the YouTube app's page on the App Store or Play Store, depending on their device.</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/.well-known/apple-app-site-association")
async def apple_app_site_association():
    # Projeye göre düzenlenmiş yolu tanımlayın
    aasa_file_path = os.path.join(
        os.path.dirname(__file__),  # Bu dosyanın bulunduğu dizin
        '.well-known', 'apple-app-site-association'  # `.well-known` altındaki dosya
    )
    return FileResponse(aasa_file_path, media_type='application/json', headers={"Content-Type": "application/json; charset=utf-8"})
    
# <!DOCTYPE html>
# <html>
# <head>
#     <title>Your Website Title</title>
#     <meta name="viewport" content="width=device-width, initial-scale=1">
#     <script type="text/javascript">
#         window.onload = function() {
#             var isAndroid = /android/i.test(navigator.userAgent);
#             var isiOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
#             if (isAndroid) {
#                 // Redirect to the Play Store
#                 window.location.href = 'https://play.google.com/store/apps/details?id=com.google.android.youtube';
#             } else if (isiOS) {
#                 // Redirect to the App Store
#                 window.location.href = 'https://apps.apple.com/app/youtube-watch-listen-stream/id544007664';
#             }
#         }
#     </script>
# </head>
# <body>
#     <h1>AppLink Test</h1>
#     <p>This is an example of a website that redirects users to the YouTube app's page on the App Store or Play Store, depending on their device.</p>
# </body>
# </html>

@app.get("/get_data_from_csv", response_model=List[WeeklyMenu])
def get_data_from_csv(user_age: int, user_gender: str, week: int):
    # user_age: int, user_gender: str, week: int
    data = diet_planning.get_diet_menu(
        user_age= user_age,
        user_gender=user_gender,
        week=week
    )
    if not isinstance(data, list):
        return {"error": "Invalid data format. Expected a list of dictionaries."}
    return data







# -----------------------------------------------------------
# @app.get("/")
# async def root():
#     return {"message": f"Hello {get_access_token()}"}

# import google.auth.transport.requests

# from google.oauth2 import service_account

# SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']

# def get_access_token():
#   """Retrieve a valid access token that can be used to authorize requests.

#   :return: Access token.
#   """
#   credentials = service_account.Credentials.from_service_account_file(
#     'ondan-service.json', scopes=SCOPES)
#   request = google.auth.transport.requests.Request()
#   credentials.refresh(request)
#   return credentials.token

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

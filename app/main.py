#.\venv-api\Scripts\Activate.ps1
#uvicorn main:app --reload(development environment)
#order matters in requests as api goes down the list and matches the first one to host
#HTTP Get request --> API(fetches data) and goes back to the sender
#HTTP Post request(carries data(title or content)) --> API(sends back post to sender)


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models
from app.database import engine
from app.routers import post, users, auth, vote
from app.config import settings

# models.Base.metadata.create_all(bind= engine)

app = FastAPI()

origins = ["https://www.google.com"]

# Allow all origins (development only — not safe for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,  # <- allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # <- allow all HTTP methods
    allow_headers=["*"],  # <- allow all headers
)








app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


#it matches request: GET method and URL:"/"
#route/path operation set up
@app.get("/") #decorator turns it into fastapi/send a get request method to our api/ The "/" is the route path
def read_root(): #Function
    return {"message": "Welcome to my API, made by Faizan"} #return a data





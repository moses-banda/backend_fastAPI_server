from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import superbase
from schemas import WaitlistRequest

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/waitlist")
def join_waitlist(data: WaitlistRequest):
    email = data.email.lower()
    response = superbase.table("waitlist").insert({
        "email" : email
    }).execute()

    if response.error:
        if "duplicate key" in response.error.message.lower():
            raise HTTPException(status_code=409, detail="already on the waitlist")
        raise HTTPException(status_code=500, detail="Database Error")
    
    return{
        "success": True,
        "message": "We have added your name in the stars"
    }
        


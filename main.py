from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import superbase
from schemas import WaitlistRequest
from postgrest.exceptions import APIError

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
    try:
        response = superbase.table("waitlist").insert({
            "email" : email
        }).execute()
        
    except APIError as e:
        # Check for duplicate key error (Postgres code 23505)
        if e.code == "23505":
            raise HTTPException(status_code=409, detail="already on the waitlist")
        print(f"Database Error: {e}")
        raise HTTPException(status_code=500, detail="Database Error")
    except Exception as e:
        print(f"Unexpected Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    return{
        "success": True,
        "message": "We have added your name in the stars"
    }
        


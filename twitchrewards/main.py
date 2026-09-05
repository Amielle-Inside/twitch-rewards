"""Wires available routes."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from twitchrewards.controllers import (
    authentication_router,
    home_router,
    profile_router,
    trophy_router,
    user_router,
)

app = FastAPI()

# streamlabs make the request from multiple ports, making it hard
# to set a specific origin
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="twitchrewards/static"), name="static")

app.include_router(authentication_router)
app.include_router(home_router)
app.include_router(user_router, prefix="/users")
app.include_router(profile_router, prefix="/profiles")
app.include_router(trophy_router, prefix="/trophies")

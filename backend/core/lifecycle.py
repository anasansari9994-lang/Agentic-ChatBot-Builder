from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.state import state
from models.Vit_model import load_vlm

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("loading vlm model ---")
    state.vlm_model, state.processor = load_vlm()
    print("vlm loaded ---")

    yield
    
    state.vlm_model = None
    state.processor = None

    print("Shutdown the FastApi")
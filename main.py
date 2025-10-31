from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
from dotenv import load_dotenv
import uvicorn

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL", "https://api.weatherapi.com/v1")

app = FastAPI(title="Weather Proxy API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "✅ Weather Proxy API running!"}


@app.get("/search.json")
async def search_city(q: str = Query(...)):
    async with httpx.AsyncClient() as client:
        params = {"key": API_KEY, "q": q}
        try:
            res = await client.get(f"{BASE_URL}/search.json", params=params)
            res.raise_for_status()
            return res.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/forecast.json")
async def forecast_city(
    q: str = Query(...),
    days: int = 14,
    aqi: str = "yes",
    alerts: str = "no"
):
    async with httpx.AsyncClient() as client:
        params = {
            "key": API_KEY,
            "q": q,
            "days": days,
            "aqi": aqi,
            "alerts": alerts,
        }
        try:
            res = await client.get(f"{BASE_URL}/forecast.json", params=params)
            res.raise_for_status()
            return res.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 9000))
    print(f"🚀 Starting Weather Proxy API on http://localhost:{port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

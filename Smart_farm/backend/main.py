from fastapi import FastAPI
from pydantic import BaseModel

from agents.tools.smartfarm_brain import SmartFarmBrain
from agents.tools.smartfarm_router import SmartFarmRouter
from agents.weather_agent import WeatherAgent
from agents.usda_agent import USDAAgent
from agents.crop_risk_agent import CropRiskAgent
from agents.advisor_agent import AdvisorAgent
from agents.reviewer_agent import ReviewerAgent

app = FastAPI()

brain = SmartFarmBrain()
router = SmartFarmRouter()
weather = WeatherAgent()
usda = USDAAgent()
risk_agent = CropRiskAgent()
advisor = AdvisorAgent()
reviewer = ReviewerAgent()


class AdvisoryRequest(BaseModel):
    prompt: str
    lat: float | None = None
    lon: float | None = None


@app.post("/advisory")
def advisory(req: AdvisoryRequest):
    return {"response": router.handle(req.prompt, req.lat, req.lon)}


@app.get("/weather")
def get_weather(lat: float, lon: float):
    data = weather.run(lat, lon)
    return data


@app.get("/usda")
def get_usda(crop: str):
    data = usda.run(crop)
    return data


@app.post("/risk")
def get_risk(weather_data: dict, scenario: dict):
    return risk_agent.run(weather_data, scenario)


@app.post("/recommendations")
def get_recommendations(weather_data: dict, risks: dict, scenario: dict):
    return advisor.run(weather_data, risks, scenario)


@app.post("/review")
def review_recommendations(decisions: dict):
    return reviewer.run(decisions)

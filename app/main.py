import os
import json
import plotly
import uvicorn

from fastapi import FastAPI, Request, HTTPException
from fastapi.logger import logger
from fastapi.templating import Jinja2Templates
from models.fastapi_models import SimulationSubmitBody, OptimizationSubmitBody
from lib.reach_simulator import ReachSimulator
from lib.budget_optimizer import BudgetOptimizer
from utils.graph_data_utils import GraphDataUtils

APP = FastAPI()

TEMPLATES = Jinja2Templates(directory='templates')


@APP.get("/")
def index(request: Request):
    return TEMPLATES.TemplateResponse("index.html",
                                      context={"request": request})


@APP.post("/simulation/submit")
def simulation_submit(request_body: SimulationSubmitBody):
    logger.info(request_body)
    budget = request_body.budget
    media_name = request_body.media
    reach = ReachSimulator(budget, media_name).execute()
    graph_data = GraphDataUtils().line_graph_data(budget, media_name)
    graph_data_json = json.dumps(graph_data, cls=plotly.utils.PlotlyJSONEncoder)
    return {"graph": graph_data_json, "reach": reach*1_000_000}


@APP.post("/optimization/submit")
def optimization_submit(request_body: OptimizationSubmitBody):
    logger.info(request_body)
    allocated_budget, status = BudgetOptimizer(request_body).execute()
    if not status == 'optimal':
        raise HTTPException(
            status_code=400,
            detail="Can not optimize under the given conditions",
        )
    graph_data = GraphDataUtils().waterfall_graph_data(allocated_budget)
    graph_data_json = json.dumps(graph_data, cls=plotly.utils.PlotlyJSONEncoder)
    return {"graph": graph_data_json}


if __name__ == '__main__':
    uvicorn.run(APP, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

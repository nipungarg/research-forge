from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import uuid

# DB layer
from storage.db import (
    init_db,
    create_job,
    get_job,
    update_job
)

# LangGraph
from langgraph_app.main import build_graph

# ------------------------
# INIT
# ------------------------
app = FastAPI()
init_db()

graph = build_graph()


# ------------------------
# REQUEST SCHEMA
# ------------------------
class ResearchRequest(BaseModel):
    query: str


# ------------------------
# HEALTH CHECK
# ------------------------
@app.get("/")
def health():
    return {"status": "ok"}


# ------------------------
# BACKGROUND AGENT RUNNER
# ------------------------
def run_agent(job_id: str, query: str):
    try:
        state = {
            "query": query,
            "facts": [],
            "sources": [],
            "draft": "",
            "feedback": {},
            "iteration": 0,
            "llm_calls": 0,
            "memory": [],
            "job_id": job_id,
            "logs": []
        }

        # Initial state
        update_job(job_id, state=state, logs=["Job started"], status="running")

        # Run graph (node-level persistence happens inside)
        result = graph.invoke(state)

        # Final update
        update_job(
            job_id,
            state=result,
            status="completed"
        )

    except Exception as e:
        update_job(
            job_id,
            logs=[f"Error: {str(e)}"],
            status="failed"
        )


# ------------------------
# START RESEARCH (ASYNC)
# ------------------------
@app.post("/research/start")
def start_research(request: ResearchRequest, background_tasks: BackgroundTasks):
    if not request.query:
        raise HTTPException(status_code=400, detail="Query is required")

    job_id = str(uuid.uuid4())

    # Create job
    create_job(job_id)

    # 🔥 Launch in background
    background_tasks.add_task(run_agent, job_id, request.query)

    return {
        "job_id": job_id,
        "status": "running"
    }


# ------------------------
# GET STATUS / RESULT
# ------------------------
@app.get("/research/{job_id}")
def get_result(job_id: str):
    job = get_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    state = job.get("state", {})

    return {
        "job_id": job["job_id"],
        "status": job["status"],
        "result": {
            "answer": state.get("draft"),
            "iterations": state.get("iteration"),
            "llm_calls": state.get("llm_calls")
        }
    }


# ------------------------
# GET LOGS
# ------------------------
@app.get("/research/{job_id}/logs")
def get_logs(job_id: str):
    job = get_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "job_id": job_id,
        "logs": job.get("logs", [])
    }
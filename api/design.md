# API DESIGN — AI Research System

---

## 1. Start Research

### POST /research/start

### Input
{
  "query": "string"
}

### Output
{
  "job_id": "string",
  "status": "started"
}

### Errors
- 400: Missing query
- 500: Internal error

---

## 2. Get Result

### GET /research/{job_id}

### Output
{
  "job_id": "string",
  "status": "running | completed | failed",
  "result": {
    "answer": "string",
    "iterations": int,
    "llm_calls": int
  }
}

### Errors
- 404: Job not found

---

## 3. Get Logs

### GET /research/{job_id}/logs

### Output
{
  "logs": [
    "Step 1: Research started",
    "Step 2: Writing draft",
    ...
  ]
}
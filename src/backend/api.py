# src/backend/api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from typing import Dict, Any

from src.backend.scientific_paper_agent import graph
from src.backend.utils.utils import print_stream

app = FastAPI()

class Query(BaseModel):
    query: str

class Response(BaseModel):
    answer: str

@app.post("/api/query", response_model=Response)
async def process_query(query: Query) -> Dict[str, Any]:
    try:
        # Process the query using the scientific paper agent
        final_message = await print_stream(graph, query.query)
        
        if final_message:
            return {"answer": final_message.content}
        else:
            return {"answer": "No response generated."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the API server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
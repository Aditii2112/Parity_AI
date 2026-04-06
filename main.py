from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from backend_core import MCPBackend
from pydantic import BaseModel

# This handles startup and shutdown logic cleanly
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await backend.initialize()
    yield
    # Shutdown logic (optional: close MCP connections here)

app = FastAPI(title="Unified Context API", lifespan=lifespan)
backend = MCPBackend()

class QueryRequest(BaseModel):
    text: str

@app.get("/")
async def root():
    return {"status": "API is active", "version": "1.0.0"}

@app.post("/ask")
async def ask_agent(request: QueryRequest):
    try:
        answer = await backend.query(request.text)
        return {"answer": answer}
    except Exception as e:
        print(f"❌ Error during query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
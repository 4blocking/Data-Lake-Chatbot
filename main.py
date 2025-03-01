from fastapi import FastAPI
# Initialize FastAPI app
app = FastAPI(
    title="DataLakes Chatbot API",
    description="An AI-powered chatbot for querying and enriching HDFS data sources.",
    version="1.0.0"
)

# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the DataLakes Chatbot API!"}

from app.api.chatbot_endpoints import router
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

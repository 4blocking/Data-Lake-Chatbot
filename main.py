from fastapi import FastAPI
from app.api.chat_endpoints import router as chatbot_router
from app.api.user_endpoints import router as user_router
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


app.include_router(chatbot_router, prefix="/api")
app.include_router(user_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI
from backend.app.routes import router

app = FastAPI(title="TestRetry Landing API", version="1.0.0")

# Include routes
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Welcome to the TestRetry Landing API"}

@app.get("/health")
def health_check():
    return {"status": "Healthy"}

@app.get("/about")
def about():
    return {"info": "This is a business landing backend for TestRetry"}
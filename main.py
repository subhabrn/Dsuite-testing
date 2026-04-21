import uvicorn
import os

def run_server():
    """Run the FastAPI server using uvicorn"""
    from backend.main import app

    # Get port from environment or default to 8000
    port = int(os.environ.get("PORT", 8000))

    # Run the application
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=True)

if __name__ == "__main__":
    run_server()

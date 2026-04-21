
import uvicorn
from pathlib import Path
import sys

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent))

from backend.main import app

if __name__ == "__main__":
    # The uvicorn server configuration
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload in development
        log_level="info",
        proxy_headers=True,
        forwarded_allow_ips="*",
    )

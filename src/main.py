from fastapi import FastAPI

import uvicorn
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as hotels_router
from src.config import settings

app = FastAPI()

app.include_router(hotels_router)


@app.get("/")
def root():
    return {"message": "Hello World"}


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)
if __name__ == "__main__":
    main()






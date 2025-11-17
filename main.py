import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import create_document, get_documents
from schemas import Briefrequest, Creatorapplication, Subscriber

app = FastAPI(title="DSM API", description="Dusk Society Media backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "DSM API running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from DSM backend"}

# Brief requests
@app.post("/api/brief-requests")
def create_brief_request(payload: Briefrequest):
    try:
        doc_id = create_document("briefrequest", payload)
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Creator applications
@app.post("/api/creator-applications")
def create_creator_application(payload: Creatorapplication):
    try:
        doc_id = create_document("creatorapplication", payload)
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Subscribers
@app.post("/api/subscribers")
def create_subscriber(payload: Subscriber):
    try:
        doc_id = create_document("subscriber", payload)
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Showcase items (simple read-only list; could be moved to DB later)
class ShowcaseItem(BaseModel):
    title: str
    type: str
    cover: str
    tags: Optional[List[str]] = None

@app.get("/api/showcase", response_model=List[ShowcaseItem])
def get_showcase_items():
    # In a real system this would query the database. Here we return a fast static list.
    return [
        {"title": "Back Alley Cypher", "type": "Film", "cover": "/covers/cypher.jpg", "tags": ["film", "music", "night"]},
        {"title": "Steel & Neon", "type": "Photo", "cover": "/covers/steel-neon.jpg", "tags": ["photo", "city", "grit"]},
        {"title": "Walls Talk", "type": "Doc", "cover": "/covers/walls-talk.jpg", "tags": ["doc", "graffiti"]},
        {"title": "Heatwave", "type": "Edit", "cover": "/covers/heatwave.jpg", "tags": ["edit", "motion"]},
    ]

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        from database import db
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = getattr(db, 'name', '✅ Connected')
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except ImportError:
        response["database"] = "❌ Database module not found"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

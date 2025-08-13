from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
import crud
import models
import schemas
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="MedBrief Backend")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.mount("/PPT", StaticFiles(directory="PPT"), name="ppt")

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Topic Management API ---

@app.post("/topics/", response_model=schemas.Topic, status_code=201)
def create_topic(topic: schemas.TopicCreate, db: Session = Depends(get_db)):
    """
    Create a new topic.
    """
    return crud.create_topic(db=db, topic=topic)

@app.get("/topics/", response_model=List[schemas.Topic])
def list_topics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get a list of all topics.
    """
    topics = crud.get_topics(db, skip=skip, limit=limit)
    return topics

@app.get("/topics/{topic_id}", response_model=schemas.Topic)
def get_topic(topic_id: int, db: Session = Depends(get_db)):
    """
    Get details of a specific topic.
    """
    db_topic = crud.get_topic(db, topic_id=topic_id)
    if db_topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return db_topic

@app.put("/topics/{topic_id}", response_model=schemas.Topic)
def update_topic(topic_id: int, topic: schemas.TopicCreate, db: Session = Depends(get_db)):
    """
    Update an existing topic.
    """
    db_topic = crud.update_topic(db, topic_id=topic_id, topic_update=topic)
    if db_topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return db_topic

@app.delete("/topics/{topic_id}", status_code=204)
def delete_topic(topic_id: int, db: Session = Depends(get_db)):
    """
    Delete a topic.
    """
    if not crud.delete_topic(db, topic_id=topic_id):
        raise HTTPException(status_code=404, detail="Topic not found")
    return

@app.get("/topics/{topic_id}/history", response_model=schemas.TopicHistory)
def get_topic_update_history(topic_id: int, db: Session = Depends(get_db)):
    """
    Get the update history for a topic.
    """
    db_topic = crud.get_topic(db, topic_id=topic_id)
    if db_topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    updates = crud.get_topic_history(db, topic_id=topic_id)
    return schemas.TopicHistory(topic_id=topic_id, updates=updates)


# --- Literature Updates API ---

@app.get("/topics/{topic_id}/literature-analysis", response_model=schemas.LiteratureAnalysis)
def get_literature_analysis_for_topic(topic_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Get literature analysis for a specific topic.
    """
    db_topic = crud.get_topic(db, topic_id=topic_id)
    if db_topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    analysis_data = crud.get_literature_analysis(db, topic_id=topic_id, skip=skip, limit=limit)
    return analysis_data


# --- PPT Push History API ---

@app.get("/ppt-history/", response_model=List[schemas.PPTPushRecord])
def get_ppt_push_history(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get the history of PPT pushes.
    """
    return crud.get_ppt_push_history(db, skip=skip, limit=limit)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
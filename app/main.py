from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel
import datetime
import os

# 1. Database Setup (Reads from Docker Compose environment)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://gazi_user:gazi_password@db:5432/gazi_db")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. ORM Model (Creates the 'items' table)
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# Automatically create the tables when the app starts
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gazi BMT-408 API")

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 3. Pydantic Schemas (For input validation)
class ItemCreate(BaseModel):
    title: str
    content: str

class ItemResponse(ItemCreate):
    id: int
    created_at: datetime.datetime
    class Config:
        from_attributes = True

# 4. API Endpoints

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/items", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(title=item.title, content=item.content)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items", response_model=list[ItemResponse])
def read_items(db: Session = Depends(get_db)):
    return db.query(Item).all()

@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, updated_item: ItemCreate, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item.title = updated_item.title
    item.content = updated_item.content
    db.commit()
    db.refresh(item)
    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item deleted"}

from http.client import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import SessionLocal
from app.routers.dependencies import get_current_user

router = APIRouter(prefix="/books")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def list_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()


@router.post("/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db),
                user=Depends(get_current_user),
                ):
    obj = models.Book(title=book.title,
                      author=book.author,
                      description=book.description,
                      year=book.year,
                      )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.put("/{book_id}", response_model=schemas.Book)
def update_book(
        book_id: int,
        book: schemas.BookUpdate,
        db: Session = Depends(get_db),
        user=Depends(get_current_user),
):
    obj=db.query(models.Book).filter(models.Book.id == book_id).first()
    if not obj:
        raise HTTPException(status_code=404,detail="Book not found")
    for field, value in book.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{book_id}")
def delete_book(
        book_id: int,
        db: Session = Depends(get_db),
        user=Depends(get_current_user),
):
    obj=db.query(models.Book).filter(models.Book.id == book_id).first()
    if not obj:
        raise HTTPException(status_code=404,detail="Book not found")

    db.delete(obj)
    db.commit()
    return {"detail" : "Book deleted"}

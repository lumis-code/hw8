from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import schemas, models, repositories, security
from .database import engine
from .deps import get_db, get_current_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Flowers API with SQLAlchemy")


@app.post("/signup", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def signup(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    repo = repositories.UsersRepository(db)
    if repo.get_by_username(user_data.username) or repo.get_by_email(user_data.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    return repo.create(user_data)


@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = repositories.UsersRepository(db).authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token = security.create_access_token({"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/profile", response_model=schemas.UserRead)
def profile(current_user: models.User = Depends(get_current_user)):
    return current_user


@app.get("/flowers", response_model=list[schemas.FlowerRead])
def list_flowers(db: Session = Depends(get_db)):
    return repositories.FlowersRepository(db).list_all()


@app.post("/flowers", response_model=schemas.FlowerRead, status_code=status.HTTP_201_CREATED)
def create_flower(flower_data: schemas.FlowerCreate, db: Session = Depends(get_db)):
    return repositories.FlowersRepository(db).create(flower_data)


@app.patch("/flowers/{flower_id}", response_model=schemas.FlowerRead)
def update_flower(flower_id: int, update_data: schemas.FlowerUpdate, db: Session = Depends(get_db)):
    repo = repositories.FlowersRepository(db)
    flower = repo.get_by_id(flower_id)
    if not flower:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flower not found")
    return repo.update(flower, update_data)


@app.delete("/flowers/{flower_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_flower(flower_id: int, db: Session = Depends(get_db)):
    repo = repositories.FlowersRepository(db)
    flower = repo.get_by_id(flower_id)
    if not flower:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flower not found")
    repo.delete(flower)


@app.get("/cart/items", response_model=list[schemas.CartItemRead])
def get_cart_items(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return repositories.PurchasesRepository(db).get_cart_items(current_user.id)


@app.post("/purchased", response_model=schemas.PurchaseRead, status_code=status.HTTP_201_CREATED)
def buy_item(purchase_data: schemas.PurchaseCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return repositories.PurchasesRepository(db).add_purchase(current_user.id, purchase_data)


@app.get("/purchased", response_model=list[schemas.PurchaseRead])
def list_purchases(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return repositories.PurchasesRepository(db).get_purchased(current_user.id)

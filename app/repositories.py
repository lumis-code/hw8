from sqlalchemy.orm import Session
from . import models, schemas
from .security import get_password_hash, verify_password


class UsersRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> models.User | None:
        return self.db.query(models.User).filter(models.User.username == username).first()

    def get_by_email(self, email: str) -> models.User | None:
        return self.db.query(models.User).filter(models.User.email == email).first()

    def get_by_id(self, user_id: int) -> models.User | None:
        return self.db.query(models.User).filter(models.User.id == user_id).first()

    def create(self, user_create: schemas.UserCreate) -> models.User:
        hashed_password = get_password_hash(user_create.password)
        user = models.User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate(self, username: str, password: str) -> models.User | None:
        user = self.get_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user


class FlowersRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> list[models.Flower]:
        return self.db.query(models.Flower).all()

    def get_by_id(self, flower_id: int) -> models.Flower | None:
        return self.db.query(models.Flower).filter(models.Flower.id == flower_id).first()

    def create(self, flower_create: schemas.FlowerCreate) -> models.Flower:
        flower = models.Flower(**flower_create.model_dump())
        self.db.add(flower)
        self.db.commit()
        self.db.refresh(flower)
        return flower

    def update(self, flower: models.Flower, update_data: schemas.FlowerUpdate) -> models.Flower:
        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(flower, field, value)
        self.db.commit()
        self.db.refresh(flower)
        return flower

    def delete(self, flower: models.Flower) -> None:
        self.db.delete(flower)
        self.db.commit()


class PurchasesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_cart_items(self, user_id: int) -> list[models.Purchase]:
        return (
            self.db.query(models.Purchase)
            .filter(models.Purchase.user_id == user_id, models.Purchase.status == models.PurchaseStatus.in_cart)
            .all()
        )

    def get_purchased(self, user_id: int) -> list[models.Purchase]:
        return (
            self.db.query(models.Purchase)
            .filter(models.Purchase.user_id == user_id, models.Purchase.status == models.PurchaseStatus.purchased)
            .all()
        )

    def add_purchase(self, user_id: int, purchase_create: schemas.PurchaseCreate) -> models.Purchase:
        purchase = models.Purchase(
            user_id=user_id,
            flower_id=purchase_create.flower_id,
            quantity=purchase_create.quantity,
            status=models.PurchaseStatus(purchase_create.status.value),
        )
        self.db.add(purchase)
        self.db.commit()
        self.db.refresh(purchase)
        return purchase

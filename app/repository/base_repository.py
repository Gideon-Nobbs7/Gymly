from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.config.database_config import get_db
from app.core.exceptions import NotFoundError


class BaseRepository:
    """
    Base Repository to perform CRUD operations on database models
    """

    def __init__(self, model: None, db: Session = Depends(get_db)):
        self.model = model
        self.db = db

    def create(self, schema):
        query = self.model(**schema.model_dump())
        try:
            self.db.add(query)
            self.db.commit()
            self.db.refresh(query)
            return query
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A member with this unique field already exists."
            )
        except Exception as e:
            self.db.rollback()
            raise e

    def read_all(
        self, eager=False, order_by=None, limit: int = 10, page: int = 1, **filters
    ):
        query = self.db.query(self.model)
        if eager:
            for eager in getattr(self.model, "eagers", []):
                query = query.options(joinedload(getattr(self.model, eager)))

        for key, value in filters.items():
            query = query.filter(getattr(self.model, key) == value)

        if order_by is not None:
            query = query.order_by(order_by)

        return query.limit(limit).offset((page - 1) * limit).all()

    def read_one(self, id: int | str, eager=False, order_by=None):
        query = self.db.query(self.model)
        if eager:
            for eager in getattr(self.model, "eagers", []):
                query = query.options(joinedload(getattr(self.model, eager)))

        if order_by is not None:
            query = query.order_by(order_by)

        query = query.filter(self.model.id == id).first()
        if not query:
            raise NotFoundError(
                message=f"{self.model.__name__} with id {id} not found",
                detail="Not Found",
            )

        return query

    def read_where(self, order_by=None, limit=None, **filters):
        query = self.db.query(self.model)
        for key, value in filters.items():
            query = query.filter(getattr(self.model, key) == value)

        if order_by is not None:
            query = query.order_by(order_by)

        if limit is None:
            query = query.limit(limit)

        return query.first() if limit == 1 else query.all()

    def update(self, id: int | str, schema):
        query = self.read_one(id)
        for key, value in schema.model_dump(exclude_unset=True).items():
            setattr(query, key, value)
        self.db.commit()
        self.db.refresh(query)
        return query

    def delete(self, id: int | str):
        query = self.read_one(id)
        self.db.delete(query)
        self.db.commit()
        return

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi import HTTPException, status
from pydantic import BaseModel

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, and_, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import exists

from db.base_class import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """ CRUD object with default methods to Create, Read, Update, & Delete

        Args:
            model (Type[ModelType]): A SQLAlchemy model class
        """
        self.model = model


    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """ Get row from model where id == model.id

        Args:
            db (AsyncSession): Async db session
            id (Any): Id to filter

        Returns:
            Optional[ModelType]: ModelType instance or None if id not exists
        """
        res = await db.execute(select(self.model).where(self.model.id == id))
        return res.scalar()
    

    async def get_or_404(
        self,
        db: AsyncSession,
        id: Any
    ) -> Optional[ModelType]:
        """ Try to dgt row from model where id == model.id

        Args:
            db (AsyncSession): Async db session
            id (Any): Id to filter

        Raises:
            HTTPException: HTTP_404_NOT_FOUND if item does not exist

        Returns:
            Optional[ModelType]: ModelType instance
        """

        # try get item
        obj = await self.get(db=db, id=id)
        
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} {id} does not exist"
            )

        return obj

    
    async def get_all(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        """ Get multi items from database without filter criteria

        Args:
            db (AsyncSession): Async db session
            skip (int, optional): Optional Offset. Defaults to 0.
            limit (int, optional): Optional limit. Defaults to 100.

        Returns:
            List[ModelType]: Matching results list
        """
        results = await db.execute(select(self.model).offset(skip).limit(limit))
        return results.scalars().all()
    

    async def filter(
        self,
        db: AsyncSession,
        *,
        whereclause: Any,
        skip: int = 0,
        limit: int = 100,
    ) -> Union[List[ModelType], ModelType]:
        """ Get items from database using `filters` to filter

        Args:
            db (AsyncSession): Async db session
            filters (Union[list, tuple]): [description]
            criterion (str, optional): [description]. Defaults to 'and'.
            skip (int, optional): Optional Offset. Defaults to 0.
            limit (int, optional): Optional limit. Defaults to 100.
            multiple (bool, optional): 
                Optional bool to get single or multi items.
                Defaults to True.

        Returns:
            Union[List[ModelType], ModelType]: 
                Instance or list of intance of matching items.
        """
        
        # try to get
        result = await db.execute(
            select(self.model)
            .where(whereclause)
            .offset(skip)
            .limit(limit)
        )

        return result.scalars().all()
    

    async def create(
        self,
        db: AsyncSession,
        *,
        data: CreateSchemaType
    ) -> ModelType:
        """ Try to create item in database

        Args:
            db (AsyncSession): Async db session
            data (CreateSchemaType): Schema to create

        Raises:
            HTTPException: HTTP_400_BAD_REQUEST if item already exists
            HTTPException: HTTP_400_BAD_REQUEST for other errors

        Returns:
            ModelType: Instance of created object
        """

        try:
            # try json encode
            # obj_data = jsonable_encoder(obj)
            db_obj = self.model(**jsonable_encoder(data))
            
            # add to database
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)

            # return instance
            return db_obj
            
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{self.model.__name__} already exists. Check parameters"
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Somethig was wrong"
            )
        
    
    async def update(
        self,
        db: AsyncSession,
        *,
        obj: ModelType,
        data: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """ Update a database item with an update schema

        Args:
            db (AsyncSession): Async db session
            obj (ModelType): Item to update
            obj (Union[UpdateSchemaType, Dict[str, Any]]): 
                New partial or full data for database item

        Returns:
            ModelType: [description]
        """
        
        # obj to dict
        if isinstance(data, dict):
            update_data = data
        else:
            update_data = data.model_dump(exclude_unset=True)
        
        # update obj with each field of obj
        for field, value in update_data.items():
            setattr(obj, field, value)

        # save, commit and refresh session
        db.add(obj)
        await db.commit()
        await db.refresh(obj)

        # return updated object
        return obj
    

    async def delete(self, db: AsyncSession, *, id: int) -> ModelType:
        """ Delete an item from database

        Args:
            db (AsyncSession): Async db session
            id (int): Id of model to delete

        Returns:
            ModelType: Deleted object instance
        """
        obj = await self.get_or_404(db=db, id=id)

        await db.delete(obj)
        await db.commit()

        return obj
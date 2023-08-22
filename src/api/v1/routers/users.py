from typing import List
from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from api import dependencies as deps
from schemas import users as user_schemas
from crud import users as crud_users


router = APIRouter(include_in_schema=True)


@router.get('/')
async def get_users(
    *,
    db: AsyncSession = Depends(deps.get_db)
) -> List[user_schemas.User]:
    """Get users

    Args:
        db (AsyncSession, optional):
            Database Session.
            Defaults to Depends(deps.get_db).

    Returns:
        List[user_schemas.User]: [description]
    """
    
    return await crud_users.get_all(db=db)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(
    *,
    data: user_schemas.UserCreate,
    db: AsyncSession = Depends(deps.get_db),
) -> user_schemas.User:
    """Create user with inner data

    Args:
        db (AsyncSession, optional):
            Database Session.
            Defaults to Depends(deps.get_db).
        data (user_schemas.UserCreate): User schema data

    Raises:
        HTTPException: HTTP_400_BAD_REQUEST if item already exists

    Returns:
        user_schemas.User: User data
    """

    return await crud_users.create(db=db, data=data)


@router.get('/{id}')
async def get_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int = Path(...)
) -> user_schemas.User:
    """Get User by internal id

    Args:
        db (AsyncSession, optional):
            Database Session.
            Defaults to Depends(deps.get_db).
        id (int): Internal id

    Raises:
        HTTPException: HTTP_404_NOT_FOUND if user does not exist

    Returns:
        user_schemas.User: User data
    """

    # get user from db
    return await crud_users.get_or_404(db=db, id=id)


@router.delete('/{id}')
async def delete_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int = Path(...),
) -> user_schemas.User:
    """Delete user by id

    Args:
        db (AsyncSession, optional):
            Database Session.
            Defaults to Depends(deps.get_db).
        id (int): User internal Id

    Raises:
        HTTPException: HTTP_404_NOT_FOUND if user does not exist

    Returns:
        user_schemas.User: Data of deleted user
    """

    return await crud_users.delete(db=db, id=id)


@router.patch('/{id}')
async def update_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int = Path(...),
    data: user_schemas.UserUpdate
) -> user_schemas.User:
    """Partial or complete update of an user

    Args:
        db (AsyncSession, optional):
            Database Session.
            Defaults to Depends(deps.get_db).
        id (int): User internal Id
        data (user_schemas.UserUpdate): New user data

    Raises:
        HTTPException: HTTP_404_NOT_FOUND

    Returns:
        user_schemas.User: Full User data with new values
    """

    # get User
    user = await crud_users.get_or_404(db=db, id=id)
    
    # update data and return updated
    return await crud_users.update(
        db=db,
        obj=user,
        data=data
    )
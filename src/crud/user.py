from crud.base import CRUDBase
from models import User as UserModel
from schemas.users import UserCreate, UserUpdate


class CRUDUser(CRUDBase[UserModel, UserCreate, UserUpdate]):
    ...


users = CRUDUser(UserModel)
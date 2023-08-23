import base64 as b64
import jwt
from uuid import uuid1
from datetime import datetime, timedelta
from typing import Union, Any

from .config import settings
from cryptography.fernet import Fernet


cipher = Fernet(settings.SECRET_KEY)


def create_access_token(sub: Union[str, int, Any]) -> str:
    """Create an access token for a specific sub

    Args:
        sub (Union[str, int, Any]): User, session or other

    Returns:
        str: JWT Token
    """
    
    # expire time
    expire = datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRE_MINS)

    # base keys
    to_encode = {
        "uuid": str(uuid1()),
        "sub": str(sub),
        "exp": int(expire.timestamp())
    }

    # create token
    return jwt.encode(
        payload=to_encode,
        key=b64.b64decode(settings.PRIVATE_KEY),
        algorithm=settings.TOKEN_ALGORITHM
    )


def encrypt_password(password: str) -> str:
    """ Encrypt a password using Fernet cipher

    Args:
        password (str): Password to encrypt

    Returns:
        str: Crypted password
    """

    return cipher.encrypt(password.encode('utf-8')).decode('utf-8')


def decrypt_password(encrypted_password: str) -> str:
    """ Decrypt a Fernet encrypted

    Args:
        encrypted_password (str): Encrypted password

    Returns:
        str: Decrypted password
    """

    return cipher.decrypt(encrypted_password.encode('utf-8')).decode('utf-8')
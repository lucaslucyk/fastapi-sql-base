import base64 as b64
import logging
import typer
from typing import Tuple
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.fernet import Fernet


def get_RSA_keys(
    public_exponent: int = 65537,
    key_size: int = 2048
) -> Tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:

    # generate RSA private key
    private_key = rsa.generate_private_key(
        public_exponent=public_exponent,
        key_size=key_size,
    )

    return private_key, private_key.public_key()


def get_pem_from_rsa(
    private_key: rsa.RSAPrivateKey,
    public_key: rsa.RSAPublicKey
) -> Tuple[bytes, bytes]:

    # serialize private key
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # serialize public key
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem, public_pem


def get_b64_from_pem(
    private_pem: bytes,
    public_pem: bytes
) -> Tuple[bytes, bytes]:
    return b64.b64encode(private_pem), b64.b64encode(public_pem)


def get_pem_from_b64(
    private_b64: bytes,
    public_b64: bytes
) -> Tuple[bytes, bytes]:
    return b64.b64decode(private_b64), b64.b64decode(public_b64)


if __name__ == "__main__":
    def _generate_keys(
        public_exponent: int = 65537,
        key_size: int = 2048
    ) -> None:
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        private_key, public_key = get_RSA_keys(
            public_exponent=public_exponent,
            key_size=key_size
        )
        private_pem, public_pem = get_pem_from_rsa(private_key, public_key)
        private_b64, public_b64 = get_b64_from_pem(private_pem, public_pem)

        logging.info(f"PRIVATE_KEY={private_b64.decode()}")
        logging.info(f"PUBLIC_KEY={public_b64.decode()}")
        logging.info(f"SECRET_KEY={Fernet.generate_key().decode()}")
    
    typer.run(_generate_keys)
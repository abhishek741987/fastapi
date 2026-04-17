from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_password_hash(password: str):
    print('password', password)
    return bcrypt_context.hash(password)

# import secrets
# def generate_secret_key():
#     return secrets.token_hex(16)
# if __name__ == '__main__':
#     secret_key = generate_secret_key()
#     print(f"Generated Secret Key: {secret_key}")

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
def generate_bcrypt_hash(password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    return hashed_password
if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python generate_hash.py <password>")
        sys.exit(1)
    password = sys.argv[1]
    hashed_password = generate_bcrypt_hash(password)
    print(f"Bcrypt Hash for '{password}': {hashed_password}")
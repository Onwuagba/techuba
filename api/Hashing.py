import bcrypt

def hash_password(self, password):
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password

def check_password(input, hashed):
    return bcrypt.checkpw(input, hashed)
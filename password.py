import bcrypt
import os

DIARY_PWD = "password_hash.txt"
PER_PWD="per_password_hash.txt"

def per_save(passwordie,filename1=PER_PWD):
    hashed1=bcrypt.hashpw(passwordie.encode(),bcrypt.gensalt())
    with open(filename1,"wb") as file1:
        file1.write(hashed1)
    print("Personal password saved successfully")

def per_load(filename1=PER_PWD):
    if os.path.exists(filename1):
        with open(filename1,"rb") as file1:
            return file1.read()
    return None

def save_psd(password, filename=DIARY_PWD):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    with open(filename, "wb") as file:
        file.write(hashed)
    print("Password saved successfully!")

def verify():
    per_password_hash=per_load()
    if not per_password_hash:
        return False


def load_psd(filename=DIARY_PWD):
    if os.path.exists(filename):
        with open(filename, "rb") as file:
            return file.read()
    return None


def set_psd():
    password_hash=load_psd()
    if not password_hash:
        new_psw = input("Enter new password: ")
        save_psd(new_psw)
        print("Password updated successfully.")


def auth_user2():
    password_hash = load_psd()
    if not password_hash:
        set_psd()
        return True

    per_password_hash = per_load()
    if not per_password_hash:
        verify()
        return True

    while True:
        entered_password = input("Enter your password to access the diary: ")
        if bcrypt.checkpw(entered_password.encode(), password_hash):
            print("Authentication successful.")
            return True
        else:
            print("Incorrect password.")
        while True:
            if input("Forgot password? (y/n): ").strip().lower() in ["y", "yes"]:
                per_password_hash=per_load()
                verification=input("Enter your favourite snack/food:")
                if bcrypt.checkpw(verification.encode(),per_password_hash):
                    new_psw = input("Enter new password: ")
                    save_psd(new_psw)
                    print("Password updated successfully.")
                else:
                    print("Access denied.")

                password_hash = load_psd()

                entered_password = input("Enter your new password to access the diary: ")
                if bcrypt.checkpw(entered_password.encode(), password_hash):
                    print("Authentication successful.")
                    return True
                else:
                    print("Incorrect password.")
                    continue
            else:
                print("Password unchanged.")
                break
        continue


def set_per_psd():
    per_psd_hash=per_load()
    if not per_psd_hash:
        print("Answer the following question to save it as your permanent password.")
        new_per_psd=input("Enter your favourite food/snack:")
        per_save(new_per_psd)
        print("Your permanent password created successfully!")

def main_psw():
    current_assword_hash = load_psd()
    if not current_assword_hash:
        new_psw = input("Enter your first password:")
        save_psd(new_psw)
        print("Password created successfully!")
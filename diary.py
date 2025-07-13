import datetime
import os.path
import time
from password import main_psw, load_psd, set_psd, auth_user2, save_psd, per_load, set_per_psd, verify, per_save
from colorama import Back,Fore
import cryptography
from cryptography.fernet import Fernet

print(f"{Fore.MAGENTA}")

KEY_FILE="secret.key"

def generate_key():
    if not os.path.exists(KEY_FILE):
        Key=Fernet.generate_key()
        with open(KEY_FILE,"wb") as key_file:
            key_file.write(Key)


def load_key():
    return open(KEY_FILE,"rb").read()

authenticated = False

DIARY_DIRECTORY="diaries"

if not os.path.exists(DIARY_DIRECTORY):
    os.makedirs(DIARY_DIRECTORY)

def per_load():
    try:
        with open("per_password_hash.txt","rb") as file1:
            return file1.read()
    except FileNotFoundError:
        return None

def load_psd():
    try:
        with open("password_hash.txt", "rb") as file:
            return file.read()
    except FileNotFoundError:
        return None

def auth_user():
    current_assword_hash = load_psd()
    if not current_assword_hash:
        main_psw()
        return

def verify_user():
    per_password_hash=per_load()
    if not per_password_hash:
        set_per_psd()
        return

def encrypt_message(message):
    Key=load_key()
    fernet=Fernet(Key)
    encrypted_message=fernet.encrypt(message.encode())
    return encrypted_message

def save_diary(content, title):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{title}.txt"
    encrypted_content=encrypt_message(content)
    os.makedirs(DIARY_DIRECTORY, exist_ok=True)
    with open(os.path.join(DIARY_DIRECTORY,filename), "wb") as file:
        file.write(encrypted_content)
    print(f"'{filename}' saved at {timestamp}.")

def decrypt_message(encrypted_content):
    try:
        key = load_key()
        fernet = Fernet(key)
        decrypted_content = fernet.decrypt(encrypted_content).decode()
        return decrypted_content
    except Exception as e:
        print(f"Error decrypting content: {e}")
        return ""


def read_diary(filename):
    try:
        with open(os.path.join(DIARY_DIRECTORY, filename), "rb") as file:
            encrypted_content = file.read()
        content = decrypt_message(encrypted_content)
        return content
    except Exception as e:
        print(f"Error reading diary: {e}")
        return ""


def write_diary():
    auth_user()
    verify_user()

    while True:
        content = input("Write your diary here...('q' to quit)\n>>>")
        if content.lower() in ["q", "quit"]:
            break

        title = input("Enter a title:")
        if not title:
            print("Title shouldn't be empty.")
            continue

        print("Saving...")
        time.sleep(3)
        valid_title = "".join(c for c in title if c.isalnum() or c in (" ", "-")).rstrip()
        save_diary(content, valid_title)
        return main()

def search_diary():
    auth_user2()
    set_psd()
    print("Your diary entries:")
    entries=os.listdir(DIARY_DIRECTORY)
    if entries:
        for entry in entries:
            print(f"- {entry}")
    else:
        print("No directory entries found.")
    search=input("Write the name of the diary to search:").strip()
    if search not in["q","quit"]:
        match=[entry for entry in entries if search in entry]
        if match:
            for i, entry in enumerate(match, 1):
                print(f"{i}. {entry}")

            try:
                choice = int(input("\nEnter the number of the diary you want to read: "))
                if 1 <= choice <= len(match):
                    selected_entry = match[choice - 1]
                    content=read_diary(selected_entry)
                    title=selected_entry.split('_')[0]
                    if '.' in title:
                        title = title.rsplit('.', 1)[0]
                    print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
                    print(title)
                    print("---------------------------------------------------------------------------------------------------------------------------------------")
                    print(content)
                    print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n")
                    exit=input("")
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Please enter a valid number.")
        else:
            print("No matching diary entries found.")
            exitin=input("")
            return main()
    else:
        return main()


def edit_diary():
    auth_user2()
    set_psd()
    print("Your diary entries:")
    entriees=os.listdir(DIARY_DIRECTORY)
    if entriees:
        for ent in entriees:
            print(f"- {ent}")
    else:
        print("No directory entries found.")
        exitin = input("")
        return main()
    enter=input("Enter the name of diary you want to edit:").strip()
    if enter not in["q","quit"]:
        matchs=[ent for ent in entriees if enter in ent]
        if not matchs:
            print("No diary entries found.")
            exitin = input("")
            return main()
        if len(matchs)>1:
            for i,ent in enumerate(matchs,1):
                print(f"{i}. {ent}")
            try:
                ch=int(input("Enter the number of diary you want to edit:"))
                if 1<=ch<=len(matchs):
                    sel_entry=matchs[ch-1]
                    file_path = os.path.join(DIARY_DIRECTORY, sel_entry)
                    with open(file_path, "rb") as file:  # Open in binary mode to decrypt
                        encrypted_content = file.read()
                    content = decrypt_message(encrypted_content)
                    print(f"\n{sel_entry}:\n")
                    print(content)
                else:
                    print("Invalid choice.")
                    return
            except ValueError:
                print("Enter a valid choice.")
                return
        else:
            sel_entry=matchs[0]

        file_path = os.path.join(DIARY_DIRECTORY, sel_entry)
        with open(file_path, "rb") as file:
            encrypted_content = file.read()
        content = read_diary(sel_entry)
        if content:
            print(f"\nTitle: {sel_entry.split('_')[0]}")
            print("-" * 60)
            print(content)

        new_content = input("\nEnter new content to replace the current one (or type 'add' to add new content): ").strip()
        if new_content.lower() == "add":
            print("---------------------------------------------------------------------------------------------------------------------------------------")
            additional_content = input("Enter the additional content: ")
            print("---------------------------------------------------------------------------------------------------------------------------------------")
            content += "\n" + additional_content
        else:
            content = new_content
        encrypted_content=encrypt_message(content)
        with open(file_path, "wb") as file:
            file.write(encrypted_content)
        print(f"Diary entry {sel_entry} has been updated successfully.")
    else:
        return main()

def del_diary():
    auth_user2()
    set_psd()
    print("Your diary entries:")
    entries = os.listdir(DIARY_DIRECTORY)
    if entries:
        for entry in entries:
            print(f"- {entry}")
    else:
        print("No directory entries found.")
        exitin = input("")
        return

    delete=input("Enter a file name you want to delete:")
    if delete not in["q","quit"]:
        match=[entry for entry in entries if delete in entry]
        if not match:
            print("No diary entries found.")
            exitin = input("")
            return
        if match:
            if len(match)>1:
                for i,entry in enumerate(match,1):
                    print(f"{i}. {entry}")
                try:
                    choice=int(input("Enter the number of diary you want to delete:"))
                    if 1<=choice<=len(match):
                        select_entry=match[choice-1]
                    else:
                        print("Invalid choice.")
                        return
                except ValueError:
                    print("Enter a valid choice")
                    return
            else:
                select_entry=match[0]

            confirm=input(f"Do you want to permanently delete {select_entry}?(y/n):")
            if confirm in ["y","yes"]:
                file_path=os.path.join(DIARY_DIRECTORY,select_entry)
                os.remove(file_path)
                print(f"{select_entry} has been removed from your directory successfully.")
                return
            else:
                print("Deletion cancelled.")
                return
        else:
            print("No directory entries found.")
            exitin = input("")
            return
    else:
        return main()

def main():
    set_per_psd()
    main_psw()
    time.sleep(1)
    while True:
        print("---------------------------------------------------------------------------------------------------------------------------------------")
        choice = input("What would you like to do?\n1.Write a new diary\n2.Search for the existing diary\n3.Edit a diary\n4.Delete an existing diary\n5.Exit\n>>>")
        if choice == '1':
            write_diary()
        elif choice == '2':
            search_diary()
        elif choice == '3':
            edit_diary()
        elif choice == '4':
            del_diary()
        elif choice == '5':
            exit(1)
        else:
            continue


if __name__ == "__main__":
    main()
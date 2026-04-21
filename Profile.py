import os
import shutil
from NewsManagment import NewsManager
from Email_Maintance import send_verification_code
import Password_Security
class Profile:
    def __init__(self, id, profile_pic = None,display_color = None):
        self.id = id
        self.display_color = display_color
        self.profile_pic = profile_pic
        self.article_preferences = []
        self.saved_articles = []
        self.new_manager = NewsManager()
        self.page_size = 20

    def change_email(self,cursor,conn):
        while True:
            new_email = input("Enter new email: ").strip()
            if "@" not in new_email or "." not in new_email:
                print("Invalid email")
                continue
            else:
                break
        code = send_verification_code(new_email)
        if not code:
            print("Failed to send verification email.")
            return
        while True:
            verification = input("Enter your verification code: ")
            if verification != code:
                print("Incorrect code, please try again")
            else:
                break
        sql = """ UPDATE "user" SET email = %s WHERE id = %s; """
        cursor.execute(sql,(new_email,self.id))
        conn.commit()
        print("Your email has changed")

    def change_password(self,cursor,conn):
        class InvalidPasswordChange(Exception):
            pass
        attempts = 0
        sql = """ SELECT email FROM "user" WHERE id = %s; """
        cursor.execute(sql,(self.id,))
        result = cursor.fetchone()
        user_db_email = result["email"]
        while True:
            email = input("Enter email: ")
            if user_db_email != email:
                print("Incorrect email please try again")
                continue
            else:
                code = send_verification_code(email)
                print("A code was sent to your email for verification.")
                verify_code = input("Please input the code: ")
                if verify_code != code:
                    print("Incorrect code, please try again")
                else:
                    break
        while True:
            try:
                new_password = input("Enter new password: ")
                if len(new_password) < 8 or len(new_password) > 32:
                    raise InvalidPasswordChange("Password must be 8-32 characters")
                elif not any(char.isupper() for char in new_password) or not any(char.islower() for char in new_password):
                    raise InvalidPasswordChange("Must contain at least must 1 upper case and 1 lowercase letter")
                elif not any(char.isdigit() for char in new_password):
                    raise InvalidPasswordChange("Must have at least one digit in your password")
                else:
                    password_hash = Password_Security.hash_password(new_password)
                    sql = """UPDATE "user" SET password = %s WHERE id = %s;"""
                    cursor.execute(sql,(password_hash,self.id))
                    conn.commit()
                    print("Your password has changed.")
                    break
            except InvalidPasswordChange as e:
                print(e)

    def profile_pic(self):
        profile_pic_folder = "profile pics"
        file_path = input("Path for profile pic: ").strip()
        if not os.path.exists(file_path):
            print("Path does not exist")
            return
        if not os.path.exists(profile_pic_folder):
            os.makedirs(profile_pic_folder)
        file_ext = os.path.splitext(file_path)[1]
        user_pic = str(self.id) + file_ext
        destination_path = os.path.join(profile_pic_folder, user_pic)
        shutil.copy(file_path, destination_path)
        self.profile_pic = user_pic

    def change_username(self,user,cursor,conn):
        class InvalidUserSetup(Exception):
            pass
        while True:
            try:
                new_username = input("Enter new username: ").strip()
                if len(new_username) < 8 or len(new_username) > 32:
                    raise InvalidUserSetup("Username must be 8-32 characters")
                sql = """SELECT EXISTS(SELECT 1 FROM "user" WHERE username = %s);
                """
                cursor.execute(sql, (new_username,))
                exists = cursor.fetchone()['exists']
                if exists:
                    raise InvalidUserSetup("This username is taken")
                break
            except InvalidUserSetup as e:
                print(e)
        sql = """ UPDATE "user" SET username = %s WHERE id = %s; """
        cursor.execute(sql, (new_username, self.id))
        conn.commit()
        user.username = new_username
        print("Username changed")

    def delete_profile(self,cursor,conn):
        sql = """DELETE FROM "user" WHERE id = %s;"""
        cursor.execute(sql,(self.id,))
        conn.commit()
        print("Account deleted")
        return True

    def change_page_size(self):
        while True:
            try:
                size = int(input("How many articles would you like to see at a time? (1-100): "))
                if 1 <= size <= 100:
                    self.page_size = size
                    print(f"Updated. You'll now see {size} articles at a time.")
                    break
                else:
                    print("Please enter a number between 1 and 100.")
            except ValueError:
                print("Please enter a valid number.")

def forgot_password(cursor,conn):
    class InvalidPasswordChange(Exception):
        pass
    username_email = input('Enter your username/email: ').strip()
    sql = 'SELECT * FROM "user" WHERE username = %s OR email = %s;'
    cursor.execute(sql, (username_email, username_email))
    user = cursor.fetchone()
    if not user:
        print("No account found")
        return None
    email = user["email"]
    while True:
        code = send_verification_code(email)
        print("A code was sent to your email for verification.")
        verify_code = input("Please input the code: ")
        if verify_code != code:
            print("Incorrect code, please try again")
        else:
            break
    while True:
        try:
            new_password = input("Enter new password: ")
            if len(new_password) < 8 or len(new_password) > 32:
                raise InvalidPasswordChange("Password must be 8-32 characters")
            elif not any(char.isupper() for char in new_password) or not any(
                    char.islower() for char in new_password):
                raise InvalidPasswordChange("Must contain at least must 1 upper case and 1 lowercase letter")
            elif not any(char.isdigit() for char in new_password):
                raise InvalidPasswordChange("Must have at least one digit in your password")
            else:
                password_hash = Password_Security.hash_password(new_password)
                sql = """UPDATE "user" SET password = %s WHERE id = %s;"""
                cursor.execute(sql, (password_hash, user["id"]))
                conn.commit()
                print("Your password has changed.")
                break
        except InvalidPasswordChange as e:
            print(e)

def forgot_username(cursor,conn):
    class InvalidUserSetup(Exception):
        pass
    email = input("Enter email: ").strip()
    sql = """SELECT * FROM "user" WHERE email = %s;"""
    cursor.execute(sql,(email,))
    user = cursor.fetchone()
    if not user:
        print("Email does not exist")
        return None
    while True:
        code = send_verification_code(email)
        print("A code was sent to your email for verification.")
        verify_code = input("Please input the code: ")
        if verify_code != code:
            print("Incorrect code, please try again")
        else:
            break
    while True:
        try:
            username = input("Enter Username: ")
            if len(username) < 8 or len(username) > 32:
                raise InvalidUserSetup("Username must be 8-32 characters")
            sql = """SELECT EXISTS(SELECT 1 FROM "user" WHERE username = %s);
                         """
            cursor.execute(sql, (username,))
            exists = cursor.fetchone()['exists']
            if exists:
                raise InvalidUserSetup("This username is taken")
            break
        except InvalidUserSetup as e:
            print(e)
    sql = """UPDATE "user" SET username = %s WHERE email = %s;"""
    cursor.execute(sql, (username, email))
    conn.commit()
    print("Your username has been updated.")


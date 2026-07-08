from datetime import datetime
import time
import uuid
from psycopg2.extras import RealDictCursor, register_uuid
from Profile import Profile
import threading
import Password_Security
import db
class User:
    def __init__(self, id, dob, username, password, email, new_user = True):
        # Every user has these specific traits to themselves
        self.id = id
        self.DOB = dob
        self.username = username
        self.password = password
        self.email = email
        self.newUser = new_user
        self.profile = Profile(id)
class InvalidUserSetup(Exception):
    pass
#Password Security

email_domains = ["gmail.com","outlook.com","hotmail.com","yahoo.com"]

register_uuid()

def generate_id():
    return uuid.uuid4()


cooldown_active = False
def cooldown(duration):
    global cooldown_active
    cooldown_active = True
    print(f"Try again in 5 minutes.")
    time.sleep(duration)  # pause only this thread
    cooldown_active = False
    print("You can try logging in again now!")

def create_account():
    conn = db.get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    username = ""
    while True:
        print()
        print("(Create an Account)")
        try:
            username = input("Enter a Username: ")
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
    while True:
        try:
            email = input("Enter your email: ").strip()
            if "@" not in email or "." not in email or "com" not in email:
                raise InvalidUserSetup("Invalid email format")
            sql = """SELECT EXISTS(SELECT 1 FROM "user" WHERE email = %s); """
            cursor.execute(sql, (email,))
            exists = cursor.fetchone()['exists']
            if exists:
                raise InvalidUserSetup("This email is taken")
            break
        except InvalidUserSetup as e:
            print(e)
    while True:
        try:
            dob_input = input("Date of birth (ie: MM/DD/YYYY): ").strip()
            parts = dob_input.split("/")

            if len(parts) != 3:
                raise ValueError("Incorrect format. Must be MM/DD/YYYY")

            month_str, day_str, year_str = parts

            if len(month_str) != 2 or len(day_str) != 2 or len(year_str) != 4:
                raise ValueError("Incorrect date. Must be MM/DD/YYYY")

            month, day, year = map(int, parts)

            dob_date = datetime(year, month, day)
            today = datetime.now()
            age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
            if age < 15:
                raise InvalidUserSetup("You can not access this app")
            break
        except InvalidUserSetup as e:
            print(e)
            time.sleep(5)
        except ValueError as e:
            print(e)
    # A blocker would prevent the user from accessing it
    password = ""
    while True:
        try:
            password = input("Enter your password: ").strip()
            if len(password) < 8 or len(password) > 32:
                raise InvalidUserSetup("Password must be 8-32 characters")
            elif not any(char.isupper() for char in password) or not any(char.islower() for char in password):
                raise InvalidUserSetup("Must contain at least must 1 upper case and 1 lowercase letter")
            elif not any(char.isdigit() for char in password):
                raise InvalidUserSetup("Must have at least one digit in your password")
            break
        except InvalidUserSetup as e:
            print(e)
    while True:
        confirm = input("Re enter your password: ")
        if password != confirm:
            print("Passwords don't match")
        else:
            break
    password_hash = Password_Security.hash_password(password)

    id = generate_id()
    sql = """
    INSERT INTO "user" (id, username, email, password, dob)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id;
    """
    cursor.execute(sql,(id, username, email, password_hash,dob_date))
    conn.commit()
    print("Account created.")

def login():
    print()
    conn = db.get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    print("(Login)")
    user = None
    if cooldown_active:
        print("Login temporarily blocked. Try again later.")
        return None
    attempts = 5
    username_email = input('Enter your username/email: ').strip()
    sql = 'SELECT * FROM "user" WHERE username = %s OR email = %s;'
    cursor.execute(sql, (username_email, username_email))
    user = cursor.fetchone()
    if not user:
        print("No account found")
        return None
    while attempts > 0:
        password = input("Enter your password: ")
        if Password_Security.verify_password(user['password'], password):
            return User(
        id=user['id'],
        dob=user['dob'],
        username=user['username'],
        password=user['password'],
        email=user['email'],
        new_user=False
    )
        else:
            print("Incorrect Password. Please try again")
            attempts -= 1
            if attempts == 0:
                print("You've exceeded your attempts")
                t = threading.Thread(target=cooldown, args=(300,))
                t.start()
                return None

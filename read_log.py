import sys
import os

try:
    filename = sys.argv[1]
except IndexError:
    filename = 'server_log_2.txt'

text = ""
if os.path.exists(filename):
    encodings = ['utf-8', 'utf-16le', 'cp1252', 'latin-1']
    for enc in encodings:
        try:
            with open(filename, 'r', encoding=enc) as f:
                text = f.read()
            break
        except Exception:
            continue
else:
    print(f"File {filename} not found.")
    sys.exit(1)

# Replace \r with \n to avoid overwriting lines in output
text = text.replace('\r', '\n')

with open('server_log_utf8.txt', 'w', encoding='utf-8') as out_f:
    out_f.write(text)
print("Log converted to server_log_utf8.txt")

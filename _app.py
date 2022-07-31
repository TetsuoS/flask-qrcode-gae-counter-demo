from flask import Flask
import os.path

def inc_counter():
    is_file = os.path.exists(r"count.txt")
    if not is_file:
        f = open('count.txt', 'w')
        f.write('0')
        f.close()
    with open('count.txt', 'r+') as f:
        data = f.read()
        counter = int(data)
        counter += 1
        new_count = str(counter)
        f.seek(0) 
        f.write(new_count)
        return new_count

app = Flask(__name__)

@app.route("/")
def main():
	counter = inc_counter()
	return counter

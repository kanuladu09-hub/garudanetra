from flask import Flask, render_template, request, redirect, url_for
import json, uuid, os

app = Flask(__name__)

def load():
    try:
        with open("data.json") as f:
            return json.load(f)
    except:
        return []

def save(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/book', methods=["GET", "POST"])
def book():
    if request.method == "POST":
        data = load()

        booking = {
            "id": "GN-" + str(uuid.uuid4())[:6],
            "location": request.form["location"],
            "distance": request.form["distance"],
            "type": request.form["type"],
            "status": "Pending"
        }

        data.append(booking)
        save(data)

        return redirect(url_for('home'))

    return render_template("book.html")

@app.route('/admin')
def admin():
    return render_template("admin.html", bookings=load())

@app.route('/complete/<id>', methods=["POST"])
def complete(id):
    data = load()
    for b in data:
        if b["id"] == id:
            b["status"] = "Completed"
    save(data)
    return redirect(url_for('admin'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
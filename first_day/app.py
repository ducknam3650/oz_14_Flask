from flask import Flask, render_template

app = Flask(__name__)
@app.route("/")
def user_info():
    users = [
        {"username": "traveler", "name": "Alex"},
        {"username": "photographer", "name": "Sam"},
        {"username": "gourmet", "name": "Chris"}
    ]
    return render_template("user.html", user_info = users)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request, redirect, make_response, render_template_string

app = Flask(__name__)

FLAG = "flag{cookie_monster_was_here}"

# Simple login page template
login_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Cumbs Chall Login</title>
</head>
<body>
    <h2>🍪 Cumbs  Login</h2>
    <form method="POST">
        <label>Username: </label><input name="username" required><br><br>
        <label>Password: </label><input type="password" name="password" required><br><br>
        <button type="submit">Login</button>
    </form>
</body>
</html>
"""

# Basic user dashboard template
dashboard_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Cumbs Chall</title>
</head>
<body>
    <h2>Welcome, {{user}}</h2>
    {% if role == "admin" %}
        <h3>Admin Console</h3>
        <p>{{flag}}</p>
    {% else %}
        <p>You are logged in as a  user.</p>
    {% endif %}
    <a href="/logout">Logout</a>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    username = request.cookies.get("username")
    role = request.cookies.get("role")

    # if there's a cookie but no valid user, clear it
    if username and not role:
        resp = make_response(redirect("/"))
        resp.delete_cookie("username")
        resp.delete_cookie("role")
        return resp

    # if user is logged in
    if username:
        # role=admin should ONLY show flag if manually tampered
        flag = FLAG if role == "admin" else None
        return render_template_string(dashboard_page, user=username, role=role, flag=flag)

    # otherwise, login
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # auto-create any username/password
        resp = make_response(redirect("/"))
        resp.set_cookie("username", username)
        resp.set_cookie("role", "user")
        return resp

    return login_page


@app.route("/logout")
def logout():
    resp = make_response(redirect("/"))
    resp.delete_cookie("username")
    resp.delete_cookie("role")
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


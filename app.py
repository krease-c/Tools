
from flask import Flask, request, redirect, make_response, render_template_string

app = Flask(__name__)

FLAG = "flag{Co0kie_monst3r_w4s_her3}"

# --- HTML + CSS Templates ---

login_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cumbs Chall - Login</title>
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #1e293b, #0f172a);
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            padding: 40px;
            width: 350px;
            text-align: center;
            box-shadow: 0 0 20px rgba(255,255,255,0.1);
            animation: fadeIn 1.2s ease-in-out;
        }
        input {
            width: 85%;
            padding: 10px;
            margin: 10px 0;
            border: none;
            border-radius: 8px;
            background: rgba(255,255,255,0.2);
            color: white;
            outline: none;
        }
        button {
            width: 90%;
            background: #38bdf8;
            border: none;
            border-radius: 8px;
            padding: 10px;
            color: #0f172a;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }
        button:hover {
            background: #7dd3fc;
        }
        h2 {
            margin-bottom: 10px;
        }
        p {
            font-size: 0.9em;
            opacity: 0.8;
        }
        @keyframes fadeIn {
            from {opacity: 0; transform: translateY(20px);}
            to {opacity: 1; transform: translateY(0);}
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>🍪 Crumbs </h2>
        <p>Login to continue</p>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>
"""

dashboard_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cumbs Chall</title>
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .card {
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 40px;
            width: 400px;
            text-align: center;
            box-shadow: 0 0 25px rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
            animation: fadeIn 1.2s ease-in-out;
        }
        h2 {
            margin-bottom: 10px;
        }
        p {
            font-size: 1em;
        }
        .flag {
            background: rgba(56, 189, 248, 0.2);
            border: 1px solid #38bdf8;
            border-radius: 10px;
            padding: 10px;
            margin-top: 20px;
            color: #7dd3fc;
            font-weight: bold;
        }
        a {
            color: #38bdf8;
            text-decoration: none;
            font-weight: bold;
        }
        a:hover {
            color: #7dd3fc;
        }
        @keyframes fadeIn {
            from {opacity: 0; transform: translateY(20px);}
            to {opacity: 1; transform: translateY(0);}
        }
    </style>
</head>
<body>
    <div class="card">
        <h2>Welcome, {{user}}</h2>
        {% if role == "admin" %}
            <h3>Admin Console</h3>
            <div class="flag">{{flag}}</div>
        {% else %}
            <p>You are logged in .</p>
        {% endif %}
        <br>
        <a href="/logout">Logout</a>
    </div>
</body>
</html>
"""

# --- Flask routes ---

@app.route("/", methods=["GET", "POST"])
def index():
    username = request.cookies.get("username")
    role = request.cookies.get("role")

    # If a tampered admin cookie exists, clear it
    if role == "admin" and username != "admin":
        resp = make_response(redirect("/"))
        resp.delete_cookie("username")
        resp.delete_cookie("role")
        return resp

    # If already logged in
    if username:
        flag = FLAG if role == "admin" else None
        return render_template_string(dashboard_page, user=username, role=role, flag=flag)

    # Handle login
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        resp = make_response(redirect("/"))
        resp.set_cookie("username", username, httponly=True)  # session-only
        resp.set_cookie("role", "user", httponly=True)        # session-only
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

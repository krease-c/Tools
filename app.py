from flask import Flask, request, render_template, redirect, make_response

app = Flask(__name__)

USERS = {}  # Dynamic users
FLAG = "flag{crumbs_in_the_cookie_jar}"

@app.route('/')
def home():
    role = request.cookies.get('role')
    username = request.cookies.get('username')
    if role == 'admin':
        return render_template('admin.html', flag=FLAG)
    elif username:
        return render_template('index.html', username=username)
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            return render_template('login.html', error='All fields required.')

        # Auto-create user if not exists
        USERS[username] = password
        resp = make_response(redirect('/'))
        resp.set_cookie('username', username)
        resp.set_cookie('role', 'user')
        return resp

    return render_template('login.html')

@app.route('/logout')
def logout():
    resp = make_response(redirect('/login'))
    resp.delete_cookie('role')
    resp.delete_cookie('username')
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


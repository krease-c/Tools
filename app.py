from flask import Flask, request, render_template, redirect, make_response
app = Flask(__name__)

USERS = {}
FLAG = "flag{crumbs_in_the_cookie_jar}"

@app.route('/')
def home():
    role = request.cookies.get('role')
    if role == 'admin':
        return render_template('admin.html', flag=FLAG)
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            if username not in USERS:
                USERS[username] = password
            if USERS[username] == password:
                resp = make_response(redirect('/'))
                resp.set_cookie('role', 'user')
                return resp
            return render_template('login.html', error='Invalid password.')
        return render_template('login.html', error='Missing fields.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    resp = make_response(redirect('/'))
    resp.delete_cookie('role')
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

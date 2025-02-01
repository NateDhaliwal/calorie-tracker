from flask import Flask, redirect, render_template, request, session, make_response, flash
from fatsecret import Fatsecret
from sqlitedict import SqliteDict
from werkzeug.security import generate_password_hash, check_password_hash

fs = Fatsecret("8298b96e554841309a2ee6094cd60be4", "e0d939065cb54d5c871d135a27eb6f7a")
userdata = SqliteDict("userdata.sqlite", autocommit=True)

'''
foods = fs.foods_search("Nasi Lemak")
for food in foods:
    if food['food_name'] == "Nasi Lemak":
        print(food['food_description'])
'''
app = Flask(__name__)
app.config['SECRET_KEY'] = '897988c5237443caa9fa4af12de3df7a'


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        username = session['username']
        if username:
            return redirect('/'), flash('Login successful!')
    except KeyError:
        pass

    if request.method == 'POST':
        username = request.form.get('username')
        passwordRaw = request.form.get('password')
        passwordMatched = check_password_hash(userdata[username]['passwordHashed'], passwordRaw)
        if passwordMatched:
            # Login successful, redirect user to '/'
            session['username'] = username
            return redirect('/')
        else:
            flash('Username or password incorrect')
            return render_template('login.html')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        username = session['username']
        if username:
            return redirect('/'), flash('Login successful!')
    except KeyError:
        pass

    if request.method == 'POST':
        username = request.form.get('username')
        passwordRaw = request.form.get('password')
        age = request.form.get('age')
        weight = request.form.get('weight')
        gender = request.form.get('gender')
        height = request.form.get('height')
        passwordHashed = generate_password_hash(passwordRaw)
        # Create user data
        userdata[username] = {
            'username': username,
            'passwordHashed': passwordHashed,
            'age': age,
            'weight': weight,
            'gender': gender,
            'height': height,
            'calories_total': {}
        }
        # Login successful, redirect user to '/'
        session['username'] = username
        return redirect('/')
    return render_template('login.html')


@app.route('/')
def home():
    return render_template('home.html')


app.run('0.0.0.0', port=8080, debug=True)
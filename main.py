from flask import Flask, redirect, render_template, request, session, make_response, flash, current_app
from fatsecret import Fatsecret
from sqlitedict import SqliteDict
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps

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


# Only applied to some pages, like admin or chat
def login_required(function):
  @wraps(function)

  def wrapper(*args, **kwargs):
    try:
        username = session['username']
        if username:
            pass
    except KeyError:
        session['username'] = ''

    if session['username'] != '':
      return function(*args, **kwargs)
    return redirect(request.referrer)
  return wrapper




@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        username = session['username']
        if username:
            return redirect('/'), flash('success|Login successful!')
    except KeyError:
        session['username'] = ''

    if request.method == 'POST':
        username = request.form.get('username')
        passwordRaw = request.form.get('password')
        print(username)
        try:

            userd = userdata[username]
            
        except KeyError:
            return render_template('login.html'), flash('danger|No such user exists.')
        
        passwordMatched = check_password_hash(userdata[username]['passwordHashed'], passwordRaw)
        if passwordMatched:
            # Login successful, redirect user to '/'
            session['username'] = username
            return redirect('/')
        else:
            
            return render_template('login.html'), flash('danger|Username or password incorrect')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        username = session['username']
        if username:
            return redirect('/'), flash('success|Login successful!')
    except KeyError:
        session['username'] = ''

    if request.method == 'POST':
        username = str(request.form.get('username'))
        passwordRaw = str(request.form.get('password'))
        age = int(request.form.get('age'))
        weight = int(request.form.get('weight'))
        gender = str(request.form.get('gender'))
        height = int(request.form.get('height'))
        passwordHashed = generate_password_hash(passwordRaw)
        max_calories = 0
        # Create user data
        if gender == 'Male':
            max_calories = round(66.47 + (13.75*weight) + (5.003*height) - (6.755*age))
        elif gender == 'Female':
            max_calories = round(655.1 + (9.563*weight) + (1.850*height) - (4.676*age))
        userdata[username] = {
            'username': username,
            'passwordHashed': passwordHashed,
            'age': age,
            'weight': weight,
            'gender': gender,
            'height': height,
            'max_calories': max_calories,
            'total_calories': {}
        }
        # Login successful, redirect user to '/'
        session['username'] = username
        return redirect('/')
    return render_template('register.html')


@app.route('/')
def home():
    # Clear the database
    #userdata.clear()
    #session.clear()

    username = ''
    try:
        username = session['username']
    except KeyError:
        session['username'] = ''
        username = session['username']

    if username == '':
        return render_template('home.html')
    else:
        total_calories = 0
    for date, list_items in userdata[username]['total_calories'].items():
        if str(date) == str(datetime.now().strftime('%d/%m/%Y')):
            for item in list_items:
                for name, data in item.items():
                    total_calories += int(data['calories'].rstrip('kcal'))
        else:
            continue
    return render_template('home.html', userdata=userdata[username], total_calories=total_calories)


@login_required
@app.route('/logout')
def logout():
    username = ''
    try:
        username = session['username']
    except KeyError:
        session['username'] = ''
        username = session['username']

    if username != '':
        usernamePopped = session.pop('username')

    return redirect('/'), flash(f'success|You have been logged out.')


@login_required
@app.route('/add', methods=['GET', 'POST'])
def add_food():
    if request.method == 'POST':
        vegetables = ''
        meats = ''
        whole_meal = ''
        drink = ''
        possible_drink_list = []
        possible_whole_meal_list = []
        possible_meats_list = {}
        possible_vegetables_list = {}
        if str(request.form.get('current_page')) == '1':
            vegetables = str(request.form.get('vegetable')) if str(request.form.get('vegetable')).lower() != 'nil' else None
            meats = str(request.form.get('meat')) if str(request.form.get('meat')).lower() != 'nil' else None
            whole_meal = str(request.form.get('whole_meal')) if str(request.form.get('whole_meal')).lower() != 'nil' else None
            drink = str(request.form.get('drink')) if str(request.form.get('drink')).lower() != 'nil' else None
            if vegetables:
                vegetables = vegetables.split(',')
                for vegetable in vegetables:
                    vegetable.strip().lower()

            if meats:
                meats = meats.split(',')
                for meat in meats:
                    meat.strip().lower()
            
            
            if vegetables:
                for vegetable in vegetables:
                    possible_vegetables_list[vegetable] = []
                    for possible_vegetable in fs.foods_search(vegetable, max_results=20):
                        possible_vegetables_list[vegetable].append(possible_vegetable)

            
            if meats:
                for meat in meats:
                    possible_meats_list[meat] = []
                    for possible_meat in fs.foods_search(meat, max_results=20):
                        possible_meats_list[meat].append(possible_meat)

            
            if whole_meal:
                for possible_meal in fs.foods_search(whole_meal, max_results=20):
                    possible_whole_meal_list.append(possible_meal)

            
            if drink:
                for possible_drink in fs.foods_search(drink, max_results=20):
                    possible_drink_list.append(possible_drink)

            return render_template('add-food.html', page=2, possible_drink_list=possible_drink_list, possible_meats_list=possible_meats_list, possible_vegetables_list=possible_vegetables_list, possible_whole_meal_list=possible_whole_meal_list)

        
    return render_template('add-food.html', page=1)


@login_required
@app.route('/added', methods=['GET', 'POST'])
def added_all_food():
    final_foods = {}
    total_calories = 0
    for name, value in request.form.items():
        final_foods[name] = {'full_name': value.split('|')[0], 'calories': value.split('|')[1]}
        total_calories += int(value.split('|')[1].rstrip('kcal'))

    print(total_calories)
    userd = userdata[session['username']]
    datenow = str(datetime.now().strftime('%d/%m/%Y'))
    if datenow in userd['total_calories'].keys():
        pass
    else:
        userd['total_calories'][datenow] = []
    userd['total_calories'][datenow].append(final_foods)
    userdata[session['username']] = userd
    return redirect('/')


@login_required
@app.route('/activity')
def activity():
    username = session['username']
    
    return render_template('activity.html')
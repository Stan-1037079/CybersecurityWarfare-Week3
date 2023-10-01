from flask import Flask, request, render_template, redirect, url_for, jsonify, abort, session
from flask_cors import CORS, cross_origin
import sqlite3
from datetime import datetime
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_talisman import Talisman

app = Flask(__name__)
csp = {
    'default-src': "'self'",
    'style-src': ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net"],
    'style-src-elem': ["'self'", "https://cdnjs.cloudflare.com", "'unsafe-inline'"],
    'script-src': ["'self'", "https://cdnjs.cloudflare.com", "https://cdn.jsdelivr.net", "'unsafe-inline'"],
}

Talisman(app, content_security_policy=csp, frame_options='DENY')

app.secret_key = 'supersecretkey'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SERVER_NAME'] = None

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

def row_to_event(row):
    event = {}
    event['id'] = row[0]
    event['title'] = row[1]
    event['location'] = row[2]
    event['start'] = row[3]
    event['end'] = row[4]
    event['link'] = row[5]
    return event

def row_to_deleteduser(row):
    userd = {}
    userd['id'] = row[0]
    userd['role'] = row[1]
    userd['first_name'] = row[2]
    userd['last_name'] = row[3]
    return userd

@app.route('/chart-data')
def chart_data():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT rol, COUNT(*) FROM personen GROUP BY rol")
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    data = {
        'labels': [],
        'student_counts': [],
        'teacher_counts': []
    }

    for rol, count in results:
        if rol == 'Student':
            data['student_counts'].append(count)
        elif rol == 'Teacher':
            data['teacher_counts'].append(count)

    data['labels'].append('Students')
    data['labels'].append('Teachers')

    return jsonify(data)


@app.route('/')
def index():
    form = LoginForm()
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT rol FROM personen")
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    if 'username' in session:
        return redirect(url_for('hometeacher'))
    else:
        return render_template('login.html', student_count=result, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        user = form.username.data
        passwd = form.password.data
        conn = sqlite3.connect('Database.db')
        c = conn.cursor()
        c.execute(
            "SELECT * FROM personen WHERE persoon_id=? AND password=?", (user, passwd))
        result_student = c.fetchone()
        if result_student == None:
            error = 'Invalid username or password. Please try again.'
            return render_template('login.html', error=error)
        result_user = result_student[2] + ' ' + result_student[3]
        rol_check = result_student[4]
        conn.close()
        if result_student:
            session["is_admin"] = False
            session['is_teacher'] = False
            session['username'] = result_user
            if rol_check == 'Student':
                return redirect(url_for('homestudent'))
            elif rol_check == 'Teacher':
                session["is_teacher"] = True
                return redirect(url_for('hometeacher'))
            elif rol_check == 'Admin':
                session["is_admin"] = True
                return redirect(url_for('home'))
        return render_template('login.html', form=form, error=error)

@app.route('/home')
def home():
    if 'username' in session and session["is_admin"] == True:
        return render_template('home.html', username=session['username'])
    elif 'username' in session and session["is_teacher"] == True:
        return render_template('hometeacher.html', username=session['username'])
    else:
        return redirect(url_for('homestudent'))

@app.route('/homestudent')
def homestudent():
    if 'username' in session:
        return render_template('homestudent.html', username=session['username'])
    else:
        return redirect(url_for('index'))

@app.route('/hometeacher')
def hometeacher():
    if 'username' in session and session["is_admin"] == True or session["is_teacher"] == True:
        return render_template('hometeacher.html', username=session['username'])
    else:
        return redirect(url_for('homestudent'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/calendarteacher')
def calendarteacher():
    if 'username' in session:
        return render_template('calendarteacher.html', username=session['username'])
    else:
        return redirect(url_for('index'))

@app.route('/calendarteacheradmin')
def calendarteacheradmin():
    if 'username' in session:
        return render_template('calendarteacheradmin.html', username=session['username'])
    else:
        return redirect(url_for('index'))

@app.route('/calendarstudent')
def calendarstudent():
    if 'username' in session:
        return render_template('calendarstudent.html', username=session['username'])
    else:
        return redirect(url_for('index'))

@app.route('/calendarstudentadmin')
def calendarstudentadmin():
    if 'username' in session:
        return render_template('calendarstudentadmin.html', username=session['username'])
    else:
        return redirect(url_for('index'))

@app.route('/api/get_events', methods=['GET'])
def get_events():
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM events')
    rows = c.fetchall()
    events = [row_to_event(row) for row in rows]
    conn.close()
    return jsonify(events)

@app.route('/api/get_deleted_users', methods=['GET'])
def get_deleted_users():
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM deletedusers')
    rows = c.fetchall()
    deleted_users = [row_to_deleteduser(row) for row in rows]
    conn.close()
    return jsonify(deleted_users)

@app.route('/add_event', methods=['POST'])
def add_event():
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    title = request.form['title']
    location = request.form['location']
    start = request.form['start']
    end = request.form['end']
    link = request.form['link']
    c.execute('INSERT INTO events (title, location, start, end, link) VALUES (?, ?, ?, ?, ?)',
              (title, location, start, end, link))
    conn.commit()
    conn.close()
    if session["is_admin"] == True:
        return redirect(url_for('calendarteacheradmin'))
    else:
        return redirect(url_for('calendarteacher'))

@app.route('/update_event', methods=['POST'])
def update_event():
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    title = request.form['title']
    start = request.form['start']
    end = request.form['end']
    id = request.form['id']
    c.execute('UPDATE events SET title = ?, start = ?, end = ? WHERE id = ?',
              (title, start, end, id))
    conn.commit()
    conn.close()
    return ('', 204)

@app.route('/delete_event', methods=['POST'])
def delete_event():
    event_id = request.form['event_id']
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    c.execute("DELETE from events WHERE id=?", (event_id,))
    conn.commit()
    conn.close()
    if session["is_admin"] == True:
        return redirect(url_for('calendarteacheradmin'))
    else:
        return redirect(url_for('calendarteacher'))

@app.route('/event_admin/<int:event_id>')
def event_admin(event_id):
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM events WHERE id = ?', (event_id,))
    event = c.fetchone()
    conn.close()
    if event is None:
        abort(404)
    return render_template('event_admin.html', event=event, event_id=event_id)

@app.route('/event_docent/<int:event_id>')
def event_docent(event_id):
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM events WHERE id = ?', (event_id,))
    event = c.fetchone()
    conn.close()
    if event is None:
        abort(404)
    return render_template('event_docent.html', event=event, event_id=event_id)

@app.route('/event_student/<int:event_id>')
def event_student(event_id):
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM events WHERE id = ?', (event_id,))
    event = c.fetchone()
    conn.close()
    if event is None:
        abort(404)
    username = session.get('username')
    return render_template('event_student.html', event=event, event_id=event_id, username=username)

@app.route('/add_event_page')
def add_event_page():
    start = request.args.get('start')
    end = request.args.get('end')
    title = request.args.get('title')
    location = request.args.get('location')
    link = request.args.get('link')
    return render_template('add_event_page.html', start=start, end=end, title=title, location=location, link=link)

@app.route('/add_event_page_admin')
def add_event_page_admin():
    start = request.args.get('start')
    end = request.args.get('end')
    title = request.args.get('title')
    location = request.args.get('location')
    link = request.args.get('link')
    return render_template('add_event_page_admin.html', start=start, end=end, title=title, location=location, link=link)

@app.route('/search')
def search():
    query = request.args.get('query')
    conn = sqlite3.connect('Database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT personen.persoon_id, personen.rol, personen.voornaam, personen.achternaam, personen.klas_id, klas.klas_naam FROM personen JOIN klas ON personen.klas_id = klas.klas_id WHERE personen.voornaam LIKE ? OR personen.achternaam LIKE ? OR personen.persoon_id LIKE ?", ('%'+query+'%', '%'+query+'%','%'+query+'%',))
    results = cursor.fetchall()
    conn.close()
    return render_template('search_results.html', results=results)

@app.template_filter('join_tables')
def join_tables_filter(klas_id):
    conn = sqlite3.connect('Database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT klas_naam FROM klas WHERE klas_id = ?", (klas_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return ''

@app.route('/api/classlist')
def classlist():
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    c.execute('SELECT persoon_id, voornaam, achternaam, klas_id, rol FROM personen')
    personen = c.fetchall()
    conn.close()
    return jsonify(personen=personen)

# Leave this code here unless I need it later :P
# app.jinja_env.filters['join_tables'] = join_tables_filter

@app.route('/checkinbutton', methods=['POST'])
def checkinbutton():
    username = request.form.get('username')
    event_id = request.form.get('event_id')
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    c.execute("INSERT INTO attendance (persoon_id, checktime) VALUES (?, ?)", (username, datetime.now()))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/checkinlist')
def checkinlist():
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    c.execute('SELECT persoon_id, checktime FROM attendance')
    checkins = c.fetchall()
    conn.close()
    return jsonify(checkins=checkins)

@app.route('/checkinlist')
def checkinlist_page():
    return render_template('checkinlist.html')

@app.route('/add_or_remove_button', methods=['GET', 'POST'])
def add_or_remove_button():
    if request.method == 'POST':
        return render_template('add_or_remove.html')

#this is the code for adding and removing people from the database. Modiefied a few times. Q--
@app.route('/add_or_remove', methods=['GET', 'POST'])
def add_or_remove():
    if request.method == 'POST':
        # Getting the form data that was submitted by the user Q--
        persoon_id = request.form['persoon_id']
        rol = request.form['rol']
        voornaam = request.form['voornaam']
        achternaam = request.form['achternaam']
        klas_id = request.form['klas_id']

        # Insert the form data into the SQLite database Q--
        con = sqlite3.connect('Database.db')
        c = con.cursor()
        c.execute("INSERT INTO personen (persoon_id, rol, voornaam, achternaam, klas_id) VALUES (?, ?, ?, ?, ?)",
                  (persoon_id, rol, voornaam, achternaam, klas_id))
        con.commit()
        con.close()
        return render_template('home.html')

@app.route('/user_profile_retrieve/<int:persoon_id>', methods=['GET'])
def user_profile(persoon_id):
    # Retrieve the data for the specified person ID from the SQLite database
    con = sqlite3.connect('Database.db')
    c = con.cursor()
    c.execute("SELECT * FROM personen WHERE persoon_id = ?", (persoon_id,))
    user_data = c.fetchone()
    c.execute("SELECT * FROM attendance WHERE persoon_id = ?", (persoon_id,))
    attendance_data = c.fetchall()
    con.close()

    # Pass the user data to the template for rendering
    return render_template('user_profile.html', user=user_data, attendance=attendance_data)

@app.route('/deleteconfirmation/<deleteid>')
def deleteconfirmation(deleteid):
    con = sqlite3.connect('Database.db')
    c = con.cursor()
    c.execute("SELECT * FROM personen WHERE persoon_id = ?", (deleteid,))
    person_data = c.fetchone()
    if person_data:
        c.execute("INSERT INTO deletedusers (id, voornaam) SELECT persoon_id, voornaam FROM personen WHERE persoon_id = ?", (deleteid,))
        c.execute("DELETE FROM personen WHERE persoon_id = ?", (deleteid,))
        con.commit()
        con.close()
        success_message = {'deletesuccess': 'User successfully deleted'}
        return jsonify(success_message)
    else:
        error_message = {'deleteerror': 'User not found'}
        con.close()
        return jsonify(error_message)

# app.route('/deleteuser')
# def deletedusers():
#     con = sqlite3.connect('Database.db')
#     c = con.cursor()
#     c.execute("DELETE ", (persoon_id,))
#     user_data = c.fetchone()
#     c.execute())
#     attendance_data = c.fetchall()
#     con.close()

@app.route('/checkinsystem', methods=['POST'])
def check_in():
    event_id = request.form['eventID']
    student_name = request.form['studentName']
    other_details = request.form['otherDetails']

    store_check_in(event_id, student_name, other_details)

    checked_in_students = get_checked_in_students(event_id)

    return jsonify({'message': 'Check-in successful', 'students': checked_in_students})


@app.route('/get_checked_in_students', methods=['POST'])
def get_checked_in_students():
    event_id = request.form.get('event_id')
    checked_in_students = fetch_checked_in_students(event_id)
    return jsonify({'checked_in_students': checked_in_students})


def fetch_checked_in_students(event_id):
    query = "SELECT student_name FROM check_ins WHERE event_id = ?"
    con = sqlite3.connect('Database.db')
    c = con.cursor()
    c.execute(query, (event_id,))
    students = c.fetchall()
    con.close()  # Close the database connection after fetching the data
    return [student[0] for student in students]


def store_check_in(event_id, student_name, other_details):
    query = "INSERT INTO check_ins (event_id, student_name, other_details) VALUES (?, ?, ?)"
    con = sqlite3.connect('Database.db')
    c = con.cursor()
    c.execute(query, (event_id, student_name, other_details))
    con.commit()

conn = sqlite3.connect('Database.db')
cursor = conn.cursor()

#E-mailconfiguratie
email_host = 'smtp.example.com'
email_port = 587
email_username = 'your_email@example.com'
email_password = 'your_email_password'

def send_email_notification(student_name):
    subject = 'Nieuwe studentregistratie'
    message = f'Er is een nieuwe student geregistreerd: {student_name}'

    msg = MIMEMultipart()
    msg['From'] = email_username
    msg['To'] = 'teacher@example.com'
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP(email_host, email_port)
    server.starttls()
    server.login(email_username, email_password)
    server.send_message(msg)
    server.quit()

@app.route('/sign_up', methods=['POST','GET'])
def signup():
    return render_template('sign_up_student.html')

@app.route('/register', methods=['POST', 'GET'])
def register_student():
    # Studentgegevens ophalen uit de POST-verzoek
    student_id = request.form['id']
    student_password = request.form['password']
    student_firstname = request.form['firstname']
    student_lastname = request.form['lastname']
    student_role = request.form['role']
    student_class = request.form['class']

    #Student toevoegen aan de SQLite3-database
    
    cursor.execute("INSERT INTO personen (persoon_id, password, voornaam, achternaam, rol, klas_id) VALUES (?, ?, ?, ?, ?, ?)", (student_id, student_password, student_firstname, student_lastname, student_role, student_class))
    conn.commit()

    # E-mailnotificatie verzenden naar de leraren
    send_email_notification(student_id)

    return "Signup succesvol"

if __name__ == '__main__':
    app.run(debug=True)

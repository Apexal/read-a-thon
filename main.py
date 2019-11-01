import os
import datetime
from flask import Flask, escape, request, url_for, redirect, render_template, escape, session

from csv import DictReader

app = Flask(__name__)

app.secret_key = os.environ['SECRET_KEY']

readathon = {
    'school_id': 1,
    'start': datetime.datetime(2019, 10, 30),
    'end': datetime.datetime(2019, 11, 7)
}

school = {
    'id': 1,
    'name': 'Test School'
}

student = {
    'id': 1,
    'first_name': 'Frank',
    'last_name': 'Matranga'
}


@app.route('/')
def homepage():
    if True:  # if logged in
        current_stats = {
            'hours': 5,
            'minutes': 25
        }
        average_daily_minutes = 20

        return render_template('pages/student_homepage.html', student=student, school=school, current_stats=current_stats, average_daily_minutes=average_daily_minutes)
    else:
        return render_template('pages/homepage.html')

@app.route('/today', methods=['POST'])
def today():
    # Create or update record for student today
    record = {
        'student_id': 1, # TODO: real id
        'date': datetime.datetime.today(),
        'minutes': int(request.form['minutes-today'])
    }
    return record

# ---------- AUTHENTICATION ----------
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('pages/login.html')
#     else:
#         # Login form submitted
#         session['student_id'] = request.form['student_id']

#         # Find student
#         student = None
#         for s in students:
#             if s['id'] == request.form['student_id']:
#                 student = s
#                 break

#         session['student'] = student

#         return redirect(url_for('homepage'))

# @app.route('/logout')
# def logout():
#     # remove the username from the session if it's there
#     session.pop('student_id', None)
#     session.pop('student', None)
#     return redirect(url_for('homepage'))
# ------------------------------------

# ------------ ERROR HANDLING --------
# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('pages/not_found.html'), 404
# ------------------------------------

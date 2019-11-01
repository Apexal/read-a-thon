import os

from flask import Flask, escape, request, url_for, redirect, render_template, escape, session

from csv import DictReader

app = Flask(__name__)

app.secret_key = os.environ['SECRET_KEY']

@app.route('/')
def homepage():
    if True: # if logged in
        return render_template('pages/student_homepage.html', student={ 'first_name': 'Frank', 'last_name': 'Matranga' }, school={ 'name': 'Test School' })
    else:
        return render_template('pages/homepage.html')

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
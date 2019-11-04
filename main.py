import os
import datetime
from flask import Flask, escape, request, abort, url_for, redirect, render_template, escape, session
from flask_sqlalchemy import SQLAlchemy

from csv import DictReader

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/test.db'
db = SQLAlchemy(app)


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    classes = db.relationship('SchoolClass', backref='school', lazy=True)
    students = db.relationship('Student', backref='school', lazy=True)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(80), unique=True, nullable=False)
    last_name = db.Column(db.String(120), unique=True, nullable=False)

    school_id = db.Column(db.Integer, db.ForeignKey('school.id'),
                          nullable=False)

    school_class_id = db.Column(db.Integer, db.ForeignKey('school_class.id'),
                                nullable=False)

    reading_records = db.relationship(
        'ReadingRecord', backref='student', lazy=True)

    def __repr__(self):
        return f'<Student "{self.first_name} {self.last_name}">'


class SchoolClass(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'),
                          nullable=False)

    name = db.Column(db.String(200), nullable=False)

    students = db.relationship('Student', backref='school_class', lazy=True)


class ReadingRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey(
        'student.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    minutes = db.Column(db.Integer, nullable=False)

    def as_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'minutes': self.minutes
        }

    def __repr__(self):
        return f'<ReadingRecord id={self.id} date={self.date}>'

app.secret_key = os.environ['SECRET_KEY']

readathon = {
    'school_id': 1,
    'start': datetime.datetime(2019, 10, 30),
    'end': datetime.datetime(2019, 11, 7)
}


@app.route('/')
def homepage():
    if 'student_id' in session:  # if logged in
        print('logged in')
        student = Student.query.get(session['student_id'])
        school = student.school
        current_stats = {
            'hours': 5,
            'minutes': 25
        }
        average_daily_minutes = 20
        today_str = datetime.date.today().strftime('%A, %B %-d')
        today_reading_record = ReadingRecord.query.filter_by(
            student_id=session['student_id'], date=datetime.date.today()).first()

        return render_template('pages/student_homepage.html', student=student, school=school, current_stats=current_stats, average_daily_minutes=average_daily_minutes, today_reading_record=today_reading_record, today_str=today_str)
    else:
        print('not logged in')
        return render_template('pages/homepage.html')

@app.route('/daily-minutes', methods=['GET'])
def daily_minutes():
    reading_minutes = ReadingRecord.query.filter(ReadingRecord.date > readathon['start'], ReadingRecord.student_id == session['student_id'])
    all_minutes = []
    for record in reading_minutes:
        all_minutes.append(record.as_dict())
    return { 'reading_minutes': all_minutes }

@app.route('/today', methods=['POST'])
def today():
    # Create or update record for student today
    today = datetime.date.today()
    reading_record = ReadingRecord.query.filter_by(
        student_id=session['student_id'], date=today).first()
    
    if reading_record == None:
        reading_record = ReadingRecord(student_id=session['student_id'],
                                        date=today,
                                       minutes=int(
                                           request.form['minutes-today'])
                                       )
    else:
        reading_record.minutes = int(request.form['minutes-today'])
    
    db.session.add(reading_record)
    db.session.commit()

    return redirect(url_for('homepage'))

# ---------- AUTHENTICATION ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('pages/login.html')
    else:
        # Login form submitted
        student_id = int(request.form['student_id'])

        # Find student
        student = Student.query.get(student_id)
        if student == None:
            abort(404)

        session['student_id'] = student_id

        # print(session)
        return redirect(url_for('homepage'))


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('student_id', None)
    return redirect(url_for('homepage'))
# ------------------------------------

# ------------ ERROR HANDLING --------
# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('pages/not_found.html'), 404
# ------------------------------------

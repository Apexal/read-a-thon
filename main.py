from flask import Flask, escape, request, render_template

from csv import DictReader

app = Flask(__name__)

schools = []
with open('data/schools.csv') as f:
    for row in DictReader(f):
        schools.append(row)

classes = []
with open('data/classes.csv') as f:
    for row in DictReader(f):
        classes.append(row)

@app.route('/')
def homepage():
    name = request.args.get("name", "World")
    print(schools)
    return render_template('pages/homepage.html')

@app.route('/school/<int:school_id>')
def school_overview(school_id):
    # Find school
    school = None
    for s in schools:
        if int(s['id']) == school_id:
            school = s
            break
    
    return render_template('pages/school_overview.html', school=school)
"""
Author:Lingwen Kong
Date:12/05/2020
Documentation: SSW810  HW12
"""
from flask import Flask, render_template
import sqlite3
from typing import Dict

DB_FILE: str = 'db/HW11.db'

app = Flask(__name__, template_folder="templates")


@app.route('/')
def summary() -> str:
    query = "select s.name, s.cwid, g.Course, g.Grade,i.name from students s join grades as g on s.cwid = g.StudentCWID join instructors i on i.cwid = g.InstructorCWID order by s.name ASC"

    db: sqlite3.Connection = sqlite3.connect(DB_FILE)

    data: Dict[str, str] = [{
        'name': name, 'cwid': cwid, 'course': course, 'grade': grade, 'instructor': instructor}
        for cwid, name, course, grade, instructor in db.execute(query)
    ]

    db.close()
    return render_template('student_template.html', title="Stevens Repository",
                           table_title="Student, Course, Grade and "
                                       "Instructor",
                           data=data, developer="Lingwen kong")


@app.route('/base')
def base_template():
    return render_template("base.html", base_title="Base Template", body="This is base template")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", error="wrong path"), 404


if __name__ == '__main__':
    app.run(debug=True)

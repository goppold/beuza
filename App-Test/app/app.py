from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
import os
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, StringField
from wtforms.validators import DataRequired

from flask_datepicker import datepicker
from sqlalchemy import create_engine

from .db_communication import getEvents, getEventMembers, getEventNames, getMemberID, setVote, getCurrentCycleID, getUserID
from .forms import VoteForm

"""Tests for DB"""
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = \
#    'sqlite:///' + os.path.join(basedir, 'data.sqlite')

# app.config['SQLALCHEMY_DATABASE_URI'] = \
#    'sql:///' + os.path.join(basedir, 'hp_app_db_1.sql')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'TEST'
bootstrap = Bootstrap(app)

engine = create_engine('postgresql://sebi:beuza@v220200284142109433.supersrv.de:5432/hpapp')


def setDeviceID():
    # Only for Test
    global global_device_id
    global_device_id = str(2)

def __setVote__():
    vote = request.form['vote']
    event_id = request.form['event_id']
    cycle_id = getCurrentCycleID(engine, event_id)
    user_id = getUserID(engine, global_device_id, event_id)
    setVote(user_id, voter_user_id=vote, cycle_id=cycle_id, engine=engine)
    print('finish')

@app.cli.command()
def test():
    """Run the unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.route('/', methods=['GET', 'POST'])
def index():
    setDeviceID()
    res = getEvents(engine=engine, device_id=global_device_id)
    event_names = getEventNames(res, engine=engine)

    try:
        __setVote__()
    except:
        print('pass')
        pass

    # TODO amount of events muss irgendwie noch umgangen werden. Kann nicht die Lösung sein
    return render_template('index.html', amount_of_events=len(event_names), event_names=event_names, event_IDs=res)


@app.route('/decision')
def decision():
    return render_template('decision.html')


@app.route('/decision-unclear')
def decisionUnclear():
    return render_template('decision-unclear.html')


@app.route('/event/<event_id>', methods=['GET', 'POST'])
def event(event_id):
    event_names = getEventNames(event_id, engine=engine)
    user_id = getMemberID(event_id, engine=engine)
    event_user = getEventMembers(event_id, engine=engine)
    return render_template('event.html', event_name=event_names, event_id=event_id, event_users=event_user,
                           user_id=user_id, amount_of_user=len(event_user))


@app.route('/create-HP')
def createHP():
    return render_template('create-HP.html')


@app.route('/result')
def result():
    return render_template('result.html')


@app.route('/give-slugs')
def giveSlugs():
    return render_template('give-slugs.html')


@app.route('/invitation')
def invitation():
    return render_template('invitation.html')


@app.route('/invitation-accepted')
def invitationAccepted():
    return render_template('invitation-accepted.html')


if __name__ == '__main__':
    bootstrap = Bootstrap(app)
    bootstrap.run()
    datepicker(app)
    # app.run()

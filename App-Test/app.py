from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TEST'
bootstrap = Bootstrap(app)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/decision')
def decision():
    return render_template('decision.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('settings'))
    return render_template('settings.html', form=form, name=session.get('name'))

@app.route('/event')
def event():

    return render_template('event.html')

if __name__ == '__main__':
    bootstrap = Bootstrap(app)
    bootstrap.run()
    #app.run()

from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap

from flask_datepicker import datepicker

from .db_communication import getEvents, getEventUsersName, getEventNames, getEventUserID, setVote, getCurrentCycleID, \
    getUserID, getCurrentCycleState, hasVoted, countVotes, checkCycle, getVote, getCurrentCycleTimestamp, setSlugs

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'TEST'
bootstrap = Bootstrap(app)


def setDeviceID():
    # Only for Test
    # Hier soll mal die Device_Id oder Email abgefragt werden
    global global_device_id
    global_device_id = str(2)


def __setVote__():
    """
    Setzt Vote und checkt zugleich ob Cycle geändert werden muss
    """
    vote = request.form['vote']
    event_id = request.form['event_id']
    cycle_id = getCurrentCycleID(event_id)
    user_id = getUserID(global_device_id, event_id)
    setVote(user_id=user_id, voted_user_id=vote, cycle_id=cycle_id)

    # Refresh Cycle if needed
    checkCycle(cycle_id=cycle_id, event_id=event_id)

def __setSlugs__():
    """
    Setzt Vote und checkt zugleich ob Cycle geändert werden muss
    """
    clicks = request.form['voting']
    event_id = request.form['event_id']
    cycle_id = getCurrentCycleID(event_id)
    user_id = getUserID(global_device_id, event_id)
    event_user_ids = getEventUserID(event_id)
    i = 0
    for slug in clicks:
        if slug > 0:
            setSlugs(user_id=user_id, voted_user_id=event_user_ids(i), cycle_id=cycle_id, amount_of_slugs=slug)
        i = i + 1
    # TODO: Hier muss notification für Trinker eingebaut werden


def getNumberOfSlugsToSpread(user_id, event_id):
    # TODO muss noch mit Quote verrechnet werden
    return 4


def getNumberOfSlugsToDrink(user_id, event_id):
    # TODO
    return 3


def getOwnVote(votes, cycle_id, ownUser_id, user_id):
    """
    Returns 1 falls vote richtig
    sonst 0
    """
    print(votes)
    winning_id = getVote(cycle_id, ownUser_id)
    res = 0
    print(user_id[votes.index(max(votes))])
    print(winning_id)

    if user_id[votes.index(max(votes))] == winning_id:
        res = 1

    return res


def checkVote(user_id, cycle_id):
    """
    Checkt für alle User (user_id) in einem Cycle (cycle_id) ob diese bereits gevotet haben
    """
    res = []
    for i in user_id:
        res.append(hasVoted(user_id=i, cycle_id=cycle_id))
    return res


@app.cli.command()
def test():
    """Run the unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.route('/', methods=['GET', 'POST'])
def index():
    setDeviceID()
    res = getEvents(device_id=global_device_id)
    event_names = getEventNames(res)

    try:
        __setSlugs__()
    except:
        print('pass-1')
        pass

    try:
        # TODO evtl is hier onsubmit() besser
        __setVote__()
    except:
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
    cycle_id = getCurrentCycleID(event_id)
    state = getCurrentCycleState(cycle_id)
    if state == 'closed':
        checkCycle(cycle_id=cycle_id, event_id=event_id)
        cycle_id = getCurrentCycleID(event_id)
        state = getCurrentCycleState(cycle_id)

    event_names = getEventNames(event_id)
    event_user = getEventUsersName(event_id)
    user_id = getEventUserID(event_id)

    if state == 'betting':
        if hasVoted(user_id=getUserID(device_id=global_device_id, event_id=event_id), cycle_id=cycle_id, ):
            isclosed = 0
            checkVoteList = checkVote(cycle_id=cycle_id, user_id=user_id)
            print(checkVoteList)
            return render_template('decision-unclear.html', event_name=event_names, amount_of_user=len(event_user),
                                   event_users=event_user, checkVoteList=checkVoteList, isclosed=isclosed)
        else:
            print('Hab noch nicht abgestimmt')
            return render_template('event.html', event_name=event_names, event_id=event_id, event_users=event_user,
                                   user_id=user_id, amount_of_user=len(event_user))

    elif state == 'voting':  # Todo hier nur für tests closed eingegeben -> voting
        print('voting')
        if hasVoted(user_id=getUserID(device_id=global_device_id, event_id=event_id), cycle_id=cycle_id):
            votes = countVotes(cycle_id=cycle_id, user_id=user_id)
            if sum(votes) == len(event_user):
                # ownVote ist 1 falls richtig sonst 0
                ownVote = getOwnVote(votes, cycle_id, getUserID(device_id=global_device_id, event_id=event_id), user_id)
                link = str("/give-slugs/" + event_id)
                return render_template('decision.html', amount_of_user=len(event_user), event_name=event_names,
                                       event_users=event_user, votes=votes, ownVote=ownVote, link=link)
            else:
                checkVoteList = checkVote(cycle_id=cycle_id, user_id=user_id)
                return render_template('decision-unclear.html', event_name=event_names, amount_of_user=len(event_user),
                                       event_users=event_user, checkVoteList=checkVoteList, isclosed=0)

        else:
            print('Hab noch nicht abgestimmt')
            return render_template('event.html', event_name=event_names, event_id=event_id, event_users=event_user,
                                   user_id=user_id, amount_of_user=len(event_user))


    elif state == 'closed':
        isclosed = 1
        checkVoteList = checkVote(cycle_id=cycle_id, user_id=user_id)
        return render_template('decision-unclear.html', event_name=event_names, amount_of_user=len(event_user),
                               event_users=event_user, checkVoteList=checkVoteList, isclosed=isclosed)
    else:
        print('we got a problem')


@app.route('/create-HP')
def createHP():
    return render_template('create-HP.html')


@app.route('/result')
def result():
    return render_template('result.html')


@app.route('/give-slugs/<event_id>', methods=['GET', 'POST'])
def giveSlugs(event_id):
    event_names = getEventNames(event_id)
    numberOfSlugsToSpread = getNumberOfSlugsToSpread(event_id=event_id,
                                                     user_id=getUserID(device_id=global_device_id, event_id=event_id))
    event_users = getEventUsersName(event_id)
    return render_template('give-slugs.html', event_name=event_names, numberOfSlugsToSpread=numberOfSlugsToSpread,
                           event_users=event_users, amount_of_user=len(event_users))


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

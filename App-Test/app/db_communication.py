"""
Methods for DB communication
"""

import time
from sqlalchemy import create_engine

engine = create_engine('postgresql://sebi:beuza@v220200284142109433.supersrv.de:5432/hpapp')

"""
METHODS FOR VOTES
"""

def countVotes(cycle_id, user_id):
    """
    Zähl alle votes in einem Cycle pro user_id

    Gibt Liste mit der Anzahl zurück. Sortiert nach der user_id
    """
    counts = []
    for i in range(len(user_id)):
        with engine.connect() as connection:
            result = connection.execute(
                "select user_id from votes where cycle_id=" + str(cycle_id) + "AND voted_user_id = " + str(user_id[i]))
            res = 0
            for r in result:
                res = res + 1
        counts.append(res)
        connection.close()
    return counts

def hasVoted(cycle_id, user_id):
    """
    Gibt für eine user_id zu einem Zeitpunkt (cycle_id) an ob user schon gevotet hat
    """
    with engine.connect() as connection:
        result = connection.execute(
            "select voted_user_id from votes where user_id=" + str(user_id) + "and cycle_id=" + str(cycle_id))
        res = 0
        for r in result:
            res = 1
    connection.close()
    return res

def setVote(user_id, voted_user_id, cycle_id):
    """
    Vote abgeben. Beschreibt hierfür die votes Tabelle
    """
    with engine.connect() as connection:
        connection.execute(
            "insert into votes (user_id, cycle_id, voted_user_id) values (" + str(user_id) + "," + str(
                cycle_id) + "," + str(voted_user_id) + ")")
    connection.close()


"""
METHODS FOR USERS
"""

def getUserID(device_id, event_id):
    """
    Gibt die eigene user_id bzgl. device_id und event_id zurück
    """
    with engine.connect() as connection:
        result = connection.execute(
            "select user_id from users where device_id=" + str(device_id) + "AND event_id = " + str(event_id))
        for r in result:
            res = r[0]
    connection.close()
    return res

def getEventUsersName(eventID):
    """
    Gibt die Usernamen zu einem Event (eventID) aus
    """
    with engine.connect() as connection:
        res = []
        result = connection.execute("select name from users where event_id=" + str(eventID))

        for r in result:
            res.append(r['name'])
    connection.close()

    return res

def getEventUserID(event_ids):
    """
    Gibt UserIDs aus für ein oder mehrere Events
    """

    with engine.connect() as connection:
        res = []
        for e in event_ids:
            result = connection.execute("select user_id from users where event_id=" + str(e))

            for r in result:
                res.append(r['user_id'])

    connection.close()
    return res

"""
METHODS FOR EVENTS
"""

def getEvents(device_id):
    """
    Gibt alle event_id für eine device_id an
    """
    res = []
    with engine.connect() as connection:
        result = connection.execute("select event_id from users where device_id=" + str(device_id))
        for r in result:
            res.append(r['event_id'])
    connection.close()
    return res

def getEventNames(event_ids):
    """
    Gibt Namen der Events anhand einer/mehrere event_ids aus
    """
    with engine.connect() as connection:
        res = []
        for e in event_ids:
            result = connection.execute("select name from events where event_id=" + str(e))

            for r in result:
                res.append(r['name'])

    connection.close()
    return res

"""
METHODS FOR CYCLES
"""

def getCurrentCycleID(event_id):
    """
    Gibt die aktuelle cycle_id eines events (event_id) zurück
    """
    with engine.connect() as connection:
        result = connection.execute("select max(cycle_id) from cycles where event_id=" + str(event_id))
        for r in result:
            res = r[0]
    connection.close()
    return res

def getCurrentCycleState(cycle_id):
    """
    Gibt den aktuell Status eines Cycles (cycle_id) zurück.
    """
    with engine.connect() as connection:
        result = connection.execute("select state from cycles where cycle_id=" + str(cycle_id))
        for r in result:
            res = r[0]
    connection.close()
    return res

def checkCycle(cycle_id, event_id):
    """
    Checkt den aktuellen Cycle. Falls nötig wird auf den nächste Cycle umgestellt.

    Aktuell wird nur von betting auf closed umgestellt.
    """
    user_IDs = getEventUserID(event_id, engine)
    votes = countVotes(engine, cycle_id, user_IDs)
    currentCycleState = getCurrentCycleState(engine, cycle_id)
    if currentCycleState == "betting" and votes == len(user_IDs):
        with engine.connect() as connection:
            connection.execute("insert into cycles (cycle_id, state, end_date_time, event_id) values (" + str(
                cycle_id + 1) + "," + "closed" + "," + str(time.time()) + "," + str(event_id) + ")")
        connection.close()

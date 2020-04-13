"""
Methods for DB communication
"""

def getUserID(engine,device_id, event_id):
    with engine.connect() as connection:
        result = connection.execute("select user_id from users where device_id=" + str(device_id) + "AND event_id = " + str(event_id))
        for r in result:
            res = r[0]
    connection.close()
    return res

def getEvents(engine, device_id):
    res = []
    with engine.connect() as connection:
        result = connection.execute("select event_id from users where device_id=" + str(device_id))
        for r in result:
            res.append(r['event_id'])
        """
        For Testing
        for row in result:
            print("events:", row['event_id'])
            """
    connection.close()
    return res

def getCurrentCycleID(engine, event_id):
    with engine.connect() as connection:
        result = connection.execute("select max(cycle_id) from cycles where event_id=" + str(event_id))
        for r in result:
            res = r[0]
    connection.close()
    return res

def setVote(user_id, voter_user_id, cycle_id, engine):
    with engine.connect() as connection:
        result = connection.execute("insert into votes (user_id, cycle_id, voted_user_id) values (" + str(user_id) + "," +str(cycle_id) +"," + str(voter_user_id) + ")")
        # TODO bekommt man hier eine bestätigung?
    connection.close()

def getEventMembers(eventID, engine):
    with engine.connect() as connection:
        res = []
        # TODO Warum is e hier so komisch definiert?
        result = connection.execute("select name from users where event_id=" + str(eventID))

        for r in result:
            res.append(r['name'])

        """
        For Testing
        for row in result:
            print("events:", row['event_id'])
            """
    connection.close()
    return res


def getMemberID(events, engine):
    with engine.connect() as connection:
        res = []
        for e in events:
            # TODO Warum is e hier so komisch definiert?
            result = connection.execute("select user_id from users where event_id=" + str(e))

            for r in result:
                res.append(r['user_id'])

        """
        For Testing
        for row in result:
            print("events:", row['event_id'])
            """
    connection.close()
    return res


def getEventNames(events, engine):
    with engine.connect() as connection:
        res = []
        for e in events:
            # TODO Warum is e hier so komisch definiert?
            result = connection.execute("select name from events where event_id=" + str(e))

            for r in result:
                res.append(r['name'])

        """
        For Testing
        for row in result:
            print("events:", row['event_id'])
            """
    connection.close()
    return res

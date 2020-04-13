"""
Methods for DB communication
"""

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

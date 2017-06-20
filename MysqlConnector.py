import MySQLdb


class MysqlConnector:
    def __init__(self, host, port, user, password):
        self.dataBase = MySQLdb.connect(host=host, port=port, user=user, passwd=password)
        self.cursor = self.dataBase.cursor()
        self.cursor.execute("SHOW DATABASES;")
        self.dataBase.commit()
        dbs = self.cursor.fetchall()
        dbs = list(dbs)
        vote_dbs = []
        for db in dbs:
            db = str(db)
            db = db[2:len(db)-3]
            if "vote_database" in db:
                vote_dbs = vote_dbs + [db]
        self.cursor.execute("USE " + vote_dbs[len(vote_dbs)-1]+";")

    def check_credentials(self, raw_data):
        credentials = parse_data(raw_data)
        username = credentials[0]
        password = credentials[1]
        self.cursor.execute("SELECT username,password FROM voters WHERE username=\""+username+"\";")
        self.dataBase.commit()
        credentials = self.cursor.fetchone()
        if credentials is None:
            return False
        if username == credentials[0] and password == credentials[1]:
            return True
        else:
            return False

    def check_voting_status(self):
        self.cursor.execute("SELECT * FROM status;")
        self.dataBase.commit()
        result = self.cursor.fetchone()
        return result[0]

    def check_voter_status(self, username):
        self.cursor.execute("SELECT casted FROM voters WHERE username=\""+username+"\";")
        self.dataBase.commit()
        result = self.cursor.fetchone()
        return result[0]

    def get_candidates(self):
        result = "candidates~"
        self.cursor.execute("SELECT username FROM candidates;")
        self.dataBase.commit()
        names = self.cursor.fetchall()
        for name in names:
            result = result + name[0] + "~"
        return result

    def save_vote(self, username, candidate):
        self.cursor.execute("UPDATE voters SET casted=1, vote=\"" + candidate + "\" WHERE "
                                                                                "username=\"" + username + "\";")
        self.dataBase.commit()

    def voting_results(self):
        candidates = self.get_candidates()
        candidates = candidates.split("~")
        result = ""
        for i in range(1, len(candidates)-1, 1):
            name = candidates[i]
            if name != "candidates" or name != "":
                self.cursor.execute("SELECT COUNT(vote) FROM voters WHERE vote =\"" + name + "\";")
                self.dataBase.commit()
                votes = self.cursor.fetchone()[0]
                result = result + name + " : " + str(votes) + "\n"
        return result


def parse_data(raw_string):
    return raw_string.split("~")
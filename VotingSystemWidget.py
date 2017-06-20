from kivy.uix.accordion import Accordion
from kivy.uix.accordion import AccordionItem
from VoterRegistrationWidget import VoterRegistrationWidget
from LoginWidget import LoginWidget
from ElectionControlWidget import ElectionControlWidget
from CandidateRegistrationWidget import CandidateRegistrationWidget
from kivy.core.window import Window
import thread
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import time
import datetime
import MySQLdb
from kivy.app import App
from kivy.properties import ListProperty
from ConnectionServer import ConnectionServer

Status = False


class VotingSystemWidget(Accordion):
    userNames = ListProperty()
    candidateNames = ListProperty()

    def __init__(self, **kwargs):
        super(VotingSystemWidget, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.selectedDataBase = ""
        self.electionControlLayout = AccordionItem(title="Election control")
        self.electionControlWidget = ElectionControlWidget()
        self.electionControlWidget.resetButton.bind(on_press=self.reset_voting)
        self.electionControlWidget.electionSwitch.bind(on_press=self.start_stop_election)
        self.electionControlWidget.countResultButton.bind(on_press=self.count_results)
        self.electionControlLayout.add_widget(self.electionControlWidget)
        self.candidateRegistrationLayout = AccordionItem(title="Candidate Registration")
        self.candidateRegistrationWidget = CandidateRegistrationWidget()
        self.candidateRegistrationLayout.add_widget(self.candidateRegistrationWidget)
        self.voterRegistrationLayout = AccordionItem(title="Voter Registration")
        self.voterRegistrationWidget = VoterRegistrationWidget()
        self.voterRegistrationLayout.add_widget(self.voterRegistrationWidget)
        self.add_widget(self.electionControlLayout)
        self.add_widget(self.candidateRegistrationLayout)
        self.add_widget(self.voterRegistrationLayout)
        Window.size = (1024, 600)
        self.dataBase = None
        self.cursor = None

        thread.start_new_thread(self.connect_to_database, ())

        self.voterRegistrationWidget.addVoterBtn.bind(on_press=self.add_voter)
        self.voterRegistrationWidget.votersListAdapter.bind(on_selection_change=self.update_voter_widget)
        self.voterRegistrationWidget.editVoterBtn.bind(on_press=self.edit_voter)
        self.voterRegistrationWidget.deleteVoterBtn.bind(on_press=self.delete_voter)

        self.candidateRegistrationWidget.addCandidateBtn.bind(on_press=self.add_candidate)
        self.candidateRegistrationWidget.editCandidateBtn.bind(on_press=self.edit_candidate)
        self.candidateRegistrationWidget.deleteCandidateBtn.bind(on_press=self.delete_candidate)
        self.candidateRegistrationWidget.candidateListAdapter.bind(on_selection_change=self.update_candidate_widget)

        self.popupBtn = Button()
        self.popup = Popup(title="Attention..!!!", content=self.popupBtn)
        self.popupBtn.bind(on_press=self.dismiss_popup)

    def on_userNames(self, instance, value):
        self.voterRegistrationWidget.votersListAdapter.data = list(self.userNames)
        self.update_voter_widget(self.voterRegistrationWidget.votersListAdapter)

    def on_candidateNames(self, instance, value):
        self.candidateRegistrationWidget.candidateListAdapter.data = list(self.candidateNames)
        self.update_candidate_widget(self.candidateRegistrationWidget.candidateListAdapter)

    def update_candidate_widget(self, adapter):
        candidate = ""
        for i in range(adapter.get_count()):
            if self.candidateRegistrationWidget.candidateListAdapter.get_view(i).is_selected:
                candidate = self.candidateRegistrationWidget.candidateListAdapter.get_view(i).text
                break
        if candidate != "":
            query = "SELECT id,name FROM candidates WHERE username=\""+candidate+"\";"
            self.cursor.execute(query)
            self.dataBase.commit()
            temp = self.cursor.fetchone()
            self.candidateRegistrationWidget.userNameTextInput.text = candidate
            self.candidateRegistrationWidget.idTextInput.text = temp[0]
            self.candidateRegistrationWidget.nameTextInput.text = temp[1]

    def add_candidate(self, btn):
        flag = False
        user = self.candidateRegistrationWidget.userNameTextInput.text.strip()
        _id = self.candidateRegistrationWidget.idTextInput.text.strip()
        name = self.candidateRegistrationWidget.nameTextInput.text.strip()
        if user != "":
            if _id != "":
                if name != "":
                    if len(self.candidateNames) == 0:
                        flag = True
                    for nam in self.candidateNames:
                        if user == nam:
                            flag = False
                            break
                        else:
                            flag = True
        if flag:
            query = "INSERT INTO candidates(name,id,username) VALUES (\"" + name + "\",\"" + \
                    _id + "\",\"" + user + "\");"
            self.cursor.execute(query)
            self.dataBase.commit()
            self.popupBtn.text = user + " added to Database"
            self.popup.open()
            self.load_candidates()
            self.update_candidate_widget(self.candidateRegistrationWidget.candidateListAdapter)
        else:
            self.popupBtn.text = "please fill the credentials correctly"
            self.popup.open()

    def edit_candidate(self, btn):
        flag = False
        user = self.candidateRegistrationWidget.userNameTextInput.text.strip()
        _id = self.candidateRegistrationWidget.idTextInput.text.strip()
        name = self.candidateRegistrationWidget.nameTextInput.text.strip()
        if user != "":
            if _id != "":
                if name != "":
                    if len(self.candidateNames) == 0:
                        flag = False
                    else:
                        flag = True
        candidate = ""
        for i in range(self.candidateRegistrationWidget.candidateListAdapter.get_count()):
            if self.candidateRegistrationWidget.candidateListAdapter.get_view(i).is_selected:
                candidate = self.candidateRegistrationWidget.candidateListAdapter.get_view(i).text
                break
        count = 0
        if candidate != "":
            for nam in self.candidateNames:
                if nam == user and nam != candidate:
                    count += 1
            if count > 0:
                flag = False
        else:
            flag = False
        if flag:
            query = "UPDATE candidates SET username=\"" + user + "\", id=\"" + _id + "\", name=\"" + name + \
                    "\" WHERE username=\"" + candidate + "\";"
            self.cursor.execute(query)
            self.dataBase.commit()
            self.popupBtn.text = user + " is updated in Database"
            self.popup.open()
            self.load_candidates()
            self.update_candidate_widget(self.candidateRegistrationWidget.candidateListAdapter)
        else:
            self.popupBtn.text = "please fill the credentials correctly"
            self.popup.open()

    def delete_candidate(self, btn):
        candidate = ""
        for i in range(self.candidateRegistrationWidget.candidateListAdapter.get_count()):
            if self.candidateRegistrationWidget.candidateListAdapter.get_view(i).is_selected:
                candidate = self.candidateRegistrationWidget.candidateListAdapter.get_view(i).text
                break
        if candidate != "":
            query = "DELETE FROM candidates WHERE username=\""+candidate+"\";"
            self.cursor.execute(query)
            self.dataBase.commit()
            self.load_candidates()
            self.update_candidate_widget(self.candidateRegistrationWidget.candidateListAdapter)

    def load_candidates(self):
        self.cursor.execute("SELECT username FROM candidates;")
        self.dataBase.commit()
        names = list(self.cursor.fetchall())
        self.candidateNames = []
        temp = []
        if len(names) != 0:
            for i in range(len(names)):
                temp.append(names[i][0])
        self.candidateNames = temp

    def add_voter(self, arg):
        flag = False
        user = self.voterRegistrationWidget.userNameTextInput.text.strip()
        _id = self.voterRegistrationWidget.idTextInput.text.strip()
        name = self.voterRegistrationWidget.nameTextInput.text.strip()
        password = self.voterRegistrationWidget.passwordTextInput.text.strip()
        if user != "":
            if _id != "":
                if name != "":
                    if password != "":
                        if password == self.voterRegistrationWidget.reTypePasswordTextInput.text.strip():
                            if len(self.userNames) == 0:
                                flag = True
                            for nam in self.userNames:
                                if user == nam:
                                    flag = False
                                    break
                                else:
                                    flag = True
        if flag:
            query = "INSERT INTO voters(name,id,username,password) VALUES (\"" + name + "\",\"" + \
                    _id + "\",\"" + user + "\",\"" + password + "\");"
            self.cursor.execute(query)
            self.dataBase.commit()
            self.popupBtn.text = user + " added to Database"
            self.popup.open()
            self.load_username()
            self.update_voter_widget(self.voterRegistrationWidget.votersListAdapter)
        else:
            self.popupBtn.text = "please fill the credentials correctly"
            self.popup.open()

    def load_username(self):
        self.cursor.execute("SELECT username FROM voters;")
        self.dataBase.commit()
        names = list(self.cursor.fetchall())
        self.userNames = []
        temp = []
        if len(names) != 0:
            for i in range(len(names)):
                temp.append(names[i][0])
        self.userNames = temp

    def dismiss_popup(self, arg):
        self.popup.dismiss()

    def edit_voter(self, args):
        flag = False
        user = self.voterRegistrationWidget.userNameTextInput.text.strip()
        _id = self.voterRegistrationWidget.idTextInput.text.strip()
        name = self.voterRegistrationWidget.nameTextInput.text.strip()
        password = self.voterRegistrationWidget.passwordTextInput.text.strip()
        if user != "":
            if _id != "":
                if name != "":
                    if password != "":
                        if password == self.voterRegistrationWidget.reTypePasswordTextInput.text.strip():
                            if len(self.userNames) == 0:
                                flag = False
                            else:
                                flag = True
        voter = ""
        for i in range(self.voterRegistrationWidget.votersListAdapter.get_count()):
            if self.voterRegistrationWidget.votersListAdapter.get_view(i).is_selected:
                voter = self.voterRegistrationWidget.votersListAdapter.get_view(i).text
                break
        count = 0
        if voter != "":
            for nam in self.userNames:
                if nam == user and nam != voter:
                    count += 1
            if count > 0:
                flag = False
        else:
            flag = False
        if flag:
            query = "UPDATE voters SET username=\"" + user + "\", id=\"" + _id + "\", name=\"" + name + \
                    "\", password=\"" + password + "\" WHERE username=\"" + voter + "\";"
            self.cursor.execute(query)
            self.dataBase.commit()
            self.popupBtn.text = user + " is updated in Database"
            self.popup.open()
            self.load_username()
            self.update_voter_widget(self.voterRegistrationWidget.votersListAdapter)
        else:
            self.popupBtn.text = "please fill the credentials correctly"
            self.popup.open()

    def update_voter_widget(self, adapter):
        voter = ""
        for i in range(adapter.get_count()):
            if self.voterRegistrationWidget.votersListAdapter.get_view(i).is_selected:
                voter = self.voterRegistrationWidget.votersListAdapter.get_view(i).text
                break
        if voter != "":
            query = "SELECT id,name FROM voters WHERE username=\""+voter+"\";"
            self.cursor.execute(query)
            self.dataBase.commit()
            temp = self.cursor.fetchone()
            self.voterRegistrationWidget.userNameTextInput.text = voter
            self.voterRegistrationWidget.idTextInput.text = temp[0]
            self.voterRegistrationWidget.nameTextInput.text = temp[1]

    def delete_voter(self, args):
        voter = ""
        for i in range(self.voterRegistrationWidget.votersListAdapter.get_count()):
            if self.voterRegistrationWidget.votersListAdapter.get_view(i).is_selected:
                voter = self.voterRegistrationWidget.votersListAdapter.get_view(i).text
                break
        if voter != "":
            query = "DELETE FROM voters WHERE username=\""+voter+"\";"
            self.cursor.execute(query)
            self.dataBase.commit()
            self.load_username()
            self.update_voter_widget(self.voterRegistrationWidget.votersListAdapter)

    def connect_to_database(self):
        self.dataBase = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", passwd="1234")

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
        if len(vote_dbs) == 0:
            t = time.localtime()
            t = datetime.datetime(*t[:6])
            name = str(t.date()).replace("-", "") + str(t.time()).replace(":", "")
            self.cursor.execute("CREATE DATABASE vote_database"+name+";")
            self.dataBase.commit()
            self.cursor.execute("USE vote_database"+name+";")
            self.dataBase.commit()
            self.selectedDataBase = "vote_database"+name
        else:
            self.cursor.execute("USE " + vote_dbs[len(vote_dbs)-1]+";")
            self.dataBase.commit()
            self.selectedDataBase = vote_dbs[len(vote_dbs)-1]
        self.create_tables()
        time.sleep(1)
        self.load_username()
        self.load_candidates()
        ConnectionServer("", 12345)

    def create_tables(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS voters(name VARCHAR(65),id VARCHAR(20), username VARCHAR(65),"
                            "password VARCHAR(10), vote VARCHAR(65), casted TINYINT UNSIGNED DEFAULT 0);")
        self.dataBase.commit()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS candidates(name VARCHAR(65),id VARCHAR(20),"
                            "username VARCHAR(65));")
        self.dataBase.commit()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS status(flag TINYINT);")
        self.dataBase.commit()
        self.cursor.execute("SELECT * FROM status;")
        self.dataBase.commit()
        if len(self.cursor.fetchall()) == 0:
            self.cursor.execute("INSERT INTO status (flag) VALUES (0);")
            self.dataBase.commit()
        else:
            self.cursor.execute("SELECT * FROM status;")
            self.dataBase.commit()
            if self.cursor.fetchone()[0] == 2:
                self.electionControlWidget.pollingResultsListAdapter.data = ["Polling is over now start counting"]
                self.electionControlWidget.electionSwitch.text = "Reset Election for new Election"
                self.electionControlWidget.electionSwitch.disabled = True

    def start_stop_election(self, arg):
        if arg.state == "down":
            self.electionControlWidget.countResultButton.disabled = True
            self.electionControlWidget.resetButton.disabled = True
            self.electionControlWidget.electionSwitch.text = "Stop Election Now"
            self.cursor.execute("UPDATE status SET flag = 1;")
            self.dataBase.commit()
            self.candidateRegistrationWidget.disabled = True
            self.voterRegistrationWidget.disabled = True
            thread.start_new_thread(self.update_voter_status, ())
        else:
            self.electionControlWidget.countResultButton.disabled = False
            self.electionControlWidget.resetButton.disabled = False
            self.electionControlWidget.electionSwitch.text = "Start Election Now"
            self.cursor.execute("UPDATE status SET flag = 2;")
            self.dataBase.commit()
        self.cursor.execute("SELECT * FROM status;")
        self.dataBase.commit()
        if self.cursor.fetchone()[0] == 2:
            self.electionControlWidget.pollingResultsListAdapter.data = ["Polling is over now start counting"]
            self.electionControlWidget.electionSwitch.text = "Reset Election for new Election"
            self.electionControlWidget.electionSwitch.disabled = True
            self.voterRegistrationLayout.disabled = True
            self.candidateRegistrationLayout.disabled = True

    def reset_voting(self, instance):
        t = time.localtime()
        t = datetime.datetime(*t[:6])
        name = str(t.date()).replace("-", "") + str(t.time()).replace(":", "")
        self.cursor.execute("CREATE DATABASE vote_database"+name+";")
        self.dataBase.commit()
        self.cursor.execute("USE vote_database"+name+";")
        self.dataBase.commit()
        self.create_tables()
        self.electionControlWidget.pollingResultsListAdapter.data = ["Results not yet counted"]
        self.electionControlWidget.electionSwitch.text = "Start Election"
        self.electionControlWidget.electionSwitch.disabled = False
        self.voterRegistrationLayout.disabled = False
        self.candidateRegistrationLayout.disabled = False
        self.load_username()
        self.update_voter_widget(self.voterRegistrationWidget.votersListAdapter)
        self.load_candidates()
        self.update_candidate_widget(self.candidateRegistrationWidget.candidateListAdapter)

    def count_results(self, instance):
        candidates = self.candidateRegistrationWidget.candidateListAdapter.data
        table = []
        for name in candidates:
            self.cursor.execute("SELECT COUNT(vote) FROM voters WHERE vote =\"" + name + "\";")
            self.dataBase.commit()
            votes = self.cursor.fetchone()[0]
            table.append(name + " - " + str(votes))
        self.electionControlWidget.pollingResultsListAdapter.data = table

    def update_voter_status(self):
        voters = self.voterRegistrationWidget.votersListAdapter.data
        db = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", passwd="1234")
        cur = db.cursor()
        print(self.selectedDataBase)
        cur.execute("USE " + self.selectedDataBase + ";")
        db.commit()
        while True:
            table = []
            for name in voters:
                cur.execute("SELECT casted FROM voters WHERE username=\"" + name + "\";")
                db.commit()
                status = cur.fetchone()[0]
                print status
                if status == 0:
                    table.append(name + " - vote not casted")
                else:
                    table.append(name + " - vote casted")
            print table
            self.electionControlWidget.pollingListAdapter.data = table
            time.sleep(5)


class VotingSystemApp(App):
    def build(self):
        return VotingSystemWidget()


class LoginApp(App):
    def __init__(self, **kwargs):
        super(LoginApp, self).__init__(**kwargs)
        self.widget = LoginWidget()

    def login_status(self):
        return self.widget.loginSuccess

    def build(self):
        return self.widget


def monitor_login_status(app):
    while True:
        try:
            global status
            status = app.login_status()
            time.sleep(0.3)
        except:
            break

if __name__ == "__main__":
    app = LoginApp()
    thread.start_new(monitor_login_status, (app,))
    app.run()
    if status:
        VotingSystemApp().run()


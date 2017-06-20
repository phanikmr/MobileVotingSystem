from kivy.uix.listview import ListView
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App


class VoterRegistrationWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(VoterRegistrationWidget, self).__init__(**kwargs)

        self.leftLayout = BoxLayout(orientation="vertical")
        self.rightLayout = BoxLayout(orientation="vertical")
        self.addVoterBtn = Button(text="Add New Voter", size_hint_y=0.1)
        self.leftLayout.add_widget(self.addVoterBtn)
        self.editVoterBtn = Button(text="Edit Selected Voter", size_hint_y=0.1)
        self.leftLayout.add_widget(self.editVoterBtn)
        self.deleteVoterBtn = Button(text="Delete Selected Voter", size_hint_y=0.1)
        self.leftLayout.add_widget(self.deleteVoterBtn)
        ListItemButton.selected_color = [0, 0.93, 1, 1]
        ListItemButton.deselected_color = [0.25, 0.25, 0.25, 1]
        self.votersListAdapter = ListAdapter(data=[],
                                             allow_empty_selection=False, selection_mode="single", cls=ListItemButton)

        self.voterListView = ListView(adapter=self.votersListAdapter)
        self.leftLayout.add_widget(self.voterListView)

        self.userNameLabel = Label(text="UserName")
        self.userNameTextInput = TextInput(multiline=False)
        self.userNameTextInput.text_size = [self.userNameTextInput.width, None]
        self.rightLayout.add_widget(add_to_boxlayout(self.userNameLabel, self.userNameTextInput))
        self.idLabel = Label(text="ID")
        self.idTextInput = TextInput(multiline=False)
        self.idTextInput.text_size = [self.idTextInput.width, None]
        self.rightLayout.add_widget(add_to_boxlayout(self.idLabel, self.idTextInput))
        self.nameLabel = Label(text="Name")
        self.nameTextInput = TextInput(multiline=False)
        self.nameTextInput.text_size = [self.nameTextInput.width, None]
        self.rightLayout.add_widget(add_to_boxlayout(self.nameLabel, self.nameTextInput))
        self.passwordLabel = Label(text="Password")
        self.passwordTextInput = TextInput(password=True, multiline=False)
        self.passwordTextInput.text_size = [self.passwordTextInput.width, None]
        self.rightLayout.add_widget(add_to_boxlayout(self.passwordLabel, self.passwordTextInput))
        self.reTypePasswordLabel = Label(text="Re-type Password")
        self.reTypePasswordTextInput = TextInput(password=True, multiline=False)
        self.reTypePasswordTextInput.text_size = [self.reTypePasswordTextInput.width, None]
        self.rightLayout.add_widget(add_to_boxlayout(self.reTypePasswordLabel, self.reTypePasswordTextInput))

        self.add_widget(self.leftLayout)
        self.add_widget(self.rightLayout)

    def update_selection(self, adapter):
        for i in range(adapter.get_count()):
            if self.votersListAdapter.get_view(i).is_selected:
                self.selected_voter = self.votersListAdapter.get_view(i).text
                break


def add_to_boxlayout(widget1, widget2):
    layout = BoxLayout()
    layout.add_widget(widget1)
    layout.add_widget(widget2)
    return layout


class AdminLogin(App):
    def build(self):
        widget = VoterRegistrationWidget()
        widget.votersListAdapter.data = ["Item #{0}".format(i) for i in range(10)]
        return widget


if __name__ == "__main__":
    AdminLogin().run()

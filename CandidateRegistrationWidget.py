from kivy.uix.listview import ListView
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from VoterRegistrationWidget import add_to_boxlayout


class CandidateRegistrationWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(CandidateRegistrationWidget, self).__init__(**kwargs)

        self.selectedCandidate = ""

        self.leftLayout = BoxLayout(orientation="vertical")
        self.addCandidateBtn = Button(text="Add New Candidate", size_hint_y=0.1)
        self.leftLayout.add_widget(self.addCandidateBtn)
        self.editCandidateBtn = Button(text="Edit Selected Candidate", size_hint_y=0.1)
        self.leftLayout.add_widget(self.editCandidateBtn)
        self.deleteCandidateBtn = Button(text="Delete Selected Candidate", size_hint_y=0.1)
        self.leftLayout.add_widget(self.deleteCandidateBtn)
        ListItemButton.selected_color = [0, 0.93, 1, 1]
        ListItemButton.deselected_color = [0.25, 0.25, 0.25, 1]
        self.candidateListAdapter = ListAdapter(data=[],
                                                allow_empty_selection=False, selection_mode="single", cls=ListItemButton)
        self.candidateListAdapter.bind(on_selection_change=self.update_selection)
        self.candidateListView = ListView(adapter=self.candidateListAdapter)
        self.leftLayout.add_widget(self.candidateListView)
        self.add_widget(self.leftLayout)

        self.rightLayout = BoxLayout(orientation="vertical")
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

        self.add_widget(self.rightLayout)

    def update_selection(self, adapter):
        for i in range(adapter.get_count()):
            if self.candidateListAdapter.get_view(i).is_selected:
                self.selectedCandidate = self.candidateListAdapter.get_view(i).text
                break


class AdminLogin(App):
    def build(self):
        widget = CandidateRegistrationWidget()
        return widget


if __name__ == "__main__":
    AdminLogin().run()

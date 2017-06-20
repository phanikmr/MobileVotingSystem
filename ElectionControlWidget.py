from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.listview import ListView
from kivy.adapters.simplelistadapter import SimpleListAdapter
from kivy.app import App


class ElectionControlWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(ElectionControlWidget, self).__init__(**kwargs)
        self.orientation = "horizontal"

        self.leftLayout = BoxLayout(orientation="vertical")
        self.electionSwitch = ToggleButton(text="Start Election Now", size_hint_y=0.1)
        self.leftLayout.add_widget(self.electionSwitch)
        self.resetButton = Button(text="Reset Election", size_hint_y=0.1)
        self.leftLayout.add_widget(self.resetButton)
        self.countResultButton = Button(text="Count Results", size_hint_y=0.1)
        self.leftLayout.add_widget(self.countResultButton)
        self.pollingResultsLabel = Label(text="Polling Results", size_hint_y=0.1, color=[0, 0.93, 1, 1])
        self.leftLayout.add_widget(self.pollingResultsLabel)
        self.pollingResultsListAdapter = SimpleListAdapter(data=["Not yet counted"], cls=Label)
        self.polingResultsListView = ListView(adapter=self.pollingResultsListAdapter)
        self.leftLayout.add_widget(self.polingResultsListView)
        self.add_widget(self.leftLayout)

        self.rightLayout = BoxLayout(orientation="vertical")
        self.pollingLabel = Label(text="Current polling status", size_hint_y=0.1, color=[0, 0.93, 1, 1])
        self.rightLayout.add_widget(self.pollingLabel)
        self.pollingListAdapter = SimpleListAdapter(data=["Polling not started"], cls=Label)
        self.polingListView = ListView(adapter=self.pollingListAdapter)
        self.rightLayout.add_widget(self.polingListView)
        self.add_widget(self.rightLayout)


class AdminLogin(App):
    def build(self):
        return ElectionControlWidget()


if __name__ == "__main__":
    AdminLogin().run()

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

class TodoList(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.task_label = Label(text="Priority:")
        self.add_widget(self.task_label)
        self.tasks = []
        self.priority = []
        self.text_input = TextInput(multiline=False)

        self.priority_input = TextInput(multiline=False)
        self.add_widget(self.priority_input)
        self.priority_label = Label(text="Task:")
        self.add_widget(self.priority_label)
        self.add_widget(self.text_input)
        self.add_button = Button(text="Add")
        self.add_button.bind(on_press=self.add_task)
        self.add_widget(self.add_button)
        self.view_button = Button(text="View")
        self.view_button.bind(on_press=self.view_tasks)
        self.add_widget(self.view_button)
        self.task_labels = []
        self.load_list()


    def add_task(self, instance):
        task = self.text_input.text
        priority = self.priority_input.text
        self.tasks.append(task)
        self.priority.append(priority)
        self.save_list()
        self.text_input.text = ""
        self.priority_input.text = ""



    def view_tasks(self, instance):
        for label in self.task_labels:
            self.remove_widget(label)
        self.task_labels = []
        for task, priority in zip(self.tasks, self.priority):
            label = Label(text=f"{task} ({priority})", font_size=20)
            if priority == "High":
                label.color = (1, 0, 0, 1)
            elif priority == "Medium":
                label.color = (0, 1, 0, 1)
            elif priority == "Low":
                label.color = (0, 0, 1, 1)
            delete_button = Button(text="X", size_hint_x=None, width=40)
            delete_button.task = task
            delete_button.bind(on_press=self.delete_task)
            row = BoxLayout(size_hint_y=None, height=40)
            row.add_widget(label)
            row.add_widget(delete_button)
            self.add_widget(row)
            self.task_labels.append(row)

    def delete_task(self, instance):
        task = instance.task
        index = self.tasks.index(task)
        self.tasks.pop(index)
        self.priority.pop(index)
        self.save_list()
        self.view_tasks(None)

    def save_list(self):
        with open("todo_list.txt", "w") as f:
            for task, priority in zip(self.tasks, self.priority):
                f.write(f"{task},{priority}\n")

    def load_list(self):
        try:
            with open("todo_list.txt", "r") as f:
                lines = f.readlines()
                for line in lines:
                    task, priority = line.strip().split(",")
                    self.tasks.append(task)
                    self.priority.append(priority)
        except:
            pass

class TodoApp(App):
    def build(self):

        return TodoList()

if __name__ == "__main__":
    TodoApp().run()
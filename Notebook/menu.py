from notebooks import Note, Notebook

class Menu():
    
    def __init__(self):
        self.notebook = Notebook()
        self.choices = {
            '1': self.show_notes,
            '2': self.search_notes,
            '3': self.add_note,
            '4': self.modify_note,
            '0': self.quit,
        }

    def display_menu(self):
        print("""
        Notebook Menu
        
        1. Show all Notes
        2. Search Notes
        3. Add Note
        4. Modify Note
        0. Quit
        """)
    
    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter an option: ")
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print(f'{choice} is not an avalible option')

    def show_notes(self, note_list=None):
        if not note_list:
            note_list = self.notebook.note_list
        for note in note_list:
            print(f"{note.id_}. {note.tags}\n{note.memo}")

    def search_notes(self):
        filter_ = input('Search for: ')
        notes = self.notebook.search(filter_)
        self.show_notes(note_list=notes)
    
    def add_note(self):
        memo = input("Enter a memo: ")
        self.notebook.new_note(memo)
        print("Your note has been added")
    
    def modify_note(self):
        id_ = input("Enter a note id: ")
        memo = input("Enter a memo: ")
        tags = input("Enter a tags: ")
        if memo:
            self.notebook.modify_memo(int(id_), memo)
        if tags:
            self.notebook.modify_tags(int(id_), tags)
    
    def quit(self):
        print("Exiting...")
        exit(0)


if __name__ == "__main__":
    Menu().run()
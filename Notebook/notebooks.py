from datetime import datetime

last_id = 0

class Note():
    'Some title'
    def __init__(self, memo, tags=''):
        self.memo = memo
        self.tags = tags
        self.creation_date = datetime.today().date()
        global last_id
        self.id_ = last_id
        last_id += 1

    def match(self, filter_):
        return filter_ in self.memo or filter_ in self.tags
    
class Notebook():
    def __init__(self):
        self.note_list = []

    def new_note(self, memo, tags=''):
        self.note_list.append(Note(memo, tags))

    def modify_memo(self, note_id, memo):
        self.note_list[note_id].memo = memo
    
    def modify_tags(self, note_id, tags):
        self.note_list[note_id].tags = tags

    def search(self, filter_):
        return [note for note in self.note_list if
                note.match(filter_)]
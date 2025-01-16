# HANDLERS

# ---------------------------------------------------------------------------------------------------------------------
# IMPORT LIBRARIES
from watchdog.events import FileSystemEventHandler

# ---------------------------------------------------------------------------------------------------------------------
# HANDLERS CLASSES

class MainEventHandler(FileSystemEventHandler):
    def __init__(self):
        self.changes_item_lst = []    # keep path to changes files or directories
    def on_created(self, event):
        self.changes_item_lst.append(event.src_path)

    def on_deleted(self, event):
        try:
            self.changes_item_lst.remove(event.src_path)
        except ValueError:
            ...

    def on_moved(self, event):
        current_path = event.src_path
        new_path = event.dest_path
        for path in self.changes_item_lst:
            if current_path == path:
                self.changes_item_lst.remove(current_path)
                self.changes_item_lst.append(new_path)
                break
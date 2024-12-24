import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def delete_file(file_path: str) -> bool:
    # Удаление файла
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f'Файл {file_path} удалён.')
        return 1
    else:
        print(f'Файл {file_path} не существует.')
        return 0


def delete_non_empty_directory(dir_path: str) -> bool:
    # Удаление директории с содержимым
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        print(f'Директория {dir_path} с содержимым удалена.')
        return 1
    else:
        print(f'Директория {dir_path} не существует.')
        return 0


def main():
    class MyEventHandler(FileSystemEventHandler):
        def on_created(self, event):
            changes_item_lst.append(event.src_path)

        def on_deleted(self, event):
            try:
                changes_item_lst.remove(event.src_path)
            except ValueError:
                ...

        def on_moved(self, event):
            current_path = event.src_path
            new_path = event.dest_path
            for path in changes_item_lst:
                if current_path == path:
                    changes_item_lst.remove(current_path)
                    changes_item_lst.append(new_path)
                    break

    changes_item_lst = []   # keep path to changes files or directories
    path = "/home/vlad/Desktop"
    event_handler = MyEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    observer.start()
    print('Programm started')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print(f'\n{changes_item_lst=}')

    while changes_item_lst:
        file_name = ''
        directory_name = ''

        current_path_to_obj = changes_item_lst[0]
        base = current_path_to_obj.split('.')

        if len(base) == 2:    # if this file 
            file_name = base[-1]
        else:    # if this directory
            directory_name = current_path_to_obj.split('/')[-1]

        if file_name:
            result_statue = delete_file(current_path_to_obj)
        elif directory_name:
            result_statue = delete_non_empty_directory(current_path_to_obj)
        changes_item_lst.remove(current_path_to_obj)
        


if __name__ == "__main__":
    print('Programm starting...')
    main()
    print('Programm finished')

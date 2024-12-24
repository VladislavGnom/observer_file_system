# import requests 
# import json
# from hashlib import md5

# API_URL = "http://127.0.0.1:8000"
# prompt_image = 'https://static-cse.canva.com/blob/191106/00_verzosa_winterlandscapes_jakob-owens-tb-2640x1485.jpg'
# SECURITY_KEY_FOR_WEBAPP_API = '4f1413482bb60b38a18c580c14d305f3'

# # Определяем заголовки
# headers = {
#     'User-Agent': 'my-app/0.0.1',
#     'Authorization': md5(SECURITY_KEY_FOR_WEBAPP_API.encode()).hexdigest(),
# }

# data = requests.get(f'{API_URL}/load_photo', params={'image_name':prompt_image}, headers=headers)

# print(data.json()['url'])

import os
import logging
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def delete_file(file_path: str) -> bool:
    # Удаление файла
    if os.path.exists(file_path):
        os.remove(file_path)
        logging.info(f'Файл {file_path} удалён.')
        return 1
    else:
        logging.info(f'Файл {file_path} не существует.')
        return 0


def delete_non_empty_directory(dir_path: str) -> bool:
    # Удаление директории с содержимым
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        logging.info(f'Директория {dir_path} с содержимым удалена.')
        return 1
    else:
        logging.info(f'Директория {dir_path} не существует.')
        return 0


def main(path_name):
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
    path = path_name
    event_handler = MyEventHandler()
    observer = Observer()
    try:
        observer.schedule(event_handler, path, recursive=True)
    except Exception as exc:
        logging.error(exc)

    observer.start()
    print('Programm started')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    logging.info(f'{changes_item_lst=}')

    while changes_item_lst:
        file_name = ''
        directory_name = ''

        current_path_to_obj = changes_item_lst[0]
        base = current_path_to_obj.split('.')

        if len(base) == 2:    # if this file 
            file_name = base[-1]
        else:    # if this directory
            directory_name = current_path_to_obj.split('/')[-1]

        if file_name and file_name != 'program.log':
            result_statue = delete_file(current_path_to_obj)
        elif directory_name:
            result_statue = delete_non_empty_directory(current_path_to_obj)
        changes_item_lst.remove(current_path_to_obj)
        


if __name__ == "__main__":
    path_name = "/home/vlad/Desktop"    # path to trackable directory
    logging.basicConfig(filename=os.path.join(path_name, 'program.log'), filemode='w+', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    print('Programm starting...')
    logging.info('Programm starting...')
    main(path_name)
    print('Programm finished')
    logging.info('Programm finished')

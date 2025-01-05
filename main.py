import os
import signal
import logging
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


interrupted = False    # run main loop


class MyEventHandler(FileSystemEventHandler):
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
        for path in changes_item_lst:
            if current_path == path:
                self.changes_item_lst.remove(current_path)
                self.changes_item_lst.append(new_path)
                break
            

def signal_handler(sig, frame):
    global interrupted
    logging.info('Получен сигнал завершения. Завершение работы...')
    # Здесь можно добавить код для очистки или завершения работы
    interrupted = True

# Установка обработчика сигнала
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


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
    global interrupted
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
        while not interrupted:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    except Exception as error:
        logging.error(error)
    changes_item_lst = event_handler.changes_item_lst    # get list of paths
    #observer.join()    # problem with it
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
        try:
            changes_item_lst.remove(current_path_to_obj)
        except Exception as error:
            logging.error(error)


if __name__ == "__main__":
    path_name = "/home/vlad/Desktop"    # path to trackable directory
    logging.basicConfig(filename=os.path.join(path_name, 'program.log'), filemode='a+', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    print('Programm starting...')
    logging.info('\n\nProgramm starting...')
    main(path_name)
    print('Programm finished')
    logging.info('Programm finished')

# OBSERVER

# ---------------------------------------------------------------------------------------------------------------------
# IMPORT LIBRARIES
import os
import signal
import logging
import time

from watchdog.observers import Observer

from utils import signal_handler
from handlers import MainEventHandler
from actions import delete_file, delete_non_empty_directory

# ---------------------------------------------------------------------------------------------------------------------
# MAIN FILE

interrupted = False    # run main loop

# Установка обработчика сигнала
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def main(path_name):
    global interrupted
    path = path_name
    event_handler = MainEventHandler()
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
    logging.info('Programm starting...')
    main(path_name)
    print('Programm finished')
    logging.info('Programm finished\n\n')

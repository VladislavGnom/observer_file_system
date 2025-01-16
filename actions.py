# ACTIONS

# ---------------------------------------------------------------------------------------------------------------------
# IMPORT LIBRARIES
import os
import shutil
import logging

# ---------------------------------------------------------------------------------------------------------------------
# ACTION FUNCS

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
# UTILS

# ---------------------------------------------------------------------------------------------------------------------
# IMPORT LIBRARIES
import logging
import time

# ---------------------------------------------------------------------------------------------------------------------
# UTILS FUNCS

def signal_handler(sig, frame):
    global interrupted
    logging.info('Получен сигнал завершения. Завершение работы...')
    # Здесь можно добавить код для очистки или завершения работы
    print(interrupted)    
    interrupted = True

def active_venv(script_name='script.sh'):
    import subprocess
    print(['source /home/vlad/Desktop/Projects/Python/Observer/%s' % script_name])
    subprocess.run(['./%s' % script_name], capture_output=True, text=True)
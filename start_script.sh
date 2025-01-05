#!/bin/bash

# Запуск Python-скрипта в фоновом режиме
source venv/bin/activate
sudo sysctl fs.inotify.max_user_watches=1000000
python /home/vlad/main.py &
echo $! > pidfile

# Функция, которая будет выполнена при завершении скрипта
cleanup() {
    echo "Завершение работы скрипта..."
    # Имитация нажатия Ctrl+C
    kill -SIGINT $(<pidfile)
    echo $(<pidfile)
    # Убедитесь, что процесс завершён
    wait $(<pidfile)
    echo "Скрипт завершён."
}

# Установка trap для перехвата сигнала SIGTERM
trap cleanup SIGTERM

echo $(<pidfile)

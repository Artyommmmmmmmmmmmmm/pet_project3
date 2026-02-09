#!/usr/bin/env python
import os
import sys
import subprocess
import time
from threading import Thread

def run_command(cmd, name=""):
    """Запускает команду и логирует вывод"""
    print(f"🚀 Запуск {name}...")
    try:
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        # Вывод в реальном времени
        for line in process.stdout:
            print(f"[{name}] {line}", end='')
        
        process.wait()
        if process.returncode == 0:
            print(f"✅ {name} успешно завершен")
        else:
            print(f"❌ {name} завершен с ошибкой")
    except Exception as e:
        print(f"⚠️ Ошибка при запуске {name}: {e}")

def main():
    print("=" * 50)
    print("🚀 ЗАПУСК DJANGO ПРОЕКТА")
    print("=" * 50)
    
    # 1. Активация виртуального окружения (если нужно)
    # venv_path = os.path.join(os.path.dirname(__file__), 'venv')
    # if os.path.exists(venv_path):
    #     activate_script = os.path.join(venv_path, 'Scripts' if sys.platform == 'win32' else 'bin', 'activate')
    #     os.environ['VIRTUAL_ENV'] = venv_path
    
    # 2. Проверка зависимостей
    print("📦 Проверка зависимостей...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # 3. Применение миграций
    print("🔄 Применение миграций...")
    subprocess.run([sys.executable, "manage.py", "migrate"])
    
    # 4. Сбор статики (для продакшена)
    # subprocess.run([sys.executable, "manage.py", "collectstatic", "--noinput"])
    
    # 5. Запуск фоновых сервисов в отдельных потоках
    services = [
        # (["celery", "-A", "project", "worker", "-l", "info"], "Celery Worker"),
        # (["celery", "-A", "project", "beat", "-l", "info"], "Celery Beat"),
        # (["redis-server"], "Redis"),
    ]
    
    threads = []
    for cmd, name in services:
        thread = Thread(target=run_command, args=(" ".join(cmd), name), daemon=True)
        thread.start()
        threads.append(thread)
        time.sleep(1)  # Небольшая задержка между запусками
    
    # 6. Запуск Django сервера
    print("🌐 Запуск Django сервера...")
    print("=" * 50)
    print("Сервер доступен по адресу: http://127.0.0.1:8000")
    print("Для остановки нажмите Ctrl+C")
    print("=" * 50)
    
    # Основной процесс - Django сервер
    os.execvp(sys.executable, [sys.executable, "../project/manage.py", "runserver", "0.0.0.0:8000"])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Остановка сервера...")
        sys.exit(0)
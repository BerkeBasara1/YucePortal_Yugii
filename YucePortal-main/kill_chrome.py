import psutil

def kill_chrome():
    for proc in psutil.process_iter():
        try:
            if "chrome" in proc.name().lower():
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
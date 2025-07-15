import time
import subprocess
import sys


def run_crons_periodically():

    while True:
        try:
            subprocess.run([sys.executable, "manage.py", "delete_expired_users"])
        except Exception as e:
            pass

        time.sleep(300)

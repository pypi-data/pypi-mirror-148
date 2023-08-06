import subprocess


class Pm2Manager:
    def __init__(self):
        pass

    @staticmethod
    def start(app_name='all'):
        subprocess.call(['pm2', 'start', app_name])

    @staticmethod
    def stop(app_name='all'):
        subprocess.call(['pm2', 'stop', app_name])

    @staticmethod
    def restart(app_name='all'):
        subprocess.call(['pm2', 'restart', app_name])

    @staticmethod
    def delete(app_name='all'):
        subprocess.call(['pm2', 'delete', app_name])

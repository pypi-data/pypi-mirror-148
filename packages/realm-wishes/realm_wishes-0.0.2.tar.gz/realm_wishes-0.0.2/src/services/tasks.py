from celery import Celery


app = Celery('wish_tasks', backend='redis://localhost/0', broker='redis://localhost/0')

def wish_tasks():
    return

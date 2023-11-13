from celery import shared_task
from time import sleep

@shared_task
def add(x,y):
    result = x + y
    sleep(5)
    print(f"The result of {x} + {y} is: {result}")
    return result
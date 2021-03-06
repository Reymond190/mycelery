import os
from celery import Celery
from django.conf import settings
from app1.tasks import main_func
settings.configure()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celdj.settings')



app = Celery('db1')

app.config_from_object('django.conf:settings',namespace='CELERY')

@app.task
def see_you():
    main_func()
    print("See you in ten seconds!")


# app.conf.beat_schedule = {
#     "see-you-in-ten-seconds-task": {
#         "task": "one.tasks.all"
#     }
#
# }


# Load task modules from all registered Django app configs.
# app.autodiscover_tasks(see_you)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# def main():
#     x = see_you.delay()
#     print(x.get())
#
# if __name__ == '__main__':
#     main()
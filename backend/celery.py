from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# Встановлюємо Django налаштування за замовчуванням для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

# Завантажуємо конфігурацію Celery з Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматично знаходить асинхронні завдання в додатках
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

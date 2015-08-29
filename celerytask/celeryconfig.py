BROKER_URL = 'django://'
#CELERY_RESULT_BACKEND = 'amqp://'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True

# CELERY_ROUTES = {
#     'celerytask.tasks.add_task': 'low-priority',
# }

CELERY_ANNOTATIONS = {
    'celerytask.tasks.add_task': {'rate_limit': '2/m'}
}
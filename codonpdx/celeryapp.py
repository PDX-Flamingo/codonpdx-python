from __future__ import absolute_import

from celery import Celery

app = Celery('codonpdx',
             include=['codonpdx.tasks'])

app.config_from_object('codonpdx.celeryconfig')

if __name__ == '__main__':
    app.start()

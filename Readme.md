install gevent and eventlet using conda
```
conda install -c conda-forge gevent -y
```

### start redis server using WSL in windows
```
redis-server
```

### start celery worker
```
celery -A config worker --pool=solo -l INFO
```

### start celery beat
```
celery -A config beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

### run the django server
```
python manage.py runserver
```

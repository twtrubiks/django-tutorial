# Django Multiple databases

官網可參考 [multiple-databases](https://docs.djangoproject.com/en/4.2/topics/db/multi-db/#multiple-databases)

先執行

```cmd
docker-compose up -d
```

接著手動進去再建立兩個 db, 分別是 primary_db 以及 readonly_db,

對應的 [settings.py](https://github.com/twtrubiks/django-tutorial/blob/django4_multi_db/django_tutorial/settings.py)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'password123',
        'HOST': 'localhost',
        'PORT': 5432,
    },
    'primary': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'primary_db',
        'USER': 'postgres',
        'PASSWORD': 'password123',
        'HOST': 'localhost',
        'PORT': 5432,
    },
    'readonly': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'readonly_db',
        'USER': 'postgres',
        'PASSWORD': 'password123',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}
```

接著開始 makemigrations

```cmd
python manage.py makemigrations musics
```

db migrate

```cmd
python manage.py migrate --database=default
python manage.py migrate --database=primary
python manage.py migrate --database=readonly
```

設定 [my_router/rotuer_1.py](https://github.com/twtrubiks/django-tutorial/blob/django4_multi_db/my_router/rotuer_1.py),

```python
class Router1:
    route_app_labels = "musics"

    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.route_app_labels:
            return "readonly"
        return None # 回傳 None 等於回傳 default

    def db_for_write(self, model, **hints):
        if model._meta.app_label == self.route_app_labels:
            return "primary"
        return None # 回傳 None 等於回傳 default

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
```

再到 [settings.py](https://github.com/twtrubiks/django-tutorial/blob/django4_multi_db/django_tutorial/settings.py) 中加入,

```python
DATABASE_ROUTERS = [
    'my_router.rotuer_1.Router1',
]
```

如果今天有很多的 router, 就是一直往下去, 如果找到就不再往下找.

```python
>>> from musics.models import Music
>>> # 只會被建立在 primary_db
>>> Music.objects.create()
<Music: Music object (1)>

>>> # 讀取資料只會從 readonly_db
>>> Music.objects.filter(id=1)
<QuerySet []>

>>> # 透過 using 強制指定 db (可以 pass 掉 router)
>>> Music.objects.using('primary').filter(id=1)
<QuerySet [<Music: Music object (1)>]>

>>> # user 只會被建立在 default db
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user("test", "test@test.com", "pwd123")
```

## 執行環境

* Python 3.9

## Reference

* [Django](https://www.djangoproject.com/)

## Donation

文章都是我自己研究內化後原創，如果有幫助到您，也想鼓勵我的話，歡迎請我喝一杯咖啡:laughing:

![alt tag](https://i.imgur.com/LRct9xa.png)

[贊助者付款](https://payment.opay.tw/Broadcaster/Donate/9E47FDEF85ABE383A0F5FC6A218606F8)

## License

MIT license

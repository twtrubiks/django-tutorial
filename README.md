# django_contenttypes

今天要來介紹很酷的 contenttypes,

官方文件[contenttypes](https://docs.djangoproject.com/en/5.0/ref/contrib/contenttypes/)

```text
Django includes a contenttypes application that can track all of the models installed in your Django-powered project, providing a high-level, generic interface for working with your models.
```

簡單說, 可以透過 contenttypes 連結全部的 model,

## 教學

首先, 如果你沒有特別設定, 預設都是有啟用的,

就在 [settings.py](https://github.com/twtrubiks/django-tutorial/blob/django_contenttypes/django_tutorial/settings.py) 底下的 INSTALLED_APPS,

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes", # <<<<<<<
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "musics",
]
```

先把 db 啟動, `docker compose up -d`,

然後 migrate

```cmd
python3 manage.py makemigrations
python3 manage.py migrate
```

其實 django_content_type 就是一張表, 等等下面會提到,

他負責紀錄和其他 model 之前的關係.

接著進入 shell

```cmd
python3 manage.py shell
```

開始介紹之前, 先看 [models.py](https://github.com/twtrubiks/django-tutorial/blob/django_contenttypes/musics/models.py)

```python
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

# class Sheet(models.Model):
#     name = models.CharField(default="sheet name")

# class Sheet2(models.Model):
#     name = models.CharField(default="sheet2 name")

# class Music(models.Model):
#     song = models.TextField(default="song")
#     singer = models.TextField(default="AKB48")
#     count = models.IntegerField(blank=True, null=True)
#     last_modify_date = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)
#     sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE, null=True)
#     sheet2 = models.ForeignKey(Sheet2, on_delete=models.CASCADE, null=True)

#     class Meta:
#         db_table = "music"

#     def display_type_name(self):
#         return self.get_type_display()


class Sheet(models.Model):
    name = models.CharField(default="sheet name")

    # 如果有加入這行, 可以反查(在 table 中不會增加欄位)
    musics = GenericRelation('Music')

class Sheet2(models.Model):
    name = models.CharField(default="sheet2 name")

class Music(models.Model):
    song = models.TextField(default="song")
    content_type = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)

    # 在 table 中不會增加欄位
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        db_table = "music"
```

註解掉的部份是正常的寫法, 沒註解掉的是透過 contenttypes 的寫法,

仔細看兩個的差異, 你會發現不需要寫那個多的 ForeignKey 了,

多出來的是 `content_type` `object_id` `content_object`,

直接來看範例,

```python
# 先建立一個 Sheet 和 一個 Sheet2 和一個 User
>>> from musics.models import Sheet, Sheet2
>>> sheet = Sheet.objects.create(name="sheet")
>>> sheet2 = Sheet2.objects.create(name="sheet2")

# 再建立一個內建的 User
from django.contrib.auth.models import User
user = User.objects.create(username="user1")
```

```python
# 建立 Music
>>> from musics.models import Music
>>> music_1 =  Music.objects.create(song="song", content_object=sheet)
>>> music_2 =  Music.objects.create(song="song", content_object=sheet2)
>>> music_3 =  Music.objects.create(song="song", content_object=user)

>>> music_1, music_1.content_type, music_1.content_type.name
(<Music: Music object (1)>, <ContentType: musics | sheet>, 'sheet')
>>> music_2, music_2.content_type, music_2.content_type.name
(<Music: Music object (2)>, <ContentType: musics | sheet2>, 'sheet2')
>>> music_3, music_3.content_type, music_3.content_type.name
(<Music: Music object (3)>, <ContentType: auth | user>, 'user')
```

你會發現, content_object 可以放入任何的物件,

(這邊放了 Sheet, Sheet2, User)

是不是非常的強大!!

如果你去看資料庫, music table 如下,

```sql
postgres=# SELECT id, song, content_type_id, object_id FROM public.music;
postgres-#
 id | song | content_type_id | object_id
----+------+-----------------+-----------
  1 | song |               7 |         1
  2 | song |               9 |         1
  3 | song |               4 |         1
(3 rows)
```

object_id 對應的是 model 中的 id,

content_type_id 對應的是 model 中的關係 (就是 django_content_type table),

django_content_type table 如下,

```sql
postgres=# SELECT * FROM public.django_content_type;
 id |  app_label   |    model
----+--------------+-------------
  1 | admin        | logentry
  2 | auth         | permission
  3 | auth         | group
  4 | auth         | user
  5 | contenttypes | contenttype
  6 | sessions     | session
  7 | musics       | sheet
  8 | musics       | music
  9 | musics       | sheet2
(9 rows)
```

`7` sheet model

`9` sheet2 model

`4` user model

其實他的原理就是透過 django_content_type 這張表去幫你找出答案的.

如果今天你想從 Sheet 去反查出 Music 也是可以,

在 Sheet 底下我們有加入 `musics = GenericRelation('Music')`


```python
>>> from musics.models import Sheet, Sheet2

sheet = Sheet.objects.get(pk=1)
>>> sheet.musics.all() # 成功反查, 因為有設定 GenericRelation
<QuerySet [<Music: Music object (1)>]>

sheet2 = Sheet2.objects.get(pk=1)
>>> sheet2.musics.all() # 反查失敗, 因為沒設定 GenericRelation
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: 'Sheet2' object has no attribute 'musics'
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

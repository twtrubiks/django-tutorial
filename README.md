# django-manager-tutorial

本篇文章介紹 django 的 manager, 什麼事 manager ❓

如果你有使用過 django,

你一定對 `models.objects.all()` 不陌生, 其中裡面的 objects 就是一種 manager,

今天要來介紹 manager, 目的是如果有特定的需求一直重複使用, 可以考慮把它寫成 Manager.

使用 djagno `5.0.6` 加上透過 `django-extensions` 觀察 ORM 實際 SQL,

migrate 後, 進入 shell 模式, 請使用以下指令

```cmd
python3 manage.py migrate
python3 manage.py shell_plus --print-sql
```

如果你不想要透過 `django-extensions` 這個指令,

可以使用 `str(queryset.query)` 查看 SQL 指令.

如果進入 shell 模式, 但方向鍵會印出很多奇怪的字符,

像是這樣 `^[[C^[[A^[[A^[[D^[[B^[`

請安裝以下套件進行修正

```cmd
pip3 install gnureadline
```

## Django Manager

更多 django Manager 的用法可參考 [managers](https://docs.djangoproject.com/en/5.0/topics/db/managers/)

### Adding extra manager methods

先來看一個簡單的範例

```python
class MusicSheetManager(models.Manager):

    def with_counts(self):
        return self.count()

class Sheet(models.Model):
    name = models.CharField(default="sheet name", max_length=64)

    objects = MusicSheetManager()
```

這邊定義了新的方法, 叫做 `with_counts`,

使用方法如下,

```python
>>> from musics.models import Sheet
>>> Sheet.objects.with_counts()
SELECT COUNT(*) AS "__count"
  FROM "musics_sheet"

0
```

原本的 `Sheet.objects.all()` 保持原本的行為, 就是多了一個 `with_counts` 可以使用.

### custom manager

接下來我們看怎麼增加新的 manger

```python
class MusicManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(song="song")

class Music(models.Model):
    ......

    objects = models.Manager()  # The default manager.
    custom_objects = MusicManager()  # The new manager.

    ......
```

`Music.objects.all()` 一樣保持原本的行為.

但在這邊定義了新的 `custom_objects` Manager,

這裡面直接改變了預設的 query, 固定過濾 song,

直接看以下的範例

```python
>>> from musics.models import Music

>>> # 你會發現預設的 all(), 就會去執行自己定義好的 get_queryset
>>> # SQL 多去過濾了 "song"
>>> Music.custom_objects.all()
SELECT "music"."id",
       "music"."song",
       "music"."singer",
       "music"."count",
       "music"."last_modify_date",
       "music"."created",
       "music"."sheet_id"
  FROM "music"
 WHERE "music"."song" = 'song'
 LIMIT 21

<QuerySet []>

>>> # 然後這個自己定義的 Manager 也是可以依照 ORM 下去操作
>>> # 就算用了 count, 可以正常使用, 也會預設過濾 "song"
>>> Music.custom_objects.count()
SELECT COUNT(*) AS "__count"
  FROM "music"
 WHERE "music"."song" = 'song'

0

>>> # 依照 ORM 下去操作都是沒問題的, 這邊再多加個過濾
>>> Music.custom_objects.filter(count=10)
SELECT "music"."id",
       "music"."song",
       "music"."singer",
       "music"."count",
       "music"."last_modify_date",
       "music"."created",
       "music"."sheet_id"
  FROM "music"
 WHERE ("music"."song" = 'song' AND "music"."count" = 10)
 LIMIT 21

<QuerySet []>
```

新增的 Manager, 也可以像前面一樣加入 extra manager methods,

```python
class MusicManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(song="song")

    def with_counts(self):
        return self.count()

class Music(models.Model):
    ......

    objects = models.Manager()  # The default manager.
    custom_objects = MusicManager()  # The new manager.

    ......
```

使用方法如下

```python
>>> from musics.models import Music
>>> Music.custom_objects.with_counts()
SELECT COUNT(*) AS "__count"
  FROM "music"
 WHERE "music"."song" = 'song'

0
```

你可以定義非常多的 Manager 來滿足使用情境.

## 執行環境

* Python 3.11

## Reference

* [Django](https://www.djangoproject.com/)

## Donation

文章都是我自己研究內化後原創，如果有幫助到您，也想鼓勵我的話，歡迎請我喝一杯咖啡 :laughing:

![alt tag](https://i.imgur.com/LRct9xa.png)

[贊助者付款](https://payment.opay.tw/Broadcaster/Donate/9E47FDEF85ABE383A0F5FC6A218606F8)

## License

MIT license

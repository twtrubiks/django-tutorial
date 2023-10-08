# django-orm-tutorial

使用 djagno `4.2.6` 加上透過 `django-extensions` 觀察 ORM 實際 SQL,

進入 shell 模式, 請使用以下指令

```cmd
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

## Django 匯入匯出

dumpdata 和 loaddata 是 django 提供匯入匯出的一個工具.

- 匯出

官網可參考 [dumpdata](https://docs.djangoproject.com/en/4.2/ref/django-admin/#dumpdata)

```cmd
python manage.py dumpdata > db.json
```

匯出特定的 table

```cmd
python3 manage.py dumpdata musics > db.json
```

- 匯入

官網可參考 [loaddata](https://docs.djangoproject.com/en/4.2/ref/django-admin/#loaddata)

```cmd
python manage.py loaddata db.json
```

請執行以下指令匯入 demo 資料

```cmd
python3 manage.py makemigrations musics
python3 manage.py migrate
python3 manage.py loaddata db.json
```

## Django ORM

先介紹 `Q` 這個東西, 這個的目的主要是處理更複雜的邏輯運算

```cmd
>>> from django.db.models import Q
>>> # 透過 Q 建立查詢條件
>>> condition1 = Q(song__icontains="test")
>>> condition2 = Q(created__gte="2023-01-01")
>>> condition3 = Q(count=3)
>>> # 查詢 song 包含 "test" 並且 created 大於等於 2023-01-01 或者 count 等於 3
>>> combined_condition = condition1 & condition2 | condition3
>>> Music.objects.filter(combined_condition)
```

介紹 `F` 這個東西, 他是針對特定的 fields 進行操作

```cmd
>>> from musics.models import Music
>>> from django.db.models import F, Value
>>> from django.db.models.functions import Concat
>>> # 將全部的 song 字段 加上 "_data"
>>> Music.objects.update(song=Concat(F('song'),Value('_data')))
3

>>> # 將全部的 count 字段 加上 100
>>> Music.objects.update(count=F('count')+ 100)
3
```

介紹 `query.select_for_update()` 官網 可參考 [select-for-update](https://docs.djangoproject.com/en/4.2/ref/models/querysets/#select-for-update)


`SELECT ... FOR UPDATE`

```python
>>> from musics.models import Music
>>> from django.db import transaction
>>> with transaction.atomic():
...     Music.objects.select_for_update().get(id=2)
...
SELECT "music"."id",
       "music"."song",
       "music"."singer",
       "music"."count",
       "music"."last_modify_date",
       "music"."created",
       "music"."sheet_id"
  FROM "music"
 WHERE "music"."id" = 2
 LIMIT 21
   FOR UPDATE
```

`SELECT ... FOR UPDATE SKIP LOCKED`

```python
>>> from musics.models import Music
>>> from django.db import transaction
>>> with transaction.atomic():
...     Music.objects.select_for_update(skip_locked=True).get(id=2)
...
SELECT "music"."id",
       "music"."song",
       "music"."singer",
       "music"."count",
       "music"."last_modify_date",
       "music"."created",
       "music"."sheet_id"
  FROM "music"
 WHERE "music"."id" = 2
 LIMIT 21
   FOR UPDATE SKIP LOCKED
```

更多資訊可參考我之前介紹的 [Postgresql Lock FOR UPDATE](https://github.com/twtrubiks/postgresql-note/tree/main/pg-lock-tutorial#for-update)

`values`

只回傳特定 fields 的值(dict), 而不是回傳整個 model.

```text
Returns a QuerySet that returns dictionaries, rather than model instances, when used as an iterable.
```

官網可參考 [values](https://docs.djangoproject.com/en/4.2/ref/models/querysets/#values)

```cmd
>>> from musics.models import Music
>>> Music.objects.filter(id=2).values('id', 'song')
<QuerySet [{'id': 2, 'song': 'test_data'}]>
```

`values-list`

類似 values, 但回傳 tuples.

```text
This is similar to values() except that instead of returning dictionaries, it returns tuples when iterated over.
```

官網可參考 [values-list](https://docs.djangoproject.com/en/4.2/ref/models/querysets/#values-list)

```cmd
>>> from musics.models import Music
>>> Music.objects.filter(id=2).values_list('id', 'song')
<QuerySet [(2, 'test_data')]>
```

`aggregate`

直接把他想成就是 聚合函數,

官網可參考 [aggregation](https://docs.djangoproject.com/en/4.2/topics/db/aggregation/) (值得花時間看看)

```cmd
>>> from musics.models import Music
>>> from django.db.models import Avg, Sum
>>> Music.objects.aggregate(sum_count=Sum('count'))
SELECT SUM("music"."count") AS "sum_count"
  FROM "music"
Execution time: 0.000510s [Database: default]
{'sum_count': 6}

>>> Music.objects.all().aggregate(avg_count=Avg('count'))
SELECT AVG("music"."count") AS "avg_count"
  FROM "music"
Execution time: 0.000367s [Database: default]
{'avg_count': 2.0}
```

`annotate`

更進階一點, 把他想成是 group by

```cmd
>>> from musics.models import Music, Sheet
>>> from django.db.models import Avg, Sum, Count

>>> # 計算出每個 sheet 底下有多少個 music
>>> Sheet.objects.annotate(num_music=Count("music"))
SELECT "musics_sheet"."id",
       "musics_sheet"."name",
       COUNT("music"."id") AS "num_music"
  FROM "musics_sheet"
  LEFT OUTER JOIN "music"
    ON ("musics_sheet"."id" = "music"."sheet_id")
 GROUP BY "musics_sheet"."id"
 LIMIT 21

>>> # 如果想要排序, 可以再加上 order_by
>>> Sheet.objects.annotate(num_music=Count("music")).order_by("-num_music")
SELECT "musics_sheet"."id",
       "musics_sheet"."name",
       COUNT("music"."id") AS "num_music"
  FROM "musics_sheet"
  LEFT OUTER JOIN "music"
    ON ("musics_sheet"."id" = "music"."sheet_id")
 GROUP BY "musics_sheet"."id"
 ORDER BY 3 DESC
 LIMIT 21


>>> # 依照 song 進行 group by, 並且針對 count 進行 sum 運算
>>> Music.objects.values('song').annotate(sum_count=Sum('count'))
SELECT "music"."song",
       SUM("music"."count") AS "sum_count"
  FROM "music"
 GROUP BY "music"."song"
 LIMIT 21
Execution time: 0.000687s [Database: default]
<QuerySet [{'song': 'test', 'sum_count': 2}, {'song': 'song', 'sum_count': 4}]>
```

`conditional-expressions`

在資料庫中的 When Case, django 也可以使用

官網可參考 [conditional-expressions](https://docs.djangoproject.com/en/4.2/ref/models/conditional-expressions/)

```cmd
>>> from musics.models import Music
>>> from django.db.models import Case, When, Value
>>> Music.objects.annotate(
...      my_data=Case(
...          When(count=1, then=Value("5%")),
...          When(count=2, then=Value("10%")),
...          default=Value("0%")
...       )
...     ).values_list("id", "my_data")
SELECT "music"."id",
       CASE WHEN "music"."count" = 1 THEN '5%'
            WHEN "music"."count" = 2 THEN '10%'
            ELSE '0%'
             END AS "my_data"
  FROM "music"
 LIMIT 21
Execution time: 0.000468s [Database: default]
<QuerySet [(1, '5%'), (2, '10%'), (3, '0%')]>
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

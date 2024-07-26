# django-orm-tutorial

使用 djagno `5.0.6` 加上透過 `django-extensions` 觀察 ORM 實際 SQL,

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

官網可參考 [dumpdata](https://docs.djangoproject.com/en/5.0/ref/django-admin/#dumpdata)

```cmd
python manage.py dumpdata > db.json
```

也可以指定匯出的個格式, 例如匯出 yaml

```cmd
python3 manage.py dumpdata musics --format yaml > db.yaml
```

匯出特定的 table

```cmd
python3 manage.py dumpdata musics > db.json
```

- 匯入

官網可參考 [loaddata](https://docs.djangoproject.com/en/5.0/ref/django-admin/#loaddata)

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

更多 django orm 的用法可參考 [querysets](https://docs.djangoproject.com/en/5.0/ref/models/querysets/)

先介紹 `Q` 這個東西, 這個的目的主要是處理更複雜的邏輯運算

可參考 [Complex lookups with Q objects](https://docs.djangoproject.com/en/5.0/topics/db/queries/#complex-lookups-with-q-objects)

```python
>>> from django.db.models import Q
>>> # 透過 Q 建立查詢條件
>>> condition1 = Q(song__icontains="test")
>>> condition2 = Q(created__gte="2023-01-01")
>>> condition3 = Q(count=3)
>>> # 查詢 song 包含 "test" 並且 created 大於等於 2023-01-01 或者 count 等於 3
>>> combined_condition = condition1 & condition2 | condition3
>>> Music.objects.filter(combined_condition)

SELECT "music"."id",
       "music"."song",
       "music"."singer",
       "music"."count",
       "music"."last_modify_date",
       "music"."created",
       "music"."sheet_id",
       "music"."localization"
  FROM "music"
 WHERE ((UPPER("music"."song"::text) LIKE UPPER('%test%') AND "music"."created" >= '2023-01-01T00:00:00+00:00'::timestamptz) OR "music"."count" = 3)

<QuerySet [<Music: Music object (2)>, <Music: Music object (3)>]>
```

Q objects can be negated using the `~` operator, 也就是 not 的意思

```python
>>> from django.db.models import Q
>>> Music.objects.filter(~Q(count=3)).values('id')
SELECT "music"."id"
  FROM "music"
 WHERE NOT ("music"."count" = 3 AND "music"."count" IS NOT NULL)

<QuerySet [{'id': 1}, {'id': 2}, {'id': 4}]>
```

介紹 `F` 這個東西, 他是針對特定的 fields 進行操作

```python
>>> from musics.models import Music
>>> from django.db.models import F, Value
>>> from django.db.models.functions import Concat
>>> # 將全部的 song 字段 加上 "_data"
>>> Music.objects.update(song=Concat(F('song'),Value('_data')))
UPDATE "music"
   SET "song" = COALESCE("music"."song", '') || COALESCE('_data', '')
3

>>> # 將全部的 count 字段 加上 100
>>> Music.objects.update(count=F('count')+ 100)
UPDATE "music"
   SET "count" = ("music"."count" + 100)
3
```

介紹 [ArrayField](https://docs.djangoproject.com/en/5.0/ref/contrib/postgres/fields/#arrayfield)

假如想要過濾 tags, 有包含 0 或 7 或 3

範例資料如下

```sql
postgres=# SELECT * FROM public.music_tag;
 id |  tags   | music_id
----+---------+----------
  1 | {2,3}   |        4
  2 | {4,5,6} |        3
  3 | {7,8}   |        2
  4 | {0}     |        1
(4 rows)
```

看一下 table, 主要是看 tags, 它的 type 是 text[]

```python
postgres=# \d public.music_tag;
                          Table "public.music_tag"
  Column  |  Type  | Collation | Nullable |             Default
----------+--------+-----------+----------+----------------------------------
 id       | bigint |           | not null | generated by default as identity
 tags     | text[] |           | not null |
 music_id | bigint |           | not null |
```

可以使用 [overlap](https://docs.djangoproject.com/en/5.0/ref/contrib/postgres/fields/#overlap) (Uses the SQL operator `&&`)

```python
Music.objects.filter(musictag__tags__overlap=['7', '0', '3'])
<QuerySet [<Music: Music object (4)>, <Music: Music object (2)>, <Music: Music object (1)>]>
```

介紹 [JSONField](https://docs.djangoproject.com/en/5.0/ref/models/fields/#jsonfield)

範例資料如下

```sql
postgres=# SELECT * FROM public.music;
 id | song | singer | count |      last_modify_date      |          created           | sheet_id |    localization
----+------+--------+-------+----------------------------+----------------------------+----------+--------------------
  4 | data | test   |     0 | 2023-10-07 04:41:00.204+00 | 2023-10-07 03:41:00.204+00 |        3 | {"zh_tw": "data"}
  3 | song | AKB48  |     3 | 2023-10-07 03:41:00.204+00 | 2023-10-07 03:41:00.204+00 |        1 | {"zh_tw": "test"}
  2 | test | AKB48  |     2 | 2023-10-07 03:40:55.581+00 | 2023-10-07 03:40:55.581+00 |        1 | {"es_US": "test2"}
  1 | song | AKB48  |     1 | 2023-10-07 03:40:42.256+00 | 2023-10-07 03:40:42.256+00 |        1 | {"zh_hk": "bbb"}
(4 rows)
```

看一下 table, 主要是看 localization, 它的 type 是 jsonb

```python
postgres=# \d public.music;
                                         Table "public.music"
      Column      |           Type           | Collation | Nullable |             Default
------------------+--------------------------+-----------+----------+----------------------------------
 id               | bigint                   |           | not null | generated by default as identity
 song             | text                     |           | not null |
 singer           | text                     |           | not null |
 count            | integer                  |           |          |
 last_modify_date | timestamp with time zone |           | not null |
 created          | timestamp with time zone |           | not null |
 sheet_id         | bigint                   |           |          |
 localization     | jsonb                    |           |          |
```

```python
# 找出 localization 的 zh_tw value 為 data
Music.objects.filter(localization__zh_tw__icontains='data')
<QuerySet [<Music: Music object (4)>]>

# 找出 localization 的 key 是 zh_tw
Music.objects.filter(localization__has_key='zh_tw')
<QuerySet [<Music: Music object (4)>, <Music: Music object (3)>]>

# 找出 localization 的 key 是 es_US or zh_hk
Music.objects.filter(localization__has_any_keys=['es_US', 'zh_hk'])
<QuerySet [<Music: Music object (2)>, <Music: Music object (1)>]>
```

介紹 `query.select_for_update()` 官網 可參考 [select-for-update](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#select-for-update)


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

官網可參考 [values](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#values)

```python
>>> from musics.models import Music
>>> Music.objects.filter(id=2).values('id', 'song')
<QuerySet [{'id': 2, 'song': 'test_data'}]>
```

`values-list`

類似 values, 但回傳 tuples.

```text
This is similar to values() except that instead of returning dictionaries, it returns tuples when iterated over.
```

官網可參考 [values-list](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#values-list)

```python
>>> from musics.models import Music
>>> Music.objects.filter(id=2).values_list('id', 'song')
<QuerySet [(2, 'test_data')]>

>>> # 也可以取 ForeignKey 的資料
>>> Music.objects.filter(id=2).values_list('id', 'song', 'sheet__name')
<QuerySet [(2, 'test', 'sheet_1')]>

>>> Music.objects.filter(id=2).values_list('id', flat=True)
<QuerySet [2]>

# there is more than one field
>>> Music.objects.filter(id=2).values_list('id', 'song', named=True)
<QuerySet [Row(id=2, song='test_data')]>
```

`exists`

官網可參考 [exists](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#django.db.models.query.QuerySet.exists)

```python
>>> from musics.models import Music
>>> Music.objects.filter(id=2).exists()
SELECT 1 AS "a"
  FROM "music"
 WHERE "music"."id" = 2
 LIMIT 1

True
```

`only`

只使用選擇的字段.

官網可參考 [only](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#only)

```python
>>> from musics.models import Music
>>> Music.objects.only('song')
SELECT "music"."id",
       "music"."song"
  FROM "music"
 LIMIT 21

>>> # 注意順序性, 只有最後的會生效
>>> Music.objects.only('song', 'singer').only('count')
SELECT "music"."id",
       "music"."count"
  FROM "music"
 LIMIT 21
```

`defer`

和 only 相反, 排除選擇的字段

官網可參考 [defer](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#defer)

```python
>>> from musics.models import Music
>>> # 排除 'song', 'singer', 'created'
>>> Music.objects.defer('song', 'singer', 'created')
SELECT "music"."id",
       "music"."count",
       "music"."last_modify_date",
       "music"."sheet_id",
       "music"."localization"
  FROM "music"
 LIMIT 21
```

`reverse`

官網可參考 [reverse](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#reverse)

這個我覺的沒什麼用, 因為直接使用 `order_by("id")` `order_by("-id")` 控制就可以了.

```python
>>> from musics.models import Music
>>> # 需要搭配 orderby
>>> Music.objects.all().only("singer").order_by("id")
SELECT "music"."id",
       "music"."singer"
  FROM "music"
 ORDER BY "music"."id" ASC

>>> Music.objects.all().only("singer").order_by("id").reverse()
SELECT "music"."id",
       "music"."singer"
  FROM "music"
 ORDER BY "music"."id" DESC
```

`latest` `earliest`

存在的目的只是為了可讀性.

官網可參考 [latest](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#latest)

官網可參考 [earliest](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#earliest)

```python
>>> from musics.models import Music
>>> Music.objects.filter(created__isnull=False).latest("singer")
SELECT "music"."id",
       "music"."song",
       "music"."singer",
       "music"."count",
       "music"."last_modify_date",
       "music"."created",
       "music"."sheet_id",
       "music"."localization"
  FROM "music"
 WHERE "music"."created" IS NOT NULL
 ORDER BY "music"."singer" DESC
 LIMIT 1

>>> Music.objects.filter(created__isnull=False).earliest("singer")
SELECT "music"."id",
       "music"."song",
       "music"."singer",
       "music"."count",
       "music"."last_modify_date",
       "music"."created",
       "music"."sheet_id",
       "music"."localization"
  FROM "music"
 WHERE "music"."created" IS NOT NULL
 ORDER BY "music"."singer" ASC
 LIMIT 1
```


`explain`

可以看 execution plan

官網可參考 [explain](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#explain)

```python
>>> from musics.models import Music
>>> Music.objects.only('id', 'singer').filter(created__isnull=False).explain()
EXPLAIN SELECT "music"."id",
       "music"."singer"
  FROM "music"
 WHERE "music"."created" IS NOT NULL
'Seq Scan on music  (cost=0.00..15.10 rows=507 width=40)\n  Filter: (created IS NOT NULL)'

>>> Music.objects.only('id', 'singer').filter(pk=2).explain()
EXPLAIN SELECT "music"."id",
       "music"."singer"
  FROM "music"
 WHERE "music"."id" = 2

'Index Scan using music_pkey on music  (cost=0.15..8.17 rows=1 width=40)\n  Index Cond: (id = 2)'
```

`exact`

Exact match. 忽略大小寫可使用 `iexact`

官網可參考 [exact](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#exact)

```python
>>> from musics.models import Music

>>> Music.objects.filter(id__exact=1).values('id')
SELECT "music"."id"
  FROM "music"
 WHERE "music"."id" = 1

<QuerySet [{'id': 1}]>


>>> Music.objects.filter(song__exact=None).values('id')
SELECT "music"."id"
  FROM "music"
 WHERE "music"."song" IS NULL

<QuerySet []>

>>> Music.objects.filter(song__exact="").values('id')
SELECT "music"."id"
  FROM "music"
 WHERE "music"."song" = ''

<QuerySet []>
```

其實這個語法和底下的語法所產生的 SQL 是一樣的,

```python
Music.objects.filter(song="").values('id')
```

`distinct`

官網可參考 [distinct](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#distinct)

```python
>>> from musics.models import Music
>>> Music.objects.distinct("count").values_list('id')
SELECT DISTINCT
    ON ("music"."count") "music"."id"
  FROM "music"

<QuerySet [(4,), (1,), (2,), (3,)]>
```

如果搭配 order_by 要稍微注意一下

```python
>>> from musics.models import Music
>>> Music.objects.order_by("count").distinct("count").values_list('id')
SELECT DISTINCT
    ON ("music"."count") "music"."id"
  FROM "music"
 ORDER BY "music"."count" ASC

<QuerySet [(2,)]>
```

如果 distinct 的欄位沒有在 order_by 中會錯誤 😱, 如下

```python
>>> from musics.models import Music
>>> Music.objects.order_by("id").distinct("count").values_list('id')
django.db.utils.ProgrammingError: SELECT DISTINCT ON expressions must match initial ORDER BY expressions
```

`exclude`

官網可參考 [exclude](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#exclude)

```python
>>> from musics.models import Music
>>> Music.objects.exclude(singer="test").values_list('id')

SELECT "music"."id"
  FROM "music"
 WHERE NOT ("music"."singer" = 'test')

<QuerySet [(1,), (2,), (3,)]>
```

`contains`

官網可參考 [contains](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#contains)

```python
>>> Music.objects.filter(song__contains='on').values_list('id', 'song')
SELECT "music"."id",
       "music"."song"
  FROM "music"
 WHERE "music"."song"::text LIKE '%on%'

<QuerySet [(3, 'song'), (1, 'song')]>
```

`icontaons`

Case-insensitive 忽略大小寫

官網可參考 [icontaons](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#contains)

```python
>>> Music.objects.filter(song__icontains='on').values_list('id', 'song')
SELECT "music"."id",
       "music"."song"
  FROM "music"
 WHERE UPPER("music"."song"::text) LIKE UPPER('%on%')

<QuerySet [(3, 'song'), (1, 'song')]>
```

假如我想要同時找出 song 有包含 "on" 或是 "es" 的, 必須搭配 `Q`

```python
>>> from django.db.models import Q
>>> Music.objects.filter(Q(song__icontains='on') | Q(song__icontains='es'))
SELECT "music"."id",
       "music"."song",
       "music"."singer",
       "music"."count",
       "music"."last_modify_date",
       "music"."created",
       "music"."sheet_id",
       "music"."localization"
  FROM "music"
 WHERE (UPPER("music"."song"::text) LIKE UPPER('%on%') OR UPPER("music"."song"::text) LIKE UPPER('%es%'))

<QuerySet [<Music: Music object (3)>, <Music: Music object (2)>, <Music: Music object (1)>]>
```

`startswith`

官網可參考 [startswith](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#startswith)

```python
>>> Music.objects.filter(song__startswith='te').values_list('id', 'song')
SELECT "music"."id",
       "music"."song"
  FROM "music"
 WHERE "music"."song"::text LIKE 'te%'

<QuerySet [(2, 'test')]>
```

`endswith`

官網可參考 [endswith](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#endswith)

```python
>>> Music.objects.filter(song__endswith='t').values_list('id', 'song')
SELECT "music"."id",
       "music"."song"
  FROM "music"
 WHERE "music"."song"::text LIKE '%t'

<QuerySet [(2, 'test')]>
```

`date`

官網可參考 [date](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#date)

```python
>>> from datetime import datetime, date
>>> Music.objects.filter(last_modify_date__date=date(2023, 10, 7)).values_list('id', 'song')
SELECT "music"."id",
       "music"."song"
  FROM "music"
 WHERE ("music"."last_modify_date" AT TIME ZONE 'UTC')::date = '2023-10-07'::date

<QuerySet [(4, 'data'), (3, 'song'), (2, 'test'), (1, 'song')]>
```

`range`

官網可參考 [range](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#range)

```python
>>> from datetime import datetime, date
>>> start_date = date(2023, 1, 1)
>>> end_date = date(2023, 12, 31)
>>> Music.objects.filter(last_modify_date__range=(start_date, end_date)).values_list('id', 'song')
SELECT "music"."id",
       "music"."song"
  FROM "music"
 WHERE "music"."last_modify_date" BETWEEN '2023-01-01T00:00:00+00:00'::timestamptz AND '2023-12-31T00:00:00+00:00'::timestamptz

<QuerySet [(4, 'data'), (3, 'song'), (2, 'test'), (1, 'song')]>
```

`isnull`

官網可參考 [isnull](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#isnull)

```python
>>> Music.objects.filter(sheet__isnull=True).values_list('id', 'song')
SELECT "music"."id",
       "music"."song"
  FROM "music"
 WHERE "music"."sheet_id" IS NULL

<QuerySet []>
```

`aggregate`

直接把他想成就是 聚合函數,

官網可參考 [aggregation](https://docs.djangoproject.com/en/5.0/topics/db/aggregation/) (值得花時間看看)

```python
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

原理一樣是使用 group by, 但是它強大的地方在於, 可以在原本的 model 上增加新的字段,

```python
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

>>> sheet = Sheet.objects.annotate(num_music=Count("music"))
>>> sheet[0].num_music # 可以使用計算出來的字段
>>> sheet.filter(num_music__gt=1) # 甚至可以使用 ORM 來過濾自定義的字段

>>> # 來看一下 SQL, 其實就是用 HAVING
>>> Sheet.objects.annotate(num_music=Count("music")).filter(num_music__gt=1)
SELECT "tutorial_sheet"."id",
       "tutorial_sheet"."name",
       COUNT("music"."id") AS "num_music"
  FROM "tutorial_sheet"
  LEFT OUTER JOIN "music"
    ON ("tutorial_sheet"."id" = "music"."sheet_id")
 GROUP BY "tutorial_sheet"."id"
HAVING COUNT("music"."id") > 1
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

官網可參考 [conditional-expressions](https://docs.djangoproject.com/en/5.0/ref/models/conditional-expressions/)

```python
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

`bulk-create`

[bulk-create](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#bulk-create)

```python
from musics.models import Music
Music.objects.bulk_create([
    Music(song="song11", singer="singer11"),
    Music(song="song22", singer="singer22"),
])
```

對應的原生 sql 如下,

```sql
INSERT INTO "music" ("song", "singer", "count", "last_modify_date", "created", "sheet_id")
VALUES ('song11', 'singer11', NULL, '2024-04-09 12:04:46.046720', '2024-04-09 12:04:46.046765', NULL), ('song22', 'singer22', NULL, '2024-04-09 12:04:46.046796', '2024-04-09 12:04:46.046811', NULL)
```

還有一個 batch_size 可以使用, 用來完成批次(一次最多新增幾比).

例如

```python
Music.objects.bulk_create([
    Music(song="song11", singer="singer11"),
    Music(song="song22", singer="singer22"),
    Music(song="song33", singer="singer33"),
    Music(song="song44", singer="singer44"),
], 2)
```

如果你看原生 SQL 你會發現執行了兩個 INSERT INTO.

`bulk-update`

[bulk-update](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#bulk-update)

```python
from musics.models import Music
musics = []
for index, music in enumerate(Music.objects.all()):
    music.song = f"song_{index}"
    musics.append(music)

bulk_update_count = Music.objects.bulk_update(musics, ['song'])
```

bulk_update_count 會回傳更新的比數.

對應的原生 sql 如下,

```sql
UPDATE "music"
   SET "song" =
      CASE WHEN ("music"."id" = 1) THEN 'song_0'
           WHEN ("music"."id" = 2) THEN 'song_1'
      ELSE NULL
      END
 WHERE "music"."id" IN (1, 2)
```

`get_or_create`

[get_or_create](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#get-or-create)

如果有符合的資料且只有一比就回傳, 沒有的話就建立.

```python
from musics.models import Music
obj, created = Music.objects.get_or_create(song="song113")
```

obj 會回傳物件, created 則會回傳是否有建立.

為了避免 concurrent requests 的錯誤, 透過 get_or_create 會更好,

如果今天多比被找到, 會跳出 raises MultipleObjectsReturned.

`update_or_create`

[update_or_create](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#get-or-create)


```python
from musics.models import Music
obj, created = Music.objects.update_or_create(
    song="song113",
    defaults={"song": "song_default"},
)
```

obj 會回傳物件, created 則會回傳是否有建立.

如果找到 song 為 song113, 就將找到的單比的 song 更新為 song_default,

如果沒找到, 就用 create_defaults 裡面的內容建立,

如果今天多比被找到, 會跳出 raises MultipleObjectsReturned.

`in-bulk`

[in-bulk](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#in-bulk)

```python
from musics.models import Music
Music.objects.in_bulk([1, 2])
# {1: <Music: Music object (1)>, 2: <Music: Music object (2)>}

# 如果沒有指定, 會找出全部的
Music.objects.in_bulk()
```

`Func() expressions`

使用 database functions like COALESCE and LOWER

[Func() expressions](https://docs.djangoproject.com/en/5.0/ref/models/expressions/#func-expressions)

範例, 將字串改成大寫,

```python
>>> from django.db.models import Func
>>> from musics.models import Music
>>> class Upper(Func):
...     function = "UPPER"
...

>>> Music.objects.annotate(song_upper=Upper("song")).values_list("id", "song_upper", "song")
SELECT "music"."id",
       "music"."song",
       UPPER("music"."song") AS "song_upper"
  FROM "music"

<QuerySet [(4, 'DATA', 'data'), (3, 'SONG', 'song'), (2, 'TEST', 'test'), (1, 'SONG', 'song')]>
```

範例, 將 array 全部展開,

```python
>>> from django.db.models import Func, CharField
>>> from musics.models import MusicTag
>>> class Unnest(Func):
...     function = "unnest"
...     output_field = CharField()
...

>>> MusicTag.objects.annotate(tag_name=Unnest("tags")).values_list("id", "tag_name", "tags")
SELECT "music_tag"."id",
       "music_tag"."tags",
       unnest("music_tag"."tags") AS "tag_name"
  FROM "music_tag"

<QuerySet [(1, '2', ['2', '3']), (1, '3', ['2', '3']), (2, '4', ['4', '5', '6']), (2, '5', ['4', '5', '6']), (2, '6', ['4', '5', '6']), (3, '7', ['7', '8']), (3, '8', ['7', '8']), (4, '0', ['0'])]>
```

`custom lookups`

[How to write custom lookups](https://docs.djangoproject.com/en/5.0/howto/custom-lookups/)

自己定義 lookups, 可參考 [models.py](https://github.com/twtrubiks/django-tutorial/blob/django4_and_orm/musics/models.py#L44)

```python
@Field.register_lookup
class NotEqual(Lookup):
    lookup_name = "ne"

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return "%s <> %s" % (lhs, rhs), params
```

如果想要 debug `as_sql` 裡面的東西, 要觸發這個中斷點請使用以下指令,

這樣你就可以看出它組出什麼字串.

```python
print(Music.objects.filter(song__ne='test').query)
```

經過上面這樣的定義, 可以使用自己定義的 `ne`,

`<> 'test'` 在 SQL 中的意思是不等於 test 的意思

```python
>>> Music.objects.filter(song__ne='test').values_list("song")
SELECT "music"."song"
  FROM "music"
 WHERE "music"."song" <> 'test'

<QuerySet [('data',), ('song',), ('song',)]>
```

## Performing raw SQL queries

官網可參考 [Performing raw SQL queries](https://docs.djangoproject.com/en/5.0/topics/db/sql/)

```python
>>> result = Music.objects.raw('SELECT * FROM music where song ilike %s', [f"%song%"])
>>> [(rec.id, rec.song) for rec in result]
[(3, 'song'), (1, 'song')]
```

## 執行環境

* Python 3.10.12

## Reference

* [Django](https://www.djangoproject.com/)

## Donation

文章都是我自己研究內化後原創，如果有幫助到您，也想鼓勵我的話，歡迎請我喝一杯咖啡:laughing:

![alt tag](https://i.imgur.com/LRct9xa.png)

[贊助者付款](https://payment.opay.tw/Broadcaster/Donate/9E47FDEF85ABE383A0F5FC6A218606F8)

## License

MIT license

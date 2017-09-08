# django-tutorial

 Django 基本教學 - 從無到有 Django-Beginners-Guide， 教你建立自己的第一個 [Django](https://github.com/django/django) 程式 📝

* [Youtube Tutorial PART 1](https://youtu.be/tB3kwu2E0GM)
* [Youtube Tutorial PART 2](https://youtu.be/2LP5WvhXLUM)

[Django](https://github.com/django/django)  非常強大，尤其是 [Django REST framework](http://www.django-rest-framework.org/) ( DRF )，打造 REST API 極為方便快速，

在這裡先帶大家進入 [Django](https://github.com/django/django) 的世界  :smile:

## 教學

請先確認電腦有安裝 [Python](https://www.python.org/)

接著我們安裝 [Django](https://github.com/django/django)

請在你的命令提示字元 (cmd ) 底下輸入

>pip install django

基本上安裝應該沒什麼問題，可以再使用 cmd 確認，如下圖

![alt tag](http://i.imgur.com/O0esVe9.jpg)

### 建立 Django Project

建議直接安裝 [PyCharm](https://www.jetbrains.com/pycharm/) ，然後新增一個 Django Project

![alt tag](http://i.imgur.com/ZVOUmVb.jpg)

用 [PyCharm](https://www.jetbrains.com/pycharm/) 建立 project 還有一個好處，就是一些設定會先幚你設定好，不用全部重新自己動手設設定。

### 執行 Django

直接點選 [PyCharm](https://www.jetbrains.com/pycharm/) 右上角執行程式 ( 一個是Debug模式 )，如下圖

![alt tag](http://i.imgur.com/CWDVlnj.jpg)

正常來說，如果沒有任何錯誤，去瀏覽 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  可以看到下圖，

![alt tag](http://i.imgur.com/qhgX4Tz.jpg)

如果你沒有安裝 [PyCharm](https://www.jetbrains.com/pycharm/) 或你喜歡下指令，就必須在命令提示字元 (cmd ) 底下輸入

>python manage.py runserver

![alt tag](http://i.imgur.com/PxvPJ9m.jpg)

恭喜你~   成功第一步了   :smile:

### 建立 Django App

先建立一個觀念，在 [Django](https://github.com/django/django) 中，通常我們會依照 **功能** 去建議一個 App ， 例如範例的 musics ，代表他是 管理音樂 的部份。

有了這個觀念之後，我們動手開始做吧～

請在你的命令提示字元 (cmd ) 底下輸入

>python manage.py startapp musics

如果順利執行，你會發現你的專案內多出一個 musics 資料夾

![alt tag](http://i.imgur.com/nn5YY8A.jpg)

***建立完請記得要將 App 加入設定檔***

請在 settings.py 裡面的 **INSTALLED_APPS** 加入 musics (也就是你自己建立的 App 名稱)

![alt tag](http://i.imgur.com/LCPHObL.jpg)

### Views

請先在 **templates** 裡面新增一個  **hello_django.html**，並在裡面輸入下方程式碼 (下圖)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    {{data}}
</body>
</html>
```

![alt tag](http://i.imgur.com/ULHqOBH.jpg)

hello_django.html 裡面的第 8 行，只是透過  views.py 傳值過來而已。

關於第 8 行 的用法，更多可以參考 [Django Templates](https://docs.djangoproject.com/en/1.10/ref/templates/)。

接著我們將 views.py 裡面新增下方程式碼  (下圖)

```python
from django.shortcuts import render


# Create your views here.
def hello_view(request):
    return render(request, 'hello_django.html', {
        'data': "Hello Django ",
    })

```

![alt tag](http://i.imgur.com/obbdTH4.jpg)

 views.py 裡面的第 7 行，就是回傳給 hello_django.html 的資料。

 注意，最後還必須設定 URLconf。

### URLconf

請再將 urls.py 裡面增加一些程式碼，如下圖

```python
from django.conf.urls import url
from django.contrib import admin
from musics.views import hello_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^hello/', hello_view),
]

```

![alt tag](http://i.imgur.com/YOjwZyE.jpg)

簡單講，就是將 views.py import 進來 (第 18 行)，

並且設定他的 URL (第 22 行)

最後執行 Django ， 然後瀏覽  [http://127.0.0.1:8000/hello/](http://127.0.0.1:8000/hello/)

你應該會看到如下圖

![alt tag](http://i.imgur.com/Wd79870.jpg)

接下來我們來看 Models

### Models

定義出資料庫中的結構（schema），並且透過 Django 中的指令去建立資料庫。

[Django](https://github.com/django/django) 預設是使用 [SQLite](https://www.sqlite.org/) ，如果想要修改為其他的資料庫，可以在 settings.py  裡面進行修改。

首先，請先在 models.py 裡面增加下方程式碼 (下圖)

```python
from django.db import models


# Create your models here.
class Music(models.Model):
    song = models.TextField(default="song")
    singer = models.TextField(default="AKB48")
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "music"

```

default : 代表默認值，也就是如果你沒有指定的話會用默認值。

auto_now_add : 新增時會幚你自動加上建立時間。

auto_now : 資料有更新時會幚你自動加上更新的時間。

更多可以參考 [Django fields](https://docs.djangoproject.com/en/1.10/ref/models/fields/)

![alt tag](http://i.imgur.com/cyjgYp5.jpg)

接著在命令提示字元 (cmd ) 底下輸入

>python manage.py makemigrations

![alt tag](http://i.imgur.com/mmqLn9F.jpg)

> python manage.py migrate

![alt tag](http://i.imgur.com/8sCX6x6.jpg)

makemigrations ： 會幚你建立一個檔案，去記錄你更新了哪些東西。

migrate ： 根據 makemigrations 建立的檔案，去更新你的 DATABASE 。

執行完上面的指令之後，

你可以使用[SQLiteBrowser](http://sqlitebrowser.org/) 或  [PyCharm](https://www.jetbrains.com/pycharm/) 觀看 DATABASE，

你會發現多出一個 **music** 的 table ( 如下圖 )

![alt tag](http://i.imgur.com/xVbTtjq.jpg)

有沒有注意到我們明明在 models.py 裡面就沒有輸入 id ，可是 database 裡面卻有 id 欄位，

這是因為 Django 預設會幫你帶入，所以可以不用設定。

### Django ORM

先了解什麼是 CRUD ，他分別代表 Create, Retrieve, Update, Delete，

[Django QuerySet API](https://docs.djangoproject.com/en/1.10/ref/models/querysets/) 可以讓你簡單的處理 CRUD 。

直接使用 Python Console 簡單介紹 Django ORM

![alt tag](http://i.imgur.com/JuBjDPR.jpg)

記得必須先 import 你的 models

> from musics.models import Music

![alt tag](http://i.imgur.com/Bog2YmN.jpg)

#### Create

![alt tag](http://i.imgur.com/mPwY3o7.jpg)

> Music.objects.create(song='song1', singer='SKE48')

用[SQLiteBrowser](http://sqlitebrowser.org/) 或  [PyCharm](https://www.jetbrains.com/pycharm/) 觀看 DATABASE，如下圖，成功多了一比資料
![alt tag](http://i.imgur.com/aemyLiy.jpg)

或者

> Music.objects.create()

![alt tag](http://i.imgur.com/VHQs5ts.jpg)

為什麼沒帶參數也可以新增呢?

這是因為 models.py 裡的 song 以及 singer 有設定 default ，所以可以不用帶入參數。

#### Read

> Music.objects.all()

![alt tag](http://i.imgur.com/WTSzn2U.jpg)

> Music.objects.get(pk=3)

![alt tag](http://i.imgur.com/QACYB8x.jpg)
> Music.objects.filter(id=1)

![alt tag](http://i.imgur.com/jFCM1op.jpg)

#### Update

> data=Music.objects.filter(id=1)
>
> data.update(song='song_update')

![alt tag](http://i.imgur.com/Dk1rsv3.jpg)

執行完上述程式碼，就會發現資料被更新了 ( 如下圖 )

![alt tag](http://i.imgur.com/OJT2UAT.jpg)

#### Delete

> data=Music.objects.filter(id=4)
>
> data.delete()

![alt tag](http://i.imgur.com/shWLKwn.jpg)

執行完上述程式碼，就會發現資料被刪除了

### Admin Site

[Django](https://github.com/django/django) 內建有後台管理介面。

請先確定 settings.py 裡的 INSTALLED_APPS 裡有 django.contrib.admin

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    ......
]

```

![alt tag](http://i.imgur.com/y3lw5P7.jpg)

設定 URL

![alt tag](http://i.imgur.com/FIfOnls.jpg)

接著使用命令提示字元 (cmd ) 建立超級使用者

>python manage.py createsuperuser

![alt tag](http://i.imgur.com/wqacaCR.jpg)

#### 註冊 model

我們可以註冊 model，讓後台可以操作 database

請在 admin.py 裡面新增下方程式碼，這段程式碼只是去註冊 model 而已

```python
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from musics.models import Music

admin.site.register(Music)

```

![alt tag](http://i.imgur.com/A8k8rQc.jpg)

接著執行 Django ，然後到  [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)，

應該會看到下圖，我的 帳號/密碼 設定為 twtrubiks/password123

![alt tag](http://i.imgur.com/vFrjyzs.jpg)

現在，你可以在裡面對 Musics 執行 新增、查詢、修改、刪除 (CRUD)，也可以管理使用者。

![alt tag](http://i.imgur.com/DYrJBgk.jpg)

#### Model Field.choices

因為蠻實用的，所以加入 Model Field.choices ，使用方法可參考 [models.py](https://github.com/twtrubiks/django-tutorial/blob/master/musics/models.py)  以及 [hello_django.html](https://github.com/twtrubiks/django-tutorial/blob/master/templates/hello_django.html)，

`Choice` ，可以透過 `get_FOO_display()` 的方法取得名稱，如下

```python
TYPE_CHOICES = (
    ('T1', 'type 1'),
    ('T2', 'type 2'),
    ('T3', 'type 3'),
    ('T4', 'type 4'),
)

class Music(models.Model):
    ......
    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default="T1"
    )

    class Meta:
        db_table = "music"

    def display_type_name(self):
        return self.get_type_display()
```

詳細可參考 [https://docs.djangoproject.com/en/1.11/ref/models/fields/#choices](https://docs.djangoproject.com/en/1.11/ref/models/fields/#choices)

恭喜你，基本上到這裡，已經是一個非常簡單的  [Django](https://github.com/django/django) 程式了，趕快動手下去玩玩吧 :stuck_out_tongue:

後記：

我是先接觸 [Flask](http://flask.pocoo.org/)，後來才接觸到 [Django](https://github.com/django/django) ，

有些人一開始應該也會和我一樣覺得 [Django](https://github.com/django/django) 的設定很多，非常麻煩，

但其實了解他之後，會發現他並沒有想像中的那麼複雜，而且功能非常強大。

下一步可以參考更酷更強大的 [Django-REST-framework 基本教學 - 從無到有 DRF-Beginners-Guide](https://github.com/twtrubiks/django-rest-framework-tutorial)

或是使用 Django 實現一個可以使用社交平台登入並且註冊的網站 [django_social_login_tutorial](https://github.com/twtrubiks/django_social_login_tutorial)。

## 執行環境

* Python 3.4.3

## Reference

* [Django](https://www.djangoproject.com/)

## License

MIT license

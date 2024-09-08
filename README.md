# django-custom-management-commands-tutorial

這邊紀錄如何客製化 management commands


## 教學

將這個 management commands 放到 musics 資料夾底下,

資料夾結構如下

```python
musics/
    __init__.py
    models.py
    management/
        __init__.py
        commands/
            __init__.py
            welcome.py
    tests.py
    views.py
```

然後記得一定要將 musics 加入到 `INSTALLED_APPS` 底下,

否則 django 不會偵測.

```python
INSTALLED_APPS = [
    ......
    "musics",
]

```

[welcome.py](https://github.com/twtrubiks/django-tutorial/blob/django4_custom_management_commands/musics/management/commands/welcome.py) 程式碼如下,

```python
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    # python3 manage.py help welcome

    help = 'hello django custom management commands'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("name", type=str)

    def handle(self, *args, **kwargs):
        msg = f'handle - hello django custom management commands: {kwargs["name"]}'
        self.stdout.write(self.style.SUCCESS("success"))
        self.stdout.write(msg)
```

使用方法也很簡單, 先來測試一下是否有正確載入,

如果有出現 welcome 代表成功,

```cmd
❯ python3 manage.py help

[musics]
    welcome
```

接著來測試一下指令

```cmd
❯ python3 manage.py welcome test
success
handle - hello django custom management commands: test
```

如果你想 透過 vscode debug django custom management commands,

可參考 [設定 Django Shell 中斷點](https://github.com/twtrubiks/vscode_django_note?tab=readme-ov-file#%E8%A8%AD%E5%AE%9A-django-shell-%E4%B8%AD%E6%96%B7%E9%BB%9E).

如果想定期執行, 可以搭配 [Linux 指令教學-Crontab](https://github.com/twtrubiks/linux-note/tree/master/crontab-tutorual) 來執行定期需要執行的內容.

## 執行環境

* Python 3.9

## Reference

* [Django custom-management-commands](https://docs.djangoproject.com/en/5.0/howto/custom-management-commands/)

## Donation

文章都是我自己研究內化後原創，如果有幫助到您，也想鼓勵我的話，歡迎請我喝一杯咖啡:laughing:

![alt tag](https://i.imgur.com/LRct9xa.png)

[贊助者付款](https://payment.opay.tw/Broadcaster/Donate/9E47FDEF85ABE383A0F5FC6A218606F8)

## License

MIT license

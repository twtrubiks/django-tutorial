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

from django.db import models
from django.db.models import Field
from django.db.models import Lookup
from django.contrib.postgres.fields import ArrayField

class Sheet(models.Model):
    name = models.CharField(default="sheet name", max_length=64)

class Music(models.Model):
    song = models.TextField(default="song")
    singer = models.TextField(default="AKB48")
    count = models.IntegerField(blank=True, null=True)
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE, null=True)
    # sheet = models.ForeignKey(Sheet, on_delete=models.PROTECT, null=True)
    # sheet = models.ForeignKey(Sheet, on_delete=models.SET_NULL, null=True)
    """
    會依照不同的設定, 決定是否可刪除
    Sheet.objects.get(pk=3).delete()
    """

    localization = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = "music"

    def display_type_name(self):
        return self.get_type_display()

class MusicTag(models.Model):
    music = models.OneToOneField(Music, on_delete=models.CASCADE)
    tags = ArrayField(models.TextField(), default=list, blank=False, null=False)

    class Meta:
        db_table = "music_tag"


# ref
# https://docs.djangoproject.com/en/5.0/howto/custom-lookups/
# can use -> Music.objects.filter(song__ne='test')
@Field.register_lookup
class NotEqual(Lookup):
    lookup_name = "ne"

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return "%s <> %s" % (lhs, rhs), params
from django.db import models

class MusicSheetManager(models.Manager):

    def with_counts(self):
        return self.count()

class Sheet(models.Model):
    name = models.CharField(default="sheet name", max_length=64)

    objects = MusicSheetManager()

class MusicManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(song="song")

    def with_counts(self):
        return self.count()

class Music(models.Model):
    song = models.TextField(default="song")
    singer = models.TextField(default="AKB48")
    count = models.IntegerField(blank=True, null=True)
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE, null=True)

    objects = models.Manager()  # The default manager.
    custom_objects = MusicManager()  # The new manager.

    class Meta:
        db_table = "music"

    def display_type_name(self):
        return self.get_type_display()

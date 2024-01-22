from django.db import models

class Sheet(models.Model):
    name = models.CharField(default="sheet name")

class Music(models.Model):
    song = models.TextField(default="song")
    singer = models.TextField(default="AKB48")
    count = models.IntegerField(blank=True, null=True)
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "music"

    def display_type_name(self):
        return self.get_type_display()
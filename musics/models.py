from django.db import models

TYPE_CHOICES = (
    ('T1', 'type 1'),
    ('T2', 'type 2'),
    ('T3', 'type 3'),
    ('T4', 'type 4'),
)


# Create your models here.
class Music(models.Model):
    song = models.TextField(default="song")
    singer = models.TextField(default="AKB48")
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default="T1"
    )

    class Meta:
        db_table = "music"

    def display_type_name(self):
        return self.get_type_display()

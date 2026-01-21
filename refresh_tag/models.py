from django.db import models


class RefreshTag(models.Model):
    client_id = models.CharField(max_length=50)

    edate = models.DateField()
    etime = models.DateTimeField()
    userid = models.CharField(max_length=20)
    remark = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "refresh_tag"

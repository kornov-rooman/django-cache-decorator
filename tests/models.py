from django.db import models


class SomeModel(models.Model):
    some_field = models.CharField('Some Field', max_length=255, blank=False, null=False, default='some field value')

    class Meta:
        app_label = 'tests'

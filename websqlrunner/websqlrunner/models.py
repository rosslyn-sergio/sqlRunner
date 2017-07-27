import re

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validate_connection_strings(value):
    conns = value.split('\n')
    pattern = re.compile("^Data Source=[^;]+;Initial Catalog=[^;]+;[ ]*User id=[^;]+;[ ]*Password=[^;]+;[ ]*Connection Timeout=[0-9]+$")

    for con in conns:
        if not pattern.match(con):
            raise ValidationError(con + " is not a valid connection string")

class SqlScript(models.Model):
    name = models.CharField(max_length=1000, unique=True)
    description = models.CharField(max_length=500, null=True)
    createdby = models.ForeignKey(User)
    file = models.FileField(upload_to='scripts')

    class Meta:
        ordering = ['name']

    def get_file_name(self):
        return self.file.name.split('/')[-1]

    def __str__(self):
        return self.name


class Run(models.Model):
    date = models.DateTimeField()
    user = models.ForeignKey(User)
    script = models.ForeignKey(SqlScript)
    connstrings = models.TextField(validators=[validate_connection_strings])

    STATUS = (("R","Running"),("S","Success"),("F","Fail"),)
    status = models.CharField(max_length=50, choices=STATUS, default="R")

    class Meta:
        ordering = ['date']

    def __str__(self):
        return str(self.script) + " " + str(self.date)



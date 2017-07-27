
from django.contrib import admin

from .models import SqlScript
from .models import Run

admin.site.register(SqlScript)
admin.site.register(Run)
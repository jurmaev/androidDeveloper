from django.contrib import admin
import app.models as models

# Register your models here.
admin.site.register(models.YearStatistics)
admin.site.register(models.CitySalaryStatistics)
admin.site.register(models.CityShareStatistics)
admin.site.register(models.TopSkills)
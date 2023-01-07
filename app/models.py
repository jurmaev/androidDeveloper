from django.db import models
from app.services.statistics import Statistics as stats


class Profession(models.Model):
    name = models.CharField('Название', max_length=50)
    description = models.TextField('Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Профессия'
        verbose_name_plural = 'Профессии'

class YearStatistics(models.Model):
    year = models.IntegerField('Год')
    average_salary = models.FloatField('Средняя зарплата')
    number_of_vacancies = models.IntegerField('Количество вакансий')
    average_salary_by_profession = models.FloatField('Средняя зарплата по профессии')
    number_of_vacancies_by_profession = models.IntegerField('Количество вакансий по профессии')


# statistics = stats('salary_info.sqlite3', 'Аналитик')
# demand_statistics = statistics.get_demand_statistics()
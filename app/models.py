from django.db import models

class YearStatistics(models.Model):
    year = models.IntegerField('Год', primary_key=True)
    average_salary = models.FloatField('Средняя зарплата')
    number_of_vacancies = models.IntegerField('Количество вакансий')
    average_salary_by_profession = models.FloatField('Средняя зарплата по профессии')
    number_of_vacancies_by_profession = models.IntegerField('Количество вакансий по профессии')

    def __str__(self):
        return str(self.year)

    class Meta:
        verbose_name = 'Статистика по годам'
        verbose_name_plural = 'Статистика по годам'

class CitySalaryStatistics(models.Model):
    city = models.CharField('Город', max_length= 50, primary_key=True)
    average_salary = models.FloatField('Средняя зарплата')

    def __str__(self):
        return self.city

    class Meta:
        verbose_name = 'Средняя зарплата по городу'
        verbose_name_plural = 'Средняя зарплата по городам'

class CityShareStatistics(models.Model):
    city = models.CharField('Город', max_length=50, primary_key=True)
    share = models.FloatField('Часть')

    def __str__(self):
        return self.city

    class Meta:
        verbose_name = 'Доля вакансий по городу'
        verbose_name_plural = 'Доля вакансий по городам'

class TopSkills(models.Model):
    year = models.IntegerField('Год', primary_key=True)
    skills = models.TextField('Топ-10 навыков', default='')

    def __str__(self):
        return str(self.year)

    def get_skills(self):
        return self.skills.split(',')

    class Meta:
        verbose_name = 'Топ-10 навыков по году'
        verbose_name_plural = 'Топ-10 навыков по годам'
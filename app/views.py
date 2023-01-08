from django.shortcuts import render
from app.models import CityShareStatistics, CitySalaryStatistics, TopSkills

def index_page(request):
    return render(request, 'app/index.html')

def demand_page(request):
    return render(request, 'app/demand.html')

def geo_page(request):
    data = {'headings': ['Город', 'Средняя зарплата', 'Город', 'Доля вакансий'],
            'city_salary': CitySalaryStatistics.objects.all(),
            'city_share': CityShareStatistics.objects.all()}
    return render(request, 'app/geo.html', data)

def skills_page(request):
    data = {'skills_by_year': TopSkills.objects.all()}
    return render(request, 'app/skills.html', data)

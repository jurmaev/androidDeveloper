from django.shortcuts import render
from app.models import Profession
from app.models import YearStatistics
import app.services.statistics as stats

def index_page(request):
    data = {'profession': Profession.objects.get(id=1)}
    return render(request, 'app/index.html', data)

def demand_page(request):
    # vacancy = 'Аналитик'
    # statistics = stats.Statistics('services/salary_info.sqlite3', vacancy)
    # demand_statistics = statistics.get_demand_statistics()
    # geo_statistics = statistics.get_geo_statistics()
    #
    # report = stats.Report(vacancy)
    # report.generate_demand_images(demand_statistics)
    # report.generate_city_images(geo_statistics)

    # year_stats = YearStatistics(year=1,average_salary=1,
    #                             number_of_vacancies=1,
    #                             average_salary_by_profession=1,
    #                             number_of_vacancies_by_profession=1)
    # year_stats.save()

    return render(request, 'app/demand.html')

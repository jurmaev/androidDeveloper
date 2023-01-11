from django.shortcuts import render
from app.models import CityShareStatistics, CitySalaryStatistics, TopSkills, YearStatistics
from app.services.statistics import VacanciesApi


def index_page(request):
    return render(request, 'app/index.html')


def demand_page(request):
    vacancy = 'Android-разработчик'
    data = {'headings': ['Год', 'Средняя зарплата', f'Средняя зарплата - {vacancy}', 'Количество вакансий',
                         f'Количество вакансий - {vacancy}'],
            'year_statistics': YearStatistics.objects.all()}
    return render(request, 'app/demand.html', data)


def geo_page(request):
    data = {'headings': ['Город', 'Средняя зарплата', 'Город', 'Доля вакансий'],
            'city_salary': CitySalaryStatistics.objects.all(),
            'city_share': CityShareStatistics.objects.all()}
    return render(request, 'app/geo.html', data)


def skills_page(request):
    data = {'skills_by_year': TopSkills.objects.all()}
    return render(request, 'app/skills.html', data)


def vacancies_page(request):
    data = {'headings': ['Название', 'Описание', 'Навыки', 'Компания', 'Оклад', 'Регион', 'Дата публикации'],
            'vacancies': VacanciesApi(['android-разработчик', 'android', 'андроид', 'andorid', 'andoroid', 'andriod', 'andrind', 'xamarin']).get_date_vacancies('15')}
    return render(request, 'app/vacancies.html', data)


def fill_models(request):
    key_skills = {'2009': [], '2010': [], '2011': [], '2012': [], '2013': [], '2014': [],
                  '2015': ['Android', 'iOS', 'Java', 'Android SDK', 'Программирование iOS, Android',
                           'Разработка iOS Android', 'Git', 'ООП', 'Objective-C', 'REST'],
                  '2016': ['Android', 'Java', 'Android SDK', 'Git', 'ООП', 'iOS', 'SQLite', 'C#', 'JSON API',
                           'JavaScript'],
                  '2017': ['Android', 'Java', 'Android SDK', 'Git', 'ООП', 'iOS', 'C#', 'SQL', 'REST', 'JSON API'],
                  '2018': ['Android', 'Java', 'Android SDK', 'Git', 'ООП', 'Kotlin', 'iOS', 'JavaScript', 'C#', 'REST'],
                  '2019': ['Android', 'Java', 'Android SDK', 'Kotlin', 'Git', 'ООП', 'iOS', 'REST', 'C++', 'SQL'],
                  '2020': ['Android', 'Java', 'Android SDK', 'Git', 'Kotlin', 'ООП', 'Java SE', 'iOS', 'SQL', 'SQLite'],
                  '2021': ['Android', 'Java', 'Android SDK', 'Kotlin', 'Git', 'ООП', 'iOS', 'MVVM', 'Английский язык',
                           'Java SE'],
                  '2022': ['Android', 'Java', 'Kotlin', 'Android SDK', 'Git', 'ООП', 'Английский язык', 'MVVM', 'iOS',
                           'Scrum']}
    demand_statistics = (
        {'2003': 40930.1436, '2004': 42762.1674, '2005': 372027.8215, '2006': 41090.381, '2007': 44215.301,
         '2008': 48536.7632, '2009': 44810.8149, '2010': 44648.5714, '2011': 46476.0328, '2012': 47924.5968,
         '2013': 53514.0729, '2014': 49200.8903, '2015': 51735.8414, '2016': 61206.1237, '2017': 60374.5153,
         '2018': 65793.171, '2019': 69993.6221, '2020': 73080.4084, '2021': 83204.4272, '2022': 95145.1001},
        {'2003': 1070, '2004': 4322, '2005': 9364, '2006': 23057, '2007': 35341, '2008': 46657, '2009': 31081,
         '2010': 51686, '2011': 77413, '2012': 95137, '2013': 129438, '2014': 141439, '2015': 147608, '2016': 177251,
         '2017': 203556, '2018': 282917, '2019': 265999, '2020': 234858, '2021': 136553, '2022': 47293},
        {'2003': 0, '2004': 0, '2005': 0, '2006': 0, '2007': 0, '2008': 0, '2010': 60327.7282, '2012': 66330.9059,
         '2013': 66872.7426, '2014': 72297.6287, '2011': 76076.5526, '2015': 91938.3422, '2009': 96472.8671,
         '2016': 99584.3824, '2017': 102243.4247, '2018': 110321.3789, '2019': 126956.8348, '2020': 138242.5304,
         '2021': 165777.7058, '2022': 202699.0893},
        {'2003': 0, '2004': 0, '2005': 0, '2006': 0, '2007': 0, '2008': 0, '2009': 19, '2010': 74, '2022': 274,
         '2011': 290,
         '2012': 379, '2013': 586, '2014': 887, '2021': 1150, '2015': 1222, '2016': 1877, '2020': 1901, '2017': 1952,
         '2018': 2134, '2019': 2153})
    average_salary_by_city = {'Минск': 94105.1188, 'Москва': 83633.4275, 'Киев': 79460.6742,
                              'Санкт-Петербург': 68770.4225, 'Новосибирск': 64779.2647, 'Екатеринбург': 59142.4978,
                              'Краснодар': 51582.0679, 'Казань': 51322.9766, 'Нижний Новгород': 49939.0617,
                              'Самара': 49547.6176}
    share_by_city = {'Санкт-Петербург': 0.1079, 'Самара': 0.0132, 'Ростов-на-Дону': 0.0165, 'Пермь': 0.0117,
                     'Новосибирск': 0.0241, 'Нижний Новгород': 0.0216, 'Москва': 0.3053, 'Минск': 0.0265,
                     'Краснодар': 0.0158, 'Киев': 0.0125}
    for year, skills in key_skills.items():
        if not key_skills[year]: continue
        top_skill = TopSkills()
        top_skill.year = year
        top_skill.skills = ','.join(skills)
        top_skill.save()
    for city, salary in average_salary_by_city.items():
        salary_stat = CitySalaryStatistics()
        salary_stat.city = city
        salary_stat.average_salary = salary
        salary_stat.save()
    for city, share in share_by_city.items():
        share_stat = CityShareStatistics()
        share_stat.city = city
        share_stat.share = share
        share_stat.save()
    for year in demand_statistics[0].keys():
        demand_stat = YearStatistics()
        demand_stat.year = year
        demand_stat.average_salary = demand_statistics[0][year]
        demand_stat.number_of_vacancies = demand_statistics[1][year]
        demand_stat.average_salary_by_profession = demand_statistics[2][year]
        demand_stat.number_of_vacancies_by_profession = demand_statistics[3][year]
        demand_stat.save()
    return render(request, 'app/base.html')

from django.shortcuts import render
from app.models import CityShareStatistics, CitySalaryStatistics, TopSkills, YearStatistics


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


def fill_models(request):
    key_skills = {'2003': [], '2004': [], '2005': [], '2006': [], '2007': [], '2008': [], '2009': [], '2010': [],
                  '2011': [], '2012': [], '2013': [], '2014': [],
                  '2015': ['MS Excel', 'SQL', 'Python', 'язык программирования R', 'Аналитический склад ума',
                           'Пользователь ПК', 'MS PowerPoint', 'Анализ бизнес показателей', 'внимательность к деталям',
                           'Работа с большим объемом информации'],
                  '2016': ['MS Excel', 'Аналитика продаж', 'SQL', 'UML', 'Аналитический склад ума', 'Прогнозирование',
                           'MS SQL', 'VBA', 'Google Analytics', 'MS PowerPoint'],
                  '2017': ['MS Excel', 'MS SQL', 'SQL', 'Работа в команде', 'Бизнес-анализ', 'Пользователь ПК', 'UML',
                           'Управление проектами', 'Деловая переписка', 'Грамотная речь'],
                  '2018': ['MS Excel', 'SQL', 'Бизнес-анализ', 'Управление проектами', 'Аналитический склад ума',
                           'Аналитические исследования', 'Оптимизация бизнес-процессов', 'Работа в команде',
                           'Статистический анализ', 'Аналитическое мышление'],
                  '2019': ['MS Excel', 'SQL', 'MS PowerPoint', 'Аналитические исследования', 'Бизнес-анализ',
                           'Пользователь ПК', 'Аналитическое мышление', 'Работа с большим объемом информации',
                           'Работа в команде', 'Анализ данных'],
                  '2020': ['MS PowerPoint', 'Аналитическое мышление', 'Аналитические исследования', 'SQL', 'MS Access',
                           'Анализ данных', 'Бизнес-анализ', 'MS Excel', 'Работа с большим объемом информации',
                           'Работа с базами данных'],
                  '2021': ['MS PowerPoint', 'SQL', 'Аналитическое мышление', 'Работа с большим объемом информации',
                           'Анализ данных', 'MS Excel', 'Аналитические исследования', 'Бизнес-анализ', 'MS SQL',
                           'MS Access'],
                  '2022': ['Аналитическое мышление', 'MS PowerPoint', 'Работа с большим объемом информации',
                           'Анализ данных', 'MS Excel', 'Работа в команде', 'Грамотная речь', 'SQL',
                           'Аналитические исследования', 'Аналитика']}
    demand_statistics = (
        {'2003': 40930.1436, '2004': 42762.1674, '2005': 372027.8215, '2006': 41090.381, '2007': 44215.301,
         '2008': 48536.7632, '2009': 44810.8149, '2010': 44648.5714, '2011': 46476.0328, '2012': 47924.5968,
         '2013': 53514.0729, '2014': 49200.8903, '2015': 51735.8414, '2016': 61206.1237, '2017': 60374.5153,
         '2018': 65793.171, '2019': 69993.6221, '2020': 73080.4084, '2021': 83204.4272, '2022': 95145.1001},
        {'2003': 1070, '2004': 4322, '2005': 9364, '2006': 23057, '2007': 35341, '2008': 46657, '2009': 31081,
         '2010': 51686, '2011': 77413, '2012': 95137, '2013': 129438, '2014': 141439, '2015': 147608, '2016': 177251,
         '2017': 203556, '2018': 282917, '2019': 265999, '2020': 234858, '2021': 136553, '2022': 47293},
        {'2003': 36296.1168, '2004': 45755.0879, '2005': 41869.69, '2006': 37496.492, '2007': 50240.7689,
         '2008': 48737.4767, '2009': 47379.1828, '2010': 48679.7484, '2011': 53580.6471, '2012': 61111.458,
         '2013': 58406.8882, '2014': 57881.4804, '2015': 53381.6256, '2016': 56488.5149, '2017': 57230.5704,
         '2018': 63469.7492, '2019': 70197.9636, '2020': 74811.744, '2021': 86077.7833, '2022': 88132.0438},
        {'2003': 19, '2004': 70, '2005': 200, '2006': 300, '2007': 461, '2008': 613, '2009': 330, '2010': 630,
         '2011': 840,
         '2012': 945, '2013': 1011, '2014': 1250, '2015': 1524, '2016': 2103, '2017': 2703, '2018': 3364, '2019': 3644,
         '2020': 3242, '2021': 2071, '2022': 791})
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

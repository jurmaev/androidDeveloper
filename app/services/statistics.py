import sqlite3
import numpy as np
import pandas as pd
from datetime import datetime
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from dateutil import rrule
from matplotlib import pyplot as plt
from collections import Counter


class Converter:
    def __init__(self, file_name, dynamic_file_name):
        self.file_name = file_name
        self.dynamic_file_name = dynamic_file_name
        self.currency_dynamic = self.get_currency_dynamic()
        # self.get_currency_dynamic_csv()
        # self.get_currency_dynamic_db()

    def get_currency_dynamic(self):
        """
        Получает dataframe из csv файла
        :param file_name: название файла
        :return: dataframe с вакансиями
        """
        pd.set_option('expand_frame_repr', False)
        df = pd.read_csv(self.file_name,
                         dtype={'name': str, 'key_skills': str, 'salary_from': float, 'salary_to': float,
                                'salary_currency': str, 'area_name': str, 'published_at': str})
        df = df.dropna(subset=['salary_from', 'salary_to'], how='all')
        df['currency_count'] = df.groupby('salary_currency')['salary_currency'].transform('count')
        df = df[(df['currency_count'] > 5000) | (pd.isna(df['currency_count']))]
        return df

    def get_currency_dynamic_csv(self):
        """
        Создает csv файл с валютами
        :param file_name: название файла с валютами
        :param dynamic_file_name: Название выходного файла с валютами
        :return: csv файл с валютами
        """
        df = self.currency_dynamic
        print(df['salary_currency'].value_counts())
        currencies = df['salary_currency'].unique()
        currencies = currencies[currencies != 'RUR']
        start_date = datetime.strptime(df['published_at'].min(), '%Y-%m-%dT%H:%M:%S%z').replace(day=28, hour=12,
                                                                                                minute=0,
                                                                                                second=0)
        end_date = datetime.strptime(df['published_at'].max(), '%Y-%m-%dT%H:%M:%S%z').replace(day=28, hour=12, minute=0,
                                                                                              second=0)

        currency_dynamic = {key: [] for key in currencies}
        currency_dynamic['date'] = []
        for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
            tree = ET.parse(
                urlopen(f'http://www.cbr.ru/scripts/XML_daily.asp?date_req=28/{dt.strftime("%m/%Y")}d=1'))
            root = tree.getroot()
            for child in root.findall('Valute'):
                code = child.find('CharCode').text
                if code in currencies:
                    if dt.strftime('%Y-%m') not in currency_dynamic['date']:
                        currency_dynamic['date'] += [dt.strftime('%Y-%m')]
                    coeff = float(child.find('Value').text.replace(',', '.')) / float(child.find('Nominal').text)
                    currency_dynamic[code] += [coeff]
            for key in currency_dynamic.keys():
                if key != 'date' and len(currency_dynamic['date']) > len(currency_dynamic[key]):
                    currency_dynamic[key] += [None]
        currency_df = pd.DataFrame(data=currency_dynamic)
        cols = currency_df.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        currency_df = currency_df[cols]
        currency_df.to_csv(self.dynamic_file_name, index=False)

    def get_currency_dynamic_db(self):
        df = pd.read_csv(self.dynamic_file_name)

        conn = sqlite3.connect('currency_dynamic.sqlite3')
        c = conn.cursor()
        c.execute(
            'CREATE TABLE IF NOT EXISTS currency_dynamic (date text, USD float, EUR float, KZT float, UAH float, BYR float)')
        conn.commit()
        df.to_sql('currency_dynamic', conn, if_exists='replace', index=False)
        c.execute('SELECT * FROM currency_dynamic')
        conn.close()

    def convert_salary_to_rub_sqlite(self):
        def convert_to_rub(row):
            if row['salary_currency'] != 'RUR':
                date = datetime.strptime(row['published_at'], '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m')
                convert_value = \
                    c.execute(
                        f"SELECT {row['salary_currency']} FROM currency_dynamic WHERE date = '{date}'").fetchone()[0]
                return None if not convert_value else row['salary'] * convert_value
            return row['salary']

        def count_salary(row):
            if pd.isna(row['salary_from']):
                return row['salary_to']
            elif pd.isna(row['salary_to']):
                return row['salary_from']
            return (row['salary_from'] + row['salary_to']) / 2

        conn = sqlite3.connect('currency_dynamic.sqlite3')
        c = conn.cursor()
        df = self.currency_dynamic
        df['salary'] = df.apply(count_salary, axis=1)
        df['salary'] = df.apply(convert_to_rub, axis=1)
        df = df[df['salary'] != 'NaN']
        df['published_at'] = df.apply(
            lambda row: datetime.strptime(row['published_at'], '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d'), axis=1)
        conn = sqlite3.connect('salary_info.sqlite3')
        c = conn.cursor()
        c.execute(
            'CREATE TABLE IF NOT EXISTS salary_info (name text, salary float, area_name text, published_at date, key_skills text)')
        conn.commit()
        print(df.head(10))
        df.loc[:, ['name', 'salary', 'area_name', 'published_at', 'key_skills']].to_sql('salary_info', conn,
                                                                                        if_exists='replace',
                                                                                        index=False)
        c.execute('SELECT * FROM salary_info')
        conn.close()


class Statistics:
    def __init__(self, file_name, vacancy):
        self.file_name = file_name
        self.vacancy = vacancy

    @staticmethod
    def get_dict_from_df(df, key1, key2):
        return {df[key1][i]: df[key2][i] for i in range(len(df[key1]))}

    def get_demand_statistics(self):
        conn = sqlite3.connect(self.file_name)
        salary_level = pd.read_sql_query(
            "SELECT strftime('%Y', published_at) as year, ROUND(AVG(salary), 4) as average_salary FROM salary_info GROUP BY strftime('%Y', published_at)",
            conn)
        vacancies = pd.read_sql_query(
            "SELECT  strftime('%Y', published_at) as year, COUNT(name) as vacancies_number FROM salary_info GROUP BY strftime('%Y', published_at)",
            conn)
        salary_level_by_profession = pd.read_sql_query(
            f"SELECT strftime('%Y', published_at) as year, ROUND(AVG(salary),4) as average_salary FROM salary_info WHERE LOWER(name) LIKE '%{self.vacancy}%' GROUP BY strftime('%Y', published_at)",
            conn)
        vacancies_by_profession = pd.read_sql_query(
            f"SELECT  strftime('%Y', published_at) as year, COUNT(name) as vacancies_number FROM salary_info WHERE LOWER(name) LIKE '%{self.vacancy}%' GROUP BY strftime('%Y', published_at)",
            conn)

        return Statistics.get_dict_from_df(salary_level, 'year', 'average_salary'), Statistics.get_dict_from_df(
            vacancies, 'year', 'vacancies_number'), Statistics.get_dict_from_df(salary_level_by_profession, 'year',
                                                                                'average_salary'), Statistics.get_dict_from_df(
            vacancies_by_profession, 'year', 'vacancies_number')

    def get_geo_statistics(self):
        conn = sqlite3.connect(self.file_name)
        c = conn.cursor()
        all_vacancies = c.execute('SELECT COUNT(*) FROM salary_info').fetchone()[0]
        salary_level = pd.read_sql_query(
            f"SELECT  area_name as city, ROUND(AVG(salary),4) as salary FROM salary_info GROUP BY area_name HAVING COUNT(name) >= {all_vacancies} / 100 ORDER BY AVG(salary) DESC LIMIT 10",
            conn)
        share_of_vacancies = pd.read_sql_query(
            f"SELECT  area_name as city, ROUND(CAST(COUNT(name) AS FLOAT) / {all_vacancies},4) as share FROM salary_info GROUP BY area_name HAVING COUNT(name) >= {all_vacancies} / 100 ORDER BY COUNT(name) / {all_vacancies} DESC LIMIT 10",
            conn)
        return Statistics.get_dict_from_df(salary_level, 'city', 'salary'), Statistics.get_dict_from_df(
            share_of_vacancies, 'city', 'share')

    def get_skills_statistics(self):
        def append_skills(row):
            if not pd.isna(row['key_skills']):
                skills[row['published_at']].extend(row['key_skills'].split('\n'))
        conn = sqlite3.connect(self.file_name)
        df = pd.read_sql_query("SELECT * FROM salary_info", conn)
        df = df[df['name'] == self.vacancy]
        df['published_at'] = df['published_at'].transform(lambda x: x[:4])
        skills = {k: [] for k in df['published_at'].unique()}
        df.apply(append_skills, axis=1)
        for k, v in skills.items():
            skills[k] = [i[0] for i in list(sorted(dict(Counter(v)).items(), key=lambda x: x[1], reverse=True))[:10]]
        return skills


class Report:
    """
    Класс для вывода данных статистики в файл pdf

    Attributes:
        inputs (Interface): Данные с вводом пользователя
        statistics (Statistics): Статистика по вакансиям
    """

    def __init__(self, profession):
        """
        Инициализирует класс Report

        Args:
            inputs (Interface): Данные с вводом пользователя
            statistics (Statistics): Статистика по вакансиям
        """
        self.profession = profession

    def generate_demand_images(self, dicts):
        """
        Составляет графики со статистикой и сохраняет их в файл png

        Args:
            dicts (list): Список словарей со статистикой
        """
        width = 0.4
        x_nums = np.arange(len(dicts[0].keys()))
        x_list1 = x_nums - width / 2
        x_list2 = x_nums + width / 2

        fig, ax = plt.subplots()
        ax.set_title('Уровень зарплат по годам')
        ax.bar(x_list1, dicts[0].values(), width, label='средняя з/п')
        ax.bar(x_list2, dicts[2].values(), width, label=f'з/п {self.profession.lower()}')
        ax.set_xticks(x_nums, dicts[0].keys(), rotation='vertical')
        ax.tick_params(axis='both', labelsize=8)
        ax.legend(fontsize=8, loc='upper left')
        ax.grid(True, axis='y')
        plt.savefig('/static/app/img/salary_level.png')

        fig, ax = plt.subplots()
        x_nums = np.arange(len(dicts[1].keys()))
        x_list1 = x_nums - width / 2
        x_list2 = x_nums + width / 2
        ax.set_title('Уровень вакансий по годам')
        ax.bar(x_list1, dicts[1].values(), width, label='Количество вакансий')
        ax.bar(x_list2, dicts[3].values(), width, label=f'Количество вакансий\n{self.profession.lower()}')
        ax.set_xticks(x_nums, dicts[1].keys(), rotation='vertical')
        ax.tick_params(labelsize=8)
        ax.legend(fontsize=8, loc='upper left')
        ax.grid(True, axis='y')
        plt.savefig('/static/app/img/vacancies.png')

    def generate_city_images(self, dicts):
        fig, ax = plt.subplots()
        y_nums = np.arange(len(dicts[0].keys()))
        labels = [i.replace(' ', '\n').replace('-', '-\n') for i in dicts[0].keys()]
        ax.set_title('Уровень зарплат по городам')
        ax.barh(y_nums, dicts[0].values(), align='center')
        ax.set_yticks(y_nums, labels)
        ax.tick_params(labelsize=8)
        ax.tick_params(axis='y', labelsize=6)
        ax.invert_yaxis()
        ax.grid(True, axis='x')
        plt.savefig('static/app/img/salary_level_by_profession.png')

        fig, ax = plt.subplots()
        x_nums = np.concatenate(([1 - sum(dicts[1].values())], list(dicts[1].values())))
        labels = np.concatenate((['Другие'], list(dicts[1].keys())))
        ax.set_title('Доля вакансий по городам')
        ax.pie(x_nums, labels=labels, textprops={'fontsize': 6})
        plt.savefig('static/app/img/share_of_vacancies.png')


# converter = Converter('vacancies_with_skills.csv', 'currency_dynamic.csv')
# converter.convert_salary_to_rub_sqlite()

# statistics = Statistics('salary_info.sqlite3', 'Аналитик')
# skills_statistics = statistics.get_skills_statistics()
# print(skills_statistics)
# demand_statistics = statistics.get_demand_statistics()
# print(demand_statistics)
# geo_statistics = statistics.get_geo_statistics()
# print(geo_statistics[0])
# print(geo_statistics[1])

# report = Report('Аналитик')
# report.generate_demand_images(demand_statistics)
# report.generate_city_images(geo_statistics)

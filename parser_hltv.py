import requests
from bs4 import BeautifulSoup
import threading
from queue import Queue
from os import path
import csv

#Класс потока
class Downloader(threading.Thread):
    """Потоковый обработчик профилей"""

    def __init__(self, queue):
        """Инициализация потока"""
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        """Запуск потока"""
        while True:
            # Получаем url из очереди
            url = self.queue.get()

            # Скачиваем файл
            self.checking_info(url)

            # Отправляем сигнал о том, что задача завершена
            self.queue.task_done()


    def checking_info(self, url):
        """Смотрим профиль игрока и пишем в файл"""
        data = []
        import re
        pattern = re.compile(r"(\w+\W)$|(\w+)$")
        name_player = pattern.search(url)
        data.append(['Player', name_player[0]])
        info_page = get_html(url)
        soup = BeautifulSoup(info_page, "html.parser")
        table = soup.find('div', attrs={'class': 'statistics'}).find_all('div', class_='stats-row')

        for row in table:
            cols = row.find_all('span')
            data.append([x.text for x in cols])

        with open('player_ind_stat.csv', 'a') as f:
            writer = csv.writer(f, delimiter=';')
            res = []
            for i in range(len(data)):
                res.append(data[i][1])
            writer.writerow(res)


def main(urls):
    """
    Запускаем программу
    """
    queue = Queue()

    # Запускаем потом и очередь
    for i in range(2):
        t = Downloader(queue)
        t.setDaemon(True)
        t.start()

    # Даем очереди нужные нам ссылки для скачивания
    for url in urls:
        concat_url = 'https://www.hltv.org'+str(url)
        queue.put(concat_url)

    # Ждем завершения работы очереди
    queue.join()

#Делаем запрос на таблицу игрков
def get_html(url):
    import cfscrape
    r = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
    cookies={
        'hash':'61a4fe9c1ee03626bf7c5c6e61241355'
    }
    scraper = cfscrape.create_scraper(headers=headers)
    return scraper.get(url).content

#Получаем список игроков и персональный url на их страницу со статистикой
def get_info(url):
    data = []

    soup = BeautifulSoup(url, "html.parser")
    table = soup.find('table', attrs={'class': 'stats-table player-ratings-table'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')

    for row in rows:
        cols = row.find_all('a')
        data.append(cols[0]['href'])

    return data

def write_csv():
    columns = ['Player',
            'Total_kills',
            'Headshot',
            'Total_deaths',
            'K/D_Ratio',
            'Damage/Round',
            'Grenade_dmg/Round',
            'Maps_played',
            'Rounds_played',
            'Kills/round',
            'Assists/round',
            'Deaths/round',
            'Saved_by_teammate/round',
            'Saved_teammates/round',
            'Rating_2.0',
            ]
    with open('player_ind_stat.csv', 'a') as f:
        writer = csv.DictWriter(f, delimiter=';', fieldnames=columns)
        writer.writeheader()

if path.exists('player_ind_stat.csv') == False:
    write_csv()

stat_page = get_html('https://www.hltv.org/stats/players/')
d = get_info(stat_page)
main(d)



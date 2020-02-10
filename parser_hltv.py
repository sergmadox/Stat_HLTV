import requests
from bs4 import BeautifulSoup

#Делаем запрос на таблицу игрков
def get_html(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    return r.text

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

#Переходим по персональным url игроков и тащим статистику
def info_player(url):
    data = []
    import re
    pattern = re.compile(r"(\w+)$")
    name_player = pattern.search(url)
    data.append(['Player',name_player[0]])

    info_page = get_html(url)

    soup = BeautifulSoup(info_page, "html.parser")
    table = soup.find('div', attrs={'class': 'statistics'}).find_all('div', class_='stats-row')

    for row in table:
        cols = row.find_all('span')
        data.append([x.text for x in cols])

    return data

def write_csv(data):
    import csv
    with open('player_ind_stat.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data[0],data[1]))


stat_page = get_html('https://www.hltv.org/stats/players/')
d = get_info(stat_page)
srting_page_player = 'https://www.hltv.org' + str(d[1])


result = info_player(srting_page_player)
print (result)
write_csv(result)
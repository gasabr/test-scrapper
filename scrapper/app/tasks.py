import lxml
from grab import Grab

from celery.utils.log import get_task_logger
from celery import shared_task


@shared_task
def add(x, y):
    return x + y


@shared_task
def parse_specialization(url):
    ''' Yeah, I know, code is awful, I just don't remember how to use xpath.'''
    g = Grab()
    response = g.go(url).unicode_body()
    html = lxml.html.fromstring(response)

    vacancy = {}
    vacancies = []
    for row in html.xpath('//div[@class="vacancy-serp-item__row"]'):
        info_divs = row.findall('div[@class="vacancy-serp-item__info"]/div')
        link = info_divs[0].find('a')
        if link is not None:
            vacancy['link'] = link.get('href')
            vacancy['name'] = link.text

        texts = [div.text for div in info_divs]
        if texts[0] is not None:
            vacancy['short_description'] = texts[0]
        comp_div = row.find('div[@class="vacancy-serp-item__sidebar"]/div')
        compensation = comp_div.text if comp_div is not None else None
        if compensation is not None:
            c = compensation[:-5].encode('ascii', 'ignore').decode('utf-8')
            from_ = int(c.split('-')[0].replace('?', ''))
            to = int(c.split('-')[1].replace('?', ''))
            vacancy['salary_from'] = from_
            vacancy['salary_to'] = to

        if all(map(lambda x: vacancy.get(x) is not None,
                   ['link', 'name', 'short_description'])):
            # we collected all the data for one
            if 'salary_from' not in vacancy:
                vacancy['salary_from'] = None
                vacancy['salary_to'] = None

            vacancy['currency'] = 'RUB'
            vacancies.append(vacancy)
            vacancy = {}

    return vacancies

@shared_task
def get_specialization_links(url):
    g = Grab()
    response = g.go(url).unicode_body()
    html = lxml.html.fromstring(response)

    links_list = html.xpath('//a[@class="bloko-link-switch"]/@href')

    return links_list

import logging

from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from celery import Celery

from .tasks import get_specialization_links, parse_specialization
from .models import Vacancy

logger = logging.getLogger(__name__)
fh = logging.FileHandler('views.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

# Create your views here.
def search(request):
    url = 'https://spb.hh.ru/employer/889'
    try:
        logger.info("Trying to delay staff")
        links = get_specialization_links.delay(url).get()
        parsing_futures = []
        for link in links:
            logger.info(f'Parsing {link}')
            parsing_futures.append(parse_specialization.delay(
                'https://spb.hh.ru' + link)
            )

        parsing_results = []
        for future in parsing_futures:
            for vacancy in future.get():
                parsing_results.append(vacancy)

        for vacancy in parsing_results:
            logger.debug(f'Parsed vacancy: {vacancy}')
            v = Vacancy()
            for k in vacancy:
                setattr(v, k, vacancy[k])
            v.save()

    except Exception as e:
        logger.exception(e)

    return HttpResponse()


def show(request):
    try:
        all_vacancies = Vacancy.objects.values_list('name', 'salary_from')
    except ObjectDoesNotExist as e:
        logger.exception(e)
        all_vacancies = []

    logger.debug(all_vacancies)
    result = '\n'.join([v[0] + ', ' + str(v[1])
                        for v in all_vacancies])
    result += '\n'

    return HttpResponse(result)


def status(request):
    app = Celery('scrapper')
    app.config_from_object('django.conf:settings', namespace='CELERY')
    i = app.control.inspect()
    n_active_workers = sum([len(x) for x in list(i.active().values())])
    return HttpResponse(f'# active workers = {n_active_workers}\n')


def links(request):
    try:
        all_vacancies = Vacancy.objects.values_list('name', 'link')
    except ObjectDoesNotExist as e:
        logger.exception(e)
        all_vacancies = []

    logger.debug(all_vacancies)
    result = '\n'.join([v[0] + ', ' + str(v[1])
                        for v in all_vacancies])
    result += '\n'

    return HttpResponse(result)


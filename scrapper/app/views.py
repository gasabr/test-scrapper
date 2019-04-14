import logging

from django.http import HttpResponse

from .tasks import get_specialization_links, parse_specialization

logger = logging.getLogger(__name__)
fh = logging.FileHandler('views.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

# Create your views here.
def search(request):
    url = 'https://spb.hh.ru/employer/889'
    result = None
    try:
        logger.info("Trying to delay staff")
        links = get_specialization_links.delay(url).get()
        parsing_futures = []
        for link in links[:2]:
            logger.info(f'Parsing {link}')
            parsing_futures.append(parse_specialization.delay(
                'https://spb.hh.ru' + link)
            )

        parsing_results = []
        for future in parsing_futures:
            parsing_results.append(future.get())

        result = parsing_results[0]

    except Exception as e:
        logger.exception(e)

    return HttpResponse(result)


def list(request):
    return HttpResponse("list page")


def status(request):
    return HttpResponse("status page")

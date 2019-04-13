import logging

from django.http import HttpResponse

from .tasks import add

logger = logging.getLogger(__name__)
fh = logging.FileHandler('views.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

# Create your views here.
def search(request):
    try:
        logger.info("Trying to delay staff")
        inspected = add.delay(4, 4)
        logger.debug("Inspected looks like {}".format(inspected))
    except Exception as e:
        logger.exception(e)
    return HttpResponse(f"search page {inspected}")


def list(request):
    return HttpResponse("list page")


def status(request):
    return HttpResponse("status page")

from django.shortcuts import render
from appointment.templatetags.appointment_tags import make_post_context

from util_demian import utils
from appointment.forms import AppointmentForm

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


def home(request):
    context = {
        "color": "default",
        "theme": "medilab_ds",
        "naver": "https://booking.naver.com/booking/13/bizes/441781",
    }
    if request.method == 'GET':
        return render(request, f"home.html", context)
    elif request.method == "POST":
        context.update(make_post_context(request.POST, 'hj3415@gmail.com'))
        return render(request, f"home.html", context)
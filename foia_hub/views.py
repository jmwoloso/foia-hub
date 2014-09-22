from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('foia_hub', 'templates'))

import json
from django.core.serializers.json import DjangoJSONEncoder

from foia_hub.models import Agency, FOIARequest


def request_form(request, slug=None):
    agency = get_object_or_404(Agency, slug=slug)
    office = agency.office_set.first()

    template = env.get_template('request/form.html')
    return HttpResponse(template.render(agency=agency, office=office))


def request_start(request):
    template = env.get_template('request/index.html')
    return HttpResponse(template.render())


def request_success(request, id):
    #   @todo: this makes it easy for an attacker to harvest email addresses
    #   -- just look at all of the /success/##s in sequential order
    foia_request = get_object_or_404(FOIARequest, pk=id)
    requester = foia_request.requester
    office = foia_request.office
    agency = office.agency

    template = env.get_template('request/success.html')
    return HttpResponse(template.render(
        foia_request=foia_request, requester=requester, office=office,
        agency=agency))


# similar to agency API, but optimized for typeahead consumption
def request_autocomplete(request):
    agencies = Agency.objects.order_by('name').all()
    response = []
    for agency in agencies:
        response.append({
            "name": agency.name,
            "description": agency.description,
            "abbreviation": agency.abbreviation,
            "slug": agency.slug,
            "keywords": agency.keywords
        })
    agency_json = json.dumps(response, cls=DjangoJSONEncoder)
    return HttpResponse(agency_json, content_type="application/json")
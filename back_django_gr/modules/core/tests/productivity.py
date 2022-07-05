# (~005) Query compare handle test

from django.test import TestCase
from django.db import transaction
from django.db.models import OuterRef, QuerySet, Subquery
from django.db import models
from modules.core.models.hospitality import rental as Rental_Model
from modules.core.models.hospitality import reservation as Reservation_Model
from .data_factory import StandardDataSets
import datetime
import time

class test1():

    def AssesmentRawQuery(self):
        results = { 'name': 'Raw query' , 'initial_duration': None, 'fetch_duration':None, 'fetch_count':0}

        init_start = time.time()
        fetchQuery = Reservation_Model.objects.selectReservationWithLast()
        init_end = time.time()

        fetch_start = time.time()
        counter = 0
        for row in fetchQuery:
            prev_id = row.id_prev
            counter += 1

        fetch_end = time.time()

        results['initial_duration'] = init_end - init_start
        results['fetch_duration'] = fetch_end - fetch_start
        results['fetch_count'] = counter

        return results

    def AssesmentQuerySetFetch(self):
        results = { 'name': 'Query set test' , 'initial_duration': None, 'fetch_duration':None, 'fetch_count':0}

        subQueryPrevious = Reservation_Model.objects.filter(
            rental_id=OuterRef('rental_id'),
            id__lt=OuterRef('id'),
        ).order_by('-checkin')

        init_start = time.time()
        fetchQuery = Reservation_Model.objects.all().annotate(id_previos=Subquery(subQueryPrevious.values('id')[:1], output_field=models.BigIntegerField())).select_related('rental')
        init_end = time.time()

        fetch_start = time.time()
        counter = 0
        for row in fetchQuery:
            prev_id = row.id_previos
            counter += 1

        fetch_end = time.time()

        results['initial_duration'] = init_end - init_start
        results['fetch_duration'] = fetch_end - fetch_start
        results['fetch_count'] = counter

        return results

    def test(self):
        print('Testing started')
        resultTestRawQuery = self.AssesmentQuerySetFetch()
        print(f'{resultTestRawQuery["name"]} Assesment Fetch of {resultTestRawQuery["fetch_count"]} duration: {resultTestRawQuery["fetch_duration"]}')

        resultQuerySetFetch = self.AssesmentRawQuery()
        print(f'{resultQuerySetFetch["name"]} Assesment Fetch of {resultQuerySetFetch["fetch_count"]} duration: {resultQuerySetFetch["fetch_duration"]}')

# python3 manage.py shell -c "print('start');from modules.core.tests.handleTest_productivity import test1; test1().test()"
import datetime
from modules.core.models import hospitality as models

class StandardDataSets(object):

    standardIntervals = [
            {'objectDATA': {'name': 'Rental object #1'}, 'reservations': [{'checkin':datetime.date(2022, 1, 1), 'checkout':datetime.date(2022, 1, 2)},], 'rental': None, 'reservation': None},
            {'objectDATA': {'name': 'Rental object #2'}, 'reservations': [{'checkin': datetime.date(2022, 1, 2), 'checkout': datetime.date(2022, 1, 20)},], 'rental': None, 'reservation': None},
            {'objectDATA': {'name': 'Rental object #1'}, 'reservations': [{'checkin':datetime.date(2022, 1, 20), 'checkout':datetime.date(2022, 2, 10)},], 'rental': None, 'reservation': None},
            {'objectDATA': {'name': 'Rental object #2'}, 'reservations': [{'checkin': datetime.date(2022, 1, 20), 'checkout': datetime.date(2022, 2, 11)},], 'rental': None, 'reservation': None},
            {'objectDATA': {'name': 'Rental object #1'}, 'reservations': [{'checkin': datetime.date(2022, 2, 20), 'checkout': datetime.date(2022, 3, 10)},], 'rental': None, 'reservation': None},
            {'objectDATA': {'name': 'Rental object #0'},'reservations': [], 'rental': None, 'reservation': None},
    ]

    standardIntervalsFaithful = [
            {'objectDATA': {'name': 'Rental object #1'},
             'reservations': [
                {'checkin':datetime.date(2022, 1, 2), 'checkout':datetime.date(2022, 1, 7)},
                {'checkin':datetime.date(2022, 2, 17), 'checkout':datetime.date(2022, 2, 20)},
             ],
             'rental': None,
             'reservation': None,
            },
            {'objectDATA': {'name': 'Rental object #2'},
             'reservations': [
                {'checkin': datetime.date(2022, 1, 1), 'checkout': datetime.date(2022, 1, 2)},
                {'checkin': datetime.date(2022, 2, 12), 'checkout': datetime.date(2022, 2, 13)},
             ],
             'rental': None,
             'reservation': None,
             },
        ]

    standardIntervalsIntersections = [
            {'objectDATA': {'name': 'Rental object #1'},
                'reservations': [
                    {'checkin':datetime.date(2022, 1, 25), 'checkout':datetime.date(2022, 2, 15)},
                    {'checkin':datetime.date(2022, 1, 20), 'checkout':datetime.date(2022, 2, 15)},
                    {'checkin':datetime.date(2022, 2, 15), 'checkout':datetime.date(2022, 2, 25)},
                    {'checkin':datetime.date(2022, 2, 15), 'checkout':datetime.date(2022, 3, 10)},
                    {'checkin':datetime.date(2022, 2, 15), 'checkout':datetime.date(2022, 3, 15)},
                    {'checkin':datetime.date(2022, 2, 20), 'checkout':datetime.date(2022, 3, 10)},
                ]
            },
        ]
    @classmethod
    def generateStandardDataSets(cls, echoOn = False):
        for curRental in cls.standardIntervals:
            curRental['rental'] = models.rental.objects.filter(**curRental['objectDATA']).first()
            if curRental['rental'] == None:
                newRentalObject = models.rental.objects.create(**curRental['objectDATA'])
                curRental['rental'] = models.rental.objects.get(id = newRentalObject.id)

            for curReservation in curRental['reservations']:
                newReservationObject = models.reservation.objects.create(rental = curRental['rental'], **curReservation)
                curRental['reservation'] = models.reservation.objects.get(id = newReservationObject.id)
        if echoOn == True:
            print('Standard datasets successfully generated!')
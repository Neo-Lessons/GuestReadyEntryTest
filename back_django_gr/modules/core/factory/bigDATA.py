import datetime
import random
import asyncio
from asgiref.sync import sync_to_async
from modules.core.models.hospitality import rental as Rental_Model
from modules.core.models.hospitality import reservation as Reservation_Model

class BigDataSets(object):

    _generatorDataController = []
    _globalCounter = 0

    def _getManagerElement(self, rootRental_Object, edge = None):
        edge = datetime.date(2020,1,1) if edge == None else edge

        return { 'Rental_Object': rootRental_Object, 'edge' : edge}

    def _generateNewManagerElement(self, wide = 10):

        generalName = "Big rental object #"

        for iWide in range(0, wide):
            rentalName = f'{generalName} {str(iWide)}'

            rentalObject = Rental_Model.objects.filter(name = rentalName).first()
            rentalObject = rentalObject if rentalObject != None else Rental_Model.objects.create(name = rentalName)

            lastReservation = Reservation_Model.objects.filter(rental = rentalObject).order_by('-checkout').first()
            edge = None if lastReservation == None else lastReservation.checkout

            self._generatorDataController.append(self._getManagerElement(rentalObject, edge))

    @sync_to_async
    def createReservationObject(self, rental, checkin, checkout):
        Reservation_Model.objects.create(rental=rental, checkin=checkin, checkout=checkout)

    async def asyncGenerateReservations(self, inGenerator, wideReservations):
        for countElemReservation in range(0, wideReservations):
            elemReservation = inGenerator

            newCheckIN = elemReservation['edge'] + datetime.timedelta(days=random.randrange(0, 21))
            newCheckOUT = newCheckIN + datetime.timedelta(days=random.randrange(1, 21))

            await self.createReservationObject(elemReservation['Rental_Object'], newCheckIN, newCheckOUT)

            elemReservation['edge'] = newCheckOUT
            self._globalCounter += 1
            print(f'Global count {self._globalCounter} object count {countElemReservation + 1} Object {inGenerator}')

    async def asyncProcessinRentals(self, widePerRental):
        # listRental = [curGenerator['Rental_Object'] for curGenerator in self._generatorDataController]

        await asyncio.gather(\
            *(self.asyncGenerateReservations(curGenerator, widePerRental) for curGenerator in self._generatorDataController))

    def generateBigData(self, wideReservations = 10000):
        self._generateNewManagerElement()

        wideRentals = len(self._generatorDataController)

        wideReservations = int(wideReservations/wideRentals)

        asyncio.run(self.asyncProcessinRentals(wideReservations))

        # for countElemReservation in range(0, wideReservations):
        #     print(countElemReservation+1)


#manage.py shell -c "print('start');from modules.core.tests.factory_bigDATA import BigDataSets; BigDataSets().generateBigData(90000)"
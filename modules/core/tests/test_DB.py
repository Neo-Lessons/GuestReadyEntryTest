from django.test import TestCase
from django.db import transaction
from modules.core.models import hospitality as models
from .data_factory import StandardDataSets
import datetime

class DB_Reservation_01_RightsGeneral(TestCase):
    # Requirements
    #   correct creation objects

    def setUp(self):
        self.StandardDataSets = StandardDataSets()
        self.StandardDataSets.generateStandardDataSets()

    def test_01_CheckCorrectCreatingModelObjects(self):
        # Reason
        #   Requirement
        #       - The correctness of the transfer of information during creation

        CreationStructure = [
            {
                'objectDATA': {'name': 'Rental object #3'},
                'rental': None,
                'reservations': [
                    {'checkin': datetime.date(2022, 1, 25), 'checkout': datetime.date(2022, 2, 15)},
                    {'checkin': datetime.date(2022, 2, 15), 'checkout': datetime.date(2022, 2, 25)},
                    {'checkin': datetime.date(2022, 2, 25), 'checkout': datetime.date(2022, 3, 15)},
                ]
            },
        ]

        def model_hospitality_rental():
            ListFieldCheckMatching_rental = ['name']

            for curNewRental in CreationStructure:
                objectDATA = curNewRental['objectDATA']

                newRantal = models.rental(**objectDATA)
                newRantal.save()
                curNewRental['rental'] = newRantal

                for checkFieldName in ListFieldCheckMatching_rental:
                    self.assertEqual(getattr(newRantal, checkFieldName), objectDATA[checkFieldName], msg='Incorrect feel field on creating')

        def model_hospitality_reservation():
            ListFieldCheckMatching_reservation = ['checkin','checkout']

            for curRental in CreationStructure:
                rentalObject = curRental['rental']

                for curReservation in curRental['reservations']:
                    newReservation = models.reservation(rental = rentalObject, **curReservation)
                    newReservation.save()
                    for checkFieldName in ListFieldCheckMatching_reservation:
                        self.assertEqual(getattr(newReservation, checkFieldName), curReservation[checkFieldName], msg='Incorrect feel field on creating')
                    self.assertEqual(newReservation.rental.id, curRental['rental'].id, msg='Incorrect feel field on creating')

        model_hospitality_rental()
        model_hospitality_reservation()

    def test_02_ValidationOfRequiredFields(self):
        # Every reservation most me related with rental object

        # ---------------------------------------------------------------
        # Model creation 1
        # ---------------------------------------------------------------
        objectCreated = False
        errorMassage = ''
        try:
            models.reservation.object.create(rental = None, **StandardDataSets.standardIntervalsIntersections[0]['reservations'][0])
            objectCreated = True;
        except Exception as e:
            errorMassage = e;

        self.assertEqual(objectCreated, False, msg='Violation data structure reservation most be related with rental')
        # ===============================================================

        # ---------------------------------------------------------------
        # Model creation 2
        # ---------------------------------------------------------------
        objectCreated = False
        errorMassage = ''
        try:
            newReservation = models.reservation.objects.create(**StandardDataSets.standardIntervalsIntersections[0]['reservations'][0])
            objectCreated = True;
        except Exception as e:
            errorMassage = e;

        self.assertEqual(objectCreated, False, msg='Violation data structure reservation most be related with rental')
        # ===============================================================

    def test_03_CheckUniqFields(self):
        def uniqRentalName():
            # Requirement: name of Rental most be uniq

            def rentaluniqNameOnCreate():
                ObjectsCreated = False

                objName = 'oioioipoi'
                newObject1 = models.rental.objects.create(name = objName)

                try:
                    with transaction.atomic():
                        newObject2 = models.rental.objects.create(name = objName)

                    ObjectsCreated = True
                except Exception as e:
                    pass

                self.assertEqual(ObjectsCreated, False, msg='Violation restriction on create semile name objects')
            def rentaluniqNameOnChange():
                ObjectCreated = False

                newObject1 = models.rental.objects.create(name='ppppppp')

                try:
                    with transaction.atomic():
                        newObject2 = models.rental.objects.create(name='pppppp_')

                    with transaction.atomic():
                        newObject2 = models.rental.objects.create(id=newObject2.id, name='ppppppp')

                    ObjectCreated = True
                except Exception as e:
                    pass

                self.assertEqual(ObjectCreated, False, msg='Violation restriction on create semile name objects')

            rentaluniqNameOnCreate()
            rentaluniqNameOnChange()

        uniqRentalName()

    def test_04_deleteObjects(self):

        #Delete all reservation
        try:
            for curTesDataSet in self.StandardDataSets.standardIntervals:
                if len(curTesDataSet['reservations']) != 0:
                    curTesDataSet['reservation'].delete()
                    pass

            self.assertEqual(len(models.reservation.objects.all()), 0, msg='Partual delete')
        except Exception() as e:
            self.assertEqual(False, True, msg=f'Unexpected exeption on delene reservation: [{e}]')

        #Delete all rental
        try:
            for curTesDataSet in self.StandardDataSets.standardIntervals:
                curTesDataSet['rental'].delete()

            self.assertEqual(len(models.reservation.objects.all()), 0, msg='Partual delete')
        except Exception() as e:
            self.assertEqual(False, True, msg=f'Unexpected exeption on delete rental: [{e}]')

    def test_05_TableLinkViolations(self):
        # Reservation can't be cascade deleted on delete Rental
        # ID Rental can't be change with existing reservations

        ObjectDeletedOperationSeccess = False

        query = models.rental.objects.filter(id = self.StandardDataSets.standardIntervals[0]['rental'].id)
        count = len(query)
        self.assertEqual(count, 1, msg='Unexpect query result for rental table')

        objectForDelete = query.first()

        try:
            try:
                objectForDelete.delete()
                ObjectDeletedOperationSeccess = True
            except Exception as e:
                pass
        except Exception as e:
            pass

        query = models.rental.objects.filter(id = self.StandardDataSets.standardIntervals[0]['rental'].id)
        count = len(query)
        self.assertEqual(count, 1, msg='Violation of object removal')

        self.assertEqual(ObjectDeletedOperationSeccess, False, msg='Unexpectet delete restriction method')

    def test_06_TestPermitedChange(self):
        ObjectChenged = False;
        errorMassage = ''
        objForCheck = self.StandardDataSets.standardIntervals[0]['rental']

        rentalObj = models.rental.objects.get(id = objForCheck.id)
        newName = f'{rentalObj.name} chanded'
        rentalObj.name = newName
        try:
            rentalObj.save()
            ObjectChenged = True
        except Exception() as e:
            errorMassage = str(e)

        self.assertEqual(ObjectChenged, True, msg=f'Error on object change: unexpectet exceprion error [{errorMassage}]')
        rentalObjCheck = models.rental.objects.get(id = objForCheck.id)
        self.assertEqual(rentalObjCheck.name, newName, msg=f'Incorrect change field')

    def test_07_01_GeneralRequirement_rental(self):
        # Block id manipulations

        for curTestSet in self.StandardDataSets.standardIntervals:
            rentalObj = curTestSet['rental']

            idChanged = False
            rentalObj.id = 100
            rentalObj.name += ' new index'
            errorMassage = ''
            try:
                rentalObj.save()
                idChanged = True
            except Exception as e:
                errorMassage = str(e)

            self.assertEqual(idChanged, False, msg='Unexpected event on change ID for rental table')
            self.assertEqual(errorMassage, 'Changing ID forbidden', msg=f'Incorrect exception with error massage: [{errorMassage}]')

    def test_07_02_GeneralRequirement_reservation(self):
        # Block id manipulations
        for curTestSet in self.StandardDataSets.standardIntervals:
            if len(curTestSet['reservations']) == 1:
                #Test get object by id
                reservationObj = curTestSet['reservation']

                idChanged = False
                reservationObj.id = 100
                errorMassage = ''
                try:
                    reservationObj.save()
                    idChanged = True
                except Exception as e:
                    errorMassage = str(e)

                self.assertEqual(idChanged, False, msg='Unexpected event on change ID for rental table')
                self.assertEqual(errorMassage, 'Changing ID forbidden', msg=f'Incorrect exception with error massage: [{errorMassage}]')

class DB_Reservation_02_Restrictions(TestCase):

    def setUp(self):
        self.StandardDataSets = StandardDataSets()
        self.StandardDataSets.generateStandardDataSets()

    def test_01_IntersectionRestrictionOnCreate(self):
        # Reason
        #   Requirement
        #       - Uninterrupted booking intervals

        for curRental in self.StandardDataSets.standardIntervalsFaithful:
            curRentalObject = models.rental.objects.get(**curRental['objectDATA'])

            for curFaithFullInterval in curRental['reservations']:
                # ------------------------------------------------------
                #Test inersection check method
                # ------------------------------------------------------
                CheckResult = models.reservation.checkIntersectionExistence(curRentalObject, **curFaithFullInterval)
                self.assertEqual(CheckResult, False, msg='Incorret determite intersection')
                #========================================================
                # ------------------------------------------------------
                #Check save Object on intersection
                # ------------------------------------------------------
                objectCreated = None
                errorMessage = ''

                try:
                    reservation = curRentalObject.createReservation(**curFaithFullInterval)
                    objectCreated = True
                    if type(reservation) == models.reservation:
                        objectCreated = True
                    else:
                        errorMessage = 'Unknown creation error'
                except Exception as e:
                    errorMessage = str(e)
                except BaseException as e:
                    errorMessage = 'Unknown error event'

                self.assertEqual(objectCreated, True, msg='Unexpected error: [' + errorMessage + ']')
                #===========================================================================================


        for curRental in self.StandardDataSets.standardIntervalsIntersections:
            curRentalObject = models.rental.objects.get(**curRental['objectDATA'])

            for curFaithFullInterval in curRental['reservations']:
                #------------------------------------------------
                # Test inersection check method
                # ------------------------------------------------
                CheckResult = models.reservation.checkIntersectionExistence(curRentalObject, **curFaithFullInterval)
                self.assertEqual(CheckResult, True, msg='Incorret determite intersection')
                #=====================================================

                #------------------------------------------------
                # Break save Object on intersection
                # ------------------------------------------------
                objectCreated = None;
                errorMessage = ''

                try:
                    reservation = curRentalObject.createReservation(**curFaithFullInterval)
                    objectCreated = True;
                except Exception as e:
                    pass
                except BaseException as e:
                    errorMessage = f'Incorrect Error [{e}]'

                self.assertEqual(objectCreated, None, msg=f'A failed lock creates an invalid slot reservation.{errorMessage}')
                #=====================================================

    def test_02_IntersectionRestrictionsOnChangeInterval_Faithful(self):
        rentalOBJ = models.rental.objects.get(**self.StandardDataSets.standardIntervalsFaithful[0]['objectDATA'])
        reservOBJ = models.reservation.objects.create(rental = rentalOBJ,checkin = datetime.date(2020,1,1), checkout = datetime.date(2020,1,2))


        for IntersectedInterval in self.StandardDataSets.standardIntervalsFaithful[0]['reservations']:
            ObjectCreated = False

            reservOBJ.checkin = IntersectedInterval['checkin']
            reservOBJ.checkout = IntersectedInterval['checkout']
            try:
                reservOBJ.save()
                ObjectCreated = True
            except Exception as e:
                pass

            self.assertEqual(ObjectCreated, True, msg='Unexpected error on change interval to faithful data')
            self.assertEqual(reservOBJ.checkin, IntersectedInterval['checkin'], msg='Incorrect change faithful interval')
            self.assertEqual(reservOBJ.checkout, IntersectedInterval['checkout'], msg='Incorrect change faithful interval')

    def test_03_IntersectionRestrictionsOnChangeInterval_Intersections(self):
        rentalOBJ = models.rental.objects.get(**self.StandardDataSets.standardIntervalsFaithful[0]['objectDATA'])
        reservOBJ = models.reservation.objects.create(rental = rentalOBJ,checkin = datetime.date(2020,1,1), checkout = datetime.date(2020,1,2))

        for IntersectedInterval in self.StandardDataSets.standardIntervalsIntersections[0]['reservations']:
            ObjectCreated = False

            reservOBJ.checkin = IntersectedInterval['checkin']
            reservOBJ.checkout = IntersectedInterval['checkout']
            try:
                reservOBJ.save()
                ObjectCreated = True
            except Exception as e:
                pass

            self.assertEqual(ObjectCreated, False, msg='Unexpected seccessful save intersected interval')

    def test_04_IntersectionRestrictionsOnTransferInterval_Faithful(self):
        rentalOBJ = models.rental.objects.create(name = 'Rental object #3')
        rentalOBJ_transfer = models.rental.objects.get(**self.StandardDataSets.standardIntervalsFaithful[0]['objectDATA'])

        for IntersectedInterval in self.StandardDataSets.standardIntervalsFaithful[0]['reservations']:
            ObjectCreated = False
            errorMassage = ''

            reservOBJ = models.reservation.objects.create(rental=rentalOBJ, **IntersectedInterval)
            reservOBJ.rental = rentalOBJ_transfer;
            try:
                reservOBJ.save()
                ObjectCreated = True
            except Exception as e:
                errorMassage = str(e)

            self.assertEqual(ObjectCreated, True, msg=f'Unexpected error on faithful reservation transfer: [{errorMassage}]')
            self.assertEqual(reservOBJ.rental, rentalOBJ_transfer, msg='Failed faithful transfer')

    def test_04_IntersectionRestrictionsOnTransferInterval_Intersected(self):
        rentalOBJ = models.rental.objects.create(name = 'Rental object #3')
        rentalOBJ_transfer = models.rental.objects.get(**self.StandardDataSets.standardIntervalsFaithful[0]['objectDATA'])

        for IntersectedInterval in self.StandardDataSets.standardIntervalsIntersections[0]['reservations']:
            ObjectCreated = False

            reservOBJ = models.reservation.objects.create(rental=rentalOBJ, **IntersectedInterval)
            reservOBJ.rental = rentalOBJ_transfer;
            try:
                reservOBJ.save()
                ObjectCreated = True
            except Exception as e:
                reservOBJ.delete()

            self.assertEqual(ObjectCreated, False, msg='Unexpected transfer intersected reservation.')

class DB_Reservation_03_Dependecys(TestCase):
    # Requirements
    #   correct creation objects

    def setUp(self):
        self.StandardDataSets = StandardDataSets()
        self.StandardDataSets.generateStandardDataSets()

    def test_ConsistentlyID(self):
        # Requirement: Sequential numbering of elements is used for the mechanism of determining the previous reservation
        #   Addictions:
        #       models.hospitality.reservation.id_previos
        #       models.hospitality.reservation.objects.selectReservationWithLast

        def CheckSequentialNumeration():
            lastID = None
            i = 1
            for reservData in StandardDataSets.standardIntervalsFaithful[0]['reservations']:
                rentalOBJ = models.rental.objects.filter(name=StandardDataSets.standardIntervalsFaithful[0]['objectDATA']['name']).first()

                newReservation = models.reservation.objects.create(rental = rentalOBJ, **reservData)
                if i > 1:
                    self.assertEqual(newReservation.id, lastID+1, msg='Violation sequential numbering')
                i += 1
                lastID = newReservation.id

        def CheckJumpNumerationRestriction():
            rentalOBJ = models.rental.objects.filter(name = StandardDataSets.standardIntervalsFaithful[1]['objectDATA']['name']).first()

            objectCreated = False

            try:
                newID1 = 100
                newReservation1 = models.reservation.objects.create(id = newID1, rental = rentalOBJ, **StandardDataSets.standardIntervalsFaithful[1]['reservations'][0])
                newID2 = 50
                newReservation2 = models.reservation.objects.create(id = newID2, rental = rentalOBJ, **StandardDataSets.standardIntervalsFaithful[1]['reservations'][1])
                objectCreated = True
            except Exception as e:
                pass

            self.assertEqual(objectCreated, False, msg='Violation sequential numbering')


        CheckSequentialNumeration()
        CheckJumpNumerationRestriction()

class DB_Reservation_04_DataSamplesAccuracy(TestCase):

    def setUp(self):
        self.standardExaminationSample = [
            {'id_sample': 1,
             'rental_DATA': {'name': 'Rental object #1'},
             'rental_Object': None,
             'reservation_DATA': {'checkin': datetime.date(2022, 1, 1), 'checkout': datetime.date(2022, 1, 2)},
             'reservation_Object': None,
             'reservation_Examination': {'id': 1, 'id_prev': None},
             'reservation_Examination_Checked': False, },
            {'id_sample': 2,
             'rental_DATA': {'name': 'Rental object #2'},
             'rental_Object': None,
             'reservation_DATA': {'checkin': datetime.date(2022, 1, 2), 'checkout': datetime.date(2022, 1, 20)},
             'reservation_Object': None,
             'reservation_Examination': {'id': 2, 'id_prev': None},
             'reservation_Examination_Checked': False, },
            {'id_sample': 3,
             'rental_DATA': {'name': 'Rental object #1'},
             'rental_Object': None,
             'reservation_DATA': {'checkin': datetime.date(2022, 1, 20), 'checkout': datetime.date(2022, 2, 10)},
             'reservation_Object': None,
             'reservation_Examination': {'id': 3, 'id_prev': 1},
             'reservation_Examination_Checked': False, },
            {'id_sample': 4,
             'rental_DATA': {'name': 'Rental object #2'},
             'rental_Object': None,
             'reservation_DATA': {'checkin': datetime.date(2022, 1, 20), 'checkout': datetime.date(2022, 2, 11)},
             'reservation_Object': None,
             'reservation_Examination': {'id': 4, 'id_prev': 2},
             'reservation_Examination_Checked': False, },
            {'id_sample': 5,
             'rental_DATA': {'name': 'Rental object #1'},
             'rental_Object': None,
             'reservation_DATA': {'checkin': datetime.date(2022, 2, 20), 'checkout': datetime.date(2022, 3, 10)},
             'reservation_Object': None,
             'reservation_Examination': {'id': 5, 'id_prev': 3},
             'reservation_Examination_Checked': False, },
        ]

        for curExamination in self.standardExaminationSample:
            rentalObj = models.rental.objects.filter(**curExamination['rental_DATA']).first()
            if rentalObj == None:
                rentalObj = models.rental(**curExamination['rental_DATA'])
                rentalObj.save()

            curExamination['rental_Object'] = rentalObj

            resObj = models.reservation(rental=curExamination['rental_Object'], **curExamination['reservation_DATA'])
            resObj.save()

            curExamination['reservation_Object'] = resObj

    def test_SampleReservationWithLast_model1(self):
        reportSelection = models.reservation.objects.selectReservationWithLast()

        for curElement in reportSelection:
            resultFilter = list(filter(lambda exam: exam['reservation_Object'] == curElement, self.standardExaminationSample))
            self.assertEqual(len(resultFilter), 1, msg='Extra data fetching')

            findElement = resultFilter[0]
            self.assertEqual(findElement['reservation_Examination_Checked'], False, msg=f'Data dublication')
            self.assertEqual(findElement['reservation_Examination']['id_prev'], curElement.id_prev, msg=f'Incorrect data examinating')
            self.standardExaminationSample[findElement['id_sample']-1]['reservation_Examination_Checked'] = True


        NotVerifiedElements = len(list(filter(lambda exam: exam['reservation_Examination_Checked'] == False, self.standardExaminationSample)))
        self.assertEqual(NotVerifiedElements, 0, msg=f'Incomplete request data')

    def test_SampleReservationWithLast_model2(self):
        datCheck = models.reservation.objects.all()

        for curElement in datCheck:
            resultFilter = list(filter(lambda exam: exam['reservation_Object'] == curElement, self.standardExaminationSample))
            self.assertEqual(len(resultFilter), 1, msg='Extra data fetching')

            findElement = resultFilter[0]
            self.assertEqual(findElement['reservation_Examination_Checked'], False, msg=f'Data dublication')
            self.assertEqual(findElement['reservation_Examination']['id_prev'], curElement.id_previos, msg=f'Incorrect data examinating')
            self.standardExaminationSample[findElement['id_sample']-1]['reservation_Examination_Checked'] = True


        NotVerifiedElements = len(list(filter(lambda exam: exam['reservation_Examination_Checked'] == False, self.standardExaminationSample)))
        self.assertEqual(NotVerifiedElements, 0, msg=f'Incomplete request data')
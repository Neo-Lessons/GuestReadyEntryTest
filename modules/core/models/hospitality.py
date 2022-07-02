from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db.models import Q, OuterRef, Subquery
import datetime

class rental(models.Model):
    name = models.CharField(max_length=300, null=False, unique=True)
    #--------------------
    _original_id = None

    def __str__(self):
        return f'{self.name} , {str(self.id)}'

    def __new__(cls, *args, **kwargs):
        if 'id' in kwargs:
            raise Exception('Create object with id was resticted')

        if len(args) > 0:
            original_id = args[0]
        else:
            original_id = None

        newOBJ = super(rental, cls).__new__(cls)
        newOBJ._original_id = original_id
        return newOBJ

    def __init__(self, *args, **kwargs):
        super(rental, self).__init__(*args, **kwargs)
        pass
        # return newINIT

    def save(self, *args, **kwargs):
        if self._original_id != None and self.id != self._original_id:
            raise Exception('Changing ID forbidden')
        else:
            if self._original_id == None and self.id != None:
                raise Exception('Direct value assignment ID forbidden')
            else:
                super(rental, self).save(*args, **kwargs)
                self._original_id = self.id
        pass

    def createReservation(self, checkin: datetime.date, checkout: datetime.date, **kwargs):
        if isinstance(checkin, datetime.date) and isinstance(checkout, datetime.date):
            if checkin < checkout:
                NewReservation = reservation()
                NewReservation.rental = self;
                NewReservation.checkin = checkin
                NewReservation.checkout = checkout
                NewReservation.save()

                return NewReservation
            else:
                raise Exception("Incorrect date interval. ")
        else:
            raise Exception("Incorrect input types date interval. ")

class reservationManager(models.Manager):

    def selectReservationWithLast(self):
    # NEO: 02.07.22 22:36 (~002) [Change query to Django pattern]
    # COMMENT: after the change, productivity decriced by 20%
    # <CHANGE> <OLD>
    #     return self.raw('SELECT gr.id, Max(rp.id) as id_prev FROM core_reservation as gr left join core_reservation as rp on rp.id_rental = gr.id_rental and gr.id > rp.id group by gr.id')
    # </OLD> <NEW>
        subQueryPrevious = reservation.objects.filter(rental_id=OuterRef('rental_id'), id__lt=OuterRef('id')).order_by('-checkin')
        return reservation.objects.all().annotate(id_prev=Subquery(subQueryPrevious.values('id')[:1], output_field=models.BigIntegerField())).select_related('rental')
    # </NEW> </CHANGE>

class reservation(models.Model):
    # -------------------
    rental = models.ForeignKey(rental, null=False, db_column='id_rental', to_field = 'id', on_delete=models.PROTECT)
    checkin = models.DateField(null=False)
    checkout = models.DateField(null=False)
    # -------------------
    _original_id = None
    # -------------------
    objects = reservationManager()

    def __new__(cls, *args, **kwargs):
        if 'id' in kwargs:
            raise Exception('Create object with id was resticted')

        if len(args) > 0:
            original_id = args[0]
        else:
            original_id = None

        newOBJ = super(reservation, cls).__new__(cls)
        newOBJ._original_id = original_id
        return newOBJ

    def __init__(self, *args, **kwargs):
        super(reservation, self).__init__(*args, **kwargs)
        pass


    def save(self, *args, **kwargs):
        if self._original_id != None and self.id != self._original_id:
            raise Exception('Changing ID forbidden')
        else:
            if self._original_id == None and self.id != None:
                raise Exception('Direct value assignment ID forbidden')
            else:
                super(reservation, self).save(*args, **kwargs)
                self._original_id = self.id
        pass

    # NEO: 02.07.22 22:35 (~000.1) [models.hospitality.reservation.id_previos (property)]
    # <CHANGE> <OLD>
    # @property
    # def id_previos(self):
    #     sample = reservation.objects.filter(rental=self.rental, id__lt=self.id).order_by('-id')[:1]
    #     if len(sample) == 0:
    #         return None
    #     else:
    #         return sample[0].id
    # </OLD> </CHANGE>

    def validateIntersection(self):
        if self._checkIntersectionExistence_root(self.rental, self.checkin, self.checkout, self) == True:
            return 'Restriction DB error: Intersection Existence for interval ' + str(self.checkin) + ' <-> ' + str(self.checkout)
        else:
            return True

    def validateFull(self):
        ErrorList = []

        resCheck = self.validateIntersection()
        if resCheck != True:
            ErrorList.append(resCheck)

        if len(ErrorList) == 0:
            return True;
        else:
            return ErrorList;

    @staticmethod
    def _checkIntersectionExistence_root(rental: rental, checkin: datetime.date, checkout: datetime.date, exsceptionElement: 'reservation' = None) -> bool:

        selfObject = Q();

        if exsceptionElement != None:
            selfObject = ~Q(id=exsceptionElement.id)


        sample = reservation.objects.filter(
            (Q(checkin__lte = checkin, checkout__gt = checkin, rental = rental)
            |Q(checkin__lt=checkout, checkout__gte=checkout, rental = rental)
            |Q(checkin__gte=checkin, checkout__lte=checkout, rental = rental))
            &selfObject
        )
        if len(sample) == 0:
            return False
        else:
            return True

    @classmethod
    def checkIntersectionExistence(cls, rental: rental, checkin: datetime.date, checkout: datetime.date) -> bool:
        return cls._checkIntersectionExistence_root(rental, checkin, checkout)

    def __str__(self):
        return f'{str(self.id)} {str(self.checkin)} {str(self.checkout)}'

@receiver(pre_save, sender=reservation)
def create_reservation(sender, instance, *args, **kwargs):
    validateResult = instance.validateFull()
    if validateResult != True:
        raise Exception(f'ERRORS: {str(instance.validateFull())}')

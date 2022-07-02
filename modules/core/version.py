VERSION = (1, 0, 0, 3)
VERSION_INFO = '.'.join(str(nv) for nv in VERSION)
__version__ = VERSION_INFO

#Vesion history

# v1.0.0.3 [modules.core] (02.07.22)
#   [ADD] (~001) separation of settings
#   [CHANGE] (~002) Change query to Django pattern

# 1.0.0.2
#     - Disabling redundant functionality:
#   [CHANGE] (~000.1) models.hospitality.reservation.id_previos (property)
#       tests for models.hospitality.reservation.id_previos (property)

#  1.0.0.1
#   - removed confusion with property names
#   - appeded restriction on manipulations with ID on model Reservation and Rental
#   - appeded test restriction on manipulation with ID at object creating
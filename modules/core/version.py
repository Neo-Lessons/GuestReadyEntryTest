VERSION = (1, 0, 0, 1)
VERSION_INFO = '.'.join(str(nv) for nv in VERSION)
__version__ = VERSION_INFO

#Vesion history

# 1.0.0.2
#     - Disabling redundant functionality:
#       models.hospitality.reservation.id_previos (property)
#       tests for models.hospitality.reservation.id_previos (property)

#  1.0.0.1
#   - removed confusion with property names
#   - appeded restriction on manipulations with ID on model Reservation and Rental
#   - appeded test restriction on manipulation with ID at object creating
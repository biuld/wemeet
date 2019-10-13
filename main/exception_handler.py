from rest_framework.serializers import ValidationError
from jwt.exceptions import ExpiredSignatureError, DecodeError
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from .serializer import Result


def handler(exp, context):

    if isinstance(exp, ObjectDoesNotExist):
        return Result.error(Result.USER_NOT_EXISTS, data=str(exp))

    if isinstance(exp, MultipleObjectsReturned):
        return Result.error(Result.MULITIPLE_OBJECT, data=str(exp))

    if isinstance(exp, DecodeError):
        return Result.error(Result.ACTC_INVALID, data=str(exp))

    if isinstance(exp, ExpiredSignatureError):
        return Result.error(Result.ACTC_EXPIRED, data=str(exp))

    if isinstance(exp, ValidationError):
        return Result.error(Result.KEY_ERROR, data=str(exp))

    return None

    
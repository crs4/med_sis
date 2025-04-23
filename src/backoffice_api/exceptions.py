
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError):
        if hasattr(exc, 'detail'):
            errors = []
            if isinstance(exc.detail, dict):
                for field, messages in exc.detail.items():
                    if isinstance(messages, list):
                        for message in messages:
                            errors.append({
                                field: str(message)
                                #'field': field,
                                #'message': str(message)
                            })
                    else:
                        errors.append({
                            field: str(message)
                            #'field': field,
                            #'message': str(messages)
                        })
            elif isinstance(exc.detail, list):
                for message in exc.detail:
                    errors.append({
                        'message': str(message)
                    })
            else:
                errors.append({
                    'message': str(exc.detail)
                })
            
            return Response(
                data={'errors': errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    return response 
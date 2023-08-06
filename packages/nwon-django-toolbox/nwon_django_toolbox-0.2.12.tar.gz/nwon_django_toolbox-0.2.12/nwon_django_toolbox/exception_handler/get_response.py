from typing import List, Union

from nwon_baseline.typings import AnyDict

from nwon_django_toolbox.typings.error_response import ErrorResponse


def get_response(
    message: str = "",
    result: Union[AnyDict, List, None] = None,
    status_code: int = 200,
) -> AnyDict:
    return ErrorResponse(
        message=message,
        result=result,
        status_code=status_code,
    ).dict()

from typing import List, Optional, Union

from nwon_baseline.typings import AnyDict

from nwon_django_toolbox.typings.pydantic_base_django import PydanticBaseDjango


class ErrorResponse(PydanticBaseDjango):
    message: str
    result: Optional[Union[List[str], List[AnyDict], AnyDict]]
    status_code: int

import typing

import strawberry
from gqlauth.bases.scalars import ExpectedErrorType


@strawberry.interface
class OutputInterface:
    """
    A class to all public classes extend to
    padronize the output
    """

    success: bool
    errors: typing.Optional[ExpectedErrorType] = None

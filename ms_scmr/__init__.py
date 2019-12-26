from uuid import UUID
from typing import Final

from rpc.structures.presentation_syntax import PresentationSyntax

MS_SCMR_ABSTRACT_SYNTAX: Final[PresentationSyntax] = PresentationSyntax(
    if_uuid=UUID('367abb81-9844-35f1-ad32-98f038001003'),
    if_version=2
)

MS_SCMR_PIPE_NAME: Final[str] = 'svcctl'

from typing import Any
from _typeshed import StrPath, NoneType

class TesseractEngine:
    '''No documentation for this class.'''
    def __init__(
        self,
        data: StrPath | NoneType = ...,
        language: str | NoneType = ...,
        mode: Any | NoneType = ...,
        /,
    ) -> NoneType: ...

class EngineMode:
    'Engine mode group for tesseractpy.TesseractEngine'

class PixConverter:
    'No documentation for this class.'

def Init() -> NoneType: ...
def BitmapFromFile(file: StrPath, *args) -> Any: ...
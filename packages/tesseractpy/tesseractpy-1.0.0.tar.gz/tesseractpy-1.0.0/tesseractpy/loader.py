'Tesseract.dll loader'

import os
import clr # type: ignore

clr.AddReference(
    os.path.join(
        os.path.dirname(__file__),
        'Tesseract.dll'
    ),
)
clr.AddReference('System.Drawing')
from System.Drawing import Image, Bitmap # type: ignore
from Tesseract import TesseractEngine, PixConverter, EngineMode # type: ignore

__all__ = (
    'TesseractEngine', 'PixConverter', 'EngineMode', 'Image', 'Bitmap'
)
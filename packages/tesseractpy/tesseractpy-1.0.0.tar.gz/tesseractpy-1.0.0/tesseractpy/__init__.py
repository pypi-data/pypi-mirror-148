'tesseractpy - Tesseract C# wrapper wrapped in Python'

from os.path import abspath
from pkgutil import iter_modules

__all__ = (
    'EngineMode',
    'TesseractEngine',
    'PixConverter',
    'BitmapFromFile',
    'Init',
)

def Init():
    modules = [module.name for module in iter_modules()]

    if 'pythonnet' not in modules:
        from subprocess import call, PIPE

        call('pip install pythonnet --pre', stdout=PIPE, stderr=PIPE)

    global EngineMode, TesseractEngine, PixConverter, Image, Bitmap
    from .loader import EngineMode, TesseractEngine, PixConverter, Image, Bitmap

    return None

def BitmapFromFile(file, *args):
    image = Image.FromFile(abspath(file))
    return Bitmap(image, *args)
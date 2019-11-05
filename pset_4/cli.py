from luigi import build
from .tasks.data import ContentImage, DownloadImage, DownloadModel
from .tasks.stylize import Stylize


def main():
    build([
        Stylize(
            model='udnie.pth',
            image='Waluigi.jpeg'
        )], local_scheduler=True)

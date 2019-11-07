from luigi import build
from .tasks.stylize import Stylize


def main():
    build([
        Stylize(
            model='udnie.pth',
            image='luigi.jpeg'
        )], local_scheduler=True)

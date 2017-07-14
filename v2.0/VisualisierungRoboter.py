from Model import *
from Controller import Controller
from Controller import FatalException
from Gui import *
import tkMessageBox
import time


def main():

    try:
        model = Model()
        controller = Controller(model)
        controller.start()
        gui = Gui(model, controller)
        gui.show()
        controller.stop()
    except FatalException, exc:
        print('Fehler', exc.getMessage())


if __name__ == '__main__':
    main()

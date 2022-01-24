"https://pysimplegui.readthedocs.io/en/latest/#checkbox-element-cbox-cb-check"

# import PySimpleGUI as sg
# import sys
# my_new_theme = {'BACKGROUND': '#9ed7a7',
#                 'TEXT': '#090a09',
#                 'INPUT': '#c7e78b',
#                 'TEXT_INPUT': '#3d463d',
#                 'SCROLL': '#c7e78b',
#                 'BUTTON': ('#333a34', '#87b98f'),
#                 'PROGRESS': ('#60aedb', '#8bbad5'),
#                 'BORDER': 1,
#                 'SLIDER_DEPTH': 0,
#                 'PROGRESS_DEPTH': 0}

# sg.theme_add_new('MyNewTheme', my_new_theme)
# sg.theme('MyNewTheme')

# layout = [
#     [sg.Text('Please enter your Name, Address, Phone'),sg.Text(size=(15,1), key='-OUTPUT-')],
#     [sg.Text('Name', size=(15, 1)), sg.Input(key ="-IN-")],
#     [sg.Text('Address', size=(15, 1)), sg.InputText(key ="-IN-")],
#     [sg.Text('Phone', size=(15, 1)), sg.InputText(key ="-IN-")],
#     [sg.Input(key ="-IN-"), sg.FileSaveAs()],
#     [sg.Button('Submit'), sg.Cancel(), sg.Button("Version")]
# ]

# window = sg.Window('Simple data entry window', layout)

# while True:
#     event, values = window.read()
#     if event == sg.WINDOW_CLOSED or event == "Cancel":
#         break
#     if event == "Version":
#         sg.popup_scrolled(sg.get_versions())
#     if event == "Submit":
#         window['-OUTPUT-'].update(values['-IN-'])
        
# window.close()



from pathlib import Path
import sys

from PySide6.QtGui import QPainter, QBrush, QColor
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import qmlRegisterType
from PySide6.QtCore import QUrl, Property, Signal, Qt, QPointF
from PySide6.QtQuick import QQuickPaintedItem, QQuickView


class TextBalloon(QQuickPaintedItem):

    rightAlignedChanged = Signal()

    def __init__(self, parent=None):
        self._rightAligned = False
        super().__init__(parent)

    @Property(bool, notify=rightAlignedChanged)
    def rightAligned(self):
        return self._rightAligned

    @rightAligned.setter
    def rightAligned(self, value):
        self._rightAligned = value
        self.rightAlignedChanged.emit()

    def paint(self, painter: QPainter):

        brush = QBrush(QColor("#007430"))

        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.setRenderHint(QPainter.Antialiasing)

        itemSize = self.size()

        painter.drawRoundedRect(0, 0, itemSize.width(), itemSize.height() - 10, 10, 10)

        if self.rightAligned:
            points = [
                QPointF(itemSize.width() - 10.0, itemSize.height() - 10.0),
                QPointF(itemSize.width() - 20.0, itemSize.height()),
                QPointF(itemSize.width() - 30.0, itemSize.height() - 10.0),
            ]
        else:
            points = [
                QPointF(10.0, itemSize.height() - 10.0),
                QPointF(20.0, itemSize.height()),
                QPointF(30.0, itemSize.height() - 10.0),
            ]
        painter.drawConvexPolygon(points)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    view = QQuickView()
    view.setResizeMode(QQuickView.SizeRootObjectToView)
    qmlRegisterType(TextBalloon, "TextBalloonPlugin", 1, 0, "TextBalloon")
    qml_file = "D:\HuyNP\Basic\IEdriver\py_side.qml"
    view.setSource(QUrl.fromLocalFile(qml_file))

    if view.status() == QQuickView.Error:
        sys.exit(-1)
    view.show()

    sys.exit(app.exec())
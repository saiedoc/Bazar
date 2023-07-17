import sys
import time
from PySide6 import QtCore, QtWidgets, QtGui


class MyWidget(QtWidgets.QWidget):
  def __init__(self):
    super().__init__()

    self.button = QtWidgets.QPushButton("Gib mir unendlich viel zutun")
    self.text = QtWidgets.QLabel("Ich tue gerade nichts (und werde erst nach behandelten Events geupdated)", alignment=QtCore.Qt.AlignCenter)

    self.layout = QtWidgets.QVBoxLayout(self)
    self.layout.addWidget(self.text)
    self.layout.addWidget(self.button)

    self.button.clicked.connect(self.magic)

  @QtCore.Slot()
  def magic(self):
    self.text.setText("Ich habe unendlich viel zutun")
    # Das Textfeld wird erst am Ende dieser Funktion geupdated.
    # Daran ändert auch die Fkt repaint nichts, denn diese legt nur ein
    # Repaint-Event in die Event-Queue
    
    while True:
      time.sleep(30)

    
if __name__ == "__main__":
  print(f"Dieses Programm wird nicht mehr reagieren, wenn man den 'Gib mir unendlich viel zutun'-Knopf bedient.")
  
  app = QtWidgets.QApplication([])

  widget = MyWidget()
  widget.resize(800, 600)
  widget.show()

  sys.exit(app.exec())

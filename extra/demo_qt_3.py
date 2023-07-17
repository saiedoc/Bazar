import sys
import time
import random
from PySide6            import QtCore, QtWidgets, QtGui
from PySide6.QtCore     import Qt, QPointF, QThread
from PySide6.QtGui      import QPainter
from PySide6.QtWidgets  import QApplication, QMainWindow
from PySide6.QtCharts   import QLineSeries, QChart, QChartView



# Ein Hintergrundtimer, welcher die gegebene Anzahl von Sekunden wartet
# Das Ende des Timers kann eine Callbackfunktion auslösen (siehe unten)
class BackgroundTimer(QThread):
  def __init__(self, duration):
    super().__init__()
    self.duration = duration
  
  def run(self):
    time.sleep(self.duration)


# Ein Widget zum Anzeigen eines dynamisch veränderlichen Verlaufsdiagrams
class MyWidget(QtWidgets.QWidget):
  def __init__(self):
    super().__init__()
    
    #
    # Knopf
    #
    self.button = QtWidgets.QPushButton("Hi ich bin ein Knopf")
    
    #
    # Verlaufsdiagram
    #
    
    # QLineSeries für Datenpunkte
    self.series = QLineSeries()  # Erzeuge Datenpunkte
    self.series.append(0, 6)    # Füge einen Datenpunkt hinzu
    self.series.append(1, 4)    # Füge einen Datenpunkt hinzu
    self.series.append(2, 8)    # Füge einen Datenpunkt hinzu
    self.series.append(3, 4)    # Füge einen Datenpunkt hinzu
    self.series.append(4, 5)    # Füge einen Datenpunkt hinzu
    # Füge mehrere Datenpunkte hinzu
    self.series << QPointF(5, 1) << QPointF(6, 3) << QPointF(7, 6)
    self.tick = 7
    
    # QChart für Beschreibung des Kurvendiagrams
    self.chart = QChart()          # Erzeuge die Beschreibung eines Kurvendiagrams
    self.chart.addSeries(self.series)   # Füge Datenpunkte hinzu
    self.chart.legend().hide()     # Verstecke Legende
    self.chart.createDefaultAxes() # Automatische Achsenbeschriftung
    self.chart.setTitle("Einfaches Kurvendiagram") # Diagramtitel
    
    # QChartView zum Darstellen des Kurvendiagrams
    self.chartView = QChartView(self.chart) # Erzeuge eine Darstellungsform des Kurvendiagrams
    self.chartView.setRenderHint(QPainter.Antialiasing)  # Kantenglättung aktivieren
    
    #
    # Layout zusammenstecken
    #
    self.layout = QtWidgets.QVBoxLayout(self)
    self.layout.addWidget(self.chartView)
    self.layout.addWidget(self.button)
    
    #
    # Subjekte und Observer verbinden
    #
    
    # Knopf
    self.button.clicked.connect(self.knopf_callback)
    
    # Hintergrundtimer
    self.backgroundtimer = BackgroundTimer(0.3)
    self.backgroundtimer.finished.connect(self.add_pt_to_chart)
    self.backgroundtimer.start() # Starte Hintergrundtimer im Hintergrund


  @QtCore.Slot()
  def knopf_callback(self):
    pass


  def add_pt_to_chart(self):
    self.tick = self.tick + 1
    self.series << QPointF(self.tick, random.randint(1, 8))
    
    # Auch wenn es nicht direkt nachvollziehbar ist, liefert die Funktion
    # axes(...) ein QList<QAbstractAxis>-Objekt.
    # Wir nehmen das letzte Element dieser Liste und das ist ein QAbstractAxis-Objekt.
    self.chart.axes(Qt.Horizontal)[-1].setMax(self.tick)
    self.chart.axes(Qt.Horizontal)[-1].setMin(max(0, self.tick-20))
    
    self.backgroundtimer.start() # Starte Hintergrundtimer im Hintergrund



if __name__ == "__main__":
  app = QtWidgets.QApplication([])

  widget = MyWidget()
  widget.resize(800, 600)
  widget.show()

  sys.exit(app.exec())

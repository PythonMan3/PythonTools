import sys
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (qApp, QApplication, QComboBox, QFormLayout,
    QHBoxLayout, QLineEdit, QMainWindow, QPushButton, QSlider, QWidget, QFileDialog, QDialog)

from PySide2.QtTextToSpeech import QTextToSpeech, QVoice

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('Voice Player')
        self.words = []

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        layout = QFormLayout(centralWidget)

        self.readButton = QPushButton('Read CSV')
        self.readButton.clicked.connect(self.readCSV)
        layout.addRow('CSV File:', self.readButton)

        textLayout = QHBoxLayout()
        self.text = QLineEdit('')
        self.text.setClearButtonEnabled(True)
        textLayout.addWidget(self.text)
        self.sayButton = QPushButton('Say')
        textLayout.addWidget(self.sayButton)
        self.text.returnPressed.connect(self.sayButton.animateClick)
        self.sayButton.clicked.connect(self.say)
        layout.addRow('Text:', textLayout)

        self.voiceCombo = QComboBox()
        self.voiceCombo.currentIndexChanged.connect(self.indexChange)
        layout.addRow('Voice:', self.voiceCombo)

        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setValue(100)
        layout.addRow('Volume:', self.volumeSlider)

        self.engine = None
        engineNames = QTextToSpeech.availableEngines()
        if len(engineNames) > 0:
            engineName = engineNames[0]
            self.engine = QTextToSpeech(engineName)
            self.engine.stateChanged.connect(self.stateChanged)
            #self.setWindowTitle('QTextToSpeech Example ({})'.format(engineName))
            #self.voices = []
            #for voice in self.engine.availableVoices():
            #    self.voices.append(voice)
            #    self.voiceCombo.addItem(voice.name())
            self.voice = self.engine.availableVoices()[0]
        else:
            self.setWindowTitle('QTextToSpeech Example (no engines available)')
            self.sayButton.setEnabled(False)

    def indexChange(self, index):
        word = self.words[self.voiceCombo.currentIndex()]
        self.text.setText(word)

    def readCSV(self):
        fileDialog = QFileDialog(self)
        fileDialog.setNameFilters(['CSV File (*.csv)'])
        if fileDialog.exec_() == QDialog.Accepted:
            csvPath = fileDialog.selectedFiles()[0]
            self.words = []
            with open(csvPath) as fi:
                for line in fi:
                    line = line.strip()
                    if not line: continue
                    self.words.append(line)
            self.voiceCombo.clear()
            for word in self.words:
                self.voiceCombo.addItem(word)
            if len(self.words):
                word = self.words[self.voiceCombo.currentIndex()]
                self.text.setText(word)

    def say(self):
        self.sayButton.setEnabled(False)
        self.engine.setVoice(self.voice)
        self.engine.setVolume(float(self.volumeSlider.value()) / 100)
        text = self.text.text().strip()
        if not text:
            self.sayButton.setEnabled(True)
        else:
            self.engine.say(self.text.text())

    def stateChanged(self, state):
        if (state == QTextToSpeech.State.Ready):
            self.sayButton.setEnabled(True)
            currIdx = self.voiceCombo.currentIndex()
            count = self.voiceCombo.count()
            if currIdx + 1 < count:
                self.voiceCombo.setCurrentIndex(currIdx+1)
                word = self.words[self.voiceCombo.currentIndex()]
                self.text.setText(word)
            else:
                self.text.setText('')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

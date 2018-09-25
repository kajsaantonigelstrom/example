import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (qApp, QAction, QMenu, QMainWindow,
    QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget,
    QPushButton, QLineEdit, QTextEdit, QListWidget, QComboBox,
    QRadioButton, QGroupBox, QCheckBox, QSlider, QProgressBar)
from PyQt5.QtCore import QSize,Qt    
from PyQt5.QtGui import QIcon

class HelloWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def btnstate(self,b):
        return
        
    def initUI(self):

        #menu statusbar 
        self.statusBar().showMessage('Ready')
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        editMenu = menubar.addMenu('Edit')

        impMenu = QMenu('Import', self)
        impAct = QAction('Import mail', self) 
        impMenu.addAction(impAct)
        
        newAct = QAction('New', self)        
        
        fileMenu.addAction(newAct)
        fileMenu.addMenu(impMenu)

        #toolbar
        exitAct = QAction(QIcon('exit.png'), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(qApp.quit)
        
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAct)

        self.setMinimumSize(QSize(180, 180))    
        self.setWindowTitle("PyQt") 
        self.setWindowIcon(QIcon('exit.png'))

        # Create Main Widget
        mainwidget = QWidget()
        self.setCentralWidget(mainwidget)

        grid = QGridLayout()     
        mainwidget.setLayout(grid)
        # Buttons
        b1 = QPushButton('QUIT', self)
        b2 = QPushButton('button with long text', self)
        grid.addWidget(b1, 1, 1)
        grid.addWidget(b2, 2, 1)
        # Enter fields
        t1 = QLabel('text input')
        t2 = QLabel('multiline input')
        t1f = QLineEdit()
        t2f = QTextEdit()
        t2f.resize(50,250);

        grid.addWidget(t1, 3, 0)
        grid.addWidget(t1f, 3, 1)
        grid.addWidget(t2, 4, 0)
        grid.addWidget(t2f, 4, 1)
        #Listbox
        l1t = QLabel('list')
        l1 = QListWidget(self)
        l1.resize(50,50);
        for i in range(6):
            l1.addItem('alt%s' % (i + 1))
        grid.addWidget(l1t, 5, 0)
        grid.addWidget(l1, 5, 1)
        #Combo
        c1t = QLabel('combo')
        c1 = QComboBox(self)
        for i in range(6):
            c1.addItem('alt%s' % (i + 1))
        grid.addWidget(c1t, 6, 0)
        grid.addWidget(c1, 6, 1)
        #Radio
        groupBox = QGroupBox('Radio')
        layout = QHBoxLayout()
        self.b1 = QRadioButton("One")
        self.b1.setChecked(True)
        self.b1.toggled.connect(lambda:self.btnstate(self.b1))
        layout.addWidget(self.b1)
		
        self.b2 = QRadioButton("Two")
        self.b2.toggled.connect(lambda:self.btnstate(self.b2))
        layout.addWidget(self.b2)
        groupBox.setLayout(layout)
        grid.addWidget(groupBox, 7,1)
        #Checkbox
        cb = QCheckBox('toggle', self)        
        grid.addWidget(cb, 8,0)
        #Slider
        s1t = QLabel('slider')
        s1 = QSlider(Qt.Horizontal)        
        grid.addWidget(s1t, 9, 0)
        grid.addWidget(s1, 9,1)
        #progress
        p1t = QLabel('progress')
        p1 = QProgressBar(self)
        p1.setValue(40)
        grid.addWidget(p1t, 10,0)
        grid.addWidget(p1, 10,1)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = HelloWindow()
    mainWin.show()
    sys.exit( app.exec_() )
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Admin\OneDrive - fer.hr\MagNet Py\GUIfile.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
from __future__ import absolute_import, division, print_function
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import pandas, math
import logging, socket, errno
import scapy.config
import scapy.layers.l2
import scapy.route
import os, csv

logging.basicConfig(format='%(asctime)s %(levelname)-5s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
    
class myThread(QtCore.QThread):
    finished = QtCore.pyqtSignal()
    addDevice = QtCore.pyqtSignal(str)
    
    def __init__(self, parent):
        super(myThread, self).__init__(parent)

    def long2net(self, arg):
        if (arg <= 0 or arg >= 0xFFFFFFFF):
            raise ValueError("illegal netmask value", hex(arg))
        return 32 - int(round(math.log(0xFFFFFFFF - arg, 2)))


    def to_CIDR_notation(self, bytes_network, bytes_netmask):
        network = scapy.utils.ltoa(bytes_network)
        netmask = self.long2net(bytes_netmask)
        net = "%s/%s" % (network, netmask)
        if netmask < 16:
            logger.warn("%s is too big. skipping" % net)
            return None
    
        return net

    # old function [not used]
    def scan_and_print_neighbors(self, net, interface, data, timeout=5):
        # save devices to file 
        
        with open(r'mkdc/NetworkMapping.txt', 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(data)
        csvFile.close()
        
        
    def run(self):
        for network, netmask, _, interface, address, _ in scapy.config.conf.route.routes:
    
            # skip loopback network and default gw
            if network == 0 or interface == 'lo' or address == '127.0.0.1' or address == '0.0.0.0':
                continue
    
            if netmask <= 0 or netmask == 0xFFFFFFFF:
                continue
    
            net = self.to_CIDR_notation(network, netmask)
    
            if net:
                timeout=5
                masterDeviceInfo = 'X ' + socket.gethostbyname(socket.gethostname()) + ' ' + socket.gethostname()
                self.addDevice.emit(masterDeviceInfo)
                try:
                    ans, unans = scapy.layers.l2.arping(net, iface=interface, timeout=timeout, verbose=False)
                    for s, r in ans.res:
                        line = r.sprintf("%Ether.src%  %ARP.psrc%")
                        try:
                            hostname = socket.gethostbyaddr(r.psrc)
                            line += " " + hostname[0]
                        except socket.herror:
                            # failed to resolve
                            line += " X"
                            pass
                        logger.info(line)
                        self.addDevice.emit(line)
                except socket.error as e:
                    if e.errno == errno.EPERM:     # Operation not permitted
                        logger.error("%s. Did you run as root?", e.strerror)
                    else:
                        raise
        
        self.finished.emit()
        
                
                
class Ui_DistributedComputingWidget(object):
    def setupUi(self, DistributedComputingWidget):
        DistributedComputingWidget.setObjectName("DistributedComputingWidget")
        DistributedComputingWidget.setFixedSize(500, 730) 
        app.aboutToQuit.connect(self.terminateThread)
        self.thread = myThread(DistributedComputingWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout(DistributedComputingWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(DistributedComputingWidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.homePage = QtWidgets.QWidget()
        self.homePage.setObjectName("homePage")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.homePage)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(4000, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.scanButton = QtWidgets.QPushButton(self.homePage)
        self.scanButton.setMinimumSize(QtCore.QSize(220, 40))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.scanButton.setFont(font)
        self.scanButton.setStyleSheet("QPushButton#scanButton\n{\nfont: 75 20pt \"MS Shell Dlg 2\";\nbackground-color: rgb(62, 120, 195);\ncolor: rgb(255, 255, 255);\nborder-radius: 10px\n}\nQPushButton#scanButton:hover:!pressed\n{\nbackground-color: rgb(62, 120, 160);\n}")
        self.scanButton.setObjectName("scanButton")
        self.horizontalLayout_2.addWidget(self.scanButton)
        spacerItem1 = QtWidgets.QSpacerItem(4000, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.stackedWidget.addWidget(self.homePage)
    
        self.selectPage = QtWidgets.QWidget()
        self.selectPage.setObjectName("selectPage")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.selectPage)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        movie = QtGui.QMovie(r"mkdc/loadingGIF.gif")
        self.layoutGIF1 = QtWidgets.QWidget(self.selectPage)
        self.layoutGIF1.setObjectName("layoutGIF1")
        self.verticalLayoutGIF1 = QtWidgets.QVBoxLayout(self.layoutGIF1)
        self.verticalLayoutGIF1.setContentsMargins(-1, -1, 1, -1)
        self.verticalLayoutGIF1.setObjectName("verticalLayoutGIF1")
        self.labelGif1 = QtWidgets.QLabel(self.layoutGIF1)
        self.labelGif1.setMinimumSize(QtCore.QSize(50, 50))
        self.labelGif1.setMaximumSize(QtCore.QSize(50, 50))
        self.labelGif1.setText("")
        self.labelGif1.setAlignment(QtCore.Qt.AlignCenter)
        self.labelGif1.setObjectName("labelGif1")
        self.labelGif1.setMovie(movie)
        self.labelGif1.setScaledContents(True)
        self.verticalLayoutGIF1.addWidget(self.labelGif1)
        self.horizontalLayout_5.addWidget(self.layoutGIF1)
        self.scanningLabel = QtWidgets.QLabel(self.selectPage)
        self.scanningLabel.setEnabled(False)
        self.scanningLabel.setMinimumSize(QtCore.QSize(260, 50))
        self.scanningLabel.setMaximumSize(QtCore.QSize(300, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.scanningLabel.setFont(font)
        self.scanningLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.scanningLabel.setObjectName("scanningLabel")
        self.horizontalLayout_5.addWidget(self.scanningLabel)
        self.layoutGIF2 = QtWidgets.QWidget(self.selectPage)
        self.layoutGIF2.setObjectName("layoutGIF2")
        self.verticalLayoutGIF2 = QtWidgets.QVBoxLayout(self.layoutGIF2)
        self.verticalLayoutGIF2.setContentsMargins(-1, -1, 1, -1)
        self.verticalLayoutGIF2.setObjectName("verticalLayoutGIF2")
        self.labelGif2 = QtWidgets.QLabel(self.layoutGIF2)
        self.labelGif2.setMinimumSize(QtCore.QSize(50, 50))
        self.labelGif2.setMaximumSize(QtCore.QSize(50, 50))
        self.labelGif2.setText("")
        self.labelGif2.setAlignment(QtCore.Qt.AlignCenter)
        self.labelGif2.setObjectName("labelGif2")
        self.labelGif2.setMovie(movie)
        self.labelGif2.setScaledContents(True)
        self.verticalLayoutGIF2.addWidget(self.labelGif2)
        self.horizontalLayout_5.addWidget(self.layoutGIF2)
        
        movie.start()
        
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.tableWidget = QtWidgets.QTableWidget(self.selectPage)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.setStyleSheet("QTableWidget::item { padding-left: 10px;\npadding-right: 10px; }")
        header = self.tableWidget.horizontalHeader() 
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.resizeColumnsToContents()
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setContentsMargins(-1, 0, 0, -1)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem2)
        self.stopContinueButton = QtWidgets.QPushButton(self.selectPage)
        self.stopContinueButton.setMinimumSize(QtCore.QSize(150, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.stopContinueButton.setFont(font)
        self.stopContinueButton.setObjectName("stopContinueButton")
        self.horizontalLayout_8.addWidget(self.stopContinueButton)
        
        self.selectButton = QtWidgets.QPushButton(self.selectPage)
        self.selectButton.setMinimumSize(QtCore.QSize(150, 40))
        self.selectButton.setFont(font)
        self.selectButton.setObjectName("selectButton")
        self.horizontalLayout_8.addWidget(self.selectButton)
        self.rescanButton = QtWidgets.QPushButton(self.selectPage)
        self.rescanButton.setMinimumSize(QtCore.QSize(150, 40))
        self.rescanButton.setFont(font)
        self.rescanButton.setObjectName("rescanButton")
        self.horizontalLayout_8.addWidget(self.rescanButton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.stackedWidget.addWidget(self.selectPage)
        
        
       
        
        ##########################
        self.setWorkersPage = QtWidgets.QWidget()
        self.setWorkersPage.setObjectName("setWorkersPage")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.setWorkersPage)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.verticalLayout_1 = QtWidgets.QVBoxLayout()
        self.verticalLayout_1.setObjectName("verticalLayout_1")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem4)
        self.infoLabel = QtWidgets.QLabel(self.setWorkersPage)
        self.infoLabel.setEnabled(False)
        self.infoLabel.setMinimumSize(QtCore.QSize(260, 30))
        self.infoLabel.setMaximumSize(QtCore.QSize(300, 30))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(50)
        self.infoLabel.setFont(font)
        self.infoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.infoLabel.setObjectName("infoLabel")
        self.horizontalLayout_10.addWidget(self.infoLabel)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem5)
        self.verticalLayout_1.addLayout(self.horizontalLayout_10)
        
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem4)
        self.infoDescriptionLabel = QtWidgets.QLabel(self.setWorkersPage)
        self.infoDescriptionLabel.setEnabled(False)
        self.infoDescriptionLabel.setMinimumSize(QtCore.QSize(260, 100))
        self.infoDescriptionLabel.setMaximumSize(QtCore.QSize(300, 100))
        self.infoDescriptionLabel.setFont(font)
        self.infoDescriptionLabel.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.infoDescriptionLabel.setObjectName("infoDescriptionLabel")
        self.horizontalLayout_12.addWidget(self.infoDescriptionLabel)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem5)
        self.verticalLayout_1.addLayout(self.horizontalLayout_12)
        
        
        self.tableWidget_1 = QtWidgets.QTableWidget(self.setWorkersPage)
        self.tableWidget_1.setObjectName("tableWidget_1")
        self.tableWidget_1.setColumnCount(4)
        self.tableWidget_1.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_1.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_1.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_1.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_1.setHorizontalHeaderItem(3, item)
        self.tableWidget_1.verticalHeader().hide()
        self.tableWidget_1.setStyleSheet("QtableWidget::item { padding-left: 10px;\npadding-right: 10px; }")
        header = self.tableWidget_1.horizontalHeader() 
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.tableWidget_1.resizeColumnsToContents()
        self.verticalLayout_1.addWidget(self.tableWidget_1)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setContentsMargins(-1, 0, 0, -1)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem4)
        self.setWorkersButton = QtWidgets.QPushButton(self.setWorkersPage)
        self.setWorkersButton.setMinimumSize(QtCore.QSize(150, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.setWorkersButton.setFont(font)
        self.setWorkersButton.setObjectName("setWorkersButton")
        self.horizontalLayout_11.addWidget(self.setWorkersButton)
        
        
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem5)
        self.verticalLayout_1.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_9.addLayout(self.verticalLayout_1)
        self.stackedWidget.addWidget(self.setWorkersPage)
        
        ##########################

        
        self.horizontalLayout.addWidget(self.stackedWidget)
        self.retranslateUi(DistributedComputingWidget)
        self.stackedWidget.setCurrentIndex(0)
        
        #Signals and slots
        self.stopContinueButton.clicked.connect(self.stopThread)
        self.scanButton.clicked.connect(self.startThread)
        self.rescanButton.clicked.connect(self.rescanNetwork)
        self.selectButton.clicked.connect(self.selectWorkers)
        self.setWorkersButton.clicked.connect(self.saveToFile)
        self.thread.finished.connect(self.done)
        self.thread.addDevice.connect(self.addDevice)
        QtCore.QMetaObject.connectSlotsByName(DistributedComputingWidget)
    
        

    def retranslateUi(self, DistributedComputingWidget):
        _translate = QtCore.QCoreApplication.translate
        DistributedComputingWidget.setWindowTitle(_translate("DistributedComputingWidget", "Distributed Computing"))
        DistributedComputingWidget.setWindowIcon(QtGui.QIcon(r'mkdc/network.png'))
        self.scanButton.setText(_translate("DistributedComputingWidget", "Scan Network"))
        self.scanningLabel.setText(_translate("DistributedComputingWidget", "Scanning network"))
        self.infoLabel.setText(_translate("DistributedComputingWidget", "Set energy efficiency mode"))
        self.infoDescriptionLabel.setText(_translate("DistributedComputingWidget", "0: none\n1: turn off the display\n2: shutdown the workers\n3: 1 + 2"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("DistributedComputingWidget", "Select"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("DistributedComputingWidget", "Worker name"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("DistributedComputingWidget", "Worker IP"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("DistributedComputingWidget", "Worker MAC"))
        item = self.tableWidget_1.horizontalHeaderItem(0)
        item.setText(_translate("DistributedComputingWidget", "EE mode"))
        item = self.tableWidget_1.horizontalHeaderItem(1)
        item.setText(_translate("DistributedComputingWidget", "Worker name"))
        item = self.tableWidget_1.horizontalHeaderItem(2)
        item.setText(_translate("DistributedComputingWidget", "Worker IP"))
        item = self.tableWidget_1.horizontalHeaderItem(3)
        item.setText(_translate("DistributedComputingWidget", "Worker MAC"))
        self.stopContinueButton.setText(_translate("DistributedComputingWidget", "Stop"))
        self.selectButton.setText(_translate("DistributedComputingWidget", "Select"))
        self.rescanButton.setText(_translate("DistributedComputingWidget", "Rescan"))
        self.setWorkersButton.setText(_translate("DistributedComputingWidget", "Set"))
    
    def terminateThread(self):
        self.thread.terminate()
            
    def rescanNetwork(self):
        self.layoutGIF1.show()
        self.layoutGIF2.show()
        self.scanningLabel.setText("Scanning network")
        self.startThread()
        
        
    def startThread(self):
        self.numberOfDevices = 0
        self.tableWidget.setRowCount(0)
        self.workersInfo = pandas.DataFrame(columns=['MAC','IPaddress', 'PCname', 'EE'])
        
        self.stopContinueButton.setEnabled(True)
        self.selectButton.setEnabled(False)
        self.rescanButton.setEnabled(False)
        self.stackedWidget.setCurrentIndex(1)
    
        self.thread.start()
        
    
    def done(self):
        self.layoutGIF1.hide()
        self.layoutGIF2.hide()
        self.scanningLabel.setText("Select workers")
        QMessageBox.information(w, "Done!", " Scanning completed!")
        self.stopContinueButton.setEnabled(False)
        self.selectButton.setEnabled(True)
        self.rescanButton.setEnabled(True)
        
    
    def addDevice(self, deviceInfo):
        deviceInfo = ['X' if info=='' else info for info in deviceInfo.split()]
        deviceInfo.append(0)
        if str(deviceInfo[1]) == get_ip(): # if host IP was found dont add it to the list of workers
            return
    
        self.workersInfo.loc[self.numberOfDevices] = deviceInfo    #number of cores for each worker set to 0
        
        self.numberOfDevices += 1
        self.tableWidget.setRowCount(self.numberOfDevices)
        
        
        qwidget = QtWidgets.QWidget()
        checkbox = QtWidgets.QCheckBox()
        checkbox.setCheckState(QtCore.Qt.Unchecked)
        qhboxlayout = QtWidgets.QHBoxLayout(qwidget)
        qhboxlayout.addWidget(checkbox)
        qhboxlayout.setAlignment(QtCore.Qt.AlignCenter)
        qhboxlayout.setContentsMargins(0, 0, 0, 0)
        self.tableWidget.setCellWidget(self.numberOfDevices-1, 0, qwidget)
            
        item1 = QtWidgets.QTableWidgetItem(str(deviceInfo[2]))
        item1.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.tableWidget.setItem(self.numberOfDevices-1, 1, item1)
            
        item2 = QtWidgets.QTableWidgetItem(str(deviceInfo[1]))
        item2.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.tableWidget.setItem(self.numberOfDevices-1, 2, item2)
            
        item3 = QtWidgets.QTableWidgetItem(str(deviceInfo[0]))
        item3.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.tableWidget.setItem(self.numberOfDevices-1, 3, item3)
        
      
    def selectWorkers(self):
        self.selectedWorkers = np.array([False]*self.numberOfDevices)
        self.selectedDevices = 0
        for i in range(self.numberOfDevices):
            if self.tableWidget.cellWidget(i, 0).findChild(type(QtWidgets.QCheckBox())).isChecked():
                self.selectedWorkers[i] = True
                
                self.tableWidget_1.setRowCount(self.selectedDevices+1)
                spinbox = QtWidgets.QSpinBox()
                spinbox.setObjectName("spinbox")
                spinbox.setMinimum(0)
                spinbox.setMaximum(3)
                spinbox.setValue(0)
                spinbox.setStyleSheet("QSpinBox#spinbox {font: 20px; padding-left: 10px;}")
                self.tableWidget_1.setCellWidget(self.selectedDevices, 0, spinbox)
                                      
                item1 = QtWidgets.QTableWidgetItem(str(self.workersInfo.PCname.iloc[i]))
                item1.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                self.tableWidget_1.setItem(self.selectedDevices, 1, item1)
                
                item2 = QtWidgets.QTableWidgetItem(str(self.workersInfo.IPaddress.iloc[i]))
                item2.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                self.tableWidget_1.setItem(self.selectedDevices, 2, item2)
                    
                item3 = QtWidgets.QTableWidgetItem(str(self.workersInfo.MAC.iloc[i]))
                item3.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                self.tableWidget_1.setItem(self.selectedDevices, 3, item3)
                
                self.selectedDevices += 1
        
        if self.selectedDevices == 0:
            QMessageBox.information(w, "Selecting", "Select at least one worker.")
            return
        
        print(self.workersInfo[["IPaddress", "PCname"]][self.selectedWorkers])
        
        self.stackedWidget.setCurrentIndex(2)
            
        
    def saveToFile(self):
        # chech if file exist
        if not os.path.isfile('mkdc/Host&Workers.csv'):
            with open("mkdc/Host&Workers.csv", "w") as my_empty_csv: # create empty csv file
                pass
        
        self.EEmode = []
        for i in range(self.selectedDevices):
            spinbox = self.tableWidget_1.cellWidget(i, 0)
            self.EEmode.append(spinbox.value())
            
        self.workersInfo.EE.iloc[self.selectedWorkers] = self.EEmode
        self.workersInfo.loc[-1] = ['X', get_ip(), 'HostPC', '0']  # add host machine
        self.workersInfo = self.workersInfo.sort_index()
        self.workersInfo[["IPaddress", "PCname","EE"]][np.insert(self.selectedWorkers, 0, True)].to_csv(r'mkdc/Host&Workers.csv', header = True, index = False)
        
        ret = QMessageBox.information(w, "Done!", "Worker(s) mode is set.\nDo you want to close the application?", QMessageBox.Yes | QMessageBox.Cancel)
        if ret==QMessageBox.Yes:
            w.close()
        
    def stopThread(self):
        self.layoutGIF1.hide()
        self.layoutGIF2.hide()
        self.stopContinueButton.setEnabled(False)
        self.selectButton.setEnabled(True)
        self.rescanButton.setEnabled(True)
        self.scanningLabel.setText("Select workers")
        self.thread.terminate()
        
class AppWindow(QDialog):
    def __init__(self):
        QDialog.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.ui = Ui_DistributedComputingWidget()
        self.ui.setupUi(self)
        self.show()  




if __name__ == "__main__":
    import sys, os
    #os.chdir('..')
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())

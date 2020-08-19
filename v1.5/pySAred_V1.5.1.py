'''
Install with:
* Windows - pyinstaller --onefile --noconsole -i"C:\icon.ico" --add-data C:\icon.ico;images C:\pySAred_V1.5.1.py
* MacOS - sudo pyinstaller --onefile --windowed pySAred_V1.5.1.py

Requirements for a nice interface:
* PyQt<=5.12.2
'''

from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import h5py, os, sys, pkgutil, platform
import pyqtgraph as pg
from scipy.interpolate import griddata

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class Ui_MainWindow(QtGui.QMainWindow):

    def __create_element(self, object, geometry, objectName, text=None, font=None, placeholder=None, visible=None, stylesheet=None, checked=None, title=None, combo=None, enabled=None):

        object.setObjectName(objectName)

        if not geometry == [999, 999, 999, 999]: object.setGeometry(QtCore.QRect(geometry[0], geometry[1], geometry[2], geometry[3]))

        if not text == None: object.setText(text)
        if not title == None: object.setTitle(title)
        if not font == None: object.setFont(font)
        if not placeholder == None: object.setPlaceholderText(placeholder)
        if not visible == None: object.setVisible(visible)
        if not checked == None: object.setChecked(checked)
        if not enabled == None: object.setEnabled(enabled)

        if not stylesheet == None: object.setStyleSheet(stylesheet)

        if not combo == None:
            for i in combo: object.addItem(str(i))

    ##--> define user interface elements
    def setupUi(self, MainWindow):

        # Fonts
        font_headline = QtGui.QFont()
        font_headline.setPointSize(11 if platform.system() == 'Windows' else 12)
        font_headline.setBold(True)

        font_button = QtGui.QFont()
        font_button.setPointSize(10 if platform.system() == 'Windows' else 11)
        font_button.setBold(True)

        font_graphs = QtGui.QFont()
        font_graphs.setPixelSize(11 if platform.system() == 'Windows' else 12)
        font_graphs.setBold(False)

        font_ee = QtGui.QFont()
        font_ee.setPointSize(8 if platform.system() == 'Windows' else 10)
        font_ee.setBold(False)

        # Main Window
        MainWindow.setObjectName("MainWindow")
        MainWindow_size = [1180, 721] if platform.system() == 'Windows' else [1180, 701]
        MainWindow.resize(MainWindow_size[0], MainWindow_size[1])
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(MainWindow_size[0], MainWindow_size[1]))
        MainWindow.setMaximumSize(QtCore.QSize(MainWindow_size[0], MainWindow_size[1]))
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowNestedDocks|QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        MainWindow.setWindowTitle("pySAred")

        # when we create .exe with pyinstaller, we need to store icon inside it. Then we find it inside unpacked temp directory.
        for i in pkgutil.iter_importers():
            path = str(i).split("'")[1].replace("\\\\", "\\") if str(i).find('FileFinder')>=0 else None
            if path != None: self.iconpath = path + "\\images\\icon.ico"
        MainWindow.setWindowIcon(QtGui.QIcon(self.iconpath))
        MainWindow.setIconSize(QtCore.QSize(30, 30))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Block: .h5 files
        self.label_h5Scans = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_h5Scans, [15, 5, 200, 20], "label_h5Scans", text=".h5 files", font=font_headline, stylesheet="QLabel { color : blue; }")
        self.groupBox_data = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_data, [10, 11, 279, 667], "groupBox_data", font=font_ee)
        self.label_dataFiles = QtWidgets.QLabel(self.groupBox_data)
        self.__create_element(self.label_dataFiles, [10, 20, 121, 21], "label_dataFiles", text="Data", font=font_headline)
        self.tableWidget_scans = QtWidgets.QTableWidget(self.groupBox_data)
        self.__create_element(self.tableWidget_scans, [10, 45, 260, 342], "tableWidget_scans", font=font_ee)
        self.tableWidget_scans.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_scans.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_scans.setAutoScroll(True)
        self.tableWidget_scans.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.tableWidget_scans.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_scans.setColumnCount(4)
        self.tableWidget_scans.setRowCount(0)
        headers_table_scans = ["Scan", "DB", "Scan_file_full_path"]
        for i in range(0,3):
            self.tableWidget_scans.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem())
            self.tableWidget_scans.horizontalHeaderItem(i).setText(headers_table_scans[i])
        self.tableWidget_scans.horizontalHeader().setVisible(True)
        self.tableWidget_scans.verticalHeader().setVisible(False)
        self.tableWidget_scans.setColumnWidth(0, 200)
        self.tableWidget_scans.setColumnWidth(1, int(self.tableWidget_scans.width()) - int(self.tableWidget_scans.columnWidth(0)) - 2)
        self.tableWidget_scans.setColumnWidth(2, 0)
        self.pushButton_deleteScans = QtWidgets.QPushButton(self.groupBox_data)
        self.__create_element(self.pushButton_deleteScans, [10, 390, 81, 20], "pushButton_deleteScans", text="Delete scans", font=font_ee)
        self.pushButton_importScans = QtWidgets.QPushButton(self.groupBox_data)
        self.__create_element(self.pushButton_importScans, [189, 390, 81, 20], "pushButton_importScans", text="Import scans", font=font_ee)
        self.label_DB_files = QtWidgets.QLabel(self.groupBox_data)
        self.__create_element(self.label_DB_files, [10, 415, 191, 23], "label_DB_files", text="Direct Beam(s)", font=font_headline)
        self.checkBox_rearrangeDbAfter = QtWidgets.QCheckBox(self.groupBox_data)
        self.__create_element(self.checkBox_rearrangeDbAfter, [10, 435, 210, 20], "checkBox_rearrangeDbAfter", text="DB's were measured after the scans", font=font_ee)
        self.tableWidget_DB = QtWidgets.QTableWidget(self.groupBox_data)
        self.__create_element(self.tableWidget_DB, [10, 455, 260, 183], "tableWidget_DB", font=font_ee)
        self.tableWidget_DB.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_DB.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_DB.setAutoScroll(True)
        self.tableWidget_DB.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.tableWidget_DB.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_DB.setColumnCount(2)
        self.tableWidget_DB.setRowCount(0)
        headers_table_db = ["Scan", "Path"]
        for i in range(0, 2):
            self.tableWidget_DB.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem())
            self.tableWidget_DB.horizontalHeaderItem(i).setText(headers_table_db[i])
        self.tableWidget_DB.horizontalHeader().setVisible(False)
        self.tableWidget_DB.verticalHeader().setVisible(False)
        self.tableWidget_DB.setColumnWidth(0, self.tableWidget_DB.width())
        self.tableWidget_DB.setColumnWidth(1, 0)
        self.tableWidget_DB.setSortingEnabled(True)
        self.pushButton_deleteDB = QtWidgets.QPushButton(self.groupBox_data)
        self.__create_element(self.pushButton_deleteDB, [10, 640, 81, 20], "pushButton_deleteDB", text="Delete DB", font=font_ee)
        self.pushButton_importDB = QtWidgets.QPushButton(self.groupBox_data)
        self.__create_element(self.pushButton_importDB, [189, 640, 81, 20], "pushButton_importDB", text="Import DB", font=font_ee)

        # Block: Sample
        self.label_sample = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_sample, [305, 5, 200, 20], "label_sample", text="Sample", font=font_headline, stylesheet="QLabel { color : blue; }")
        self.groupBox_sampleLen = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_sampleLen, [300, 11, 282, 47], "groupBox_sampleLen", font=font_ee)
        self.label_sampleLen = QtWidgets.QLabel(self.groupBox_sampleLen)
        self.__create_element(self.label_sampleLen, [10, 24, 131, 16], "label_sampleLen", text="Sample length (mm)", font=font_ee)
        self.lineEdit_sampleLen = QtWidgets.QLineEdit(self.groupBox_sampleLen)
        self.__create_element(self.lineEdit_sampleLen, [192, 22, 83, 21], "lineEdit_sampleLen", text="50")

        # Block: Reductions and Instrument settings
        self.label_reductions = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_reductions, [305, 65, 200, 16], "label_reductions", text="Reductions", font=font_headline, stylesheet="QLabel { color : blue; }")
        self.tabWidget_reductions = QtWidgets.QTabWidget(self.centralwidget)
        self.__create_element(self.tabWidget_reductions, [300, 87, 281, 226], "tabWidget_reductions", font=font_ee)
        self.tabWidget_reductions.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget_reductions.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget_reductions.setElideMode(QtCore.Qt.ElideNone)

        # Tab: Reductions
        self.tab_reductions = QtWidgets.QWidget()
        self.tab_reductions.setObjectName("tab_reductions")
        self.checkBox_reductions_divideByMonitorOrTime = QtWidgets.QCheckBox(self.tab_reductions)
        self.__create_element(self.checkBox_reductions_divideByMonitorOrTime, [10, 10, 131, 18], "checkBox_reductions_divideByMonitorOrTime", font=font_ee, text="Divide by")
        self.comboBox_reductions_divideByMonitorOrTime = QtWidgets.QComboBox(self.tab_reductions)
        self.__create_element(self.comboBox_reductions_divideByMonitorOrTime, [80, 9, 70, 20], "comboBox_reductions_divideByMonitorOrTime", font=font_ee, combo=["monitor", "time"])
        self.checkBox_reductions_normalizeByDB = QtWidgets.QCheckBox(self.tab_reductions)
        self.__create_element(self.checkBox_reductions_normalizeByDB, [10, 35, 181, 18], "checkBox_reductions_normalizeByDB", text="Normalize by direct beam", font=font_ee)
        # User will need Attenuator only with DB. Otherwice I hide this option and replace with Scale factor
        self.checkBox_reductions_attenuatorDB = QtWidgets.QCheckBox(self.tab_reductions)
        self.__create_element(self.checkBox_reductions_attenuatorDB, [10, 60, 161, 18], "checkBox_reductions_attenuatorDB", text="Direct beam attenuator", font=font_ee, checked=True, visible=False)
        self.lineEdit_reductions_attenuatorDB = QtWidgets.QLineEdit(self.tab_reductions)
        self.__create_element(self.lineEdit_reductions_attenuatorDB, [30, 85, 221, 20], "lineEdit_reductions_subtractBkg_Skip", text="", font=font_ee, placeholder="Attenuator correction factor [default 10]", visible=False)
        self.checkBox_reductions_scaleFactor = QtWidgets.QCheckBox(self.tab_reductions)
        self.__create_element(self.checkBox_reductions_scaleFactor, [10, 60, 161, 18], "checkBox_reductions_scaleFactor", text="Scale factor", font=font_ee, checked=False)
        self.lineEdit_reductions_scaleFactor = QtWidgets.QLineEdit(self.tab_reductions)
        self.__create_element(self.lineEdit_reductions_scaleFactor, [30, 85, 221, 20], "lineEdit_reductions_scaleFactor", text="",  font=font_ee, placeholder="Divide reflectivity curve by [default 10]")
        self.checkBox_reductions_subtractBkg = QtWidgets.QCheckBox(self.tab_reductions)
        self.__create_element(self.checkBox_reductions_subtractBkg, [10, 115, 231, 18], "checkBox_reductions_subtractBkg", text="Subtract background (using 1 ROI)", font=font_ee)
        self.lineEdit_reductions_subtractBkg_Skip = QtWidgets.QLineEdit(self.tab_reductions)
        self.__create_element(self.lineEdit_reductions_subtractBkg_Skip, [30, 140, 221, 20], "lineEdit_reductions_subtractBkg_Skip", text="", font=font_ee, placeholder="Skip background corr. at Qz < [default 0]")
        self.checkBox_reductions_overilluminationCorr = QtWidgets.QCheckBox(self.tab_reductions)
        self.__create_element(self.checkBox_reductions_overilluminationCorr, [10, 170, 181, 18], "checkBox_reductions_overilluminationCorr", text="Overillumination correction", font=font_ee)
        self.tabWidget_reductions.addTab(self.tab_reductions, "")
        self.tabWidget_reductions.setTabText(0, "Reductions")

        # Tab: Instrument settings
        self.tab_instrumentSettings = QtWidgets.QWidget()
        self.tab_instrumentSettings.setObjectName("tab_instrumentSettings")
        self.label_instrument_wavelength = QtWidgets.QLabel(self.tab_instrumentSettings)
        self.__create_element(self.label_instrument_wavelength, [10, 10, 111, 16], "label_instrument_wavelength", text="Wavelength (A)", font=font_ee)
        self.lineEdit_instrument_wavelength = QtWidgets.QLineEdit(self.tab_instrumentSettings)
        self.__create_element(self.lineEdit_instrument_wavelength, [225, 10, 41, 18], "lineEdit_instrument_wavelength", font=font_ee, text="5.2")
        self.label_instrument_wavelengthResolution = QtWidgets.QLabel(self.tab_instrumentSettings)
        self.__create_element(self.label_instrument_wavelengthResolution, [10, 33, 271, 16], "label_instrument_wavelengthResolution", text="Wavelength resolution (d_lambda/lambda)", font=font_ee)
        self.lineEdit_instrument_wavelengthResolution = QtWidgets.QLineEdit(self.tab_instrumentSettings)
        self.__create_element(self.lineEdit_instrument_wavelengthResolution, [225, 33, 41, 18], "lineEdit_instrument_wavelengthResolution", font=font_ee, text="0.004")
        self.label_instrument_distanceS1ToSample = QtWidgets.QLabel(self.tab_instrumentSettings)
        self.__create_element(self.label_instrument_distanceS1ToSample, [10, 56, 241, 16], "label_instrument_distanceS1ToSample", font=font_ee, text="Mono_slit to Samplle distance (mm)")
        self.lineEdit_instrument_distanceS1ToSample = QtWidgets.QLineEdit(self.tab_instrumentSettings)
        self.__create_element(self.lineEdit_instrument_distanceS1ToSample, [225, 56, 41, 18], "lineEdit_instrument_distanceS1ToSample", font=font_ee, text="2300")
        self.label_instrument_distanceS2ToSample = QtWidgets.QLabel(self.tab_instrumentSettings)
        self.__create_element(self.label_instrument_distanceS2ToSample, [10, 79, 241, 16], "label_instrument_distanceS2ToSample", font=font_ee, text="Sample_slit to Sample distance (mm)")
        self.lineEdit_instrument_distanceS2ToSample = QtWidgets.QLineEdit(self.tab_instrumentSettings)
        self.__create_element(self.lineEdit_instrument_distanceS2ToSample, [225, 79, 41, 18], "lineEdit_instrument_distanceS2ToSample", font=font_ee, text="290")
        self.label_instrument_distanceSampleToDetector = QtWidgets.QLabel(self.tab_instrumentSettings)
        self.__create_element(self.label_instrument_distanceSampleToDetector, [10, 102, 241, 16], "label_instrument_distanceSampleToDetector", font=font_ee, text="Sample to Detector distance (mm)")
        self.lineEdit_instrument_distanceSampleToDetector = QtWidgets.QLineEdit(self.tab_instrumentSettings)
        self.__create_element(self.lineEdit_instrument_distanceSampleToDetector, [225, 102, 41, 18], "lineEdit_instrument_distanceSampleToDetector", font=font_ee, text="2500")
        self.label_instrument_sampleCurvature = QtWidgets.QLabel(self.tab_instrumentSettings)
        self.__create_element(self.label_instrument_sampleCurvature, [10, 152, 241, 16], "label_instrument_sampleCurvature", font=font_ee, text="Sample curvature (in ROI) (SFM) (rad)")
        self.lineEdit_instrument_sampleCurvature = QtWidgets.QLineEdit(self.tab_instrumentSettings)
        self.__create_element(self.lineEdit_instrument_sampleCurvature, [225, 152, 41, 18], "lineEdit_instrument_sampleCurvature", font=font_ee, text="0")
        self.label_instrument_offsetFull = QtWidgets.QLabel(self.tab_instrumentSettings)
        self.__create_element(self.label_instrument_offsetFull, [10, 175, 241, 16], "label_instrument_offsetFull", font=font_ee, text="Sample angle offset (th - deg)")
        self.lineEdit_instrument_offsetFull = QtWidgets.QLineEdit(self.tab_instrumentSettings)
        self.__create_element(self.lineEdit_instrument_offsetFull, [225, 175, 41, 18], "lineEdit_instrument_offsetFull", font=font_ee, text="0")
        self.tabWidget_reductions.addTab(self.tab_instrumentSettings, "")
        self.tabWidget_reductions.setTabText(1, "Instrument / Corrections")

        # Tab: Export options
        self.tab_exportOptions = QtWidgets.QWidget()
        self.tab_exportOptions.setObjectName("tab_exportOptions")
        self.checkBox_export_addResolutionColumn = QtWidgets.QCheckBox(self.tab_exportOptions)
        self.__create_element(self.checkBox_export_addResolutionColumn, [10, 10, 260, 18], "checkBox_export_addResolutionColumn", text="Include ang. resolution column in the output file", font=font_ee, checked=True)
        self.checkBox_export_resolutionLikeSared = QtWidgets.QCheckBox(self.tab_exportOptions)
        self.__create_element(self.checkBox_export_resolutionLikeSared, [10, 35, 250, 18], "checkBox_export_resolutionLikeSared", text="Use original 'Sared' way for ang. resolution calc.", font=font_ee, checked=False)
        self.checkBox_export_removeZeros = QtWidgets.QCheckBox(self.tab_exportOptions)
        self.__create_element(self.checkBox_export_removeZeros, [10, 60, 250, 18], "checkBox_export_removeZeros", text="Remove zeros from reduced files", font=font_ee, checked=False)
        self.label_export_angle = QtWidgets.QLabel(self.tab_exportOptions)
        self.__create_element(self.label_export_angle, [10, 85, 70, 18], "label_export_angle", font=font_ee, text="Export angle:")
        self.comboBox_export_angle = QtWidgets.QComboBox(self.tab_exportOptions)
        self.__create_element(self.comboBox_export_angle, [85, 84, 70, 20], "comboBox_export_angle", font=font_ee, combo=["Qz", "Degrees", "Radians"])
        self.tabWidget_reductions.addTab(self.tab_exportOptions, "")
        self.tabWidget_reductions.setTabText(2, "Export")

        # Block: Save reduced files at
        self.label_saveAt = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_saveAt, [305, 320, 200, 20], "label_saveAt", font=font_headline, text="Save reduced files at", stylesheet="QLabel { color : blue; }")
        self.groupBox_saveAt = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_saveAt, [299, 325, 282, 48], "groupBox_saveAt", font=font_ee, title="")
        self.lineEdit_saveAt = QtWidgets.QLineEdit(self.groupBox_saveAt)
        self.__create_element(self.lineEdit_saveAt, [10, 22, 225, 22], "lineEdit_saveAt", font=font_ee, text=self.dir_current)
        self.toolButton_saveAt = QtWidgets.QToolButton(self.groupBox_saveAt)
        self.__create_element(self.toolButton_saveAt, [248, 22, 27, 22], "toolButton_saveAt", font=font_ee, text="...")

        # Button: Clear
        self.pushButton_clear = QtWidgets.QPushButton(self.centralwidget)
        self.__create_element(self.pushButton_clear, [300, 380, 88, 30], "pushButton_clear", font=font_button, text="Clear all")

        # Button: Reduce all
        self.pushButton_reduceAll = QtWidgets.QPushButton(self.centralwidget)
        self.__create_element(self.pushButton_reduceAll, [493, 380, 88, 30], "pushButton_reduceAll", font=font_button, text="Reduce all")

        # Block: Recheck following files in SFM
        self.label_recheckFilesInSFM = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_recheckFilesInSFM, [305, 490, 250, 20], "label_recheckFilesInSFM", font=font_headline, text="Recheck following files in SFM", stylesheet="QLabel { color : blue; }")
        self.groupBox_recheckFilesInSFM = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_recheckFilesInSFM, [299, 500, 282, 178], "groupBox_recheckFilesInSFM", font=font_ee, title="")
        self.listWidget_recheckFilesInSFM = QtWidgets.QListWidget(self.groupBox_recheckFilesInSFM)
        self.__create_element(self.listWidget_recheckFilesInSFM, [10, 27, 262, 143], "listWidget_recheckFilesInSFM")

        # Block: Single File Mode
        self.label_SFM = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_SFM, [596, 5, 200, 20], "label_SFM", font=font_headline, text="Single File Mode (SFM)", stylesheet="QLabel { color : blue; }")
        self.groupBox_SFM_scan = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_SFM_scan, [591, 11, 472, 47 ], "groupBox_SFM_scan", font=font_ee)
        self.label_SFM_scan = QtWidgets.QLabel(self.groupBox_SFM_scan)
        self.__create_element(self.label_SFM_scan, [10, 24, 47, 16], "label_SFM_scan", font=font_ee, text="Scan")
        self.comboBox_SFM_scan = QtWidgets.QComboBox(self.groupBox_SFM_scan)
        self.__create_element(self.comboBox_SFM_scan, [40, 22, 300, 21], "comboBox_SFM_scan", font=font_ee)
        self.label_SFM_DB = QtWidgets.QLabel(self.groupBox_SFM_scan)
        self.__create_element(self.label_SFM_DB, [360, 24, 20, 16], "label_SFM_DB", font=font_ee, text="DB")
        self.comboBox_SFM_DB = QtWidgets.QComboBox(self.groupBox_SFM_scan)
        self.__create_element(self.comboBox_SFM_DB, [380, 22, 85, 21], "comboBox_SFM_DB", font=font_ee)
        pg.setConfigOption('background', (255, 255, 255))
        pg.setConfigOption('foreground', 'k')

        # Button: Reduce SFM
        self.pushButton_reduceSFM = QtWidgets.QPushButton(self.centralwidget)
        self.__create_element(self.pushButton_reduceSFM, [1070, 28, 100, 31], "pushButton_reduceSFM", font=font_button, text="Reduce SFM")

        # Block: Detector Images and Reflectivity preview
        self.tabWidget_SFM = QtWidgets.QTabWidget(self.centralwidget)
        self.__create_element(self.tabWidget_SFM, [592, 65, 578, 613], "tabWidget_SFM", font=font_ee)

        # Tab: Detector images
        linedit_size_X = 30
        linedit_size_Y = 18
        self.tab_SFM_detectorImage = QtWidgets.QWidget()
        self.tab_SFM_detectorImage.setObjectName("tab_SFM_detectorImage")
        self.graphicsView_SFM_detectorImage_roi = pg.PlotWidget(self.tab_SFM_detectorImage, viewBox=pg.ViewBox())
        self.__create_element(self.graphicsView_SFM_detectorImage_roi, [0, 450, 577, 90], "graphicsView_SFM_detectorImage_roi")
        self.graphicsView_SFM_detectorImage_roi.hideAxis("left")
        self.graphicsView_SFM_detectorImage_roi.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_SFM_detectorImage_roi.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_SFM_detectorImage_roi.setMouseEnabled(y=False)
        self.graphicsView_SFM_detectorImage = pg.ImageView(self.tab_SFM_detectorImage, view=pg.PlotItem(viewBox=pg.ViewBox()))
        self.graphicsView_SFM_detectorImage.setGeometry(QtCore.QRect(0, 30, 577, 510))
        self.graphicsView_SFM_detectorImage.setObjectName("graphicsView_SFM_detectorImage")
        self.graphicsView_SFM_detectorImage.ui.histogram.hide()
        self.graphicsView_SFM_detectorImage.ui.menuBtn.hide()
        self.graphicsView_SFM_detectorImage.ui.roiBtn.hide()
        self.graphicsView_SFM_detectorImage.view.showAxis("left", False)
        self.graphicsView_SFM_detectorImage.view.showAxis("bottom", False)
        self.graphicsView_SFM_detectorImage.view.getViewBox().setXLink(self.graphicsView_SFM_detectorImage_roi)
        self.label_SFM_detectorImage_incidentAngle = QtWidgets.QLabel(self.tab_SFM_detectorImage)
        self.__create_element(self.label_SFM_detectorImage_incidentAngle, [10, 7, 100, 16], "label_SFM_detectorImage_incidentAngle", font=font_ee, text="Incident ang. (deg)")
        self.comboBox_SFM_detectorImage_incidentAngle = QtWidgets.QComboBox(self.tab_SFM_detectorImage)
        self.__create_element(self.comboBox_SFM_detectorImage_incidentAngle, [110, 5, 55, 20], "comboBox_SFM_detectorImage_incidentAngle", font=font_ee)
        self.label_SFM_detectorImage_polarisation = QtWidgets.QLabel(self.tab_SFM_detectorImage)
        self.__create_element(self.label_SFM_detectorImage_polarisation, [180, 7, 60, 16], "label_SFM_detectorImage_polarisation", font=font_ee, text="Polarisation")
        self.comboBox_SFM_detectorImage_polarisation = QtWidgets.QComboBox(self.tab_SFM_detectorImage)
        self.__create_element(self.comboBox_SFM_detectorImage_polarisation, [240, 5, 40, 20], "comboBox_SFM_detectorImage_polarisation", font=font_ee)
        self.label_SFM_detectorImage_colorScheme = QtWidgets.QLabel(self.tab_SFM_detectorImage)
        self.__create_element(self.label_SFM_detectorImage_colorScheme, [295, 7, 60, 16], "label_SFM_detectorImage_colorScheme", font=font_ee, text="Colors")
        self.comboBox_SFM_detectorImage_colorScheme = QtWidgets.QComboBox(self.tab_SFM_detectorImage)
        self.__create_element(self.comboBox_SFM_detectorImage_colorScheme, [330, 5, 90, 20], "comboBox_SFM_detectorImage_colorScheme", font=font_ee, combo=["Green / Blue", "White / Black"])
        self.pushButton_SFM_detectorImage_showIntegratedRoi = QtWidgets.QPushButton(self.tab_SFM_detectorImage)
        self.__create_element(self.pushButton_SFM_detectorImage_showIntegratedRoi, [445, 5, 120, 20], "pushButton_SFM_detectorImage_showIntegratedRoi", font=font_ee, text="Integrated ROI")
        self.label_SFM_detectorImage_roi = QtWidgets.QLabel(self.tab_SFM_detectorImage)
        self.__create_element(self.label_SFM_detectorImage_roi, [10, 545, 31, 16], "label_SFM_detectorImage_roi", font=font_ee, text="ROI (")
        self.checkBox_SFM_detectorImage_lockRoi = QtWidgets.QCheckBox(self.tab_SFM_detectorImage)
        self.__create_element(self.checkBox_SFM_detectorImage_lockRoi, [38, 545, 50, 16], "checkBox_SFM_detectorImage_lockRoi", text="lock):", font=font_ee)
        self.label_SFM_detectorImage_roiX_left = QtWidgets.QLabel(self.tab_SFM_detectorImage)
        self.__create_element(self.label_SFM_detectorImage_roiX_left, [85, 545, 51, 16], "label_SFM_detectorImage_roiX_left", font=font_ee, text="left")
        self.lineEdit_SFM_detectorImage_roiX_left = QtWidgets.QLineEdit(self.tab_SFM_detectorImage)
        self.__create_element(self.lineEdit_SFM_detectorImage_roiX_left, [115, 544, linedit_size_X, linedit_size_Y], "lineEdit_SFM_detectorImage_roiX_left", font=font_ee)
        self.label_SFM_detectorImage_roiX_right = QtWidgets.QLabel(self.tab_SFM_detectorImage)
        self.__create_element(self.label_SFM_detectorImage_roiX_right, [85, 565, 51, 16], "label_SFM_detectorImage_roiX_right", font=font_ee, text="right")
        self.lineEdit_SFM_detectorImage_roiX_right = QtWidgets.QLineEdit(self.tab_SFM_detectorImage)
        self.__create_element(self.lineEdit_SFM_detectorImage_roiX_right, [115, 564, linedit_size_X, linedit_size_Y], "lineEdit_SFM_detectorImage_roiX_right", font=font_ee)
        self.label_SFM_detectorImage_roiY_bottom = QtWidgets.QLabel(self.tab_SFM_detectorImage)
        self.__create_element(self.label_SFM_detectorImage_roiY_bottom, [155, 545, 51, 16], "label_SFM_detectorImage_roiY_bottom", font=font_ee, text="bottom")
        self.lineEdit_SFM_detectorImage_roiY_bottom = QtWidgets.QLineEdit(self.tab_SFM_detectorImage)
        self.__create_element(self.lineEdit_SFM_detectorImage_roiY_bottom, [195, 544, linedit_size_X, linedit_size_Y], "lineEdit_SFM_detectorImage_roiY_bottom", font=font_ee)
        self.label_SFM_detectorImage_roiY_top = QtWidgets.QLabel(self.tab_SFM_detectorImage)
        self.__create_element(self.label_SFM_detectorImage_roiY_top, [155, 565, 51, 16], "label_SFM_detectorImage_roiY_top", font=font_ee, text="top")
        self.lineEdit_SFM_detectorImage_roiY_top = QtWidgets.QLineEdit(self.tab_SFM_detectorImage)
        self.__create_element(self.lineEdit_SFM_detectorImage_roiY_top, [195, 564, linedit_size_X, linedit_size_Y], "lineEdit_SFM_detectorImage_roiY_top", font=font_ee)
        self.label_SFM_detectorImage_roi_bkg = QtWidgets.QLabel(self.tab_SFM_detectorImage)
        self.__create_element(self.label_SFM_detectorImage_roi_bkg, [245, 545, 47, 16], "label_SFM_detectorImage_roi_bkg", font=font_ee, text="BKG:")
        self.label_SFM_detectorImage_roi_bkgX_left = QtWidgets.QLabel(self.tab_SFM_detectorImage)
        self.__create_element(self.label_SFM_detectorImage_roi_bkgX_left, [270, 545, 51, 16], "label_SFM_detectorImage_roi_bkgX_left", font=font_ee, text="left")
        self.lineEdit_SFM_detectorImage_roi_bkgX_left = QtWidgets.QLineEdit(self.tab_SFM_detectorImage)
        self.__create_element(self.lineEdit_SFM_detectorImage_roi_bkgX_left, [300, 544, linedit_size_X, linedit_size_Y], "lineEdit_SFM_detectorImage_roi_bkgX_left", font=font_ee, enabled=False, stylesheet="color:rgb(0,0,0)")
        self.label_SFM_detectorImage_roi_bkgX_right = QtWidgets.QLabel(self.tab_SFM_detectorImage)
        self.__create_element(self.label_SFM_detectorImage_roi_bkgX_right, [270, 565, 51, 16], "label_SFM_detectorImage_roi_bkgX_right", font=font_ee, text="right")
        self.lineEdit_SFM_detectorImage_roi_bkgX_right = QtWidgets.QLineEdit(self.tab_SFM_detectorImage)
        self.__create_element(self.lineEdit_SFM_detectorImage_roi_bkgX_right, [300, 564, linedit_size_X, linedit_size_Y], "lineEdit_SFM_detectorImage_roi_bkgX_right", font=font_ee)
        self.label_SFM_detectorImage_time = QtWidgets.QLabel(self.tab_SFM_detectorImage)
        self.__create_element(self.label_SFM_detectorImage_time, [350, 545, 71, 16], "label_SFM_detectorImage_time", font=font_ee, text="Time (s):")
        self.lineEdit_SFM_detectorImage_time = QtWidgets.QLineEdit(self.tab_SFM_detectorImage)
        self.__create_element(self.lineEdit_SFM_detectorImage_time, [400, 544, linedit_size_X, linedit_size_Y], "lineEdit_SFM_detectorImage_time", font=font_ee, enabled=False, stylesheet="color:rgb(0,0,0)")
        self.label_SFM_detectorImage_slits = QtWidgets.QLabel(self.tab_SFM_detectorImage)
        self.__create_element(self.label_SFM_detectorImage_slits, [450, 545, 51, 16], "label_SFM_detectorImage_slits", font=font_ee, text="Slits (mm):")
        self.label_SFM_detectorImage_slits_s1hg = QtWidgets.QLabel(self.tab_SFM_detectorImage)
        self.__create_element(self.label_SFM_detectorImage_slits_s1hg, [505, 545, 41, 16], "label_SFM_detectorImage_slits_s1hg", font=font_ee, text="s1hg")
        self.lineEdit_SFM_detectorImage_slits_s1hg = QtWidgets.QLineEdit(self.tab_SFM_detectorImage)
        self.__create_element(self.lineEdit_SFM_detectorImage_slits_s1hg, [535, 544, linedit_size_X, linedit_size_Y], "lineEdit_SFM_detectorImage_slits_s1hg", font=font_ee, enabled=False, stylesheet="color:rgb(0,0,0)")
        self.label_SFM_detectorImage_slits_s2hg = QtWidgets.QLabel(self.tab_SFM_detectorImage)
        self.__create_element(self.label_SFM_detectorImage_slits_s2hg, [505, 565, 30, 16], "label_SFM_detectorImage_slits_s2hg", font=font_ee, text="s2hg")
        self.lineEdit_SFM_detectorImage_slits_s2hg = QtWidgets.QLineEdit(self.tab_SFM_detectorImage)
        self.__create_element(self.lineEdit_SFM_detectorImage_slits_s2hg, [535, 564, linedit_size_X, linedit_size_Y], "lineEdit_SFM_detectorImage_slits_s2hg", font=font_ee, enabled=False, stylesheet="color:rgb(0,0,0)")
        self.tabWidget_SFM.addTab(self.tab_SFM_detectorImage, "")
        self.tabWidget_SFM.setTabText(self.tabWidget_SFM.indexOf(self.tab_SFM_detectorImage), "Detector Image")

        # Tab: Reflectivity preview
        self.tab_SFM_reflectivityPreview = QtWidgets.QWidget()
        self.tab_SFM_reflectivityPreview.setObjectName("tabreflectivity_preview")
        self.graphicsView_SFM_reflectivityPreview = pg.PlotWidget(self.tab_SFM_reflectivityPreview)
        self.__create_element(self.graphicsView_SFM_reflectivityPreview, [0, 20, 577, 540], "graphicsView_SFM_reflectivityPreview")
        self.graphicsView_SFM_reflectivityPreview.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_SFM_reflectivityPreview.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_SFM_reflectivityPreview.getAxis("left").tickFont = font_graphs
        self.graphicsView_SFM_reflectivityPreview.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_SFM_reflectivityPreview.showAxis("top")
        self.graphicsView_SFM_reflectivityPreview.getAxis("top").setTicks([])
        self.graphicsView_SFM_reflectivityPreview.showAxis("right")
        self.graphicsView_SFM_reflectivityPreview.getAxis("right").setTicks([])
        self.checkBox_SFM_reflectivityPreview_showOverillumination = QtWidgets.QCheckBox(self.tab_SFM_reflectivityPreview)
        self.__create_element(self.checkBox_SFM_reflectivityPreview_showOverillumination, [10, 6, 140, 18], "checkBox_SFM_reflectivityPreview_showOverillumination", text="Show Overillumination", font=font_ee)
        self.checkBox_SFM_reflectivityPreview_showZeroLevel = QtWidgets.QCheckBox(self.tab_SFM_reflectivityPreview)
        self.__create_element(self.checkBox_SFM_reflectivityPreview_showZeroLevel, [150, 6, 150, 18], "checkBox_SFM_reflectivityPreview_showZeroLevel", text="Show Zero level", font=font_ee)
        self.label_SFM_reflectivityPreview_view_reflectivity = QtWidgets.QLabel(self.tab_SFM_reflectivityPreview)
        self.__create_element(self.label_SFM_reflectivityPreview_view_reflectivity, [320, 7, 100, 16], "label_SFM_reflectivityPreview_view_reflectivity", text="View: Reflectivity", font=font_ee)
        self.comboBox_SFM_reflectivityPreview_view_reflectivity = QtWidgets.QComboBox(self.tab_SFM_reflectivityPreview)
        self.__create_element(self.comboBox_SFM_reflectivityPreview_view_reflectivity, [410, 5, 50, 20], "comboBox_SFM_reflectivityPreview_view_reflectivity", font=font_ee, combo=["Log", "Lin"])
        self.label_SFM_reflectivityPreview_view_angle = QtWidgets.QLabel(self.tab_SFM_reflectivityPreview)
        self.__create_element(self.label_SFM_reflectivityPreview_view_angle, [470, 7, 50, 16], "label_SFM_reflectivityPreview_view_angle", text="vs Angle", font=font_ee)
        self.comboBox_SFM_reflectivityPreview_view_angle = QtWidgets.QComboBox(self.tab_SFM_reflectivityPreview)
        self.__create_element(self.comboBox_SFM_reflectivityPreview_view_angle, [515, 5, 50, 20], "comboBox_SFM_reflectivityPreview_view_angle", font=font_ee, combo=["Qz", "Deg"])
        self.checkBox_SFM_reflectivityPreview_includeErrorbars = QtWidgets.QCheckBox(self.tab_SFM_reflectivityPreview)
        self.__create_element(self.checkBox_SFM_reflectivityPreview_includeErrorbars, [10, 565, 111, 18], "checkBox_SFM_reflectivityPreview_includeErrorbars", text="Include Error Bars", font=font_ee)
        self.label_SFM_reflectivityPreview_skipPoints_left = QtWidgets.QLabel(self.tab_SFM_reflectivityPreview)
        self.__create_element(self.label_SFM_reflectivityPreview_skipPoints_left, [372, 565, 100, 16], "label_SFM_reflectivityPreview_skipPoints_left", text="Points to skip:  left", font=font_ee)
        self.lineEdit_SFM_reflectivityPreview_skipPoints_left = QtWidgets.QLineEdit(self.tab_SFM_reflectivityPreview)
        self.__create_element(self.lineEdit_SFM_reflectivityPreview_skipPoints_left, [470, 565, linedit_size_X, linedit_size_Y], "lineEdit_SFM_reflectivityPreview_skipPoints_left", text="0", font=font_ee)
        self.label_SFM_reflectivityPreview_skipPoints_right = QtWidgets.QLabel(self.tab_SFM_reflectivityPreview)
        self.__create_element(self.label_SFM_reflectivityPreview_skipPoints_right, [510, 565, 80, 16], "label_SFM_reflectivityPreview_skipPoints_right", text="right", font=font_ee)
        self.lineEdit_SFM_reflectivityPreview_skipPoints_right = QtWidgets.QLineEdit(self.tab_SFM_reflectivityPreview)
        self.__create_element(self.lineEdit_SFM_reflectivityPreview_skipPoints_right, [535, 565, linedit_size_X, linedit_size_Y], "lineEdit_SFM_reflectivityPreview_skipPoints_right", text="0", font=font_ee)
        self.tabWidget_SFM.addTab(self.tab_SFM_reflectivityPreview, "")
        self.tabWidget_SFM.setTabText(self.tabWidget_SFM.indexOf(self.tab_SFM_reflectivityPreview), "Reflectivity preview")

        # Tab: 2D Map
        self.tab_2Dmap = QtWidgets.QWidget()
        self.tab_2Dmap.setObjectName("tab_2Dmap")
        # scaling options are different for different views
        # "scale" for "Qx vs Qz"
        self.label_SFM_2Dmap_QxzThreshold = QtWidgets.QLabel(self.tab_2Dmap)
        self.__create_element(self.label_SFM_2Dmap_QxzThreshold, [5, 7, 220, 16], "label_SFM_2Dmap_QxzThreshold", text="Threshold for the view (number of neutrons):", font=font_ee, visible=False)
        self.comboBox_SFM_2Dmap_QxzThreshold = QtWidgets.QComboBox(self.tab_2Dmap)
        self.__create_element(self.comboBox_SFM_2Dmap_QxzThreshold, [230, 5, 40, 20], "comboBox_SFM_2Dmap_QxzThreshold", font=font_ee, visible=False, combo=[1, 2, 5, 10])
        self.label_SFM_2Dmap_view_scale = QtWidgets.QLabel(self.tab_2Dmap)
        self.__create_element(self.label_SFM_2Dmap_view_scale, [183, 7, 40, 16], "label_SFM_2Dmap_view_scale", text="View", font=font_ee)
        self.comboBox_SFM_2Dmap_view_scale = QtWidgets.QComboBox(self.tab_2Dmap)
        self.__create_element(self.comboBox_SFM_2Dmap_view_scale, [210, 5, 50, 20], "comboBox_SFM_2Dmap_view_scale", font=font_ee, combo=["Log", "Lin"])
        self.label_SFM_2Dmap_polarisation = QtWidgets.QLabel(self.tab_2Dmap)
        self.__create_element(self.label_SFM_2Dmap_polarisation, [284, 7, 71, 16], "label_SFM_2Dmap_polarisation", text="Polarisation", font=font_ee)
        self.comboBox_SFM_2Dmap_polarisation = QtWidgets.QComboBox(self.tab_2Dmap)
        self.__create_element(self.comboBox_SFM_2Dmap_polarisation, [344, 5, 40, 20], "comboBox_SFM_2Dmap_polarisation", font=font_ee)
        self.label_SFM_2Dmap_axes = QtWidgets.QLabel(self.tab_2Dmap)
        self.__create_element(self.label_SFM_2Dmap_axes, [405, 7, 71, 16], "label_SFM_2Dmap_axes", text="Axes", font=font_ee)
        self.comboBox_SFM_2Dmap_axes = QtWidgets.QComboBox(self.tab_2Dmap)
        self.__create_element(self.comboBox_SFM_2Dmap_axes, [435, 5, 130, 20], "comboBox_SFM_2Dmap_axes", font=font_ee, combo=["Pixel vs. Point", "Alpha_i vs. Alpha_f", "Qx vs. Qz"])
        self.graphicsView_SFM_2Dmap = pg.ImageView(self.tab_2Dmap, view=pg.PlotItem())
        self.__create_element(self.graphicsView_SFM_2Dmap, [0, 30, 577, 522], "graphicsView_SFM_2Dmap")
        self.graphicsView_SFM_2Dmap.ui.menuBtn.hide()
        self.graphicsView_SFM_2Dmap.ui.roiBtn.hide()
        colmap = pg.ColorMap(np.array([0, 0.3333, 0.6666, 1]), np.array([[0, 0, 0, 255],[185, 0, 0, 255],[255, 220, 0, 255], [255, 255, 255, 255]], dtype=np.ubyte))
        self.graphicsView_SFM_2Dmap.setColorMap(colmap)
        self.graphicsView_SFM_2Dmap.view.showAxis("left")
        self.graphicsView_SFM_2Dmap.view.getAxis("left").tickFont = font_graphs
        self.graphicsView_SFM_2Dmap.view.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_SFM_2Dmap.view.showAxis("bottom")
        self.graphicsView_SFM_2Dmap.view.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_SFM_2Dmap.view.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_SFM_2Dmap.view.showAxis("top")
        self.graphicsView_SFM_2Dmap.view.getAxis("top").setTicks([])
        self.graphicsView_SFM_2Dmap.view.showAxis("right")
        self.graphicsView_SFM_2Dmap.view.getAxis("right").setTicks([])
        self.graphicsView_SFM_2Dmap.getView().getViewBox().invertY(b=False)

        # 2D map for "Qx vs Qz" is a plot, compared to "Pixel vs Points" which is Image.
        # I rescale graphicsView_SFM_2Dmap_Qxz_theta to show/hide it
        self.graphicsView_SFM_2Dmap_Qxz_theta = pg.PlotWidget(self.tab_2Dmap)
        self.__create_element(self.graphicsView_SFM_2Dmap_Qxz_theta, [0, 0, 0, 0], "graphicsView_SFM_2Dmap_Qxz_theta")
        self.graphicsView_SFM_2Dmap_Qxz_theta.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_SFM_2Dmap_Qxz_theta.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_SFM_2Dmap_Qxz_theta.getAxis("left").tickFont = font_graphs
        self.graphicsView_SFM_2Dmap_Qxz_theta.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_SFM_2Dmap_Qxz_theta.showAxis("top")
        self.graphicsView_SFM_2Dmap_Qxz_theta.getAxis("top").setTicks([])
        self.graphicsView_SFM_2Dmap_Qxz_theta.showAxis("right")
        self.graphicsView_SFM_2Dmap_Qxz_theta.getAxis("right").setTicks([])
        self.label_SFM_2Dmap_lowerNumberOfPointsBy = QtWidgets.QLabel(self.tab_2Dmap)
        self.__create_element(self.label_SFM_2Dmap_lowerNumberOfPointsBy, [5, 561, 211, 16], "label_SFM_2Dmap_lowerNumberOfPointsBy", text="Lower the number of points by factor", font=font_ee, visible=False)
        self.comboBox_SFM_2Dmap_lowerNumberOfPointsBy = QtWidgets.QComboBox(self.tab_2Dmap)
        self.__create_element(self.comboBox_SFM_2Dmap_lowerNumberOfPointsBy, [195, 559, 40, 20], "comboBox_SFM_2Dmap_lowerNumberOfPointsBy", font=font_ee, visible=False, combo=[5, 4, 3, 2, 1])
        self.label_SFM_2Dmap_rescaleImage_x = QtWidgets.QLabel(self.tab_2Dmap)
        self.__create_element(self.label_SFM_2Dmap_rescaleImage_x, [5, 561, 85, 16], "label_SFM_2Dmap_rescaleImage_x", text="Rescale image: x", font=font_ee)
        self.horizontalSlider_SFM_2Dmap_rescaleImage_x = QtWidgets.QSlider(self.tab_2Dmap)
        self.__create_element(self.horizontalSlider_SFM_2Dmap_rescaleImage_x, [95, 560, 80, 22], "horizontalSlider_SFM_2Dmap_rescaleImage_x")
        self.horizontalSlider_SFM_2Dmap_rescaleImage_x.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_SFM_2Dmap_rescaleImage_x.setMinimum(1)
        self.horizontalSlider_SFM_2Dmap_rescaleImage_x.setMaximum(15)
        self.horizontalSlider_SFM_2Dmap_rescaleImage_x.setValue(1)
        self.label_SFM_2Dmap_rescaleImage_y = QtWidgets.QLabel(self.tab_2Dmap)
        self.__create_element(self.label_SFM_2Dmap_rescaleImage_y, [185, 561, 20, 16], "label_SFM_2Dmap_rescaleImage_y", text="y", font=font_ee)
        self.horizontalSlider_SFM_2Dmap_rescaleImage_y = QtWidgets.QSlider(self.tab_2Dmap)
        self.__create_element(self.horizontalSlider_SFM_2Dmap_rescaleImage_y, [195, 560, 80, 22], "horizontalSlider_SFM_2Dmap_rescaleImage_y")
        self.horizontalSlider_SFM_2Dmap_rescaleImage_y.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_SFM_2Dmap_rescaleImage_y.setMinimum(1)
        self.horizontalSlider_SFM_2Dmap_rescaleImage_y.setMaximum(15)
        self.horizontalSlider_SFM_2Dmap_rescaleImage_y.setValue(1)
        self.pushButton_SFM_2Dmap_export = QtWidgets.QPushButton(self.tab_2Dmap)
        self.__create_element(self.pushButton_SFM_2Dmap_export, [445, 555, 120, 25], "pushButton_SFM_2Dmap_export", text="Export 2D map", font=font_button)
        self.tabWidget_SFM.addTab(self.tab_2Dmap, "")
        self.tabWidget_SFM.setTabText(self.tabWidget_SFM.indexOf(self.tab_2Dmap), "2D map")

        # StatusBar
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # MenuBar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.__create_element(self.menubar, [0, 0, 1000, 21], "menubar")
        self.menu_help = QtWidgets.QMenu(self.menubar)
        self.__create_element(self.menu_help, [999, 999, 999, 999], "menu_help", title="Help")
        MainWindow.setMenuBar(self.menubar)
        self.action_version = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_version, [999, 999, 999, 999], "action_version", text="V1.5.1")
        self.menu_help.addAction(self.action_version)
        self.menubar.addAction(self.menu_help.menuAction())

        self.tabWidget_reductions.setCurrentIndex(0)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    ##<--

class GUI(Ui_MainWindow):

    dir_current = ""
    if platform.system() == 'Windows': dir_current = os.getcwd().replace("\\", "/") + "/"
    else:
        for i in sys.argv[0].split("/")[:-4]: dir_current += i + "/"

    def __init__(self):

        super(GUI, self).__init__()
        self.setupUi(self)

        # Some parameters
        self.roiLocked = []
        self.SFM_FILE, self.SFMFileAlreadyAnalized, self.SFMFile2dCalculatedParams = "", "", []  # current file in Single File Mode
        self.SFM_psdUU, self.SFM_psdDU, self.SFM_psdUD, self.SFM_psdDD = [], [], [], []             # 2d arrays of pol detector
        self.th_current = ""                                                                            # current th point
        self.dict_overillCoeff = {}                                                                     # write calculated overillumination coefficients into library
        self.DB_INFO, self.dbAlreadyAnalized = {}, []                                                 # Write DB info into library
        self.roi_draw, self.roi_draw_bkg, self.roi_draw_2Dmap = [], [], []                             # ROI frames
        self.roi_oldCoord_Y, self.roi_draw_int = [], []                                                # Recalc intens if Y roi is changed
        self.trigger_showDetInt = True                                                                # Trigger to switch the detector image view
        self.res_aif = []                                                                               # Alpha_i vs Alpha_f array
        self.sampleCurvature_last = []                                                               # Last sample curvature (lets avoid extra recalcs)

        # Triggers
        self.action_version.triggered.connect(self.f_menu_info)

        # Triggers: Buttons
        self.pushButton_importScans.clicked.connect(self.f_button_importRemoveScans)
        self.pushButton_deleteScans.clicked.connect(self.f_button_importRemoveScans)
        self.pushButton_importDB.clicked.connect(self.f_button_importRemoveDB)
        self.pushButton_deleteDB.clicked.connect(self.f_button_importRemoveDB)
        self.toolButton_saveAt.clicked.connect(self.f_button_saveDir)
        self.pushButton_reduceAll.clicked.connect(self.f_button_reduceAll)
        self.pushButton_reduceSFM.clicked.connect(self.f_button_reduceSFM)
        self.pushButton_clear.clicked.connect(self.f_button_clear)
        self.pushButton_SFM_2Dmap_export.clicked.connect(self.f_SFM_2Dmap_export)
        self.pushButton_SFM_detectorImage_showIntegratedRoi.clicked.connect(self.f_SFM_detectorImage_draw)

        # Triggers: LineEdits
        arr_LE_roi = [self.lineEdit_SFM_detectorImage_roiX_left, self.lineEdit_SFM_detectorImage_roiX_right, self.lineEdit_SFM_detectorImage_roiY_bottom, self.lineEdit_SFM_detectorImage_roiY_top, self.lineEdit_SFM_detectorImage_roi_bkgX_right]
        arr_LE_instr = [self.lineEdit_instrument_wavelength, self.lineEdit_instrument_distanceSampleToDetector, self.lineEdit_instrument_sampleCurvature]
        arr_LE_otherParam = [self.lineEdit_sampleLen, self.lineEdit_reductions_attenuatorDB, self.lineEdit_reductions_scaleFactor, self.lineEdit_reductions_subtractBkg_Skip,  self.lineEdit_instrument_wavelengthResolution, self.lineEdit_instrument_distanceS1ToSample, self.lineEdit_instrument_distanceS2ToSample, self.lineEdit_instrument_offsetFull, self.lineEdit_SFM_reflectivityPreview_skipPoints_right, self.lineEdit_SFM_reflectivityPreview_skipPoints_left]

        [i.editingFinished.connect(self.f_SFM_roi_update) for i in arr_LE_roi]
        [i.editingFinished.connect(self.f_SFM_reflectivityPreview_load) for i in arr_LE_otherParam + arr_LE_instr]
        [i.editingFinished.connect(self.f_SFM_2Dmap_draw) for i in arr_LE_instr + arr_LE_roi]

        # Triggers: ComboBoxes
        self.comboBox_SFM_detectorImage_incidentAngle.currentIndexChanged.connect(self.f_SFM_detectorImage_draw)
        self.comboBox_SFM_detectorImage_polarisation.currentIndexChanged.connect(self.f_SFM_detectorImage_draw)
        self.comboBox_SFM_detectorImage_colorScheme.currentIndexChanged.connect(self.f_SFM_detectorImage_draw)

        self.comboBox_SFM_scan.currentIndexChanged.connect(self.f_SFM_detectorImage_load)

        self.comboBox_reductions_divideByMonitorOrTime.currentIndexChanged.connect(self.f_SFM_reflectivityPreview_load)
        self.comboBox_export_angle.currentIndexChanged.connect(self.f_SFM_reflectivityPreview_load)
        self.comboBox_SFM_DB.currentIndexChanged.connect(self.f_SFM_reflectivityPreview_load)
        self.comboBox_SFM_scan.currentIndexChanged.connect(self.f_SFM_reflectivityPreview_load)
        self.comboBox_SFM_reflectivityPreview_view_angle.currentIndexChanged.connect(self.f_SFM_reflectivityPreview_load)
        self.comboBox_SFM_reflectivityPreview_view_reflectivity.currentIndexChanged.connect(self.f_SFM_reflectivityPreview_load)

        self.comboBox_SFM_2Dmap_QxzThreshold.currentIndexChanged.connect(self.f_SFM_2Dmap_draw)
        self.comboBox_SFM_2Dmap_polarisation.currentIndexChanged.connect(self.f_SFM_2Dmap_draw)
        self.comboBox_SFM_2Dmap_axes.currentIndexChanged.connect(self.f_SFM_2Dmap_draw)
        self.comboBox_SFM_scan.currentIndexChanged.connect(self.f_SFM_2Dmap_draw)
        self.comboBox_SFM_2Dmap_lowerNumberOfPointsBy.currentIndexChanged.connect(self.f_SFM_2Dmap_draw)
        self.comboBox_SFM_2Dmap_view_scale.currentIndexChanged.connect(self.f_SFM_2Dmap_draw)

        self.comboBox_reductions_divideByMonitorOrTime.currentIndexChanged.connect(self.f_DB_analaze)


        # Triggers: CheckBoxes
        self.checkBox_reductions_divideByMonitorOrTime.stateChanged.connect(self.f_DB_analaze)
        self.checkBox_reductions_divideByMonitorOrTime.stateChanged.connect(self.f_SFM_reflectivityPreview_load)
        self.checkBox_reductions_normalizeByDB.stateChanged.connect(self.f_DB_analaze)
        self.checkBox_reductions_normalizeByDB.stateChanged.connect(self.f_SFM_reflectivityPreview_load)
        self.checkBox_reductions_attenuatorDB.stateChanged.connect(self.f_SFM_reflectivityPreview_load)
        self.checkBox_reductions_overilluminationCorr.stateChanged.connect(self.f_SFM_reflectivityPreview_load)
        self.checkBox_reductions_subtractBkg.stateChanged.connect(self.f_SFM_reflectivityPreview_load)
        self.checkBox_reductions_subtractBkg.stateChanged.connect(self.f_SFM_detectorImage_draw)
        self.checkBox_SFM_reflectivityPreview_showOverillumination.stateChanged.connect(self.f_SFM_reflectivityPreview_load)
        self.checkBox_SFM_reflectivityPreview_showZeroLevel.stateChanged.connect(self.f_SFM_reflectivityPreview_load)
        self.checkBox_SFM_reflectivityPreview_includeErrorbars.stateChanged.connect(self.f_SFM_reflectivityPreview_load)
        self.checkBox_rearrangeDbAfter.stateChanged.connect(self.f_SFM_reflectivityPreview_load)
        self.checkBox_rearrangeDbAfter.stateChanged.connect(self.f_DB_assign)
        self.checkBox_reductions_scaleFactor.stateChanged.connect(self.f_SFM_reflectivityPreview_load)
        self.checkBox_export_resolutionLikeSared.stateChanged.connect(self.f_SFM_reflectivityPreview_load)
        self.checkBox_export_addResolutionColumn.stateChanged.connect(self.f_SFM_reflectivityPreview_load)

        # Triggers: Sliders
        self.horizontalSlider_SFM_2Dmap_rescaleImage_x.valueChanged.connect(self.f_SFM_2Dmap_draw)
        self.horizontalSlider_SFM_2Dmap_rescaleImage_y.valueChanged.connect(self.f_SFM_2Dmap_draw)

    ##--> menu options
    def f_menu_info(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowIcon(QtGui.QIcon(self.iconpath))
        msgBox.setText("pySAred " + self.action_version.text() + "\n\n"
                       "Alexey.Klechikov@gmail.com\n\n"
                       "Check new version at https://github.com/Alexey-Klechikov/pySAred/releases")
        msgBox.exec_()
    ##<--

    ##--> Main window buttons
    def f_button_importRemoveScans(self):

        if self.sender().objectName() == "pushButton_importScans":

            files_import = QtWidgets.QFileDialog().getOpenFileNames(None, "FileNames", self.dir_current, ".h5 (*.h5)")
            if files_import[0] == []: return
            # Next "Import scans" will open last dir
            self.dir_current = files_import[0][0][:files_import[0][0].rfind("/")]

            for FILE in files_import[0]:
                self.tableWidget_scans.insertRow(self.tableWidget_scans.rowCount())
                self.tableWidget_scans.setRowHeight(self.tableWidget_scans.rowCount()-1, 10)
                # File name (row 0) and full path (row 2)
                for j in range(0, 3): self.tableWidget_scans.setItem(self.tableWidget_scans.rowCount()-1, j, QtWidgets.QTableWidgetItem())
                self.tableWidget_scans.item(self.tableWidget_scans.rowCount() - 1, 0).setText(FILE[FILE.rfind("/") + 1:])
                self.tableWidget_scans.item(self.tableWidget_scans.rowCount() - 1, 2).setText(FILE)

                # add file into SFM / Scan ComboBox
                self.comboBox_SFM_scan.addItem(str(FILE[FILE.rfind("/") + 1:]))

                self.f_DB_analaze()
                self.f_SFM_reflectivityPreview_load()

        if self.sender().objectName() == "pushButton_deleteScans":

            files_remove = self.tableWidget_scans.selectedItems()
            if not files_remove: return

            for FILE in files_remove:
                self.tableWidget_scans.removeRow(self.tableWidget_scans.row(FILE))

            # update SFM list
            self.comboBox_SFM_scan.clear()
            for i in range(0, self.tableWidget_scans.rowCount()):
                self.comboBox_SFM_scan.addItem(self.tableWidget_scans.item(i, 2).text()[self.tableWidget_scans.item(i, 2).text().rfind("/") + 1:])

    def f_button_importRemoveDB(self):

        if self.sender().objectName() == "pushButton_importDB":

            files_import = QtWidgets.QFileDialog().getOpenFileNames(None, "FileNames", self.dir_current, ".h5 (*.h5)")
            if files_import[0] == []: return
            # Next "Import scans" will open last dir
            self.dir_current = files_import[0][0][:files_import[0][0].rfind("/")]

            # I couldnt make tablewidget sorting work when adding files to not empty table, so this is the solution for making the list of DB files sorted
            for i in range(self.tableWidget_DB.rowCount()-1, -1, -1):
                files_import[0].append(self.tableWidget_DB.item(i, 1).text())
                self.tableWidget_DB.removeRow(i)

            for FILE in sorted(files_import[0]):
                self.tableWidget_DB.insertRow(self.tableWidget_DB.rowCount())
                self.tableWidget_DB.setRowHeight(self.tableWidget_DB.rowCount()-1, 10)
                # File name (row 0) and full path (row 2)
                for j in range(0, 2): self.tableWidget_DB.setItem(self.tableWidget_DB.rowCount()-1, j, QtWidgets.QTableWidgetItem())
                self.tableWidget_DB.item(self.tableWidget_DB.rowCount() - 1, 0).setText(FILE[FILE.rfind("/") + 1:])
                self.tableWidget_DB.item(self.tableWidget_DB.rowCount() - 1, 1).setText(FILE)

                # add file into SFM / DB ComboBox
                self.comboBox_SFM_DB.addItem(str(FILE[FILE.rfind("/") + 1:][:5]))

            self.f_DB_analaze()
            self.f_SFM_reflectivityPreview_load()

        elif self.sender().objectName() == "pushButton_deleteDB":

            files_remove = self.tableWidget_DB.selectedItems()
            if not files_remove: return

            for FILE in files_remove: self.tableWidget_DB.removeRow(self.tableWidget_DB.row(FILE))

            # update SFM list
            self.comboBox_SFM_DB.clear()
            for i in range(0, self.tableWidget_DB.rowCount()):
                self.comboBox_SFM_DB.addItem(self.tableWidget_DB.item(i, 1).text()[self.tableWidget_DB.item(i, 1).text().rfind("/") + 1:][:5])

            self.f_DB_analaze()

    def f_button_saveDir(self):
        saveAt = QtWidgets.QFileDialog().getExistingDirectory()
        if not saveAt: return
        self.lineEdit_saveAt.setText(str(saveAt) + ("" if str(saveAt)[-1] == "/" else "/"))

    def f_button_reduceAll(self):
        self.listWidget_recheckFilesInSFM.clear()

        bkg_skip = float(self.lineEdit_reductions_subtractBkg_Skip.text()) if self.lineEdit_reductions_subtractBkg_Skip.text() else 0

        dir_saveFile = self.lineEdit_saveAt.text() if self.lineEdit_saveAt.text() else self.dir_current

        if self.statusbar.currentMessage().find("Error") == 0: return

        if self.checkBox_reductions_normalizeByDB.isChecked():
            self.f_DB_analaze()

            DB_attenFactor = 1
            if self.checkBox_reductions_attenuatorDB.isChecked():
                DB_attenFactor = 10 if self.lineEdit_reductions_attenuatorDB.text() == "" else float(self.lineEdit_reductions_attenuatorDB.text())

        # iterate through table with scans
        for i in range(0, self.tableWidget_scans.rowCount()):
            file_name = self.tableWidget_scans.item(i, 2).text()[self.tableWidget_scans.item(i, 2).text().rfind("/") + 1: -3]

            # find full name DB file if there are several of them
            FILE_DB = self.tableWidget_scans.item(i, 1).text() if self.checkBox_reductions_normalizeByDB.isChecked() else ""

            with h5py.File(self.tableWidget_scans.item(i, 2).text(), 'r') as FILE:

                INSTRUMENT = FILE[list(FILE.keys())[0]].get("instrument")
                MOTOR_DATA = np.array(INSTRUMENT.get('motors').get('data')).T
                SCALERS_DATA = np.array(INSTRUMENT.get('scalers').get('data')).T

                for index, motor in enumerate(INSTRUMENT.get('motors').get('SPEC_motor_mnemonics')):
                    if "'th'" in str(motor): th_list = MOTOR_DATA[index]
                    elif "'s1hg'" in str(motor): s1hg_list = MOTOR_DATA[index]
                    elif "'s2hg'" in str(motor): s2hg_list = MOTOR_DATA[index]

                checkThisFile = 0

                # check if we have several polarisations
                for detector in INSTRUMENT.get('detectors'):
                    if str(detector) not in ("psd", "psd_du", "psd_uu", "psd_ud", "psd_dd"): continue

                    for index, scaler in enumerate(INSTRUMENT.get('scalers').get('SPEC_counter_mnemonics')):
                        if "'mon0'" in str(scaler) and str(detector) == "psd": monitor_list = SCALERS_DATA[index]
                        elif "'m1'" in str(scaler) and str(detector) == "psd_uu": monitor_list = SCALERS_DATA[index]
                        elif "'m2'" in str(scaler) and str(detector) == "psd_dd": monitor_list = SCALERS_DATA[index]
                        elif "'m3'" in str(scaler) and str(detector) == "psd_du": monitor_list = SCALERS_DATA[index]
                        elif "'m4'" in str(scaler) and str(detector) == "psd_ud": monitor_list = SCALERS_DATA[index]
                        elif "'sec'" in str(scaler): time_list = SCALERS_DATA[index]

                    original_roi_coord = np.array(INSTRUMENT.get('scalers').get('roi').get("roi"))

                    scan_intens = INSTRUMENT.get("detectors").get(str(detector)).get('data')[:, int(original_roi_coord[0]): int(original_roi_coord[1]), :].sum(axis=1)

                    new_file = open(dir_saveFile + file_name + "_" + str(detector) + " (" + FILE_DB + ")" + ".dat", "w")

                    # iterate through th points
                    for index, th in enumerate(th_list):

                        th = th - float(self.lineEdit_instrument_offsetFull.text())  # th offset

                        # analize integrated intensity for ROI
                        Intens = scan_intens[index] if len(scan_intens.shape) == 1 else sum(scan_intens[index][int(original_roi_coord[2]): int(original_roi_coord[3])])

                        if Intens == 0 and self.checkBox_export_removeZeros.isChecked(): continue

                        IntensErr = 1 if Intens == 0 else np.sqrt(Intens)

                        # read motors
                        Qz, s1hg, s2hg = (4 * np.pi / float(self.lineEdit_instrument_wavelength.text())) * np.sin(np.radians(th)), s1hg_list[index], s2hg_list[index]
                        monitor = monitor_list[index] if self.comboBox_reductions_divideByMonitorOrTime.currentText() == "monitor" else time_list[index]

                        # check if we are not in a middle of ROI in Qz approx 0.02)
                        if round(Qz, 3) > 0.015 and round(Qz, 3) < 0.03 and checkThisFile == 0:
                            scanData_0_015 = scan_intens[index][int(original_roi_coord[2]): int(original_roi_coord[3])]

                            if not max(scanData_0_015) == max(scanData_0_015[round((len(scanData_0_015) / 3)):-round((len(scanData_0_015) / 3))]):
                                self.listWidget_recheckFilesInSFM.addItem(file_name)
                                checkThisFile = 1

                        coeff = self.f_overilluminationCorrCoeff(s1hg, s2hg, round(th, 4))
                        FWHM_proj,  overillCorr = coeff[1], coeff[0] if self.checkBox_reductions_overilluminationCorr.isChecked() else 1

                        # calculate resolution in Gunnar's Sared way or other (also using overillumination correction)
                        if self.checkBox_export_resolutionLikeSared.isChecked():
                            Resolution = np.sqrt(
                                ((2 * np.pi / float(self.lineEdit_instrument_wavelength.text())) ** 2) * ((np.cos(np.radians(th))) ** 2) * (0.68 ** 2) * ((s1hg ** 2) + (s2hg ** 2)) / (
                                            (float(self.lineEdit_instrument_distanceS1ToSample.text()) - float(self.lineEdit_instrument_distanceS2ToSample.text())) ** 2) + (
                                            (float(self.lineEdit_instrument_wavelengthResolution.text()) ** 2) * (Qz ** 2)))
                        else:
                            d_alpha = np.arctan((s1hg + [s2hg if FWHM_proj == s2hg else FWHM_proj][0]) / (
                                    (float(self.lineEdit_instrument_distanceS1ToSample.text()) - float(self.lineEdit_instrument_distanceS2ToSample.text())) * 2))
                            if self.comboBox_export_angle.currentText() == "Qz":
                                k_0 = 2 * np.pi / float(self.lineEdit_instrument_wavelength.text())
                                Resolution = np.sqrt((k_0 ** 2) * (
                                            (((np.cos(np.radians(th))) ** 2) * d_alpha ** 2) + ((float(self.lineEdit_instrument_wavelengthResolution.text()) ** 2) * ((np.sin(np.radians(th))) ** 2))))
                            else: Resolution = d_alpha if self.comboBox_export_angle.currentText() == "Radians" else np.degrees(d_alpha)

                        # Save resolution in sigma rather than in FWHM units
                        Resolution = Resolution / (2 * np.sqrt(2 * np.log(2)))

                        # minus background, divide by monitor, overillumination correct + calculate errors
                        if self.checkBox_reductions_subtractBkg.isChecked() and Qz > bkg_skip:
                            Intens_bkg = sum(scan_intens[index][int(original_roi_coord[2]) - 2 * (int(original_roi_coord[3]) - int(original_roi_coord[2])): int(original_roi_coord[2]) - (int(original_roi_coord[3]) - int(original_roi_coord[2]))])

                            if Intens_bkg > 0: IntensErr, Intens = np.sqrt(Intens + Intens_bkg), Intens - Intens_bkg

                        if self.checkBox_reductions_divideByMonitorOrTime.isChecked():
                            if self.comboBox_reductions_divideByMonitorOrTime.currentText() == "monitor":
                                monitor, IntensErr = monitor_list[index], IntensErr / monitor if Intens == 0 else (Intens / monitor) * np.sqrt((IntensErr / Intens) ** 2 + (1 / monitor))
                            elif self.comboBox_reductions_divideByMonitorOrTime.currentText() == "time":
                                monitor, IntensErr = time_list[index], IntensErr / monitor

                            Intens = Intens / monitor

                        if self.checkBox_reductions_overilluminationCorr.isChecked(): IntensErr, Intens = IntensErr / overillCorr, Intens / overillCorr

                        if self.checkBox_reductions_normalizeByDB.isChecked():
                            try:
                                DB_intens = float(self.DB_INFO[str(FILE_DB) + ";" + str(s1hg) + ";" + str(s2hg)].split(";")[0]) * DB_attenFactor
                                DB_err = overillCorr * float(self.DB_INFO[str(FILE_DB) + ";" + str(s1hg) + ";" + str(s2hg)].split(";")[1]) * self.DB_attenFactor

                                IntensErr = IntensErr + DB_err if Intens == 0 else (Intens / DB_intens) * np.sqrt((DB_err / DB_intens) ** 2 + (IntensErr / Intens) ** 2)
                                Intens = Intens / DB_intens
                            except:
                                if checkThisFile == 0:
                                    self.listWidget_recheckFilesInSFM.addItem(file_name)
                                    checkThisFile = 1

                            self.checkBox_reductions_scaleFactor.setChecked(False)

                        if self.checkBox_reductions_scaleFactor.isChecked(): IntensErr, Intens = IntensErr / self.scaleFactor, Intens / self.scaleFactor

                        # check desired output angle and do conversion if needed
                        if self.comboBox_export_angle.currentText() == "Qz": angle = round(Qz, 10)
                        elif self.comboBox_export_angle.currentText() == "Degrees": angle = round(np.degrees(np.arcsin(Qz * float(self.lineEdit_instrument_wavelength.text()) / (4 * np.pi))), 10)
                        elif self.comboBox_export_angle.currentText() == "Radians": angle = round(np.arcsin(Qz * float(self.lineEdit_instrument_wavelength.text()) / (4 * np.pi)), 10)

                        # skip the first point
                        if index == 0 or (Intens == 0 and self.checkBox_export_removeZeros.isChecked()): continue

                        new_file.write(str(angle) + ' ' + str(Intens) + ' ' + str(IntensErr) + ' ')
                        if self.checkBox_export_addResolutionColumn.isChecked(): new_file.write(str(Resolution))
                        new_file.write('\n')

                    # close files
                    new_file.close()

                    # check if file is empty - then comment inside
                    if os.stat(dir_saveFile + file_name + "_" + str(detector) + " (" + FILE_DB + ")" + ".dat").st_size == 0:
                        with open(dir_saveFile + file_name + "_" + str(detector) + " (" + FILE_DB + ")" + ".dat", "w") as empty_file:
                            empty_file.write("All points are either zeros or negatives.")

        self.statusbar.showMessage(str(self.tableWidget_scans.rowCount()) + " files reduced, " + str(self.listWidget_recheckFilesInSFM.count()) + " file(s) might need extra care.")

    def f_button_reduceSFM(self):

        dir_saveFile = self.lineEdit_saveAt.text() if self.lineEdit_saveAt.text() else self.dir_current

        # polarisation order - uu, dd, ud, du
        detector = ["uu", "du", "ud", "dd"]

        for i in range(0, len(self.SFM_export_Qz)):

            SFM_DB_file_export = self.SFM_DB_FILE if self.checkBox_reductions_normalizeByDB.isChecked() else ""

            with open(dir_saveFile + self.SFM_FILE[self.SFM_FILE.rfind("/") + 1 : -3] + "_" + str(detector[i]) + " (" + SFM_DB_file_export + ")" + " SFM.dat", "w") as new_file:
                for j in range(0, len(self.SFM_export_Qz[i])):
                    if self.SFM_export_I[i][j] == 0 and self.checkBox_export_removeZeros.isChecked(): continue

                    if self.comboBox_export_angle.currentText() == "Qz": angle = round(self.SFM_export_Qz[i][j], 10)
                    elif self.comboBox_export_angle.currentText() == "Degrees":
                        angle = round(np.degrees(np.arcsin(self.SFM_export_Qz[i][j] * float(self.lineEdit_instrument_wavelength.text())/ (4* np.pi))), 10)
                    elif self.comboBox_export_angle.currentText() == "Radians":
                        angle = round(np.arcsin(self.SFM_export_Qz[i][j] * float(self.lineEdit_instrument_wavelength.text()) / (4 * np.pi)), 10)

                    new_file.write(str(angle) + ' ' + str(self.SFM_export_I[i][j]) + ' ' + str(self.SFM_export_dI[i][j]) + ' ')

                    if self.checkBox_export_addResolutionColumn.isChecked(): new_file.write(str(self.SFM_export_resolution[i][j]))
                    new_file.write('\n')

            # close new file
            new_file.close()

        self.statusbar.showMessage(self.SFM_FILE[self.SFM_FILE.rfind("/") + 1:] + " file is reduced in SFM.")

    def f_button_clear(self):

        for item in (self.comboBox_SFM_scan, self.listWidget_recheckFilesInSFM, self.graphicsView_SFM_detectorImage, self.graphicsView_SFM_2Dmap, self.graphicsView_SFM_reflectivityPreview.getPlotItem(),self.comboBox_SFM_detectorImage_incidentAngle, self.comboBox_SFM_detectorImage_polarisation, self.comboBox_SFM_2Dmap_polarisation):
            item.clear()

        for i in range(self.tableWidget_scans.rowCount(), -1, -1): self.tableWidget_scans.removeRow(i)
        for i in range(self.tableWidget_DB.rowCount(), -1, -1): self.tableWidget_DB.removeRow(i)
    ##<--

    ##--> extra functions to shorten the code
    def f_overilluminationCorrCoeff(self, s1hg, s2hg, th):

        # Check for Sample Length input
        try:
            sample_len = float(self.lineEdit_sampleLen.text())
        except: return [1, s2hg]

        config = str(s1hg) + " " + str(s2hg) + " " + str(th) + " " + str(sample_len) + " " + self.lineEdit_instrument_distanceS1ToSample.text() + " " + self.lineEdit_instrument_distanceS2ToSample.text()

        # check if we already calculated overillumination for current configuration
        if config in self.dict_overillCoeff: coeff = self.dict_overillCoeff[config]
        else:
            coeff = [0, 0]

            # for trapezoid beam - find (half of) widest beam width (OC) and flat region (OB) with max intensity
            if s1hg < s2hg:
                OB = abs(((float(self.lineEdit_instrument_distanceS1ToSample.text()) * (s2hg - s1hg)) / (2 * (float(self.lineEdit_instrument_distanceS1ToSample.text()) - float(self.lineEdit_instrument_distanceS2ToSample.text())))) + s1hg / 2)
                OC = ((float(self.lineEdit_instrument_distanceS1ToSample.text()) * (s2hg + s1hg)) / (2 * (float(self.lineEdit_instrument_distanceS1ToSample.text()) - float(self.lineEdit_instrument_distanceS2ToSample.text())))) - s1hg / 2
            elif s1hg > s2hg:
                OB = abs(((s2hg * float(self.lineEdit_instrument_distanceS1ToSample.text())) - (s1hg * float(self.lineEdit_instrument_distanceS2ToSample.text()))) / (2 * (float(self.lineEdit_instrument_distanceS1ToSample.text()) - float(self.lineEdit_instrument_distanceS2ToSample.text()))))
                OC = (float(self.lineEdit_instrument_distanceS1ToSample.text()) / (float(self.lineEdit_instrument_distanceS1ToSample.text()) - float(self.lineEdit_instrument_distanceS2ToSample.text()))) * (s2hg + s1hg) / 2 - (s1hg / 2)
            elif s1hg == s2hg:
                OB = s1hg / 2
                OC = s1hg * (float(self.lineEdit_instrument_distanceS1ToSample.text()) / (float(self.lineEdit_instrument_distanceS1ToSample.text()) - float(self.lineEdit_instrument_distanceS2ToSample.text())) - 1 / 2)

            BC = OC - OB
            AO = 1 / (BC/2 + OB)  # normalized height of trapezoid
            FWHM_beam = BC/2 + OB  # half of the beam FWHM
            sampleLen_relative = float(sample_len) * np.sin(np.radians(np.fabs(th if not th == 0 else 0.00001)))  # projection of sample surface on the beam

            # "coeff" represents how much of total beam intensity illuminates the sample
            if sampleLen_relative / 2 >= OC: coeff[0] = 1
            else:  # check if we use only middle part of the beam or trapezoid "shoulders" also
                if sampleLen_relative / 2 <= OB: coeff[0] = AO*sampleLen_relative/2 # Square part
                elif sampleLen_relative / 2 > OB: coeff[0] = AO * (OB + BC/2 - ((OC-sampleLen_relative/2)**2) / (2*BC)) # Square part + triangle - edge of triangle that dont cover the sample

            # for the beam resolution calcultion we check how much of the beam FHWM we cover by the sample
            coeff[1] = s2hg if sampleLen_relative / 2 >= FWHM_beam else sampleLen_relative

            self.dict_overillCoeff[config] = coeff

        return coeff

    def f_DB_analaze(self):

        self.DB_INFO = {}

        for i in range(0, self.tableWidget_DB.rowCount()):
            with h5py.File(self.tableWidget_DB.item(i,1).text(), 'r') as FILE_DB:
                INSTRUMENT = FILE_DB[list(FILE_DB.keys())[0]].get("instrument")
                MOTOR_DATA = np.array(INSTRUMENT.get('motors').get('data')).T
                SCALERS_DATA = np.array(INSTRUMENT.get('scalers').get('data')).T

                for index, motor in enumerate(INSTRUMENT.get('motors').get('SPEC_motor_mnemonics')):
                    if "'th'" in str(motor): th_list = MOTOR_DATA[index]
                    elif "'s1hg'" in str(motor): s1hg_list = MOTOR_DATA[index]
                    elif "'s2hg'" in str(motor): s2hg_list = MOTOR_DATA[index]

                for index, scaler in enumerate(INSTRUMENT.get('scalers').get('SPEC_counter_mnemonics')):
                    if "'mon0'" in str(scaler): monitor_list = SCALERS_DATA[index]
                    elif "'roi'" in str(scaler): intens_list = SCALERS_DATA[index]
                    elif "'sec'" in str(scaler): time_list = SCALERS_DATA[index]

                if self.checkBox_reductions_divideByMonitorOrTime.isChecked(): monitor = monitor_list if self.comboBox_reductions_divideByMonitorOrTime.currentText() == "monitor" else time_list
                else: monitor = np.ones_like(intens_list)

                for j in range(0, len(th_list)):
                    DB_intens = float(intens_list[j]) / float(monitor[j])
                    if self.checkBox_reductions_divideByMonitorOrTime.isChecked() and self.comboBox_reductions_divideByMonitorOrTime.currentText() == "monitor":
                        DB_err = DB_intens * np.sqrt(1/float(intens_list[j]) + 1/float(monitor[j]))
                    else: DB_err = np.sqrt(float(intens_list[j])) / float(monitor[j])

                    scan_slitsMonitor = self.tableWidget_DB.item(i, 0).text()[:5] + ";" + str(s1hg_list[j]) + ";" + str(s2hg_list[j])

                    self.DB_INFO[scan_slitsMonitor] = str(DB_intens) + ";" + str(DB_err)

        if self.tableWidget_DB.rowCount() == 0: return
        else: self.f_DB_assign()

    def f_DB_assign(self):

        DB_list = []
        for DB_scan_number in self.DB_INFO: DB_list.append(DB_scan_number.split(";")[0])

        for i in range(self.tableWidget_scans.rowCount()):
            scan_number = self.tableWidget_scans.item(i, 0).text()[:5]

            # find nearest DB file if there are several of them
            if len(DB_list) == 0: FILE_DB = ""
            elif len(DB_list) == 1: FILE_DB = DB_list[0][:5]
            else:
                if self.checkBox_rearrangeDbAfter.isChecked():
                    for j, DB_scan in enumerate(DB_list):
                        FILE_DB = DB_scan[:5]
                        if int(DB_scan[:5]) > int(scan_number[:5]): break
                else:
                    for j, DB_scan in enumerate(reversed(DB_list)):
                        FILE_DB = DB_scan[:5]
                        if int(DB_scan[:5]) < int(scan_number[:5]): break

            self.tableWidget_scans.item(i, 1).setText(FILE_DB)

    ##<--

    ##--> SFM
    def f_SFM_detectorImage_load(self):

        if self.comboBox_SFM_scan.currentText() == "": return

        self.comboBox_SFM_detectorImage_incidentAngle.clear()
        self.comboBox_SFM_detectorImage_polarisation.clear()
        self.comboBox_SFM_2Dmap_polarisation.clear()

        # we need to find full path for the SFM file from the table
        for i in range(0, self.tableWidget_scans.rowCount()):
            self.SFM_FILE = self.tableWidget_scans.item(i, 2).text() if self.tableWidget_scans.item(i, 0).text() == self.comboBox_SFM_scan.currentText() else self.SFM_FILE

        with h5py.File(self.SFM_FILE, 'r') as FILE:
            SCAN = FILE[list(FILE.keys())[0]]

            if not self.roiLocked == [] and self.checkBox_SFM_detectorImage_lockRoi.isChecked(): original_roi_coord = np.array(self.roiLocked[0])
            else: original_roi_coord = np.array(SCAN.get("instrument").get('scalers').get('roi').get("roi"))

            roi_width = int(str(original_roi_coord[3])[:-2]) - int(str(original_roi_coord[2])[:-2])

            # ROI
            self.lineEdit_SFM_detectorImage_roiX_left.setText(str(original_roi_coord[2])[:-2])
            self.lineEdit_SFM_detectorImage_roiX_right.setText(str(original_roi_coord[3])[:-2])
            self.lineEdit_SFM_detectorImage_roiY_bottom.setText(str(original_roi_coord[1])[:-2])
            self.lineEdit_SFM_detectorImage_roiY_top.setText(str(original_roi_coord[0])[:-2])

            # BKG ROI
            if not self.roiLocked == [] and self.checkBox_SFM_detectorImage_lockRoi.isChecked(): self.lineEdit_SFM_detectorImage_roi_bkgX_right.setText(str(self.roiLocked[1]))
            else: self.lineEdit_SFM_detectorImage_roi_bkgX_right.setText(str(int(self.lineEdit_SFM_detectorImage_roiX_left.text()) - roi_width))
            self.lineEdit_SFM_detectorImage_roi_bkgX_left.setText(str(int(self.lineEdit_SFM_detectorImage_roi_bkgX_right.text()) - roi_width))

            for index, th in enumerate(SCAN.get("instrument").get('motors').get('th').get("value")):
                self.comboBox_SFM_detectorImage_incidentAngle.addItem(str(round(th, 3)))

            if len(SCAN.get("ponos").get('data')) == 1:
                for item in (self.comboBox_SFM_detectorImage_polarisation, self.comboBox_SFM_2Dmap_polarisation): item.addItem("uu")
            for polarisation in SCAN.get("ponos").get('data'):
                if polarisation not in ("data_du", "data_uu", "data_dd", "data_ud"): continue
                if np.any(np.array(SCAN.get("ponos").get('data').get(polarisation))):
                    for item in (self.comboBox_SFM_detectorImage_polarisation, self.comboBox_SFM_2Dmap_polarisation): item.addItem(str(polarisation)[-2:])

            self.comboBox_SFM_detectorImage_polarisation.setCurrentIndex(0)
            self.comboBox_SFM_2Dmap_polarisation.setCurrentIndex(0)

    def f_SFM_detectorImage_draw(self):

        if self.comboBox_SFM_detectorImage_polarisation.currentText() == "" or self.comboBox_SFM_detectorImage_incidentAngle.currentText() == "": return

        for item in (self.graphicsView_SFM_detectorImage, self.graphicsView_SFM_detectorImage_roi): item.clear()

        if self.SFM_FILE == "": return
        with h5py.File(self.SFM_FILE, 'r') as FILE:

            self.th_current = self.comboBox_SFM_detectorImage_incidentAngle.currentText()

            INSTRUMENT = FILE[list(FILE.keys())[0]].get("instrument")
            MOTOR_DATA = np.array(INSTRUMENT.get('motors').get('data')).T
            SCALERS_DATA = np.array(INSTRUMENT.get('scalers').get('data')).T

            for index, motor in enumerate(INSTRUMENT.get('motors').get('SPEC_motor_mnemonics')):
                if "'th'" in str(motor): self.th_list = MOTOR_DATA[index]
                elif "'tth'" in str(motor): self.tth_list = MOTOR_DATA[index]
                elif "'s1hg'" in str(motor): self.s1hg_list = MOTOR_DATA[index]
                elif "'s2hg'" in str(motor): self.s2hg_list = MOTOR_DATA[index]

            for index, scaler in enumerate(INSTRUMENT.get('scalers').get('SPEC_counter_mnemonics')):
                if "'sec'" in str(scaler):
                    time_list = SCALERS_DATA[index]
                    break

            for i in INSTRUMENT.get('detectors'):
                if i not in ("psd", "psd_uu", "psd_dd", "psd_du", "psd_ud"): continue
                scan_psd = "psd" if i == "psd" else "psd_" + self.comboBox_SFM_detectorImage_polarisation.currentText()

            detector_images = INSTRUMENT.get('detectors').get(scan_psd).get('data')

            for index, th in enumerate(self.th_list):
                # check th
                if self.th_current == str(round(th, 3)):
                    self.lineEdit_SFM_detectorImage_slits_s1hg.setText(str(self.s1hg_list[index]))
                    self.lineEdit_SFM_detectorImage_slits_s2hg.setText(str(self.s2hg_list[index]))
                    self.lineEdit_SFM_detectorImage_time.setText(str(time_list[index]))

                    # seems to be a bug in numpy arrays imported from hdf5 files. Problem is solved after I subtract ZEROs array with the same dimentions.
                    detector_image = np.around(detector_images[index], decimals=0).astype(int)
                    detector_image = np.subtract(detector_image, np.zeros((detector_image.shape[0], detector_image.shape[1])))
                    # integrate detector image with respect to ROI Y coordinates
                    detector_image_int = detector_image[int(self.lineEdit_SFM_detectorImage_roiY_top.text()): int(self.lineEdit_SFM_detectorImage_roiY_bottom.text()), :].sum(axis=0).astype(int)

                    self.graphicsView_SFM_detectorImage.setImage(detector_image, axes={'x':1, 'y':0}, levels=(0,0.1))
                    self.graphicsView_SFM_detectorImage_roi.addItem(pg.PlotCurveItem(y = detector_image_int, pen=pg.mkPen(color=(0, 0, 0), width=2), brush=pg.mkBrush(color=(255, 0, 0), width=3)))

                    if self.comboBox_SFM_detectorImage_colorScheme.currentText() == "White / Black":
                        self.color_det_image = np.array([[0, 0, 0, 255], [255, 255, 255, 255], [255, 255, 255, 255]], dtype=np.ubyte)
                    elif self.comboBox_SFM_detectorImage_colorScheme.currentText() == "Green / Blue":
                        self.color_det_image = np.array([[0, 0, 255, 255], [255, 0, 0, 255], [0, 255, 0, 255]], dtype=np.ubyte)
                    pos = np.array([0.0, 0.1, 1.0])

                    self.graphicsView_SFM_detectorImage.setColorMap(pg.ColorMap(pos, self.color_det_image))

                    # add ROI rectangular
                    spots_ROI_detInt = []
                    if self.roi_draw: self.graphicsView_SFM_detectorImage.removeItem(self.roi_draw)
                    if self.roi_draw_bkg: self.graphicsView_SFM_detectorImage.removeItem(self.roi_draw_bkg)

                    # add ROI rectangular
                    spots_ROI_det_view = {'x': (int(self.lineEdit_SFM_detectorImage_roiX_left.text()), int(self.lineEdit_SFM_detectorImage_roiX_right.text()), int(self.lineEdit_SFM_detectorImage_roiX_right.text()), int(self.lineEdit_SFM_detectorImage_roiX_left.text()), int(self.lineEdit_SFM_detectorImage_roiX_left.text())),
                                 'y': (int(self.lineEdit_SFM_detectorImage_roiY_top.text()), int(self.lineEdit_SFM_detectorImage_roiY_top.text()), int(self.lineEdit_SFM_detectorImage_roiY_bottom.text()), int(self.lineEdit_SFM_detectorImage_roiY_bottom.text()), int(self.lineEdit_SFM_detectorImage_roiY_top.text()))}

                    self.roi_draw = pg.PlotDataItem(spots_ROI_det_view, pen=pg.mkPen(255, 255, 255), connect="all")
                    self.graphicsView_SFM_detectorImage.addItem(self.roi_draw)

                    # add BKG ROI rectangular
                    if self.checkBox_reductions_subtractBkg.isChecked():
                        spots_ROI_det_view = {'x': (int(self.lineEdit_SFM_detectorImage_roi_bkgX_left.text()), int(self.lineEdit_SFM_detectorImage_roi_bkgX_right.text()),
                                                    int(self.lineEdit_SFM_detectorImage_roi_bkgX_right.text()), int(self.lineEdit_SFM_detectorImage_roi_bkgX_left.text()),
                                                    int(self.lineEdit_SFM_detectorImage_roi_bkgX_left.text())),
                                              'y': (int(self.lineEdit_SFM_detectorImage_roiY_top.text()), int(self.lineEdit_SFM_detectorImage_roiY_top.text()),
                                                    int(self.lineEdit_SFM_detectorImage_roiY_bottom.text()), int(self.lineEdit_SFM_detectorImage_roiY_bottom.text()),
                                                    int(self.lineEdit_SFM_detectorImage_roiY_top.text()))}

                        self.roi_draw_bkg = pg.PlotDataItem(spots_ROI_det_view, pen=pg.mkPen(color=(255, 255, 255), style=QtCore.Qt.DashLine), connect="all")
                        self.graphicsView_SFM_detectorImage.addItem(self.roi_draw_bkg)

                    if self.roi_draw_int: self.graphicsView_SFM_detectorImage_roi.removeItem(self.roi_draw_int)

                    for i in range(0, detector_image_int.max()):
                        spots_ROI_detInt.append({'x': int(self.lineEdit_SFM_detectorImage_roiX_left.text()), 'y': i})
                        spots_ROI_detInt.append({'x': int(self.lineEdit_SFM_detectorImage_roiX_right.text()), 'y': i})

                    self.roi_draw_int = pg.ScatterPlotItem(spots=spots_ROI_detInt, size=1, pen=pg.mkPen(255, 0, 0))
                    self.graphicsView_SFM_detectorImage_roi.addItem(self.roi_draw_int)

                    break

        # Show "integrated roi" part
        if self.sender().objectName() == "pushButton_SFM_detectorImage_showIntegratedRoi":
            (height, trigger) = (420, False) if self.trigger_showDetInt else (510, True)
            self.graphicsView_SFM_detectorImage.setGeometry(QtCore.QRect(0, 30, 577, height))
            self.trigger_showDetInt = trigger

    def f_SFM_reflectivityPreview_load(self):

        self.graphicsView_SFM_reflectivityPreview.getPlotItem().clear()
        bkg_skip = 0

        self.SFM_export_Qz, self.SFM_export_I, self.SFM_export_dI, self.SFM_export_resolution = [], [], [], []

        # change interface (Include ang resolution..., Use original Sared way...)
        self.checkBox_export_resolutionLikeSared.setEnabled(True if self.checkBox_export_addResolutionColumn.isChecked() else False)

        # change interface (Scale factor, DB correction, DB attenuator)
        if self.checkBox_reductions_normalizeByDB.isChecked():
            hidden = [False, False, True, True]
            self.checkBox_reductions_scaleFactor.setChecked(False)
        else: hidden = [True, True, False, False]

        for index, element in enumerate([self.checkBox_reductions_attenuatorDB, self.lineEdit_reductions_attenuatorDB, self.checkBox_reductions_scaleFactor, self.lineEdit_reductions_scaleFactor]):
            element.setHidden(hidden[index])

        if self.comboBox_SFM_scan.currentText() == "": return

        # Input checkups
        self.statusbar.clearMessage()

        if self.checkBox_reductions_overilluminationCorr.isChecked() or self.checkBox_SFM_reflectivityPreview_showOverillumination.isChecked():
            try:
                _ = float(self.lineEdit_sampleLen.text())
            except:
                self.statusbar.showMessage("Error: Recheck 'Sample length' field.")

        if self.checkBox_reductions_normalizeByDB.isChecked() and self.tableWidget_DB.rowCount() == 0:
            self.statusbar.showMessage("Error: Direct beam file is missing.")

        if int(self.lineEdit_SFM_detectorImage_roiX_left.text()) > int(self.lineEdit_SFM_detectorImage_roiX_right.text()) or int(self.lineEdit_SFM_detectorImage_roiY_bottom.text()) < int(self.lineEdit_SFM_detectorImage_roiY_top.text()) or (self.checkBox_reductions_subtractBkg.checkState() and int(self.lineEdit_SFM_detectorImage_roi_bkgX_left.text()) < 0):
            self.statusbar.showMessage("Error: Recheck your ROI input.")

        self.scaleFactor = 1
        if self.checkBox_reductions_scaleFactor.isChecked():
            try:
                self.scaleFactor = 10 if self.lineEdit_reductions_scaleFactor.text() == "" else float(self.lineEdit_reductions_scaleFactor.text())
            except:
                self.statusbar.showMessage("Error: Recheck 'Scale Factor' field.")

        self.DB_attenFactor = 1
        if self.checkBox_reductions_attenuatorDB.isChecked():
            try:
                self.DB_attenFactor = 10 if self.lineEdit_reductions_attenuatorDB.text() == "" else float(self.lineEdit_reductions_attenuatorDB.text())
            except:
                self.statusbar.showMessage("Error: Recheck 'Direct Beam Attenuator Factor' field.")

        if self.lineEdit_reductions_subtractBkg_Skip.text():
            try:
                bkg_skip = float(self.lineEdit_reductions_subtractBkg_Skip.text())
            except:
                self.statusbar.showMessage("Error: Recheck 'Skip background' field.")

        try:
            _ = 1/float(self.lineEdit_instrument_wavelength.text())
            _ = float(self.lineEdit_instrument_wavelengthResolution.text())
            _ = float(self.lineEdit_instrument_distanceS1ToSample.text())
            _ = float(self.lineEdit_instrument_distanceS2ToSample.text())
            _ = float(self.lineEdit_instrument_distanceSampleToDetector.text())
            _ = float(self.lineEdit_instrument_sampleCurvature.text())
            _ = float(self.lineEdit_instrument_offsetFull.text())
        except:
            self.statusbar.showMessage("Error: Recheck 'Instrument / Corrections' tab for typos.")

        if self.statusbar.currentMessage(): return

        # Define analized file and DB
        for i in range(0, self.tableWidget_scans.rowCount()):
            if self.tableWidget_scans.item(i, 0).text() == self.comboBox_SFM_scan.currentText(): self.SFM_FILE = self.tableWidget_scans.item(i, 2).text()
        self.SFM_DB_FILE = self.comboBox_SFM_DB.currentText()

        # Open analized file
        with h5py.File(self.SFM_FILE, 'r') as FILE:
            INSTRUMENT = FILE[list(FILE.keys())[0]].get("instrument")
            PONOS = FILE[list(FILE.keys())[0]].get("ponos")
            SCALERS_DATA = np.array(INSTRUMENT.get('scalers').get('data')).T

            roi_coord_Y = [int(self.lineEdit_SFM_detectorImage_roiY_top.text()), int(self.lineEdit_SFM_detectorImage_roiY_bottom.text())]
            roi_coord_X = [int(self.lineEdit_SFM_detectorImage_roiX_left.text()), int(self.lineEdit_SFM_detectorImage_roiX_right.text())]
            roi_coord_X_BKG = [int(self.lineEdit_SFM_detectorImage_roi_bkgX_left.text()), int(self.lineEdit_SFM_detectorImage_roi_bkgX_right.text())]

            # recalculate if ROI was changed
            if not roi_coord_Y == self.roi_oldCoord_Y: self.SFMFileAlreadyAnalized = ""
            self.roi_oldCoord_Y = roi_coord_Y

            for index, scaler in enumerate(INSTRUMENT.get('scalers').get('SPEC_counter_mnemonics')):
                if "'mon0'" in str(scaler): monitor_list = SCALERS_DATA[index]
                elif "'m1'" in str(scaler): monitor_uu_list = SCALERS_DATA[index]
                elif "'m2'" in str(scaler): monitor_dd_list = SCALERS_DATA[index]
                elif "'m3'" in str(scaler): monitor_du_list = SCALERS_DATA[index]
                elif "'m4'" in str(scaler): monitor_ud_list = SCALERS_DATA[index]
                elif "'sec'" in str(scaler): time_list = SCALERS_DATA[index]

            if not self.SFM_FILE == self.SFMFileAlreadyAnalized:
                self.SFM_psdUU = self.SFM_psdDD = self.SFM_psdUD = self.SFM_psdDU = []

            # get or create 2-dimentional intensity array for each polarisation

            sampleCurvature_recalc = True if self.sampleCurvature_last == [i.text() for i in [self.lineEdit_instrument_sampleCurvature, self.lineEdit_SFM_detectorImage_roiX_left, self.lineEdit_SFM_detectorImage_roiX_right, self.lineEdit_SFM_detectorImage_roiY_bottom, self.lineEdit_SFM_detectorImage_roiY_top]] else False
            for scan in PONOS.get('data'):
                # avoid reSUM of intensity after each action
                # reSUM if we change SFM file or Sample curvature
                if self.SFM_FILE == self.SFMFileAlreadyAnalized and sampleCurvature_recalc: continue

                if "pnr" in list(FILE[list(FILE.keys())[0]]):
                    if str(scan) == "data_du": self.SFM_psdDU = INSTRUMENT.get("detectors").get("psd_du").get('data')[:, int(roi_coord_Y[0]): int(roi_coord_Y[1]), :].sum(axis=1)
                    elif str(scan) == "data_uu": self.SFM_psdUU = INSTRUMENT.get("detectors").get("psd_uu").get('data')[:, int(roi_coord_Y[0]): int(roi_coord_Y[1]), :].sum(axis=1)
                    elif str(scan) == "data_ud": self.SFM_psdUD = INSTRUMENT.get("detectors").get("psd_ud").get('data')[:, int(roi_coord_Y[0]): int(roi_coord_Y[1]), :].sum(axis=1)
                    elif str(scan) == "data_dd": self.SFM_psdDD = INSTRUMENT.get("detectors").get("psd_dd").get('data')[:, int(roi_coord_Y[0]): int(roi_coord_Y[1]), :].sum(axis=1)

                else: self.SFM_psdUU = INSTRUMENT.get("detectors").get("psd").get('data')[:, int(roi_coord_Y[0]) : int(roi_coord_Y[1]), :].sum(axis=1)

            if not self.SFM_FILE == self.SFMFileAlreadyAnalized: self.SFMFileAlreadyAnalized, self.sampleCurvature_last = self.SFM_FILE, "0"

            # Sample curvature correction - we need to adjust integrated 2D map when we first make it
            # perform correction if it was changed on the form
            if not sampleCurvature_recalc:

                for index, SFM_curvatureCorrection in enumerate([self.SFM_psdUU, self.SFM_psdDU, self.SFM_psdUD, self.SFM_psdDD]):

                    if self.lineEdit_instrument_sampleCurvature.text() == "0": continue
                    if SFM_curvatureCorrection == []: continue

                    SFM_curvatureCorrection_slice = SFM_curvatureCorrection[:, roi_coord_X[0]:roi_coord_X[1]]

                    detImage_recalc = [[],[],[]] # x, y, value

                    for x, col in enumerate(np.flipud(np.rot90(SFM_curvatureCorrection_slice))):
                        displacement = x * np.tan(float(self.lineEdit_instrument_sampleCurvature.text()))
                        for y, value in enumerate(col):
                            detImage_recalc[0].append(x)
                            detImage_recalc[1].append(y + displacement)
                            detImage_recalc[2].append(value)
                    np.rot90(SFM_curvatureCorrection_slice, -1)

                    # find middle of roi to define zero level
                    roi_coord_X_middle = (SFM_curvatureCorrection_slice.shape[1]) / 2
                    zero_level = int(round(roi_coord_X_middle * np.tan(float(self.lineEdit_instrument_sampleCurvature.text())) - min(detImage_recalc[1])))

                    grid_x, grid_y = np.mgrid[0:SFM_curvatureCorrection_slice.shape[1]:1, min(detImage_recalc[1]):max(detImage_recalc[1]):1]
                    SFM_curvatureCorrection_slice = np.flipud(np.rot90(griddata((detImage_recalc[0], detImage_recalc[1]), detImage_recalc[2], (grid_x, grid_y), method="linear", fill_value=float(0))))[zero_level:zero_level+SFM_curvatureCorrection_slice.shape[0], :]

                    SFM_curvatureCorrection[:, roi_coord_X[0]:roi_coord_X[1]] = SFM_curvatureCorrection_slice

                    if index == 0: self.SFM_psdUU = SFM_curvatureCorrection
                    elif index == 1: self.SFM_psdDU = SFM_curvatureCorrection
                    elif index == 2: self.SFM_psdUD = SFM_curvatureCorrection
                    elif index == 3: self.SFM_psdDD = SFM_curvatureCorrection

                self.sampleCurvature_last = [i.text() for i in [self.lineEdit_instrument_sampleCurvature, self.lineEdit_SFM_detectorImage_roiX_left, self.lineEdit_SFM_detectorImage_roiX_right, self.lineEdit_SFM_detectorImage_roiY_bottom, self.lineEdit_SFM_detectorImage_roiY_top]]

            for colorIndex, SFM_scanIntens in enumerate([self.SFM_psdUU, self.SFM_psdDU, self.SFM_psdUD, self.SFM_psdDD]):

                SFM_export_Qz_onePol, SFM_export_I_onePol, SFM_export_dI_onePol, SFM_export_resolution_onePol = [], [], [], []

                plot_I, plot_angle, plot_dI_err_bottom, plot_dI_err_top, plot_overillumination = [], [], [], [], []

                if SFM_scanIntens == []: continue

                if colorIndex == 0: color, monitorData = [0, 0, 0], [monitor_list if np.count_nonzero(monitor_uu_list) == 0 else monitor_uu_list][0] # ++
                elif colorIndex == 1: color, monitorData = [0, 0, 255], monitor_du_list # -+
                elif colorIndex == 2: color, monitorData = [0, 255, 0], monitor_ud_list # +-
                elif colorIndex == 3: color, monitorData = [255, 0, 0], monitor_dd_list # --

                for index, th in enumerate(self.th_list):
                    th = th - float(self.lineEdit_instrument_offsetFull.text()) # th offset

                    # read motors
                    Qz = (4 * np.pi / float(self.lineEdit_instrument_wavelength.text())) * np.sin(np.radians(th))
                    s1hg, s2hg, monitor = self.s1hg_list[index], self.s2hg_list[index], monitorData[index]

                    if not self.checkBox_reductions_overilluminationCorr.isChecked():
                        overillCorr, FWHM_proj = 1, s2hg
                        overillCorr_plot = self.f_overilluminationCorrCoeff(s1hg, s2hg, round(th, 4))[0]
                    else:
                        overillCorr, FWHM_proj = self.f_overilluminationCorrCoeff(s1hg, s2hg, round(th, 4))
                        overillCorr_plot = overillCorr

                    # calculate resolution in Gunnar's Sared way or other (also using overillumination correction)
                    if self.checkBox_export_resolutionLikeSared.isChecked():
                        Resolution = np.sqrt(((2 * np.pi / float(self.lineEdit_instrument_wavelength.text())) ** 2) * ((np.cos(np.radians(th))) ** 2) * (0.68 ** 2) * ((s1hg ** 2) + (s2hg ** 2)) / ((float( self.lineEdit_instrument_distanceS1ToSample.text()) - float( self.lineEdit_instrument_distanceS2ToSample.text())) ** 2) + ((float(self.lineEdit_instrument_wavelengthResolution.text()) ** 2) * (Qz ** 2)))
                    else:
                        d_alpha = np.arctan((s1hg + [s2hg if FWHM_proj == s2hg else FWHM_proj][0]) / (
                                (float(self.lineEdit_instrument_distanceS1ToSample.text()) - float(self.lineEdit_instrument_distanceS2ToSample.text())) * 2))
                        if self.comboBox_export_angle.currentText() == "Qz":
                            k_0 = 2 * np.pi / float(self.lineEdit_instrument_wavelength.text())
                            Resolution = np.sqrt((k_0 ** 2) * ( (((np.cos(np.radians(th))) ** 2) * d_alpha ** 2) + ((float(self.lineEdit_instrument_wavelengthResolution.text()) ** 2) * ((np.sin(np.radians(th))) ** 2))))
                        else: Resolution = d_alpha if self.comboBox_export_angle.currentText() == "Radians" else np.degrees(d_alpha)

                    # Save resolution in sigma rather than in FWHM units
                    Resolution = Resolution / (2 * np.sqrt(2 * np.log(2)))

                    # analize integrated intensity for ROI
                    Intens = sum(SFM_scanIntens[index][roi_coord_X[0]: roi_coord_X[1]])
                    Intens_bkg = sum(SFM_scanIntens[index][roi_coord_X_BKG[0] : roi_coord_X_BKG[1]])

                    # minus background, divide by monitor, overillumination correct + calculate errors
                    if not Intens > 0: Intens = 0
                    # I want to avoid error==0 if intens==0
                    if Intens == 0: IntensErr = 1
                    else: IntensErr = np.sqrt(Intens)

                    if self.checkBox_reductions_subtractBkg.isChecked() and Qz > bkg_skip:
                        if Intens_bkg > 0:
                            IntensErr = np.sqrt(Intens + Intens_bkg)
                            Intens = Intens - Intens_bkg

                    if self.checkBox_reductions_divideByMonitorOrTime.isChecked():

                        if self.comboBox_reductions_divideByMonitorOrTime.currentText() == "monitor":
                            monitor = monitor_list[index]
                            if Intens == 0: IntensErr = IntensErr / monitor
                            else: IntensErr = (Intens / monitor) * np.sqrt((IntensErr / Intens) ** 2 + (1 / monitor))
                        elif self.comboBox_reductions_divideByMonitorOrTime.currentText() == "time":
                            monitor = time_list[index]
                            IntensErr = IntensErr / monitor

                        Intens = Intens / monitor

                    if self.checkBox_reductions_overilluminationCorr.isChecked() and overillCorr > 0:
                        IntensErr = IntensErr / overillCorr
                        Intens = Intens / overillCorr

                    if self.checkBox_reductions_normalizeByDB.isChecked():
                        try:
                            DB_intens = float(self.DB_INFO[self.SFM_DB_FILE + ";" + str(s1hg) + ";" + str(s2hg)].split(";")[0]) * self.DB_attenFactor
                            DB_err = overillCorr * float(self.DB_INFO[self.SFM_DB_FILE + ";" + str(s1hg) + ";" + str(s2hg)].split(";")[1]) * self.DB_attenFactor
                            IntensErr = (Intens / DB_intens) * np.sqrt((DB_err / DB_intens) ** 2 + (IntensErr / Intens) ** 2)
                            Intens = Intens / DB_intens
                            self.statusbar.clearMessage()
                        except:
                            # if we try DB file without neccesary slits combination measured - show error message + redraw reflectivity_preview
                            self.statusbar.showMessage("Error: Choose another DB file for this SFM data file.")
                            self.checkBox_reductions_normalizeByDB.setCheckState(0)

                    if self.checkBox_reductions_scaleFactor.isChecked():
                        IntensErr = IntensErr / self.scaleFactor
                        Intens = Intens / self.scaleFactor

                    try:
                        show_first, show_last = int(self.lineEdit_SFM_reflectivityPreview_skipPoints_left.text()), len(self.th_list)-int(self.lineEdit_SFM_reflectivityPreview_skipPoints_right.text())
                    except: show_first, show_last = 0, len(self.th_list)

                    if not Intens < 0 and index < show_last and index > show_first:
                        # I need this for "Reduce SFM" option. First - store one pol.
                        SFM_export_Qz_onePol.append(Qz)
                        SFM_export_I_onePol.append(Intens)
                        SFM_export_dI_onePol.append(IntensErr)
                        SFM_export_resolution_onePol.append(Resolution)

                        if Intens > 0:
                            plot_I.append(np.log10(Intens))
                            plot_angle.append(Qz)
                            plot_dI_err_top.append(abs(np.log10(Intens + IntensErr) - np.log10(Intens)))

                            plot_overillumination.append(overillCorr_plot)

                            if Intens > IntensErr: plot_dI_err_bottom.append(np.log10(Intens) - np.log10(Intens - IntensErr))
                            else: plot_dI_err_bottom.append(0)

                        if self.comboBox_SFM_reflectivityPreview_view_reflectivity.currentText() == "Lin":
                            plot_I.pop()
                            plot_I.append(Intens)
                            plot_dI_err_top.pop()
                            plot_dI_err_top.append(IntensErr)
                            plot_dI_err_bottom.pop()
                            plot_dI_err_bottom.append(IntensErr)

                        if self.comboBox_SFM_reflectivityPreview_view_angle.currentText() == "Deg":
                            plot_angle.pop()
                            plot_angle.append(th)

                # I need this for "Reduse SFM" option. Second - combine all shown pol in one list variable.
                # polarisations are uu, dd, ud, du
                self.SFM_export_Qz.append(SFM_export_Qz_onePol)
                self.SFM_export_I.append(SFM_export_I_onePol)
                self.SFM_export_dI.append(SFM_export_dI_onePol)
                self.SFM_export_resolution.append(SFM_export_resolution_onePol)

                if self.checkBox_SFM_reflectivityPreview_includeErrorbars.isChecked():
                    s1 = pg.ErrorBarItem(x=np.array(plot_angle), y=np.array(plot_I), top=np.array(plot_dI_err_top), bottom=np.array(plot_dI_err_bottom), pen=pg.mkPen(color[0], color[1], color[2]), brush=pg.mkBrush(color[0], color[1], color[2]))
                    self.graphicsView_SFM_reflectivityPreview.addItem(s1)

                s2 = pg.ScatterPlotItem(x=plot_angle, y=plot_I, symbol="o", size=4, pen=pg.mkPen(color[0], color[1], color[2]), brush=pg.mkBrush(color[0], color[1], color[2]))
                self.graphicsView_SFM_reflectivityPreview.addItem(s2)

                if self.checkBox_SFM_reflectivityPreview_showOverillumination.isChecked():
                    s3 = pg.PlotCurveItem(x=plot_angle, y=plot_overillumination, pen=pg.mkPen(color=(255, 0, 0), width=1), brush=pg.mkBrush(color=(255, 0, 0), width=1) )
                    self.graphicsView_SFM_reflectivityPreview.addItem(s3)

                if self.checkBox_SFM_reflectivityPreview_showZeroLevel.isChecked():
                    if self.comboBox_SFM_reflectivityPreview_view_reflectivity.currentText() == "Lin": level = np.array([1, 1])
                    else: level = np.array([0, 0])
                    s4 = pg.PlotCurveItem(x=np.array([min(plot_angle), max(plot_angle)]), y=level, pen=pg.mkPen(color=(0, 0, 255), width=1), brush=pg.mkBrush(color=(255, 0, 0), width=1) )
                    self.graphicsView_SFM_reflectivityPreview.addItem(s4)

    def f_SFM_2Dmap_draw(self):

        self.SFM_intDetectorImage = []

        for item in (self.graphicsView_SFM_2Dmap_Qxz_theta, self.graphicsView_SFM_2Dmap): item.clear()

        # change interface if for different views
        ELEMENTS = [self.label_SFM_2Dmap_rescaleImage_x, self.label_SFM_2Dmap_rescaleImage_y, self.horizontalSlider_SFM_2Dmap_rescaleImage_x, self.horizontalSlider_SFM_2Dmap_rescaleImage_y, self.label_SFM_2Dmap_lowerNumberOfPointsBy, self.comboBox_SFM_2Dmap_lowerNumberOfPointsBy, self.label_SFM_2Dmap_QxzThreshold, self.comboBox_SFM_2Dmap_QxzThreshold, self.label_SFM_2Dmap_view_scale, self.comboBox_SFM_2Dmap_view_scale]

        if self.comboBox_SFM_2Dmap_axes.currentText() == "Pixel vs. Point": visible, geometry = [True, True, True, True, False, False, False, False, True, True], [0, 0, 0, 0]
        elif self.comboBox_SFM_2Dmap_axes.currentText() == "Qx vs. Qz": visible, geometry = [False, False, False, False, True, True, True, True, False, False], [0, 30, 577, 522]
        elif self.comboBox_SFM_2Dmap_axes.currentText() == "Alpha_i vs. Alpha_f": visible, geometry = [False, False, False, False, True, True, False, False, True, True], [0, 0, 0, 0]

        self.graphicsView_SFM_2Dmap_Qxz_theta.setGeometry(QtCore.QRect(geometry[0], geometry[1], geometry[2], geometry[3]))
        for index, index_visible in enumerate(visible): ELEMENTS[index].setVisible(index_visible)

        if self.SFM_FILE == "": return

        # start over if we selected nes SFM scan
        if not self.SFMFile2dCalculatedParams == [] and not self.SFMFile2dCalculatedParams[0] == self.SFM_FILE:
            self.comboBox_SFM_2Dmap_axes.setCurrentIndex(0)
            self.SFMFile2dCalculatedParams, self.res_aif = [], []

        try:
            self.graphicsView_SFM_2Dmap.removeItem(self.roi_draw_2Dmap)
        except: True

        # load selected integrated detector image
        if self.comboBox_SFM_2Dmap_polarisation.count() == 1: self.SFM_intDetectorImage = self.SFM_psdUU
        else:
            if self.comboBox_SFM_2Dmap_polarisation.currentText() == "uu": self.SFM_intDetectorImage = self.SFM_psdUU
            elif self.comboBox_SFM_2Dmap_polarisation.currentText() == "du": self.SFM_intDetectorImage = self.SFM_psdDU
            elif self.comboBox_SFM_2Dmap_polarisation.currentText() == "ud": self.SFM_intDetectorImage = self.SFM_psdUD
            elif self.comboBox_SFM_2Dmap_polarisation.currentText() == "dd": self.SFM_intDetectorImage = self.SFM_psdDD

        if self.SFM_intDetectorImage == []: return

        # create log array for log view
        self.SFM_intDetectorImage_log = np.log10(np.where(self.SFM_intDetectorImage < 1, 0.1, self.SFM_intDetectorImage))

        # Pixel to Angle conversion for "Qx vs Qz" and "alpha_i vs alpha_f" 2d maps
        if self.comboBox_SFM_2Dmap_axes.currentText() in ["Qx vs. Qz", "Alpha_i vs. Alpha_f"]:
            # recalculate only if something was changed
            if self.res_aif == [] or not self.SFMFile2dCalculatedParams == [self.SFM_FILE, self.comboBox_SFM_2Dmap_polarisation.currentText(),
                                              self.lineEdit_SFM_detectorImage_roiX_left.text(), self.lineEdit_SFM_detectorImage_roiX_right.text(),
                                              self.lineEdit_instrument_wavelength.text(), self.lineEdit_instrument_distanceSampleToDetector.text(),
                                              self.comboBox_SFM_2Dmap_lowerNumberOfPointsBy.currentText(), self.comboBox_SFM_2Dmap_QxzThreshold.currentText(),
                                                                                self.lineEdit_instrument_sampleCurvature.text()]:
                self.spots_Qxz, self.SFM_intDetectorImage_Qxz, self.SFM_intDetectorImage_aif, self.SFM_intDetectorImage_values_array = [], [], [[],[]], []

                roi_middle = round((self.SFM_intDetectorImage.shape[1] - float(self.lineEdit_SFM_detectorImage_roiX_left.text()) +
                                    self.SFM_intDetectorImage.shape[1] - float(self.lineEdit_SFM_detectorImage_roiX_right.text())) / 2)
                mm_per_pix = 300 / self.SFM_intDetectorImage.shape[1]

                # we need to flip the detector (X) for correct calculation
                for theta_i, tth_i, det_image_i in zip(self.th_list, self.tth_list, np.flip(self.SFM_intDetectorImage, 1)):
                    for pixel_num, value in enumerate(det_image_i):
                        # Reduce number of points to draw (to save RAM)
                        if pixel_num % int(self.comboBox_SFM_2Dmap_lowerNumberOfPointsBy.currentText()) == 0:
                            theta_f = tth_i - theta_i # theta F in deg
                            delta_theta_F_mm = (pixel_num - roi_middle) * mm_per_pix
                            delta_theta_F_deg = np.degrees(np.arctan(delta_theta_F_mm / float(self.lineEdit_instrument_distanceSampleToDetector.text()))) # calculate delta theta F in deg
                            theta_f += delta_theta_F_deg # final theta F in deg for the point
                            # convert to Q
                            Qx = (2 * np.pi / float(self.lineEdit_instrument_wavelength.text())) * (np.cos(np.radians(theta_f)) - np.cos(np.radians(theta_i)))
                            Qz = (2 * np.pi / float(self.lineEdit_instrument_wavelength.text())) * (np.sin(np.radians(theta_f)) + np.sin(np.radians(theta_i)))

                            for arr, val in zip((self.SFM_intDetectorImage_Qxz, self.SFM_intDetectorImage_aif[0], self.SFM_intDetectorImage_aif[1], self.SFM_intDetectorImage_values_array), ([Qx, Qz, value], theta_i, theta_f, value)): arr.append(val)

                            # define colors - 2 count+ -> green, [0,1] - blue
                            color = [0, 0, 255] if value < int(self.comboBox_SFM_2Dmap_QxzThreshold.currentText()) else [0, 255, 0]

                            self.spots_Qxz.append({'pos': (-Qx, Qz), 'pen': pg.mkPen(color[0], color[1], color[2])})

                if self.comboBox_SFM_2Dmap_axes.currentText() == "Alpha_i vs. Alpha_f":
                    # calculate required number of pixels in Y axis
                    self.resolution_x_pix_deg = self.SFM_intDetectorImage.shape[0] / (max(self.SFM_intDetectorImage_aif[0]) - min(self.SFM_intDetectorImage_aif[0]))
                    self.resolution_y_pix = int(round((max(self.SFM_intDetectorImage_aif[1]) - min(self.SFM_intDetectorImage_aif[1])) * self.resolution_x_pix_deg))

                    grid_x, grid_y = np.mgrid[min(self.SFM_intDetectorImage_aif[0]):max(self.SFM_intDetectorImage_aif[0]):((max(self.SFM_intDetectorImage_aif[0]) - min(self.SFM_intDetectorImage_aif[0]))/len(self.th_list)), min(self.SFM_intDetectorImage_aif[1]):max(self.SFM_intDetectorImage_aif[1]):(max(self.SFM_intDetectorImage_aif[1]) - min(self.SFM_intDetectorImage_aif[1]))/self.resolution_y_pix]
                    self.res_aif = griddata((self.SFM_intDetectorImage_aif[0], self.SFM_intDetectorImage_aif[1]), self.SFM_intDetectorImage_values_array, (grid_x, grid_y), method="linear", fill_value=float(0))
                    # create log array for log view
                    self.res_aif_log = np.log10(np.where(self.res_aif < 1, 0.1, self.res_aif))

                # record params that we used for 2D maps calculation
                self.SFMFile2dCalculatedParams = [self.SFM_FILE, self.comboBox_SFM_2Dmap_polarisation.currentText(), self.lineEdit_SFM_detectorImage_roiX_left.text(), self.lineEdit_SFM_detectorImage_roiX_right.text(), self.lineEdit_instrument_wavelength.text(), self.lineEdit_instrument_distanceSampleToDetector.text(), self.comboBox_SFM_2Dmap_lowerNumberOfPointsBy.currentText(), self.comboBox_SFM_2Dmap_QxzThreshold.currentText(), self.lineEdit_instrument_sampleCurvature.text()]

        # plot
        if self.comboBox_SFM_2Dmap_axes.currentText() == "Pixel vs. Point":

            image = self.SFM_intDetectorImage_log if self.comboBox_SFM_2Dmap_view_scale.currentText() == "Log" else self.SFM_intDetectorImage

            self.graphicsView_SFM_2Dmap.setImage(image, axes={'x': 1, 'y': 0}, levels=(0, np.max(image)), scale=(int(self.horizontalSlider_SFM_2Dmap_rescaleImage_x.value()), int(self.horizontalSlider_SFM_2Dmap_rescaleImage_y.value())))
            # add ROI rectangular
            spots_ROI = {'x':(int(self.lineEdit_SFM_detectorImage_roiX_left.text()) * int(self.horizontalSlider_SFM_2Dmap_rescaleImage_x.value()), int(self.lineEdit_SFM_detectorImage_roiX_right.text()) * int(self.horizontalSlider_SFM_2Dmap_rescaleImage_x.value()), int(self.lineEdit_SFM_detectorImage_roiX_right.text()) * int(self.horizontalSlider_SFM_2Dmap_rescaleImage_x.value()), int(self.lineEdit_SFM_detectorImage_roiX_left.text()) * int(self.horizontalSlider_SFM_2Dmap_rescaleImage_x.value()), int(self.lineEdit_SFM_detectorImage_roiX_left.text()) * int(self.horizontalSlider_SFM_2Dmap_rescaleImage_x.value())), 'y':(0,0,self.SFM_intDetectorImage.shape[0] * int(self.horizontalSlider_SFM_2Dmap_rescaleImage_y.value()),self.SFM_intDetectorImage.shape[0] * int(self.horizontalSlider_SFM_2Dmap_rescaleImage_y.value()),0)}

            self.roi_draw_2Dmap = pg.PlotDataItem(spots_ROI, pen=pg.mkPen(255, 255, 255), connect="all")
            self.graphicsView_SFM_2Dmap.addItem(self.roi_draw_2Dmap)

        elif self.comboBox_SFM_2Dmap_axes.currentText() == "Alpha_i vs. Alpha_f":
            image = self.res_aif_log if self.comboBox_SFM_2Dmap_view_scale.currentText() == "Log" else self.res_aif

            self.graphicsView_SFM_2Dmap.setImage(image, axes={'x': 0, 'y': 1}, levels=(0, np.max(image)))
            self.graphicsView_SFM_2Dmap.getImageItem().setRect(QtCore.QRectF(min(self.SFM_intDetectorImage_aif[0]), min(self.SFM_intDetectorImage_aif[1]), max(self.SFM_intDetectorImage_aif[0]) - min(self.SFM_intDetectorImage_aif[0]), max(self.SFM_intDetectorImage_aif[1]) - min(self.SFM_intDetectorImage_aif[1])))
            self.graphicsView_SFM_2Dmap.getView().enableAutoScale()

        elif self.comboBox_SFM_2Dmap_axes.currentText() == "Qx vs. Qz":
            s0 = pg.ScatterPlotItem(spots=self.spots_Qxz, size=1)
            self.graphicsView_SFM_2Dmap_Qxz_theta.addItem(s0)

        # hide Y axis in 2D map if "rescale image" is used. Reason - misleading scale
        for item in (self.graphicsView_SFM_2Dmap.view.getAxis("left"), self.graphicsView_SFM_2Dmap.view.getAxis("bottom")): item.setTicks(None)
        if self.horizontalSlider_SFM_2Dmap_rescaleImage_x.value() > 1: self.graphicsView_SFM_2Dmap.view.getAxis("bottom").setTicks([])
        if self.horizontalSlider_SFM_2Dmap_rescaleImage_y.value() > 1: self.graphicsView_SFM_2Dmap.view.getAxis("left").setTicks([])

    def f_SFM_2Dmap_export(self):
        dir_saveFile = self.lineEdit_saveAt.text() if self.lineEdit_saveAt.text() else self.dir_current

        if self.comboBox_SFM_2Dmap_axes.currentText() == "Pixel vs. Point":
            with open(dir_saveFile + self.SFM_FILE[self.SFM_FILE.rfind("/") + 1 : -3] + "_" + self.comboBox_SFM_2Dmap_polarisation.currentText() + " 2Dmap(Pixel vs. Point).dat", "w") as newFile_2Dmap:
                for line in self.SFM_intDetectorImage:
                    for row in line: newFile_2Dmap.write(str(row) + " ")
                    newFile_2Dmap.write("\n")

        elif self.comboBox_SFM_2Dmap_axes.currentText() == "Alpha_i vs. Alpha_f":
            # Matrix
            with open(dir_saveFile + self.SFM_FILE[self.SFM_FILE.rfind("/") + 1 : -3] + "_" + self.comboBox_SFM_2Dmap_polarisation.currentText() + " 2Dmap_(Alpha_i vs. Alpha_f)).dat", "w") as newFile_2Dmap_aif:
                # header
                newFile_2Dmap_aif.write("Alpha_i limits: " + str(min(self.SFM_intDetectorImage_aif[0])) + " : " + str(max(self.SFM_intDetectorImage_aif[0])) +
                                        "   Alpha_f limits: " + str(min(self.SFM_intDetectorImage_aif[1])) + " : " + str(max(self.SFM_intDetectorImage_aif[1])) + " degrees\n")
                for line in np.rot90(self.res_aif):
                    for row in line: newFile_2Dmap_aif.write(str(row) + " ")
                    newFile_2Dmap_aif.write("\n")

            # Points
            with open(dir_saveFile + self.SFM_FILE[self.SFM_FILE.rfind("/") + 1: -3] + "_" + self.comboBox_SFM_2Dmap_polarisation.currentText() + " 2Dmap_(Alpha_i vs. Alpha_f))_Points.dat", "w") as newFile_2Dmap_aifPoints:
                for index in range(len(self.SFM_intDetectorImage_values_array)):
                    newFile_2Dmap_aifPoints.write(f"{str(self.SFM_intDetectorImage_aif[0][index])} {str(self.SFM_intDetectorImage_aif[1][index])} {str(self.SFM_intDetectorImage_values_array[index])} \n")

        elif self.comboBox_SFM_2Dmap_axes.currentText() in ["Qx vs. Qz"]:
            with open(dir_saveFile + self.SFM_FILE[self.SFM_FILE.rfind("/") + 1 : -3] + "_" + self.comboBox_SFM_2Dmap_polarisation.currentText() + " points_(Qx, Qz, intens).dat", "w") as newFile_2Dmap_Qxz:
                for line in self.SFM_intDetectorImage_Qxz: newFile_2Dmap_Qxz.write(str(line[0]) + " " + str(line[1]) + " " + str(line[2]) + "\n")

    def f_SFM_roi_update(self):

        roi_width = int(self.lineEdit_SFM_detectorImage_roiX_right.text()) - int(self.lineEdit_SFM_detectorImage_roiX_left.text())

        if not self.sender().objectName() == "lineEdit_SFM_detectorImage_roi_bkgX_right":
            self.lineEdit_SFM_detectorImage_roi_bkgX_left.setText(str(int(self.lineEdit_SFM_detectorImage_roiX_left.text()) - 2 * roi_width))
            self.lineEdit_SFM_detectorImage_roi_bkgX_right.setText(str(int(self.lineEdit_SFM_detectorImage_roiX_left.text()) - roi_width))
        else: self.lineEdit_SFM_detectorImage_roi_bkgX_left.setText(str(int(self.lineEdit_SFM_detectorImage_roi_bkgX_right.text()) - roi_width))

        # record ROI coord for "Lock ROI" checkbox
        self.roiLocked = [[self.lineEdit_SFM_detectorImage_roiY_top.text() + ". ", self.lineEdit_SFM_detectorImage_roiY_bottom.text() + ". ", self.lineEdit_SFM_detectorImage_roiX_left.text() + ". ", self.lineEdit_SFM_detectorImage_roiX_right.text() + ". "], self.lineEdit_SFM_detectorImage_roi_bkgX_right.text()]

        self.f_SFM_detectorImage_draw()
        self.f_SFM_reflectivityPreview_load()
        self.f_SFM_2Dmap_draw()

    ##<--

if __name__ == "__main__":
    QtWidgets.QApplication.setStyle("Fusion")
    app = QtWidgets.QApplication(sys.argv)
    prog = GUI()
    prog.show()
    sys.exit(app.exec_())

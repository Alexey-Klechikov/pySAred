'''
Install with:
* Windows - pyinstaller --onefile --noconsole -i"C:\icon.ico" --add-data C:\icon.ico;images C:\pySAred_V1.5.py
* MacOS - sudo pyinstaller --onefile --windowed pySAred_V1.5.py

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

    groupbox_os_displ = 0 if platform.system() == 'Windows' else 2 # PyQt version/OS fix

    def __create_element(self, object, geometry, object_name, text=None, font=None, placeholder=None, visible=None, stylesheet=None, checked=None, title=None, combo=None, enabled=None):

        object.setObjectName(object_name)

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
        self.label_Files_Scans = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_Files_Scans, [15, 5, 200, 20], "label_Files_Scans", text=".h5 files", font=font_headline)
        self.groupBox_Data = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_Data, [10, 11-self.groupbox_os_displ, 279, 667+self.groupbox_os_displ], "groupBox_Data", font=font_ee)
        self.label_Data_files = QtWidgets.QLabel(self.groupBox_Data)
        self.__create_element(self.label_Data_files, [10, 20+self.groupbox_os_displ, 121, 21], "label_Data_files", text="Data", font=font_headline)
        self.tableWidget_Scans = QtWidgets.QTableWidget(self.groupBox_Data)
        self.__create_element(self.tableWidget_Scans, [10, 45+self.groupbox_os_displ, 260, 342], "tableWidget_Scans", font=font_ee)
        self.tableWidget_Scans.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_Scans.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_Scans.setAutoScroll(True)
        self.tableWidget_Scans.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.tableWidget_Scans.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_Scans.setColumnCount(4)
        self.tableWidget_Scans.setRowCount(0)
        headers_table_scans = ["Scan", "DB", "Scan_file_full_path"]
        for i in range(0,3):
            self.tableWidget_Scans.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem())
            self.tableWidget_Scans.horizontalHeaderItem(i).setText(headers_table_scans[i])
        self.tableWidget_Scans.horizontalHeader().setVisible(True)
        self.tableWidget_Scans.verticalHeader().setVisible(False)
        self.tableWidget_Scans.setColumnWidth(0, 200)
        self.tableWidget_Scans.setColumnWidth(1, int(self.tableWidget_Scans.width()) - int(self.tableWidget_Scans.columnWidth(0)) - 2)
        self.tableWidget_Scans.setColumnWidth(2, 0)
        self.pushButton_Delete_scans = QtWidgets.QPushButton(self.groupBox_Data)
        self.__create_element(self.pushButton_Delete_scans, [10, 390+self.groupbox_os_displ, 81, 20], "pushButton_Delete_scans", text="Delete scans", font=font_ee)
        self.pushButton_Import_scans = QtWidgets.QPushButton(self.groupBox_Data)
        self.__create_element(self.pushButton_Import_scans, [189, 390+self.groupbox_os_displ, 81, 20], "pushButton_Import_scans", text="Import scans", font=font_ee)
        self.label_DB_files = QtWidgets.QLabel(self.groupBox_Data)
        self.__create_element(self.label_DB_files, [10, 415+self.groupbox_os_displ, 191, 23], "label_DB_files", text="Direct Beam(s)", font=font_headline)
        self.checkBox_Rearrange_DB_after = QtWidgets.QCheckBox(self.groupBox_Data)
        self.__create_element(self.checkBox_Rearrange_DB_after, [10, 435+self.groupbox_os_displ, 210, 20], "checkBox_Rearrange_DB_after", text="DB's were measured after the scans", font=font_ee)
        self.tableWidget_DB = QtWidgets.QTableWidget(self.groupBox_Data)
        self.__create_element(self.tableWidget_DB, [10, 455+self.groupbox_os_displ, 260, 183], "tableWidget_DB", font=font_ee)
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
        self.pushButton_Delete_DB = QtWidgets.QPushButton(self.groupBox_Data)
        self.__create_element(self.pushButton_Delete_DB, [10, 640+self.groupbox_os_displ, 81, 20], "pushButton_Delete_DB", text="Delete DB", font=font_ee)
        self.pushButton_Import_DB = QtWidgets.QPushButton(self.groupBox_Data)
        self.__create_element(self.pushButton_Import_DB, [189, 640+self.groupbox_os_displ, 81, 20], "pushButton_Import_DB", text="Import DB", font=font_ee)

        # Block: Sample
        self.label_Sample = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_Sample, [305, 5, 200, 20], "label_Sample", text="Sample", font=font_headline)
        self.groupBox_Sample_len = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_Sample_len, [300, 11-self.groupbox_os_displ, 282, 47+self.groupbox_os_displ], "groupBox_Sample_len", font=font_ee)
        self.label_Sample_len = QtWidgets.QLabel(self.groupBox_Sample_len)
        self.__create_element(self.label_Sample_len, [10, 24+self.groupbox_os_displ, 131, 16], "label_Sample_len", text="Sample length (mm)", font=font_ee)
        self.lineEdit_Sample_len = QtWidgets.QLineEdit(self.groupBox_Sample_len)
        self.__create_element(self.lineEdit_Sample_len, [192, 22+self.groupbox_os_displ, 83, 21], "lineEdit_Sample_len", text="50")

        # Block: Reductions and Instrument settings
        self.label_Reductions = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_Reductions, [305, 65, 200, 16], "label_Reductions", text="Reductions", font=font_headline)
        self.tabWidget_Reductions = QtWidgets.QTabWidget(self.centralwidget)
        self.__create_element(self.tabWidget_Reductions, [300, 87, 281, 226], "tabWidget_Reductions", font=font_ee)
        self.tabWidget_Reductions.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget_Reductions.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget_Reductions.setElideMode(QtCore.Qt.ElideNone)

        # Tab: Reductions
        self.tab_Reductions = QtWidgets.QWidget()
        self.tab_Reductions.setObjectName("tab_Reductions")
        self.checkBox_Reductions_Divide_by_monitor_or_time = QtWidgets.QCheckBox(self.tab_Reductions)
        self.__create_element(self.checkBox_Reductions_Divide_by_monitor_or_time, [10, 10, 131, 18], "checkBox_Reductions_Divide_by_monitor_or_time", font=font_ee, text="Divide by")
        self.comboBox_Reductions_Divide_by_monitor_or_time = QtWidgets.QComboBox(self.tab_Reductions)
        self.__create_element(self.comboBox_Reductions_Divide_by_monitor_or_time, [80, 9, 70, 20], "comboBox_Reductions_Divide_by_monitor_or_time", font=font_ee, combo=["monitor", "time"])
        self.checkBox_Reductions_Normalize_by_DB = QtWidgets.QCheckBox(self.tab_Reductions)
        self.__create_element(self.checkBox_Reductions_Normalize_by_DB, [10, 35, 181, 18], "checkBox_Reductions_Normalize_by_DB", text="Normalize by direct beam", font=font_ee)
        # User will need Attenuator only with DB. Otherwice I hide this option and replace with Scale factor
        self.checkBox_Reductions_Attenuator_DB = QtWidgets.QCheckBox(self.tab_Reductions)
        self.__create_element(self.checkBox_Reductions_Attenuator_DB, [10, 60, 161, 18], "checkBox_Reductions_Attenuator_DB", text="Direct beam attenuator", font=font_ee, checked=True, visible=False)
        self.lineEdit_Reductions_Attenuator_DB = QtWidgets.QLineEdit(self.tab_Reductions)
        self.__create_element(self.lineEdit_Reductions_Attenuator_DB, [30, 85, 221, 20], "lineEdit_Reductions_Subtract_bkg_Skip", text="", font=font_ee, placeholder="Attenuator correction factor [default 10]", visible=False)
        self.checkBox_Reductions_Scale_factor = QtWidgets.QCheckBox(self.tab_Reductions)
        self.__create_element(self.checkBox_Reductions_Scale_factor, [10, 60, 161, 18], "checkBox_Reductions_Scale_factor", text="Scale factor", font=font_ee, checked=False)
        self.lineEdit_Reductions_Scale_factor = QtWidgets.QLineEdit(self.tab_Reductions)
        self.__create_element(self.lineEdit_Reductions_Scale_factor, [30, 85, 221, 20], "lineEdit_Reductions_Scale_factor", text="",  font=font_ee, placeholder="Divide reflectivity curve by [default 10]")
        self.checkBox_Reductions_Subtract_bkg = QtWidgets.QCheckBox(self.tab_Reductions)
        self.__create_element(self.checkBox_Reductions_Subtract_bkg, [10, 115, 231, 18], "checkBox_Reductions_Subtract_bkg", text="Subtract background (using 1 ROI)", font=font_ee)
        self.lineEdit_Reductions_Subtract_bkg_Skip = QtWidgets.QLineEdit(self.tab_Reductions)
        self.__create_element(self.lineEdit_Reductions_Subtract_bkg_Skip, [30, 140, 221, 20], "lineEdit_Reductions_Subtract_bkg_Skip", text="", font=font_ee, placeholder="Skip background corr. at Qz < [default 0]")
        self.checkBox_Reductions_Overillumination_correction = QtWidgets.QCheckBox(self.tab_Reductions)
        self.__create_element(self.checkBox_Reductions_Overillumination_correction, [10, 170, 181, 18], "checkBox_Reductions_Overillumination_correction", text="Overillumination correction", font=font_ee)
        self.tabWidget_Reductions.addTab(self.tab_Reductions, "")
        self.tabWidget_Reductions.setTabText(0, "Reductions")

        # Tab: Instrument settings
        self.tab_Instrument_settings = QtWidgets.QWidget()
        self.tab_Instrument_settings.setObjectName("tab_Instrument_settings")
        self.label_Instrument_Wavelength = QtWidgets.QLabel(self.tab_Instrument_settings)
        self.__create_element(self.label_Instrument_Wavelength, [10, 10, 111, 16], "label_Instrument_Wavelength", text="Wavelength (A)", font=font_ee)
        self.lineEdit_Instrument_Wavelength = QtWidgets.QLineEdit(self.tab_Instrument_settings)
        self.__create_element(self.lineEdit_Instrument_Wavelength, [225, 10, 41, 18], "lineEdit_Instrument_Wavelength", font=font_ee, text="5.2")
        self.label_Instrument_Wavelength_resolution = QtWidgets.QLabel(self.tab_Instrument_settings)
        self.__create_element(self.label_Instrument_Wavelength_resolution, [10, 33, 271, 16], "label_Instrument_Wavelength_resolution", text="Wavelength resolution (d_lambda/lambda)", font=font_ee)
        self.lineEdit_Instrument_Wavelength_resolution = QtWidgets.QLineEdit(self.tab_Instrument_settings)
        self.__create_element(self.lineEdit_Instrument_Wavelength_resolution, [225, 33, 41, 18], "lineEdit_Instrument_Wavelength_resolution", font=font_ee, text="0.004")
        self.label_Instrument_Distance_s1_to_sample = QtWidgets.QLabel(self.tab_Instrument_settings)
        self.__create_element(self.label_Instrument_Distance_s1_to_sample, [10, 56, 241, 16], "label_Instrument_Distance_s1_to_sample", font=font_ee, text="Mono_slit to Samplle distance (mm)")
        self.lineEdit_Instrument_Distance_s1_to_sample = QtWidgets.QLineEdit(self.tab_Instrument_settings)
        self.__create_element(self.lineEdit_Instrument_Distance_s1_to_sample, [225, 56, 41, 18], "lineEdit_Instrument_Distance_s1_to_sample", font=font_ee, text="2300")
        self.label_Instrument_Distance_s2_to_sample = QtWidgets.QLabel(self.tab_Instrument_settings)
        self.__create_element(self.label_Instrument_Distance_s2_to_sample, [10, 79, 241, 16], "label_Instrument_Distance_s2_to_sample", font=font_ee, text="Sample_slit to Sample distance (mm)")
        self.lineEdit_Instrument_Distance_s2_to_sample = QtWidgets.QLineEdit(self.tab_Instrument_settings)
        self.__create_element(self.lineEdit_Instrument_Distance_s2_to_sample, [225, 79, 41, 18], "lineEdit_Instrument_Distance_s2_to_sample", font=font_ee, text="290")
        self.label_Instrument_Distance_sample_to_detector = QtWidgets.QLabel(self.tab_Instrument_settings)
        self.__create_element(self.label_Instrument_Distance_sample_to_detector, [10, 102, 241, 16], "label_Instrument_Distance_sample_to_detector", font=font_ee, text="Sample to Detector distance (mm)")
        self.lineEdit_Instrument_Distance_sample_to_detector = QtWidgets.QLineEdit(self.tab_Instrument_settings)
        self.__create_element(self.lineEdit_Instrument_Distance_sample_to_detector, [225, 102, 41, 18], "lineEdit_Instrument_Distance_sample_to_detector", font=font_ee, text="2500")
        self.label_Instrument_Sample_curvature = QtWidgets.QLabel(self.tab_Instrument_settings)
        self.__create_element(self.label_Instrument_Sample_curvature, [10, 152, 241, 16], "label_Instrument_Sample_curvature", font=font_ee, text="Sample curvature (in ROI) (SFM) (rad)")
        self.lineEdit_Instrument_Sample_curvature = QtWidgets.QLineEdit(self.tab_Instrument_settings)
        self.__create_element(self.lineEdit_Instrument_Sample_curvature, [225, 152, 41, 18], "lineEdit_Instrument_Sample_curvature", font=font_ee, text="0")
        self.label_Instrument_Offset_full = QtWidgets.QLabel(self.tab_Instrument_settings)
        self.__create_element(self.label_Instrument_Offset_full, [10, 175, 241, 16], "label_Instrument_Offset_full", font=font_ee, text="Sample angle offset (SFM) (th - deg)")
        self.lineEdit_Instrument_Offset_full = QtWidgets.QLineEdit(self.tab_Instrument_settings)
        self.__create_element(self.lineEdit_Instrument_Offset_full, [225, 175, 41, 18], "lineEdit_Instrument_Offset_full", font=font_ee, text="0")
        self.tabWidget_Reductions.addTab(self.tab_Instrument_settings, "")
        self.tabWidget_Reductions.setTabText(1, "Instrument / Corrections")

        # Tab: Export options
        self.tab_Export_options = QtWidgets.QWidget()
        self.tab_Export_options.setObjectName("tab_Export_options")
        self.checkBox_Export_Add_resolution_column = QtWidgets.QCheckBox(self.tab_Export_options)
        self.__create_element(self.checkBox_Export_Add_resolution_column, [10, 10, 260, 18], "checkBox_Export_Add_resolution_column", text="Include ang. resolution column in the output file", font=font_ee, checked=True)
        self.checkBox_Export_Resolution_like_sared = QtWidgets.QCheckBox(self.tab_Export_options)
        self.__create_element(self.checkBox_Export_Resolution_like_sared, [30, 35, 250, 18], "checkBox_Export_Resolution_like_sared", text="Calculate ang. resolution in 'Sared' way", font=font_ee, checked=True)
        self.checkBox_Export_Remove_zeros = QtWidgets.QCheckBox(self.tab_Export_options)
        self.__create_element(self.checkBox_Export_Remove_zeros, [10, 60, 250, 18], "checkBox_Export_Remove_zeros", text="Remove zeros from reduced files", font=font_ee, checked=False)
        self.tabWidget_Reductions.addTab(self.tab_Export_options, "")
        self.tabWidget_Reductions.setTabText(2, "Export")

        # Block: Save reduced files at
        self.label_Save_at = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_Save_at, [305, 320, 200, 20], "label_Save_at", font=font_headline, text="Save reduced files at")
        self.groupBox_Save_at = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_Save_at, [299, 325-self.groupbox_os_displ, 282, 48+self.groupbox_os_displ], "groupBox_Save_at", font=font_ee, title="")
        self.lineEdit_Save_at = QtWidgets.QLineEdit(self.groupBox_Save_at)
        self.__create_element(self.lineEdit_Save_at, [10, 22+self.groupbox_os_displ, 225, 22], "lineEdit_Save_at", font=font_ee, text=self.current_dir)
        self.toolButton_Save_at = QtWidgets.QToolButton(self.groupBox_Save_at)
        self.__create_element(self.toolButton_Save_at, [248, 22+self.groupbox_os_displ, 27, 22], "toolButton_Save_at", font=font_ee, text="...")

        # Button: Clear
        self.pushButton_Clear = QtWidgets.QPushButton(self.centralwidget)
        self.__create_element(self.pushButton_Clear, [300, 380, 88, 30], "pushButton_Clear", font=font_button, text="Clear all")

        # Button: Reduce all
        self.pushButton_Reduce_all = QtWidgets.QPushButton(self.centralwidget)
        self.__create_element(self.pushButton_Reduce_all, [493, 380, 88, 30], "pushButton_Reduce_all", font=font_button, text="Reduce all")

        # Errors
        self.label_Error_sample_len_missing = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_Error_sample_len_missing, [360, 420, 191, 31], "label_Error_sample_len_missing", font=font_button, text="Sample length is missing", visible=False, stylesheet="color:rgb(255,0,0)")
        self.label_Error_DB_missing = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_Error_DB_missing, [355, 450, 191, 31], "label_Error_DB_missing", font=font_button, text="Direct beam file is missing", visible=False, stylesheet="color:rgb(255,0,0)")
        self.label_Error_DB_wrong = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_Error_DB_wrong, [365, 420, 250, 51], "label_Error_DB_wrong", font=font_button, text="Choose another DB file \n for this SFM data file.", visible=False, stylesheet="color:rgb(255,0,0)")
        self.label_Error_Save_at_missing = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_Error_Save_at_missing, [360, 435, 191, 31], "label_Error_Save_at_missing", font=font_button, text="Define 'Save at' directory", visible=False, stylesheet="color:rgb(255,0,0)")
        self.label_Error_wrong_roi_input = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_Error_wrong_roi_input, [360, 435, 191, 31], "label_Error_wrong_roi_input", font=font_button, text="Recheck your ROI input", visible=False, stylesheet="color:rgb(255,0,0)")

        # Block: Recheck following files in SFM
        self.label_Recheck_files_in_SFM = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_Recheck_files_in_SFM, [305, 490, 250, 20], "label_Recheck_files_in_SFM", font=font_headline, text="Recheck following files in SFM")
        self.groupBox_Recheck_files_in_SFM = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_Recheck_files_in_SFM, [299, 500-self.groupbox_os_displ, 282, 178+self.groupbox_os_displ], "groupBox_Recheck_files_in_SFM", font=font_ee, title="")
        self.listWidget_Recheck_files_in_SFM = QtWidgets.QListWidget(self.groupBox_Recheck_files_in_SFM)
        self.__create_element(self.listWidget_Recheck_files_in_SFM, [10, 27+self.groupbox_os_displ, 262, 143], "listWidget_Recheck_files_in_SFM")

        # Block: Single File Mode
        self.label_SFM = QtWidgets.QLabel(self.centralwidget)
        self.__create_element(self.label_SFM, [596, 5, 200, 20], "label_SFM", font=font_headline, text="Single File Mode (SFM)")
        self.groupBox_SFM_Scan = QtWidgets.QGroupBox(self.centralwidget)
        self.__create_element(self.groupBox_SFM_Scan, [591, 11-self.groupbox_os_displ, 472, 47+self.groupbox_os_displ], "groupBox_SFM_Scan", title="")
        self.label_SFM_Scan = QtWidgets.QLabel(self.groupBox_SFM_Scan)
        self.__create_element(self.label_SFM_Scan, [10, 22+self.groupbox_os_displ, 47, 20], "label_SFM_Scan", font=font_ee, text="Scan")
        self.comboBox_SFM_Scan = QtWidgets.QComboBox(self.groupBox_SFM_Scan)
        self.__create_element(self.comboBox_SFM_Scan, [40, 22+self.groupbox_os_displ, 425, 20], "comboBox_SFM_Scan", font=font_ee)
        pg.setConfigOption('background', (255, 255, 255))
        pg.setConfigOption('foreground', 'k')

        # Button: Reduce SFM
        self.pushButton_Reduce_SFM = QtWidgets.QPushButton(self.centralwidget)
        self.__create_element(self.pushButton_Reduce_SFM, [1070, 28, 100, 31], "pushButton_Reduce_SFM", font=font_button, text="Reduce SFM")

        # Block: Detector Images and Reflectivity preview
        self.tabWidget_SFM = QtWidgets.QTabWidget(self.centralwidget)
        self.__create_element(self.tabWidget_SFM, [592, 65, 578, 613], "tabWidget_SFM", font=font_ee)

        # Tab: Detector images
        linedit_size_X = 30
        linedit_size_Y = 18
        self.tab_SFM_Detector_image = QtWidgets.QWidget()
        self.tab_SFM_Detector_image.setObjectName("tab_SFM_Detector_image")
        self.graphicsView_SFM_Detector_image_Roi = pg.PlotWidget(self.tab_SFM_Detector_image, viewBox=pg.ViewBox())
        self.__create_element(self.graphicsView_SFM_Detector_image_Roi, [0, 450, 577, 90], "graphicsView_SFM_Detector_image_Roi")
        self.graphicsView_SFM_Detector_image_Roi.hideAxis("left")
        self.graphicsView_SFM_Detector_image_Roi.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_SFM_Detector_image_Roi.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_SFM_Detector_image_Roi.setMouseEnabled(y=False)
        self.graphicsView_SFM_Detector_image = pg.ImageView(self.tab_SFM_Detector_image, view=pg.PlotItem(viewBox=pg.ViewBox()))
        self.graphicsView_SFM_Detector_image.setGeometry(QtCore.QRect(0, 30, 577, 510))
        self.graphicsView_SFM_Detector_image.setObjectName("graphicsView_SFM_Detector_image")
        self.graphicsView_SFM_Detector_image.ui.histogram.hide()
        self.graphicsView_SFM_Detector_image.ui.menuBtn.hide()
        self.graphicsView_SFM_Detector_image.ui.roiBtn.hide()
        self.graphicsView_SFM_Detector_image.view.showAxis("left", False)
        self.graphicsView_SFM_Detector_image.view.showAxis("bottom", False)
        self.graphicsView_SFM_Detector_image.view.getViewBox().setXLink(self.graphicsView_SFM_Detector_image_Roi)
        self.label_SFM_Detector_image_Incident_angle = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.__create_element(self.label_SFM_Detector_image_Incident_angle, [10, 7, 100, 16], "label_SFM_Detector_image_Incident_angle", font=font_ee, text="Incident ang. (deg)")
        self.comboBox_SFM_Detector_image_Incident_angle = QtWidgets.QComboBox(self.tab_SFM_Detector_image)
        self.__create_element(self.comboBox_SFM_Detector_image_Incident_angle, [110, 5, 55, 20], "comboBox_SFM_Detector_image_Incident_angle", font=font_ee)
        self.label_SFM_Detector_image_Polarisation = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.__create_element(self.label_SFM_Detector_image_Polarisation, [180, 7, 60, 16], "label_SFM_Detector_image_Polarisation", font=font_ee, text="Polarisation")
        self.comboBox_SFM_Detector_image_Polarisation = QtWidgets.QComboBox(self.tab_SFM_Detector_image)
        self.__create_element(self.comboBox_SFM_Detector_image_Polarisation, [240, 5, 40, 20], "comboBox_SFM_Detector_image_Polarisation", font=font_ee)
        self.label_SFM_Detector_image_Color_scheme = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.__create_element(self.label_SFM_Detector_image_Color_scheme, [295, 7, 60, 16], "label_SFM_Detector_image_Color_scheme", font=font_ee, text="Colors")
        self.comboBox_SFM_Detector_image_Color_scheme = QtWidgets.QComboBox(self.tab_SFM_Detector_image)
        self.__create_element(self.comboBox_SFM_Detector_image_Color_scheme, [330, 5, 90, 20], "comboBox_SFM_Detector_image_Color_scheme", font=font_ee, combo=["Green / Blue", "White / Black"])
        self.pushButton_SFM_Detector_image_Show_integrated_roi = QtWidgets.QPushButton(self.tab_SFM_Detector_image)
        self.__create_element(self.pushButton_SFM_Detector_image_Show_integrated_roi, [445, 5, 120, 20], "pushButton_SFM_Detector_image_Show_integrated_roi", font=font_ee, text="Integrated ROI")
        self.label_SFM_Detector_image_Roi = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.__create_element(self.label_SFM_Detector_image_Roi, [10, 545, 31, 16], "label_SFM_Detector_image_Roi", font=font_ee, text="ROI (")
        self.checkBox_SFM_Detector_image_Lock_roi = QtWidgets.QCheckBox(self.tab_SFM_Detector_image)
        self.__create_element(self.checkBox_SFM_Detector_image_Lock_roi, [38, 545, 50, 16], "checkBox_SFM_Detector_image_Lock_roi", text="lock):", font=font_ee)
        self.label_SFM_Detector_image_Roi_X_Left = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.__create_element(self.label_SFM_Detector_image_Roi_X_Left, [85, 545, 51, 16], "label_SFM_Detector_image_Roi_X_Left", font=font_ee, text="left")
        self.lineEdit_SFM_Detector_image_Roi_X_Left = QtWidgets.QLineEdit(self.tab_SFM_Detector_image)
        self.__create_element(self.lineEdit_SFM_Detector_image_Roi_X_Left, [115, 544, linedit_size_X, linedit_size_Y], "lineEdit_SFM_Detector_image_Roi_X_Left", font=font_ee)
        self.label_SFM_Detector_image_Roi_X_Right = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.__create_element(self.label_SFM_Detector_image_Roi_X_Right, [85, 565, 51, 16], "label_SFM_Detector_image_Roi_X_Right", font=font_ee, text="right")
        self.lineEdit_SFM_Detector_image_Roi_X_Right = QtWidgets.QLineEdit(self.tab_SFM_Detector_image)
        self.__create_element(self.lineEdit_SFM_Detector_image_Roi_X_Right, [115, 564, linedit_size_X, linedit_size_Y], "lineEdit_SFM_Detector_image_Roi_X_Right", font=font_ee)
        self.label_SFM_Detector_image_Roi_Y_Bottom = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.__create_element(self.label_SFM_Detector_image_Roi_Y_Bottom, [155, 545, 51, 16], "label_SFM_Detector_image_Roi_Y_Bottom", font=font_ee, text="bottom")
        self.lineEdit_SFM_Detector_image_Roi_Y_Bottom = QtWidgets.QLineEdit(self.tab_SFM_Detector_image)
        self.__create_element(self.lineEdit_SFM_Detector_image_Roi_Y_Bottom, [195, 544, linedit_size_X, linedit_size_Y], "lineEdit_SFM_Detector_image_Roi_Y_Bottom", font=font_ee)
        self.label_SFM_Detector_image_Roi_Y_Top = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.__create_element(self.label_SFM_Detector_image_Roi_Y_Top, [155, 565, 51, 16], "label_SFM_Detector_image_Roi_Y_Top", font=font_ee, text="top")
        self.lineEdit_SFM_Detector_image_Roi_Y_Top = QtWidgets.QLineEdit(self.tab_SFM_Detector_image)
        self.__create_element(self.lineEdit_SFM_Detector_image_Roi_Y_Top, [195, 564, linedit_size_X, linedit_size_Y], "lineEdit_SFM_Detector_image_Roi_Y_Top", font=font_ee)
        self.label_SFM_Detector_image_Roi_bkg = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.__create_element(self.label_SFM_Detector_image_Roi_bkg, [245, 545, 47, 16], "label_SFM_Detector_image_Roi_bkg", font=font_ee, text="BKG:")
        self.label_SFM_Detector_image_Roi_bkg_X_Left = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.__create_element(self.label_SFM_Detector_image_Roi_bkg_X_Left, [270, 545, 51, 16], "label_SFM_Detector_image_Roi_bkg_X_Left", font=font_ee, text="left")
        self.lineEdit_SFM_Detector_image_Roi_bkg_X_Left = QtWidgets.QLineEdit(self.tab_SFM_Detector_image)
        self.__create_element(self.lineEdit_SFM_Detector_image_Roi_bkg_X_Left, [300, 544, linedit_size_X, linedit_size_Y], "lineEdit_SFM_Detector_image_Roi_bkg_X_Left", font=font_ee, enabled=False, stylesheet="color:rgb(0,0,0)")
        self.label_SFM_Detector_image_Roi_bkg_X_Right = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.__create_element(self.label_SFM_Detector_image_Roi_bkg_X_Right, [270, 565, 51, 16], "label_SFM_Detector_image_Roi_bkg_X_Right", font=font_ee, text="right")
        self.lineEdit_SFM_Detector_image_Roi_bkg_X_Right = QtWidgets.QLineEdit(self.tab_SFM_Detector_image)
        self.__create_element(self.lineEdit_SFM_Detector_image_Roi_bkg_X_Right, [300, 564, linedit_size_X, linedit_size_Y], "lineEdit_SFM_Detector_image_Roi_bkg_X_Right", font=font_ee)
        self.label_SFM_Detector_image_Time = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.__create_element(self.label_SFM_Detector_image_Time, [350, 545, 71, 16], "label_SFM_Detector_image_Time", font=font_ee, text="Time (s):")
        self.lineEdit_SFM_Detector_image_Time = QtWidgets.QLineEdit(self.tab_SFM_Detector_image)
        self.__create_element(self.lineEdit_SFM_Detector_image_Time, [400, 544, linedit_size_X, linedit_size_Y], "lineEdit_SFM_Detector_image_Time", font=font_ee, enabled=False, stylesheet="color:rgb(0,0,0)")
        self.label_SFM_Detector_image_Slits = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.__create_element(self.label_SFM_Detector_image_Slits, [450, 545, 51, 16], "label_SFM_Detector_image_Slits", font=font_ee, text="Slits (mm):")
        self.label_SFM_Detector_image_Slits_s1hg = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.__create_element(self.label_SFM_Detector_image_Slits_s1hg, [505, 545, 41, 16], "label_SFM_Detector_image_Slits_s1hg", font=font_ee, text="s1hg")
        self.lineEdit_SFM_Detector_image_Slits_s1hg = QtWidgets.QLineEdit(self.tab_SFM_Detector_image)
        self.__create_element(self.lineEdit_SFM_Detector_image_Slits_s1hg, [535, 544, linedit_size_X, linedit_size_Y], "lineEdit_SFM_Detector_image_Slits_s1hg", font=font_ee, enabled=False, stylesheet="color:rgb(0,0,0)")
        self.label_SFM_Detector_image_Slits_s2hg = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.__create_element(self.label_SFM_Detector_image_Slits_s2hg, [505, 565, 30, 16], "label_SFM_Detector_image_Slits_s2hg", font=font_ee, text="s2hg")
        self.lineEdit_SFM_Detector_image_Slits_s2hg = QtWidgets.QLineEdit(self.tab_SFM_Detector_image)
        self.__create_element(self.lineEdit_SFM_Detector_image_Slits_s2hg, [535, 564, linedit_size_X, linedit_size_Y], "lineEdit_SFM_Detector_image_Slits_s2hg", font=font_ee, enabled=False, stylesheet="color:rgb(0,0,0)")
        self.tabWidget_SFM.addTab(self.tab_SFM_Detector_image, "")
        self.tabWidget_SFM.setTabText(self.tabWidget_SFM.indexOf(self.tab_SFM_Detector_image), "Detector Image")

        # Tab: Reflectivity preview
        self.tab_SFM_Reflectivity_preview = QtWidgets.QWidget()
        self.tab_SFM_Reflectivity_preview.setObjectName("tabreflectivity_preview")
        self.graphicsView_SFM_Reflectivity_preview = pg.PlotWidget(self.tab_SFM_Reflectivity_preview)
        self.__create_element(self.graphicsView_SFM_Reflectivity_preview, [0, 20, 577, 540], "graphicsView_SFM_Reflectivity_preview")
        self.graphicsView_SFM_Reflectivity_preview.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_SFM_Reflectivity_preview.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_SFM_Reflectivity_preview.getAxis("left").tickFont = font_graphs
        self.graphicsView_SFM_Reflectivity_preview.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_SFM_Reflectivity_preview.showAxis("top")
        self.graphicsView_SFM_Reflectivity_preview.getAxis("top").setTicks([])
        self.graphicsView_SFM_Reflectivity_preview.showAxis("right")
        self.graphicsView_SFM_Reflectivity_preview.getAxis("right").setTicks([])
        self.checkBox_SFM_Reflectivity_preview_Show_overillumination = QtWidgets.QCheckBox(self.tab_SFM_Reflectivity_preview)
        self.__create_element(self.checkBox_SFM_Reflectivity_preview_Show_overillumination, [10, 6, 140, 18], "checkBox_SFM_Reflectivity_preview_Show_overillumination", text="Show Overillumination", font=font_ee)
        self.checkBox_SFM_Reflectivity_preview_Show_zero_level = QtWidgets.QCheckBox(self.tab_SFM_Reflectivity_preview)
        self.__create_element(self.checkBox_SFM_Reflectivity_preview_Show_zero_level, [150, 6, 150, 18], "checkBox_SFM_Reflectivity_preview_Show_zero_level", text="Show Zero level", font=font_ee)
        self.label_SFM_Reflectivity_preview_View_Reflectivity = QtWidgets.QLabel(self.tab_SFM_Reflectivity_preview)
        self.__create_element(self.label_SFM_Reflectivity_preview_View_Reflectivity, [320, 7, 100, 16], "label_SFM_Reflectivity_preview_View_Reflectivity", text="View: Reflectivity", font=font_ee)
        self.comboBox_SFM_Reflectivity_preview_View_Reflectivity = QtWidgets.QComboBox(self.tab_SFM_Reflectivity_preview)
        self.__create_element(self.comboBox_SFM_Reflectivity_preview_View_Reflectivity, [410, 5, 50, 20], "comboBox_SFM_Reflectivity_preview_View_Reflectivity", font=font_ee, combo=["Log", "Lin"])
        self.label_SFM_Reflectivity_preview_View_Angle = QtWidgets.QLabel(self.tab_SFM_Reflectivity_preview)
        self.__create_element(self.label_SFM_Reflectivity_preview_View_Angle, [470, 7, 50, 16], "label_SFM_Reflectivity_preview_View_Angle", text="vs Angle", font=font_ee)
        self.comboBox_SFM_Reflectivity_preview_View_Angle = QtWidgets.QComboBox(self.tab_SFM_Reflectivity_preview)
        self.__create_element(self.comboBox_SFM_Reflectivity_preview_View_Angle, [515, 5, 50, 20], "comboBox_SFM_Reflectivity_preview_View_Angle", font=font_ee, combo=["Qz", "Deg"])
        self.checkBox_SFM_Reflectivity_preview_Include_errorbars = QtWidgets.QCheckBox(self.tab_SFM_Reflectivity_preview)
        self.__create_element(self.checkBox_SFM_Reflectivity_preview_Include_errorbars, [10, 565, 111, 18], "checkBox_SFM_Reflectivity_preview_Include_errorbars", text="Include Error Bars", font=font_ee)
        self.label_SFM_Reflectivity_preview_Skip_points_Left = QtWidgets.QLabel(self.tab_SFM_Reflectivity_preview)
        self.__create_element(self.label_SFM_Reflectivity_preview_Skip_points_Left, [372, 565, 100, 16], "label_SFM_Reflectivity_preview_Skip_points_Left", text="Points to skip:  left", font=font_ee)
        self.lineEdit_SFM_Reflectivity_preview_Skip_points_Left = QtWidgets.QLineEdit(self.tab_SFM_Reflectivity_preview)
        self.__create_element(self.lineEdit_SFM_Reflectivity_preview_Skip_points_Left, [470, 565, linedit_size_X, linedit_size_Y], "lineEdit_SFM_Reflectivity_preview_Skip_points_Left", text="0", font=font_ee)
        self.label_SFM_Reflectivity_preview_Skip_points_Right = QtWidgets.QLabel(self.tab_SFM_Reflectivity_preview)
        self.__create_element(self.label_SFM_Reflectivity_preview_Skip_points_Right, [510, 565, 80, 16], "label_SFM_Reflectivity_preview_Skip_points_Right", text="right", font=font_ee)
        self.lineEdit_SFM_Reflectivity_preview_Skip_points_Right = QtWidgets.QLineEdit(self.tab_SFM_Reflectivity_preview)
        self.__create_element(self.lineEdit_SFM_Reflectivity_preview_Skip_points_Right, [535, 565, linedit_size_X, linedit_size_Y], "lineEdit_SFM_Reflectivity_preview_Skip_points_Right", text="0", font=font_ee)
        self.tabWidget_SFM.addTab(self.tab_SFM_Reflectivity_preview, "")
        self.tabWidget_SFM.setTabText(self.tabWidget_SFM.indexOf(self.tab_SFM_Reflectivity_preview), "Reflectivity preview")

        # Tab: 2D Map
        self.tab_2Dmap = QtWidgets.QWidget()
        self.tab_2Dmap.setObjectName("tab_2Dmap")
        # scaling options are different for different views
        # "scale" for "Qx vs Qz"
        self.label_SFM_2Dmap_Qxz_Threshold = QtWidgets.QLabel(self.tab_2Dmap)
        self.__create_element(self.label_SFM_2Dmap_Qxz_Threshold, [5, 7, 220, 16], "label_SFM_2Dmap_Qxz_Threshold", text="Threshold for the view (number of neutrons):", font=font_ee, visible=False)
        self.comboBox_SFM_2Dmap_Qxz_Threshold = QtWidgets.QComboBox(self.tab_2Dmap)
        self.__create_element(self.comboBox_SFM_2Dmap_Qxz_Threshold, [230, 5, 40, 20], "comboBox_SFM_2Dmap_Qxz_Threshold", font=font_ee, visible=False, combo=[1, 2, 5, 10])
        self.label_SFM_2Dmap_View_scale = QtWidgets.QLabel(self.tab_2Dmap)
        self.__create_element(self.label_SFM_2Dmap_View_scale, [183, 7, 40, 16], "label_SFM_2Dmap_View_scale", text="View", font=font_ee)
        self.comboBox_SFM_2Dmap_View_scale = QtWidgets.QComboBox(self.tab_2Dmap)
        self.__create_element(self.comboBox_SFM_2Dmap_View_scale, [210, 5, 50, 20], "comboBox_SFM_2Dmap_View_scale", font=font_ee, combo=["Log", "Lin"])
        self.label_SFM_2Dmap_Polarisation = QtWidgets.QLabel(self.tab_2Dmap)
        self.__create_element(self.label_SFM_2Dmap_Polarisation, [284, 7, 71, 16], "label_SFM_2Dmap_Polarisation", text="Polarisation", font=font_ee)
        self.comboBox_SFM_2Dmap_Polarisation = QtWidgets.QComboBox(self.tab_2Dmap)
        self.__create_element(self.comboBox_SFM_2Dmap_Polarisation, [344, 5, 40, 20], "comboBox_SFM_2Dmap_Polarisation", font=font_ee)
        self.label_SFM_2Dmap_Axes = QtWidgets.QLabel(self.tab_2Dmap)
        self.__create_element(self.label_SFM_2Dmap_Axes, [405, 7, 71, 16], "label_SFM_2Dmap_Axes", text="Axes", font=font_ee)
        self.comboBox_SFM_2Dmap_Axes = QtWidgets.QComboBox(self.tab_2Dmap)
        self.__create_element(self.comboBox_SFM_2Dmap_Axes, [435, 5, 130, 20], "comboBox_SFM_2Dmap_Axes", font=font_ee, combo=["Pixel vs. Point", "Alpha_i vs. Alpha_f", "Qx vs. Qz"])
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
        # I rescale graphicsView_SFM_2Dmap_Qxz_Theta to show/hide it
        self.graphicsView_SFM_2Dmap_Qxz_Theta = pg.PlotWidget(self.tab_2Dmap)
        self.__create_element(self.graphicsView_SFM_2Dmap_Qxz_Theta, [0, 0, 0, 0], "graphicsView_SFM_2Dmap_Qxz_Theta")
        self.graphicsView_SFM_2Dmap_Qxz_Theta.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_SFM_2Dmap_Qxz_Theta.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_SFM_2Dmap_Qxz_Theta.getAxis("left").tickFont = font_graphs
        self.graphicsView_SFM_2Dmap_Qxz_Theta.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_SFM_2Dmap_Qxz_Theta.showAxis("top")
        self.graphicsView_SFM_2Dmap_Qxz_Theta.getAxis("top").setTicks([])
        self.graphicsView_SFM_2Dmap_Qxz_Theta.showAxis("right")
        self.graphicsView_SFM_2Dmap_Qxz_Theta.getAxis("right").setTicks([])
        self.label_SFM_2Dmap_Lower_number_of_points_by = QtWidgets.QLabel(self.tab_2Dmap)
        self.__create_element(self.label_SFM_2Dmap_Lower_number_of_points_by, [5, 561, 211, 16], "label_SFM_2Dmap_Lower_number_of_points_by", text="Lower the number of points by factor", font=font_ee, visible=False)
        self.comboBox_SFM_2Dmap_Lower_number_of_points_by = QtWidgets.QComboBox(self.tab_2Dmap)
        self.__create_element(self.comboBox_SFM_2Dmap_Lower_number_of_points_by, [195, 559, 40, 20], "comboBox_SFM_2Dmap_Lower_number_of_points_by", font=font_ee, visible=False, combo=[5, 4, 3, 2, 1])
        self.label_SFM_2Dmap_Rescale_image_x = QtWidgets.QLabel(self.tab_2Dmap)
        self.__create_element(self.label_SFM_2Dmap_Rescale_image_x, [5, 561, 85, 16], "label_SFM_2Dmap_Rescale_image_x", text="Rescale image: x", font=font_ee)
        self.horizontalSlider_SFM_2Dmap_Rescale_image_x = QtWidgets.QSlider(self.tab_2Dmap)
        self.__create_element(self.horizontalSlider_SFM_2Dmap_Rescale_image_x, [95, 560, 80, 22], "horizontalSlider_SFM_2Dmap_Rescale_image_x")
        self.horizontalSlider_SFM_2Dmap_Rescale_image_x.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_SFM_2Dmap_Rescale_image_x.setMinimum(1)
        self.horizontalSlider_SFM_2Dmap_Rescale_image_x.setMaximum(15)
        self.horizontalSlider_SFM_2Dmap_Rescale_image_x.setValue(1)
        self.label_SFM_2Dmap_Rescale_image_y = QtWidgets.QLabel(self.tab_2Dmap)
        self.__create_element(self.label_SFM_2Dmap_Rescale_image_y, [185, 561, 20, 16], "label_SFM_2Dmap_Rescale_image_y", text="y", font=font_ee)
        self.horizontalSlider_SFM_2Dmap_Rescale_image_y = QtWidgets.QSlider(self.tab_2Dmap)
        self.__create_element(self.horizontalSlider_SFM_2Dmap_Rescale_image_y, [195, 560, 80, 22], "horizontalSlider_SFM_2Dmap_Rescale_image_y")
        self.horizontalSlider_SFM_2Dmap_Rescale_image_y.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_SFM_2Dmap_Rescale_image_y.setMinimum(1)
        self.horizontalSlider_SFM_2Dmap_Rescale_image_y.setMaximum(15)
        self.horizontalSlider_SFM_2Dmap_Rescale_image_y.setValue(1)
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
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.__create_element(self.menu_Help, [999, 999, 999, 999], "menu_Help", title="Help")
        MainWindow.setMenuBar(self.menubar)
        self.action_Algorithm_info = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Algorithm_info, [999, 999, 999, 999], "action_Algorithm_info", text="Algorithm info")
        self.action_Version = QtWidgets.QAction(MainWindow)
        self.__create_element(self.action_Version, [999, 999, 999, 999], "action_Version", text="V1.5")
        self.menu_Help.addAction(self.action_Algorithm_info)
        self.menu_Help.addAction(self.action_Version)
        self.menubar.addAction(self.menu_Help.menuAction())

        self.tabWidget_Reductions.setCurrentIndex(0)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    ##<--

class GUI(Ui_MainWindow):

    current_dir = ""
    if platform.system() == 'Windows': current_dir = os.getcwd().replace("\\", "/") + "/"
    else:
        for i in sys.argv[0].split("/")[:-4]: current_dir += i + "/"

    def __init__(self):

        super(GUI, self).__init__()
        self.setupUi(self)

        # Some parameters
        self.locked_roi = []
        self.SFM_FILE, self.sfm_file_already_analized, self.sfm_file_2d_calculated_params = "", "", []  # current file in Single File Mode
        self.psd_uu_sfm, self.psd_du_sfm, self.psd_ud_sfm, self.psd_dd_sfm = [], [], [], []             # 2d arrays of pol detector
        self.current_th = ""                                                                            # current th point
        self.overill_coeff_lib = {}                                                                     # write calculated overillumination coefficients into library
        self.DB_INFO, self.db_already_analized = {}, []                                                 # Write DB info into library
        self.draw_roi, self.draw_roi_bkg, self.draw_roi_2D_map = [], [], []                             # ROI frames
        self.old_roi_coord_Y, self.draw_roi_int = [], []                                                # Recalc intens if Y roi is changed
        self.show_det_int_trigger = True                                                                # Trigger to switch the detector image view
        self.res_Aif = []                                                                               # Alpha_i vs Alpha_f array
        self.sample_curvature_last = "0"                                                                # Last sample curvature (lets avoid extra recalcs)

        # Triggers
        self.action_Version.triggered.connect(self.menu_info)
        self.action_Algorithm_info.triggered.connect(self.menu_algorithm)

        # Triggers: Buttons
        self.pushButton_Import_scans.clicked.connect(self.button_import_remove_scans)
        self.pushButton_Delete_scans.clicked.connect(self.button_import_remove_scans)
        self.pushButton_Import_DB.clicked.connect(self.button_import_remove_db)
        self.pushButton_Delete_DB.clicked.connect(self.button_import_remove_db)
        self.toolButton_Save_at.clicked.connect(self.button_SaveDir)
        self.pushButton_Reduce_all.clicked.connect(self.button_reduce_all)
        self.pushButton_Reduce_SFM.clicked.connect(self.button_reduce_sfm)
        self.pushButton_Clear.clicked.connect(self.button_Clear)
        self.pushButton_SFM_2Dmap_export.clicked.connect(self.export_2d_map)
        self.pushButton_SFM_Detector_image_Show_integrated_roi.clicked.connect(self.draw_det_image)

        # Triggers: LineEdits
        self.lineEdit_SFM_Detector_image_Roi_X_Left.editingFinished.connect(self.update_slits)
        self.lineEdit_SFM_Detector_image_Roi_X_Right.editingFinished.connect(self.update_slits)
        self.lineEdit_SFM_Detector_image_Roi_Y_Bottom.editingFinished.connect(self.update_slits)
        self.lineEdit_SFM_Detector_image_Roi_Y_Top.editingFinished.connect(self.update_slits)
        self.lineEdit_SFM_Detector_image_Roi_bkg_X_Right.editingFinished.connect(self.update_slits)
        self.lineEdit_Sample_len.editingFinished.connect(self.load_SFM_Reflectivity_preview)
        self.lineEdit_Reductions_Attenuator_DB.editingFinished.connect(self.load_SFM_Reflectivity_preview)
        self.lineEdit_Reductions_Subtract_bkg_Skip.editingFinished.connect(self.load_SFM_Reflectivity_preview)
        self.lineEdit_Instrument_Wavelength.editingFinished.connect(self.load_SFM_Reflectivity_preview)
        self.lineEdit_Instrument_Wavelength_resolution.editingFinished.connect(self.load_SFM_Reflectivity_preview)
        self.lineEdit_Instrument_Distance_s1_to_sample.editingFinished.connect(self.load_SFM_Reflectivity_preview)
        self.lineEdit_Instrument_Distance_s2_to_sample.editingFinished.connect(self.load_SFM_Reflectivity_preview)
        self.lineEdit_Instrument_Offset_full.editingFinished.connect(self.load_SFM_Reflectivity_preview)
        self.lineEdit_SFM_Reflectivity_preview_Skip_points_Right.editingFinished.connect(self.load_SFM_Reflectivity_preview)
        self.lineEdit_SFM_Reflectivity_preview_Skip_points_Left.editingFinished.connect(self.load_SFM_Reflectivity_preview)
        self.lineEdit_Instrument_Wavelength.editingFinished.connect(self.draw_2D_map)
        self.lineEdit_Instrument_Distance_sample_to_detector.editingFinished.connect(self.draw_2D_map)
        self.lineEdit_Reductions_Scale_factor.editingFinished.connect(self.load_SFM_Reflectivity_preview)
        self.lineEdit_Instrument_Sample_curvature.editingFinished.connect(self.load_SFM_Reflectivity_preview)
        self.lineEdit_Instrument_Sample_curvature.editingFinished.connect(self.draw_2D_map)

        # Triggers: ComboBoxes
        self.comboBox_SFM_Detector_image_Incident_angle.currentIndexChanged.connect(self.draw_det_image)
        self.comboBox_SFM_Detector_image_Polarisation.currentIndexChanged.connect(self.draw_det_image)
        self.comboBox_SFM_Scan.currentIndexChanged.connect(self.load_SFM_Detector_images)
        self.comboBox_SFM_Scan.currentIndexChanged.connect(self.load_SFM_Reflectivity_preview)
        self.comboBox_SFM_Reflectivity_preview_View_Angle.currentIndexChanged.connect(self.load_SFM_Reflectivity_preview)
        self.comboBox_SFM_Reflectivity_preview_View_Reflectivity.currentIndexChanged.connect(self.load_SFM_Reflectivity_preview)
        self.comboBox_SFM_2Dmap_Qxz_Threshold.currentIndexChanged.connect(self.draw_2D_map)
        self.comboBox_SFM_2Dmap_Polarisation.currentIndexChanged.connect(self.draw_2D_map)
        self.comboBox_SFM_2Dmap_Axes.currentIndexChanged.connect(self.draw_2D_map)
        self.comboBox_SFM_Scan.currentIndexChanged.connect(self.draw_2D_map)
        self.comboBox_SFM_2Dmap_Lower_number_of_points_by.currentIndexChanged.connect(self.draw_2D_map)
        self.comboBox_SFM_Detector_image_Color_scheme.currentIndexChanged.connect(self.color_det_image)
        self.comboBox_Reductions_Divide_by_monitor_or_time.currentIndexChanged.connect(self.db_analaze)
        self.comboBox_Reductions_Divide_by_monitor_or_time.currentIndexChanged.connect(self.load_SFM_Reflectivity_preview)
        self.comboBox_SFM_2Dmap_View_scale.currentIndexChanged.connect(self.draw_2D_map)

        # Triggers: CheckBoxes
        self.checkBox_Reductions_Divide_by_monitor_or_time.stateChanged.connect(self.db_analaze)
        self.checkBox_Reductions_Divide_by_monitor_or_time.stateChanged.connect(self.load_SFM_Reflectivity_preview)
        self.checkBox_Reductions_Normalize_by_DB.stateChanged.connect(self.db_analaze)
        self.checkBox_Reductions_Normalize_by_DB.stateChanged.connect(self.load_SFM_Reflectivity_preview)
        self.checkBox_Reductions_Attenuator_DB.stateChanged.connect(self.load_SFM_Reflectivity_preview)
        self.checkBox_Reductions_Overillumination_correction.stateChanged.connect(self.load_SFM_Reflectivity_preview)
        self.checkBox_Reductions_Subtract_bkg.stateChanged.connect(self.load_SFM_Reflectivity_preview)
        self.checkBox_Reductions_Subtract_bkg.stateChanged.connect(self.draw_det_image)
        self.checkBox_SFM_Reflectivity_preview_Show_overillumination.stateChanged.connect(self.load_SFM_Reflectivity_preview)
        self.checkBox_SFM_Reflectivity_preview_Show_zero_level.stateChanged.connect(self.load_SFM_Reflectivity_preview)
        self.checkBox_SFM_Reflectivity_preview_Include_errorbars.stateChanged.connect(self.load_SFM_Reflectivity_preview)
        self.checkBox_Rearrange_DB_after.stateChanged.connect(self.load_SFM_Reflectivity_preview)
        self.checkBox_Rearrange_DB_after.stateChanged.connect(self.db_assign)
        self.checkBox_Reductions_Scale_factor.stateChanged.connect(self.load_SFM_Reflectivity_preview)

        # Triggers: Sliders
        self.horizontalSlider_SFM_2Dmap_Rescale_image_x.valueChanged.connect(self.draw_2D_map)
        self.horizontalSlider_SFM_2Dmap_Rescale_image_y.valueChanged.connect(self.draw_2D_map)

    ##--> menu options
    def menu_info(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowIcon(QtGui.QIcon(self.iconpath))
        msgBox.setText("pySAred " + self.action_Version.text() + "\n\n"
                       "Alexey.Klechikov@gmail.com\n\n"
                       "Check new version at https://github.com/Alexey-Klechikov/pySAred/releases")
        msgBox.exec_()

    def menu_algorithm(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowIcon(QtGui.QIcon(self.iconpath))
        msgBox.setText("1) Area for background estimation is automatically set to the same size as ROI.\n\n"
                       "2) File can appear in \"Recheck following files in Single File Mode\" if peak of its intensity (around Qz 0.015) is not in the middle of ROI.\n\n"
                       "3) Trapezoid beam form is used for overillumination correction.\n\n"
                       "4) Files are exported as Qz, I, dI, (dQz)\n\n"
                       "5) Button 'Reduce all' will export all Data files with no changes applied in SFM block. \n\n"
                       )

        msgBox.exec_()
    ##<--

    ##--> Main window buttons
    def button_import_remove_scans(self):

        if self.sender().objectName() == "pushButton_Import_scans":

            import_files = QtWidgets.QFileDialog().getOpenFileNames(None, "FileNames", self.current_dir, ".h5 (*.h5)")
            if import_files[0] == []: return
            # Next "Import scans" will open last dir
            self.current_dir = import_files[0][0][:import_files[0][0].rfind("/")]

            for FILE in import_files[0]:
                self.tableWidget_Scans.insertRow(self.tableWidget_Scans.rowCount())
                self.tableWidget_Scans.setRowHeight(self.tableWidget_Scans.rowCount()-1, 10)
                # File name (row 0) and full path (row 2)
                for j in range(0, 3): self.tableWidget_Scans.setItem(self.tableWidget_Scans.rowCount()-1, j, QtWidgets.QTableWidgetItem())
                self.tableWidget_Scans.item(self.tableWidget_Scans.rowCount() - 1, 0).setText(FILE[FILE.rfind("/") + 1:])
                self.tableWidget_Scans.item(self.tableWidget_Scans.rowCount() - 1, 2).setText(FILE)

                # add file into SFM / Scan ComboBox
                self.comboBox_SFM_Scan.addItem(str(FILE[FILE.rfind("/") + 1:]))

                self.db_analaze()
                self.load_SFM_Reflectivity_preview()

        if self.sender().objectName() == "pushButton_Delete_scans":

            remove_files = self.tableWidget_Scans.selectedItems()
            if not remove_files: return

            for FILE in remove_files:
                self.tableWidget_Scans.removeRow(self.tableWidget_Scans.row(FILE))

            # update SFM list
            self.comboBox_SFM_Scan.clear()

            for i in range(0, self.tableWidget_Scans.rowCount()):
                # add file into SFM
                self.comboBox_SFM_Scan.addItem(self.tableWidget_Scans.item(i, 2).text()[
                            self.tableWidget_Scans.item(i, 2).text().rfind("/") + 1:])

    def button_import_remove_db(self):

        if self.sender().objectName() == "pushButton_Import_DB":

            import_files = QtWidgets.QFileDialog().getOpenFileNames(None, "FileNames", self.current_dir, ".h5 (*.h5)")
            if import_files[0] == []: return
            # Next "Import scans" will open last dir
            self.current_dir = import_files[0][0][:import_files[0][0].rfind("/")]

            # I couldnt make tablewidget sorting work when adding files to not empty table, so this is the solution for making the list of DB files sorted
            for i in range(self.tableWidget_DB.rowCount()-1, -1, -1):
                import_files[0].append(self.tableWidget_DB.item(i, 1).text())
                self.tableWidget_DB.removeRow(i)

            for FILE in sorted(import_files[0]):
                self.tableWidget_DB.insertRow(self.tableWidget_DB.rowCount())
                self.tableWidget_DB.setRowHeight(self.tableWidget_DB.rowCount()-1, 10)
                # File name (row 0) and full path (row 2)
                for j in range(0, 2): self.tableWidget_DB.setItem(self.tableWidget_DB.rowCount()-1, j, QtWidgets.QTableWidgetItem())
                self.tableWidget_DB.item(self.tableWidget_DB.rowCount() - 1, 0).setText(FILE[FILE.rfind("/") + 1:])
                self.tableWidget_DB.item(self.tableWidget_DB.rowCount() - 1, 1).setText(FILE)

            self.db_analaze()
            self.load_SFM_Reflectivity_preview()

        elif self.sender().objectName() == "pushButton_Delete_DB":

            remove_files = self.tableWidget_DB.selectedItems()
            if not remove_files: return

            for FILE in remove_files:
                self.tableWidget_DB.removeRow(self.tableWidget_DB.row(FILE))

            self.db_analaze()

    def button_SaveDir(self):
        saveAt = QtWidgets.QFileDialog().getExistingDirectory()
        if not saveAt: return
        self.lineEdit_Save_at.setText(str(saveAt) + ("" if str(saveAt)[-1] == "/" else "/"))

    def button_reduce_all(self):
        self.listWidget_Recheck_files_in_SFM.clear()

        skip_bkg = float(self.lineEdit_Reductions_Subtract_bkg_Skip.text()) if self.lineEdit_Reductions_Subtract_bkg_Skip.text() else 0

        save_file_directory = self.lineEdit_Save_at.text() if self.lineEdit_Save_at.text() else self.current_dir

        if self.checkBox_Reductions_Overillumination_correction.isChecked() and self.lineEdit_Sample_len.text() == "":
            self.statusbar.showMessage("Sample length is missing")
            return

        if self.checkBox_Reductions_Normalize_by_DB.isChecked():
            if self.tableWidget_DB.rowCount() == 0:
                self.label_Error_DB_missing.setVisible(True)
                return

            self.db_analaze()

            db_atten_factor = 1
            if self.checkBox_Reductions_Attenuator_DB.isChecked():
                try:
                    db_atten_factor = 10 if self.lineEdit_Reductions_Attenuator_DB.text() == "" else float(self.lineEdit_Reductions_Attenuator_DB.text())
                except: True

        # iterate through table with scans
        for i in range(0, self.tableWidget_Scans.rowCount()):
            file_name = self.tableWidget_Scans.item(i, 2).text()[self.tableWidget_Scans.item(i, 2).text().rfind("/") + 1: -3]

            # find full name DB file if there are several of them
            FILE_DB = self.tableWidget_Scans.item(i, 1).text() if self.checkBox_Reductions_Normalize_by_DB.isChecked() else ""

            with h5py.File(self.tableWidget_Scans.item(i, 2).text(), 'r') as FILE:

                INSTRUMENT = FILE[list(FILE.keys())[0]].get("instrument")
                MOTOR_DATA = np.array(INSTRUMENT.get('motors').get('data')).T
                SCALERS_DATA = np.array(INSTRUMENT.get('scalers').get('data')).T

                for index, motor in enumerate(INSTRUMENT.get('motors').get('SPEC_motor_mnemonics')):
                    if "'th'" in str(motor): th_list = MOTOR_DATA[index]
                    elif "'s1hg'" in str(motor): s1hg_list = MOTOR_DATA[index]
                    elif "'s2hg'" in str(motor): s2hg_list = MOTOR_DATA[index]

                check_this_file = 0

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

                    new_file = open(save_file_directory + file_name + "_" + str(detector) + " (" + FILE_DB + ")" + ".dat", "w")

                    # iterate through th points
                    for index, th in enumerate(th_list):

                        if th == 0: continue

                        # analize integrated intensity for ROI
                        Intens = scan_intens[index] if len(scan_intens.shape) == 1 else sum(scan_intens[index][int(original_roi_coord[2]): int(original_roi_coord[3])])

                        if Intens == 0 and self.checkBox_Export_Remove_zeros.isChecked(): continue

                        Intens_err = 1 if Intens == 0 else np.sqrt(Intens)

                        # read motors
                        Qz, s1hg, s2hg = (4 * np.pi / float(self.lineEdit_Instrument_Wavelength.text())) * np.sin(np.radians(th)), s1hg_list[index], s2hg_list[index]
                        monitor = monitor_list[index] if self.comboBox_Reductions_Divide_by_monitor_or_time.currentText() == "monitor" else time_list[index]

                        # check if we are not in a middle of ROI in Qz approx 0.02)
                        if round(Qz, 3) > 0.015 and round(Qz, 3) < 0.03 and check_this_file == 0:
                            scan_data_0_015 = scan_intens[index][int(original_roi_coord[2]): int(original_roi_coord[3])]

                            if not max(scan_data_0_015) == max(scan_data_0_015[round((len(scan_data_0_015) / 3)):-round((len(scan_data_0_015) / 3))]):
                                self.listWidget_Recheck_files_in_SFM.addItem(file_name)
                                check_this_file = 1

                        coeff = self.overillumination_correct_coeff(s1hg, s2hg, round(th, 4))
                        FWHM_proj,  overill_corr = coeff[1], coeff[0] if self.checkBox_Reductions_Overillumination_correction.isChecked() else 1

                        # calculate resolution in Sared way or better
                        if self.checkBox_Export_Resolution_like_sared.isChecked():
                            Resolution = np.sqrt(((2 * np.pi / float(self.lineEdit_Instrument_Wavelength.text())) ** 2) * ((np.cos(np.radians(th))) ** 2) * (0.68 ** 2) * ((s1hg ** 2) + (s2hg ** 2)) / ((float(self.lineEdit_Instrument_Distance_s1_to_sample.text()) - float(self.lineEdit_Instrument_Distance_s2_to_sample.text())) ** 2) + ((float(self.lineEdit_Instrument_Wavelength_resolution.text()) ** 2) * (Qz ** 2)))
                        else:
                            if FWHM_proj == s2hg:
                                Resolution = np.sqrt(((2 * np.pi / float(self.lineEdit_Instrument_Wavelength.text())) ** 2) * ((np.cos(np.radians(th))) ** 2) * (0.68 ** 2) * ((s1hg ** 2) + (s2hg ** 2)) / ((float(self.lineEdit_Instrument_Distance_s1_to_sample.text()) - float(self.lineEdit_Instrument_Distance_s2_to_sample.text())) ** 2) + ((float(self.lineEdit_Instrument_Wavelength_resolution.text()) ** 2) * (Qz ** 2)))
                            else:
                                Resolution = np.sqrt(((2 * np.pi / float(self.lineEdit_Instrument_Wavelength.text())) ** 2) * ((np.cos(np.radians(th))) ** 2) * (0.68 ** 2) * ((s1hg ** 2) + (FWHM_proj ** 2)) / (float(self.lineEdit_Instrument_Distance_s1_to_sample.text()) ** 2) + ((float(self.lineEdit_Instrument_Wavelength_resolution.text()) ** 2) * (Qz ** 2)))

                        # I cite Gunnar in here "We are now saving dQ as sigma rather than FWHM for genx"
                        Resolution = Resolution / (2 * np.sqrt(2 * np.log(2)))

                        # minus background, divide by monitor, overillumination correct + calculate errors
                        if self.checkBox_Reductions_Subtract_bkg.isChecked() and Qz > skip_bkg:
                            Intens_bkg = sum(scan_intens[index][int(original_roi_coord[2]) - 2 * (int(original_roi_coord[3]) - int(original_roi_coord[2])): int(original_roi_coord[2]) - (int(original_roi_coord[3]) - int(original_roi_coord[2]))])

                            if Intens_bkg > 0: Intens_err, Intens = np.sqrt(Intens + Intens_bkg), Intens - Intens_bkg

                        if self.checkBox_Reductions_Divide_by_monitor_or_time.isChecked():
                            if self.comboBox_Reductions_Divide_by_monitor_or_time.currentText() == "monitor":
                                monitor, Intens_err = monitor_list[index], Intens_err / monitor if Intens == 0 else (Intens / monitor) * np.sqrt((Intens_err / Intens) ** 2 + (1 / monitor))
                            elif self.comboBox_Reductions_Divide_by_monitor_or_time.currentText() == "time":
                                monitor, Intens_err = time_list[index], Intens_err / monitor

                            Intens = Intens / monitor

                        if self.checkBox_Reductions_Overillumination_correction.isChecked(): Intens_err, Intens = Intens_err / overill_corr, Intens / overill_corr

                        if self.checkBox_Reductions_Normalize_by_DB.isChecked():
                            try:
                                db_intens = float(self.DB_INFO[str(FILE_DB) + ";" + str(s1hg) + ";" + str(s2hg)].split(";")[0]) * db_atten_factor
                                db_err = overill_corr * float(self.DB_INFO[str(FILE_DB) + ";" + str(s1hg) + ";" + str(s2hg)].split(";")[1]) * self.db_atten_factor

                                Intens_err = Intens_err + db_err if Intens == 0 else (Intens / db_intens) * np.sqrt((db_err / db_intens) ** 2 + (Intens_err / Intens) ** 2)
                                Intens = Intens / db_intens
                            except:
                                if check_this_file == 0:
                                    self.listWidget_Recheck_files_in_SFM.addItem(file_name)
                                    check_this_file = 1

                            self.checkBox_Reductions_Scale_factor.setChecked(False)

                        if self.checkBox_Reductions_Scale_factor.isChecked(): Intens_err, Intens = Intens_err / self.scale_factor, Intens / self.scale_factor

                        # skip the first point
                        if index == 0 or (Intens == 0 and self.checkBox_Export_Remove_zeros.isChecked()): continue

                        new_file.write(str(Qz) + ' ' + str(Intens) + ' ' + str(Intens_err) + ' ')
                        if self.checkBox_Export_Add_resolution_column.isChecked(): new_file.write(str(Resolution))
                        new_file.write('\n')

                    # close files
                    new_file.close()

                    # check if file is empty - then comment inside
                    if os.stat(save_file_directory + file_name + "_" + str(detector) + " (" + FILE_DB + ")" + ".dat").st_size == 0:
                        with open(save_file_directory + file_name + "_" + str(detector) + " (" + FILE_DB + ")" + ".dat", "w") as empty_file:
                            empty_file.write("All points are either zeros or negatives.")

        self.statusbar.showMessage(str(self.tableWidget_Scans.rowCount()) + " files reduced, " + str(self.listWidget_Recheck_files_in_SFM.count()) + " file(s) might need extra care.")

    def button_reduce_sfm(self):

        save_file_directory = self.lineEdit_Save_at.text() if self.lineEdit_Save_at.text() else self.current_dir

        # polarisation order - uu, dd, ud, du
        detector = ["uu", "du", "ud", "dd"]

        for i in range(0, len(self.sfm_Export_Qz)):

            sfm_db_file_export = self.SFM_DB_FILE if self.checkBox_Reductions_Normalize_by_DB.isChecked() else ""

            with open(save_file_directory + self.SFM_FILE[self.SFM_FILE.rfind("/") + 1 : -3] + "_" + str(detector[i]) + " (" + sfm_db_file_export + ")" + " SFM.dat", "w") as new_file:
                for j in range(0, len(self.sfm_Export_Qz[i])):
                    if self.sfm_Export_Qz[i][j] == 0 or (self.sfm_Export_I[i][j] == 0 and self.checkBox_Export_Remove_zeros.isChecked()): continue
                    new_file.write(str(self.sfm_Export_Qz[i][j]) + ' ' + str(self.sfm_Export_I[i][j]) + ' ' + str(self.sfm_Export_dI[i][j]) + ' ')
                    if self.checkBox_Export_Add_resolution_column.isChecked(): new_file.write(str(self.sfm_Export_Resolution[i][j]))
                    new_file.write('\n')

            # close new file
            new_file.close()

        self.statusbar.showMessage(self.SFM_FILE[self.SFM_FILE.rfind("/") + 1:] + " file is reduced in SFM.")

    def button_Clear(self):

        for item in (self.comboBox_SFM_Scan, self.listWidget_Recheck_files_in_SFM, self.graphicsView_SFM_Detector_image, self.graphicsView_SFM_2Dmap, self.graphicsView_SFM_Reflectivity_preview.getPlotItem(),self.comboBox_SFM_Detector_image_Incident_angle, self.comboBox_SFM_Detector_image_Polarisation, self.comboBox_SFM_2Dmap_Polarisation):
            item.clear()

        for i in range(self.tableWidget_Scans.rowCount(), -1, -1): self.tableWidget_Scans.removeRow(i)
        for i in range(self.tableWidget_DB.rowCount(), -1, -1): self.tableWidget_DB.removeRow(i)
    ##<--

    ##--> extra functions to shorten the code
    def overillumination_correct_coeff(self, s1hg, s2hg, th):

        # Check for Sample Length input
        try:
            sample_len = float(self.lineEdit_Sample_len.text())
        except: return [1, s2hg]

        config = str(s1hg) + " " + str(s2hg) + " " + str(th) + " " + str(sample_len) + " " + self.lineEdit_Instrument_Distance_s1_to_sample.text() + " " + self.lineEdit_Instrument_Distance_s2_to_sample.text()

        # check if we already calculated overillumination for current configuration
        if config in self.overill_coeff_lib: coeff = self.overill_coeff_lib[config]
        else:
            coeff = [0, 0]

            # for trapezoid beam - find (half of) widest beam width (OC) and flat region (OB) with max intensity
            if s1hg < s2hg:
                OB = abs(((float(self.lineEdit_Instrument_Distance_s1_to_sample.text()) * (s2hg - s1hg)) / (2 * (float(self.lineEdit_Instrument_Distance_s1_to_sample.text()) - float(self.lineEdit_Instrument_Distance_s2_to_sample.text())))) + s1hg / 2)
                OC = ((float(self.lineEdit_Instrument_Distance_s1_to_sample.text()) * (s2hg + s1hg)) / (2 * (float(self.lineEdit_Instrument_Distance_s1_to_sample.text()) - float(self.lineEdit_Instrument_Distance_s2_to_sample.text())))) - s1hg / 2
            elif s1hg > s2hg:
                OB = abs(((s2hg * float(self.lineEdit_Instrument_Distance_s1_to_sample.text())) - (s1hg * float(self.lineEdit_Instrument_Distance_s2_to_sample.text()))) / (2 * (float(self.lineEdit_Instrument_Distance_s1_to_sample.text()) - float(self.lineEdit_Instrument_Distance_s2_to_sample.text()))))
                OC = (float(self.lineEdit_Instrument_Distance_s1_to_sample.text()) / (float(self.lineEdit_Instrument_Distance_s1_to_sample.text()) - float(self.lineEdit_Instrument_Distance_s2_to_sample.text()))) * (s2hg + s1hg) / 2 - (s1hg / 2)
            elif s1hg == s2hg:
                OB = s1hg / 2
                OC = s1hg * (float(self.lineEdit_Instrument_Distance_s1_to_sample.text()) / (float(self.lineEdit_Instrument_Distance_s1_to_sample.text()) - float(self.lineEdit_Instrument_Distance_s2_to_sample.text())) - 1 / 2)

            BC = OC - OB
            AO = 1 / (BC/2 + OB)  # normalized height of trapezoid
            FWHM_beam = BC/2 + OB  # half of the beam FWHM
            sample_len_relative = float(sample_len) * np.sin(np.radians(np.fabs(th)))  # projection of sample surface on the beam

            # "coeff" represents how much of total beam intensity illuminates the sample
            if sample_len_relative / 2 >= OC: coeff[0] = 1
            else:  # check if we use only middle part of the beam or trapezoid "shoulders" also
                if sample_len_relative / 2 <= OB: coeff[0] = AO*sample_len_relative/2 # Square part
                elif sample_len_relative / 2 > OB: coeff[0] = AO * (OB + BC/2 - ((OC-sample_len_relative/2)**2) / (2*BC)) # Square part + triangle - edge of triangle that dont cover the sample

            # for the beam resolution calcultion we check how much of the beam FHWM we cover by the sample
            coeff[1] = s2hg if sample_len_relative / 2 >= FWHM_beam else sample_len_relative

            self.overill_coeff_lib[config] = coeff

        return coeff

    def db_analaze(self):

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

                if self.checkBox_Reductions_Divide_by_monitor_or_time.isChecked(): monitor = monitor_list if self.comboBox_Reductions_Divide_by_monitor_or_time.currentText() == "monitor" else time_list
                else: monitor = np.ones_like(intens_list)

                for j in range(0, len(th_list)):
                    db_intens = float(intens_list[j]) / float(monitor[j])
                    if self.checkBox_Reductions_Divide_by_monitor_or_time.isChecked() and self.comboBox_Reductions_Divide_by_monitor_or_time.currentText() == "monitor":
                        db_err = db_intens * np.sqrt(1/float(intens_list[j]) + 1/float(monitor[j]))
                    else: db_err = np.sqrt(float(intens_list[j])) / float(monitor[j])

                    scan_slits_monitor = self.tableWidget_DB.item(i, 0).text()[:5] + ";" + str(s1hg_list[j]) + ";" + str(s2hg_list[j])

                    self.DB_INFO[scan_slits_monitor] = str(db_intens) + ";" + str(db_err)

        if self.tableWidget_DB.rowCount() == 0: return
        else: self.db_assign()

    def db_assign(self):

        db_list = []
        for db_scan_number in self.DB_INFO: db_list.append(db_scan_number.split(";")[0])

        for i in range(self.tableWidget_Scans.rowCount()):
            scan_number = self.tableWidget_Scans.item(i, 0).text()[:5]

            # find nearest DB file if there are several of them
            if len(db_list) == 0: FILE_DB = ""
            elif len(db_list) == 1: FILE_DB = db_list[0][:5]
            else:
                if self.checkBox_Rearrange_DB_after.isChecked():
                    for j, db_scan in enumerate(db_list):
                        FILE_DB = db_scan[:5]
                        if int(db_scan[:5]) > int(scan_number[:5]): break
                else:
                    for j, db_scan in enumerate(reversed(db_list)):
                        FILE_DB = db_scan[:5]
                        if int(db_scan[:5]) < int(scan_number[:5]): break

            self.tableWidget_Scans.item(i, 1).setText(FILE_DB)
    ##<--

    ##--> SFM
    def load_SFM_Detector_images(self):

        if self.comboBox_SFM_Scan.currentText() == "": return

        self.comboBox_SFM_Detector_image_Incident_angle.clear()
        self.comboBox_SFM_Detector_image_Polarisation.clear()
        self.comboBox_SFM_2Dmap_Polarisation.clear()

        # we need to find full path for the SFM file from the table
        for i in range(0, self.tableWidget_Scans.rowCount()):
            self.SFM_FILE = self.tableWidget_Scans.item(i, 2).text() if self.tableWidget_Scans.item(i, 0).text() == self.comboBox_SFM_Scan.currentText() else self.SFM_FILE

        with h5py.File(self.SFM_FILE, 'r') as FILE:
            SCAN = FILE[list(FILE.keys())[0]]

            if not self.locked_roi == [] and self.checkBox_SFM_Detector_image_Lock_roi.isChecked(): original_roi_coord = np.array(self.locked_roi[0])
            else: original_roi_coord = np.array(SCAN.get("instrument").get('scalers').get('roi').get("roi"))

            roi_width = int(str(original_roi_coord[3])[:-2]) - int(str(original_roi_coord[2])[:-2])

            # ROI
            self.lineEdit_SFM_Detector_image_Roi_X_Left.setText(str(original_roi_coord[2])[:-2])
            self.lineEdit_SFM_Detector_image_Roi_X_Right.setText(str(original_roi_coord[3])[:-2])
            self.lineEdit_SFM_Detector_image_Roi_Y_Bottom.setText(str(original_roi_coord[1])[:-2])
            self.lineEdit_SFM_Detector_image_Roi_Y_Top.setText(str(original_roi_coord[0])[:-2])

            # BKG ROI
            if not self.locked_roi == [] and self.checkBox_SFM_Detector_image_Lock_roi.isChecked(): self.lineEdit_SFM_Detector_image_Roi_bkg_X_Right.setText(str(self.locked_roi[1]))
            else: self.lineEdit_SFM_Detector_image_Roi_bkg_X_Right.setText(str(int(self.lineEdit_SFM_Detector_image_Roi_X_Left.text()) - roi_width))
            self.lineEdit_SFM_Detector_image_Roi_bkg_X_Left.setText(str(int(self.lineEdit_SFM_Detector_image_Roi_bkg_X_Right.text()) - roi_width))

            for index, th in enumerate(SCAN.get("instrument").get('motors').get('th').get("value")):
                if str(th)[0:5] in ("-0.00", "0.00"): continue

                self.comboBox_SFM_Detector_image_Incident_angle.addItem(str(round(th, 3)))

            if len(SCAN.get("ponos").get('data')) == 1:
                for item in (self.comboBox_SFM_Detector_image_Polarisation, self.comboBox_SFM_2Dmap_Polarisation): item.addItem("uu")
            for polarisation in SCAN.get("ponos").get('data'):
                if polarisation not in ("data_du", "data_uu", "data_dd", "data_ud"): continue
                if np.any(np.array(SCAN.get("ponos").get('data').get(polarisation))):
                    for item in (self.comboBox_SFM_Detector_image_Polarisation, self.comboBox_SFM_2Dmap_Polarisation): item.addItem(str(polarisation)[-2:])

            self.comboBox_SFM_Detector_image_Polarisation.setCurrentIndex(0)
            self.comboBox_SFM_2Dmap_Polarisation.setCurrentIndex(0)

    def draw_det_image(self):

        if self.comboBox_SFM_Detector_image_Polarisation.currentText() == "" or self.comboBox_SFM_Detector_image_Incident_angle.currentText() == "": return

        for item in (self.graphicsView_SFM_Detector_image, self.graphicsView_SFM_Detector_image_Roi): item.clear()

        if self.SFM_FILE == "": return
        with h5py.File(self.SFM_FILE, 'r') as FILE:

            self.current_th = self.comboBox_SFM_Detector_image_Incident_angle.currentText()

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
                scan_psd = "psd" if i == "psd" else "psd_" + self.comboBox_SFM_Detector_image_Polarisation.currentText()

            detector_images = INSTRUMENT.get('detectors').get(scan_psd).get('data')

            for index, th in enumerate(self.th_list):
                # check th
                if self.current_th == str(round(th, 3)):
                    self.lineEdit_SFM_Detector_image_Slits_s1hg.setText(str(self.s1hg_list[index]))
                    self.lineEdit_SFM_Detector_image_Slits_s2hg.setText(str(self.s2hg_list[index]))
                    self.lineEdit_SFM_Detector_image_Time.setText(str(time_list[index]))

                    # seems to be a bug in numpy arrays imported from hdf5 files. Problem is solved after I subtract ZEROs array with the same dimentions.
                    detector_image = np.around(detector_images[index], decimals=0).astype(int)
                    detector_image = np.subtract(detector_image, np.zeros((detector_image.shape[0], detector_image.shape[1])))
                    # integrate detector image with respect to ROI Y coordinates
                    detector_image_int = detector_image[int(self.lineEdit_SFM_Detector_image_Roi_Y_Top.text()): int(self.lineEdit_SFM_Detector_image_Roi_Y_Bottom.text()), :].sum(axis=0).astype(int)

                    self.graphicsView_SFM_Detector_image.setImage(detector_image, axes={'x':1, 'y':0}, levels=(0,0.1))
                    self.graphicsView_SFM_Detector_image_Roi.addItem(pg.PlotCurveItem(y = detector_image_int, pen=pg.mkPen(color=(0, 0, 0), width=2), brush=pg.mkBrush(color=(255, 0, 0), width=3)))

                    if self.comboBox_SFM_Detector_image_Color_scheme.currentText() == "White / Black":
                        self.color_det_image = np.array([[0, 0, 0, 255], [255, 255, 255, 255], [255, 255, 255, 255]], dtype=np.ubyte)
                    elif self.comboBox_SFM_Detector_image_Color_scheme.currentText() == "Green / Blue":
                        self.color_det_image = np.array([[0, 0, 255, 255], [255, 0, 0, 255], [0, 255, 0, 255]], dtype=np.ubyte)
                    pos = np.array([0.0, 0.1, 1.0])

                    self.graphicsView_SFM_Detector_image.setColorMap(pg.ColorMap(pos, self.color_det_image))

                    # add ROI rectangular
                    spots_ROI_det_int = []
                    if self.draw_roi: self.graphicsView_SFM_Detector_image.removeItem(self.draw_roi)
                    if self.draw_roi_bkg: self.graphicsView_SFM_Detector_image.removeItem(self.draw_roi_bkg)

                    # add ROI rectangular
                    spots_ROI_det_view = {'x': (int(self.lineEdit_SFM_Detector_image_Roi_X_Left.text()), int(self.lineEdit_SFM_Detector_image_Roi_X_Right.text()), int(self.lineEdit_SFM_Detector_image_Roi_X_Right.text()), int(self.lineEdit_SFM_Detector_image_Roi_X_Left.text()), int(self.lineEdit_SFM_Detector_image_Roi_X_Left.text())),
                                 'y': (int(self.lineEdit_SFM_Detector_image_Roi_Y_Top.text()), int(self.lineEdit_SFM_Detector_image_Roi_Y_Top.text()), int(self.lineEdit_SFM_Detector_image_Roi_Y_Bottom.text()), int(self.lineEdit_SFM_Detector_image_Roi_Y_Bottom.text()), int(self.lineEdit_SFM_Detector_image_Roi_Y_Top.text()))}

                    self.draw_roi = pg.PlotDataItem(spots_ROI_det_view, pen=pg.mkPen(255, 255, 255), connect="all")
                    self.graphicsView_SFM_Detector_image.addItem(self.draw_roi)

                    # add BKG ROI rectangular
                    if self.checkBox_Reductions_Subtract_bkg.isChecked():
                        spots_ROI_det_view = {'x': (int(self.lineEdit_SFM_Detector_image_Roi_bkg_X_Left.text()), int(self.lineEdit_SFM_Detector_image_Roi_bkg_X_Right.text()),
                                                    int(self.lineEdit_SFM_Detector_image_Roi_bkg_X_Right.text()), int(self.lineEdit_SFM_Detector_image_Roi_bkg_X_Left.text()),
                                                    int(self.lineEdit_SFM_Detector_image_Roi_bkg_X_Left.text())),
                                              'y': (int(self.lineEdit_SFM_Detector_image_Roi_Y_Top.text()), int(self.lineEdit_SFM_Detector_image_Roi_Y_Top.text()),
                                                    int(self.lineEdit_SFM_Detector_image_Roi_Y_Bottom.text()), int(self.lineEdit_SFM_Detector_image_Roi_Y_Bottom.text()),
                                                    int(self.lineEdit_SFM_Detector_image_Roi_Y_Top.text()))}

                        self.draw_roi_bkg = pg.PlotDataItem(spots_ROI_det_view, pen=pg.mkPen(color=(255, 255, 255), style=QtCore.Qt.DashLine), connect="all")
                        self.graphicsView_SFM_Detector_image.addItem(self.draw_roi_bkg)

                    if self.draw_roi_int: self.graphicsView_SFM_Detector_image_Roi.removeItem(self.draw_roi_int)

                    for i in range(0, detector_image_int.max()):
                        spots_ROI_det_int.append({'x': int(self.lineEdit_SFM_Detector_image_Roi_X_Left.text()), 'y': i})
                        spots_ROI_det_int.append({'x': int(self.lineEdit_SFM_Detector_image_Roi_X_Right.text()), 'y': i})

                    self.draw_roi_int = pg.ScatterPlotItem(spots=spots_ROI_det_int, size=1, pen=pg.mkPen(255, 0, 0))
                    self.graphicsView_SFM_Detector_image_Roi.addItem(self.draw_roi_int)

                    break

        # Show "integrated roi" part
        if self.sender().objectName() == "pushButton_SFM_Detector_image_Show_integrated_roi":
            (height, trigger) = (420, False) if self.show_det_int_trigger else (510, True)
            self.graphicsView_SFM_Detector_image.setGeometry(QtCore.QRect(0, 30, 577, height))
            self.show_det_int_trigger = trigger

    def load_SFM_Reflectivity_preview(self):

        self.graphicsView_SFM_Reflectivity_preview.getPlotItem().clear()
        skip_bkg = 0

        self.sfm_Export_Qz, self.sfm_Export_I, self.sfm_Export_dI, self.sfm_Export_Resolution = [], [], [], []

        # change interface (Scale factor, DB correction, DB attenuator)
        if self.checkBox_Reductions_Normalize_by_DB.isChecked():
            hidden = [False, False, True, True]
            self.checkBox_Reductions_Scale_factor.setChecked(False)
        else: hidden = [True, True, False, False]

        for index, element in enumerate([self.checkBox_Reductions_Attenuator_DB, self.lineEdit_Reductions_Attenuator_DB, self.checkBox_Reductions_Scale_factor, self.lineEdit_Reductions_Scale_factor]):
            element.setHidden(hidden[index])

        if self.comboBox_SFM_Scan.currentText() == "": return
        self.label_Error_sample_len_missing.setVisible(False)
        self.label_Error_DB_missing.setVisible(False)
        self.label_Error_wrong_roi_input.setVisible(False)
        if not self.sender().objectName() == "checkBox_Reductions_Normalize_by_DB":
            self.label_Error_DB_wrong.setVisible(False)

        if (self.checkBox_Reductions_Overillumination_correction.isChecked() or self.checkBox_SFM_Reflectivity_preview_Show_overillumination.isChecked()) and self.lineEdit_Sample_len.text() == "":
            self.label_Error_sample_len_missing.setVisible(True)
            return

        if self.checkBox_Reductions_Normalize_by_DB.isChecked() and self.tableWidget_DB.rowCount() == 0:
            self.label_Error_DB_missing.setVisible(True)
            return

        if int(self.lineEdit_SFM_Detector_image_Roi_X_Left.text()) > int(self.lineEdit_SFM_Detector_image_Roi_X_Right.text()) or int(self.lineEdit_SFM_Detector_image_Roi_Y_Bottom.text()) < int(self.lineEdit_SFM_Detector_image_Roi_Y_Top.text()) or int(self.lineEdit_SFM_Detector_image_Roi_bkg_X_Left.text()) < 0:
            self.label_Error_wrong_roi_input.setVisible(True)
            return

        self.scale_factor = 1
        if self.checkBox_Reductions_Scale_factor.isChecked():
            try:
                self.scale_factor = 10 if self.lineEdit_Reductions_Scale_factor.text() == "" else float(self.lineEdit_Reductions_Scale_factor.text())
            except: True

        self.db_atten_factor = 1
        if self.checkBox_Reductions_Attenuator_DB.isChecked():
            try:
                self.db_atten_factor = 10 if self.lineEdit_Reductions_Attenuator_DB.text() == "" else float(self.lineEdit_Reductions_Attenuator_DB.text())
            except: True

        if self.lineEdit_Reductions_Subtract_bkg_Skip.text(): skip_bkg = float(self.lineEdit_Reductions_Subtract_bkg_Skip.text())

        for i in range(0, self.tableWidget_Scans.rowCount()):
            if self.tableWidget_Scans.item(i, 0).text() == self.comboBox_SFM_Scan.currentText():
                self.SFM_FILE, self.SFM_DB_FILE = self.tableWidget_Scans.item(i, 2).text(), self.tableWidget_Scans.item(i, 1).text()

        with h5py.File(self.SFM_FILE, 'r') as FILE:
            INSTRUMENT = FILE[list(FILE.keys())[0]].get("instrument")
            PONOS = FILE[list(FILE.keys())[0]].get("ponos")
            SCALERS_DATA = np.array(INSTRUMENT.get('scalers').get('data')).T

            roi_coord_Y = [int(self.lineEdit_SFM_Detector_image_Roi_Y_Top.text()), int(self.lineEdit_SFM_Detector_image_Roi_Y_Bottom.text())]
            roi_coord_X = [int(self.lineEdit_SFM_Detector_image_Roi_X_Left.text()), int(self.lineEdit_SFM_Detector_image_Roi_X_Right.text())]
            roi_coord_X_BKG = [int(self.lineEdit_SFM_Detector_image_Roi_bkg_X_Left.text()), int(self.lineEdit_SFM_Detector_image_Roi_bkg_X_Right.text())]

            # recalculate if ROI was changed
            if not roi_coord_Y == self.old_roi_coord_Y: self.sfm_file_already_analized = ""
            self.old_roi_coord_Y = roi_coord_Y

            for index, scaler in enumerate(INSTRUMENT.get('scalers').get('SPEC_counter_mnemonics')):
                if "'mon0'" in str(scaler): monitor_list = SCALERS_DATA[index]
                elif "'m1'" in str(scaler): monitor_uu_list = SCALERS_DATA[index]
                elif "'m2'" in str(scaler): monitor_dd_list = SCALERS_DATA[index]
                elif "'m3'" in str(scaler): monitor_du_list = SCALERS_DATA[index]
                elif "'m4'" in str(scaler): monitor_ud_list = SCALERS_DATA[index]
                elif "'sec'" in str(scaler): time_list = SCALERS_DATA[index]

            if not self.SFM_FILE == self.sfm_file_already_analized:
                self.psd_uu_sfm = self.psd_dd_sfm = self.psd_ud_sfm = self.psd_du_sfm = []

            # get or create 2-dimentional intensity array for each polarisation
            for scan in PONOS.get('data'):

                # avoid reSUM of intensity after each action
                # reSUM if we change SFM file or Sample curvature
                if self.SFM_FILE == self.sfm_file_already_analized and str(self.sample_curvature_last) == self.lineEdit_Instrument_Sample_curvature.text(): continue

                if "pnr" in list(FILE[list(FILE.keys())[0]]):
                    if str(scan) == "data_du": self.psd_du_sfm = INSTRUMENT.get("detectors").get("psd_du").get('data')[:, int(roi_coord_Y[0]): int(roi_coord_Y[1]), :].sum(axis=1)
                    elif str(scan) == "data_uu": self.psd_uu_sfm = INSTRUMENT.get("detectors").get("psd_uu").get('data')[:, int(roi_coord_Y[0]): int(roi_coord_Y[1]), :].sum(axis=1)
                    elif str(scan) == "data_ud": self.psd_ud_sfm = INSTRUMENT.get("detectors").get("psd_ud").get('data')[:, int(roi_coord_Y[0]): int(roi_coord_Y[1]), :].sum(axis=1)
                    elif str(scan) == "data_dd": self.psd_dd_sfm = INSTRUMENT.get("detectors").get("psd_dd").get('data')[:, int(roi_coord_Y[0]): int(roi_coord_Y[1]), :].sum(axis=1)
                else: self.psd_uu_sfm = INSTRUMENT.get("detectors").get("psd").get('data')[:, int(roi_coord_Y[0]) : int(roi_coord_Y[1]), :].sum(axis=1)

            if not self.SFM_FILE == self.sfm_file_already_analized: self.sfm_file_already_analized, self.sample_curvature_last = self.SFM_FILE, "0"

            # Sample curvature correction - we need to adjust integrated 2D map when we first make it
            # perform correction if it was changed on the form
            if not str(self.sample_curvature_last) == self.lineEdit_Instrument_Sample_curvature.text():

                for index, psd_sfm_curvature_correction in enumerate([self.psd_uu_sfm, self.psd_du_sfm, self.psd_ud_sfm, self.psd_dd_sfm]):

                    if self.lineEdit_Instrument_Sample_curvature.text() == "0": continue
                    if psd_sfm_curvature_correction == []: continue

                    psd_sfm_curvature_correction_slice = psd_sfm_curvature_correction[:, roi_coord_X[0]:roi_coord_X[1]]

                    recalc_det_image = [[],[],[]] # x, y, value

                    for x, col in enumerate(np.flipud(np.rot90(psd_sfm_curvature_correction_slice))):
                        displacement = x * np.tan(float(self.lineEdit_Instrument_Sample_curvature.text()))
                        for y, value in enumerate(col):
                            recalc_det_image[0].append(x)
                            recalc_det_image[1].append(y + displacement)
                            recalc_det_image[2].append(value)
                    np.rot90(psd_sfm_curvature_correction_slice, -1)

                    # find middle of roi to define zero level
                    roi_coord_X_middle = (psd_sfm_curvature_correction_slice.shape[1]) / 2
                    zero_level = int(round(roi_coord_X_middle * np.tan(float(self.lineEdit_Instrument_Sample_curvature.text())) - min(recalc_det_image[1])))

                    grid_x, grid_y = np.mgrid[0:psd_sfm_curvature_correction_slice.shape[1]:1, min(recalc_det_image[1]):max(recalc_det_image[1]):1]
                    psd_sfm_curvature_correction_slice = np.flipud(np.rot90(griddata((recalc_det_image[0], recalc_det_image[1]), recalc_det_image[2], (grid_x, grid_y), method="linear", fill_value=float(0))))[zero_level:zero_level+psd_sfm_curvature_correction_slice.shape[0], :]

                    psd_sfm_curvature_correction[:, roi_coord_X[0]:roi_coord_X[1]] = psd_sfm_curvature_correction_slice

                    if index == 0: self.psd_uu_sfm = psd_sfm_curvature_correction
                    elif index == 1: self.psd_du_sfm = psd_sfm_curvature_correction
                    elif index == 2: self.psd_ud_sfm = psd_sfm_curvature_correction
                    elif index == 3: self.psd_dd_sfm = psd_sfm_curvature_correction

                self.sample_curvature_last = str(self.lineEdit_Instrument_Sample_curvature.text())

            for color_index, scan_intens_sfm in enumerate([self.psd_uu_sfm, self.psd_du_sfm, self.psd_ud_sfm, self.psd_dd_sfm]):

                sfm_Export_Qz_one_pol, sfm_Export_I_one_pol, sfm_Export_dI_one_pol, sfm_Export_Resolution_one_pol = [], [], [], []

                plot_I, plot_angle, plot_dI_err_bottom, plot_dI_err_top, plot_overillumination = [], [], [], [], []

                if scan_intens_sfm == []: continue

                if color_index == 0: color, monitor_data = [0, 0, 0], [monitor_list if np.count_nonzero(monitor_uu_list) == 0 else monitor_uu_list][0] # ++
                elif color_index == 1: color, monitor_data = [0, 0, 255], monitor_du_list # -+
                elif color_index == 2: color, monitor_data = [0, 255, 0], monitor_ud_list # +-
                elif color_index == 3: color, monitor_data = [255, 0, 0], monitor_dd_list # --

                for index, th in enumerate(self.th_list):

                    try: # th offset. If "text" cant be converted to "float" - ignore the field
                        th = th - float(self.lineEdit_Instrument_Offset_full.text())
                    except: True

                    # read motors
                    Qz = (4 * np.pi / float(self.lineEdit_Instrument_Wavelength.text())) * np.sin(np.radians(th))
                    s1hg, s2hg, monitor = self.s1hg_list[index], self.s2hg_list[index], monitor_data[index]

                    if not self.checkBox_Reductions_Overillumination_correction.isChecked():
                        overill_corr = 1
                        overill_corr_plot = self.overillumination_correct_coeff(s1hg, s2hg, round(th, 4))[0]
                    else:
                        overill_corr, FWHM_proj = self.overillumination_correct_coeff(s1hg, s2hg, round(th, 4))
                        overill_corr_plot = overill_corr

                    # calculate resolution in Sared way or better
                    if self.checkBox_Export_Resolution_like_sared.isChecked():
                        Resolution = np.sqrt(((2 * np.pi / float(self.lineEdit_Instrument_Wavelength.text())) ** 2) * ((np.cos(np.radians(th))) ** 2) * (0.68 ** 2) * ((s1hg ** 2) + (s2hg ** 2)) / ((float( self.lineEdit_Instrument_Distance_s1_to_sample.text()) - float( self.lineEdit_Instrument_Distance_s2_to_sample.text())) ** 2) + ((float(self.lineEdit_Instrument_Wavelength_resolution.text()) ** 2) * (Qz ** 2)))
                    else:
                        if FWHM_proj == s2hg:
                            Resolution = np.sqrt(((2 * np.pi / float(self.lineEdit_Instrument_Wavelength.text())) ** 2) * ((np.cos(np.radians(th))) ** 2) * (0.68 ** 2) * ((s1hg ** 2) + (s2hg ** 2)) / ((float(self.lineEdit_Instrument_Distance_s1_to_sample.text()) - float(self.lineEdit_Instrument_Distance_s2_to_sample.text())) ** 2) + ((float(self.lineEdit_Instrument_Wavelength_resolution.text()) ** 2) * (Qz ** 2)))
                        else:
                            Resolution = np.sqrt(((2 * np.pi / float(self.lineEdit_Instrument_Wavelength.text())) ** 2) * ((np.cos(np.radians(th))) ** 2) * (0.68 ** 2) * ((s1hg ** 2) + (FWHM_proj ** 2)) / (float(self.lineEdit_Instrument_Distance_s1_to_sample.text()) ** 2) + ((float(self.lineEdit_Instrument_Wavelength_resolution.text()) ** 2) * (Qz ** 2)))

                    # I cite Gunnar in here "We are now saving dQ as sigma rather than FWHM for genx"
                    Resolution = Resolution / (2 * np.sqrt(2 * np.log(2)))

                    # analize integrated intensity for ROI
                    Intens = sum(scan_intens_sfm[index][roi_coord_X[0]: roi_coord_X[1]])
                    Intens_bkg = sum(scan_intens_sfm[index][roi_coord_X_BKG[0] : roi_coord_X_BKG[1]])

                    # minus background, divide by monitor, overillumination correct + calculate errors
                    if not Intens > 0: Intens = 0
                    # I want to avoid error==0 if intens==0
                    if Intens == 0: Intens_err = 1
                    else: Intens_err = np.sqrt(Intens)

                    if self.checkBox_Reductions_Subtract_bkg.isChecked() and Qz > skip_bkg:
                        if Intens_bkg > 0:
                            Intens_err = np.sqrt(Intens + Intens_bkg)
                            Intens = Intens - Intens_bkg

                    if self.checkBox_Reductions_Divide_by_monitor_or_time.isChecked():

                        if self.comboBox_Reductions_Divide_by_monitor_or_time.currentText() == "monitor":
                            monitor = monitor_list[index]
                            if Intens == 0: Intens_err = Intens_err / monitor
                            else: Intens_err = (Intens / monitor) * np.sqrt((Intens_err / Intens) ** 2 + (1 / monitor))
                        elif self.comboBox_Reductions_Divide_by_monitor_or_time.currentText() == "time":
                            monitor = time_list[index]
                            Intens_err = Intens_err / monitor

                        Intens = Intens / monitor

                    if self.checkBox_Reductions_Overillumination_correction.isChecked() and overill_corr > 0:
                        Intens_err = Intens_err / overill_corr
                        Intens = Intens / overill_corr

                    if self.checkBox_Reductions_Normalize_by_DB.isChecked():
                        try:
                            db_intens = float(self.DB_INFO[self.SFM_DB_FILE + ";" + str(s1hg) + ";" + str(s2hg)].split(";")[0]) * self.db_atten_factor
                            db_err = overill_corr * float(self.DB_INFO[self.SFM_DB_FILE + ";" + str(s1hg) + ";" + str(s2hg)].split(";")[1]) * self.db_atten_factor
                            Intens_err = (Intens / db_intens) * np.sqrt((db_err / db_intens) ** 2 + (Intens_err / Intens) ** 2)
                            Intens = Intens / db_intens
                            self.label_Error_DB_wrong.setVisible(False)
                        except:
                            # if we try DB file without neccesary slits combination measured - show error message + redraw reflectivity_preview
                            self.label_Error_DB_wrong.setVisible(True)
                            self.checkBox_Reductions_Normalize_by_DB.setCheckState(0)

                    if self.checkBox_Reductions_Scale_factor.isChecked():
                        Intens_err = Intens_err / self.scale_factor
                        Intens = Intens / self.scale_factor

                    try:
                        show_first, show_last = int(self.lineEdit_SFM_Reflectivity_preview_Skip_points_Left.text()), len(self.th_list)-int(self.lineEdit_SFM_Reflectivity_preview_Skip_points_Right.text())
                    except: show_first, show_last = 0, len(self.th_list)

                    if not Intens < 0 and index < show_last and index > show_first:
                        # I need this for "Reduce SFM" option. First - store one pol.
                        sfm_Export_Qz_one_pol.append(Qz)
                        sfm_Export_I_one_pol.append(Intens)
                        sfm_Export_dI_one_pol.append(Intens_err)
                        sfm_Export_Resolution_one_pol.append(Resolution)

                        if Intens > 0:
                            plot_I.append(np.log10(Intens))
                            plot_angle.append(Qz)
                            plot_dI_err_top.append(abs(np.log10(Intens + Intens_err) - np.log10(Intens)))

                            plot_overillumination.append(overill_corr_plot)

                            if Intens > Intens_err: plot_dI_err_bottom.append(np.log10(Intens) - np.log10(Intens - Intens_err))
                            else: plot_dI_err_bottom.append(0)

                        if self.comboBox_SFM_Reflectivity_preview_View_Reflectivity.currentText() == "Lin":
                            plot_I.pop()
                            plot_I.append(Intens)
                            plot_dI_err_top.pop()
                            plot_dI_err_top.append(Intens_err)
                            plot_dI_err_bottom.pop()
                            plot_dI_err_bottom.append(Intens_err)

                        if self.comboBox_SFM_Reflectivity_preview_View_Angle.currentText() == "Deg":
                            plot_angle.pop()
                            plot_angle.append(th)

                # I need this for "Reduse SFM" option. Second - combine all shown pol in one list variable.
                # polarisations are uu, dd, ud, du
                self.sfm_Export_Qz.append(sfm_Export_Qz_one_pol)
                self.sfm_Export_I.append(sfm_Export_I_one_pol)
                self.sfm_Export_dI.append(sfm_Export_dI_one_pol)
                self.sfm_Export_Resolution.append(sfm_Export_Resolution_one_pol)

                if self.checkBox_SFM_Reflectivity_preview_Include_errorbars.isChecked():
                    s1 = pg.ErrorBarItem(x=np.array(plot_angle), y=np.array(plot_I), top=np.array(plot_dI_err_top), bottom=np.array(plot_dI_err_bottom), pen=pg.mkPen(color[0], color[1], color[2]), brush=pg.mkBrush(color[0], color[1], color[2]))
                    self.graphicsView_SFM_Reflectivity_preview.addItem(s1)

                s2 = pg.ScatterPlotItem(x=plot_angle, y=plot_I, symbol="o", size=4, pen=pg.mkPen(color[0], color[1], color[2]), brush=pg.mkBrush(color[0], color[1], color[2]))
                self.graphicsView_SFM_Reflectivity_preview.addItem(s2)

                if self.checkBox_SFM_Reflectivity_preview_Show_overillumination.isChecked():
                    s3 = pg.PlotCurveItem(x=plot_angle, y=plot_overillumination, pen=pg.mkPen(color=(255, 0, 0), width=1), brush=pg.mkBrush(color=(255, 0, 0), width=1) )
                    self.graphicsView_SFM_Reflectivity_preview.addItem(s3)

                if self.checkBox_SFM_Reflectivity_preview_Show_zero_level.isChecked():
                    if self.comboBox_SFM_Reflectivity_preview_View_Reflectivity.currentText() == "Lin": level = np.array([1, 1])
                    else: level = np.array([0, 0])
                    s4 = pg.PlotCurveItem(x=np.array([min(plot_angle), max(plot_angle)]), y=level, pen=pg.mkPen(color=(0, 0, 255), width=1), brush=pg.mkBrush(color=(255, 0, 0), width=1) )
                    self.graphicsView_SFM_Reflectivity_preview.addItem(s4)

    def draw_2D_map(self):

        self.int_SFM_Detector_image = []

        for item in (self.graphicsView_SFM_2Dmap_Qxz_Theta, self.graphicsView_SFM_2Dmap): item.clear()

        # change interface if for different views
        ELEMENTS = [self.label_SFM_2Dmap_Rescale_image_x, self.label_SFM_2Dmap_Rescale_image_y, self.horizontalSlider_SFM_2Dmap_Rescale_image_x, self.horizontalSlider_SFM_2Dmap_Rescale_image_y, self.label_SFM_2Dmap_Lower_number_of_points_by, self.comboBox_SFM_2Dmap_Lower_number_of_points_by, self.label_SFM_2Dmap_Qxz_Threshold, self.comboBox_SFM_2Dmap_Qxz_Threshold, self.label_SFM_2Dmap_View_scale, self.comboBox_SFM_2Dmap_View_scale]

        if self.comboBox_SFM_2Dmap_Axes.currentText() == "Pixel vs. Point": visible, geometry = [True, True, True, True, False, False, False, False, True, True], [0, 0, 0, 0]
        elif self.comboBox_SFM_2Dmap_Axes.currentText() == "Qx vs. Qz": visible, geometry = [False, False, False, False, True, True, True, True, False, False], [0, 30, 577, 522]
        elif self.comboBox_SFM_2Dmap_Axes.currentText() == "Alpha_i vs. Alpha_f": visible, geometry = [False, False, False, False, True, True, False, False, True, True], [0, 0, 0, 0]

        self.graphicsView_SFM_2Dmap_Qxz_Theta.setGeometry(QtCore.QRect(geometry[0], geometry[1], geometry[2], geometry[3]))
        for index, index_visible in enumerate(visible): ELEMENTS[index].setVisible(index_visible)

        if self.SFM_FILE == "": return

        # start over if we selected nes SFM scan
        if not self.sfm_file_2d_calculated_params == [] and not self.sfm_file_2d_calculated_params[0] == self.SFM_FILE:
            self.comboBox_SFM_2Dmap_Axes.setCurrentIndex(0)
            self.sfm_file_2d_calculated_params, self.res_Aif = [], []

        try:
            self.graphicsView_SFM_2Dmap.removeItem(self.draw_roi_2D_map)
        except: True

        # load selected integrated detector image
        if self.comboBox_SFM_2Dmap_Polarisation.count() == 1: self.int_SFM_Detector_image = self.psd_uu_sfm
        else:
            if self.comboBox_SFM_2Dmap_Polarisation.currentText() == "uu": self.int_SFM_Detector_image = self.psd_uu_sfm
            elif self.comboBox_SFM_2Dmap_Polarisation.currentText() == "du": self.int_SFM_Detector_image = self.psd_du_sfm
            elif self.comboBox_SFM_2Dmap_Polarisation.currentText() == "ud": self.int_SFM_Detector_image = self.psd_ud_sfm
            elif self.comboBox_SFM_2Dmap_Polarisation.currentText() == "dd": self.int_SFM_Detector_image = self.psd_dd_sfm

        if self.int_SFM_Detector_image == []: return

        # create log array for log view
        self.int_SFM_Detector_image_log = np.log10(np.where(self.int_SFM_Detector_image < 1, 0.1, self.int_SFM_Detector_image))

        # Pixel to Angle conversion for "Qx vs Qz" and "alpha_i vs alpha_f" 2d maps
        if self.comboBox_SFM_2Dmap_Axes.currentText() in ["Qx vs. Qz", "Alpha_i vs. Alpha_f"]:
            # recalculate only if something was changed
            if self.res_Aif == [] or not self.sfm_file_2d_calculated_params == [self.SFM_FILE, self.comboBox_SFM_2Dmap_Polarisation.currentText(),
                                              self.lineEdit_SFM_Detector_image_Roi_X_Left.text(), self.lineEdit_SFM_Detector_image_Roi_X_Right.text(),
                                              self.lineEdit_Instrument_Wavelength.text(), self.lineEdit_Instrument_Distance_sample_to_detector.text(),
                                              self.comboBox_SFM_2Dmap_Lower_number_of_points_by.currentText(), self.comboBox_SFM_2Dmap_Qxz_Threshold.currentText(),
                                                                                self.lineEdit_Instrument_Sample_curvature.text()]:
                self.spots_Qxz, self.int_SFM_Detector_image_Qxz, self.int_SFM_Detector_image_Aif, self.int_SFM_Detector_image_values_array = [], [], [[],[]], []

                roi_middle = round((self.int_SFM_Detector_image.shape[1] - float(self.lineEdit_SFM_Detector_image_Roi_X_Left.text()) +
                                    self.int_SFM_Detector_image.shape[1] - float(self.lineEdit_SFM_Detector_image_Roi_X_Right.text())) / 2)
                mm_per_pix = 300 / self.int_SFM_Detector_image.shape[1]

                # we need to flip the detector (X) for correct calculation
                for theta_i, tth_i, det_image_i in zip(self.th_list, self.tth_list, np.flip(self.int_SFM_Detector_image, 1)):
                    for pixel_num, value in enumerate(det_image_i):
                        # Reduce number of points to draw (to save RAM)
                        if pixel_num % int(self.comboBox_SFM_2Dmap_Lower_number_of_points_by.currentText()) == 0:
                            theta_f = tth_i - theta_i # theta F in deg
                            delta_theta_F_mm = (pixel_num - roi_middle) * mm_per_pix
                            delta_theta_F_deg = np.degrees(np.arctan(delta_theta_F_mm / float(self.lineEdit_Instrument_Distance_sample_to_detector.text()))) # calculate delta theta F in deg
                            theta_f += delta_theta_F_deg # final theta F in deg for the point
                            # convert to Q
                            Qx = (2 * np.pi / float(self.lineEdit_Instrument_Wavelength.text())) * (np.cos(np.radians(theta_f)) - np.cos(np.radians(theta_i)))
                            Qz = (2 * np.pi / float(self.lineEdit_Instrument_Wavelength.text())) * (np.sin(np.radians(theta_f)) + np.sin(np.radians(theta_i)))

                            for arr, val in zip((self.int_SFM_Detector_image_Qxz, self.int_SFM_Detector_image_Aif[0], self.int_SFM_Detector_image_Aif[1], self.int_SFM_Detector_image_values_array), ([Qx, Qz, value], theta_i, theta_f, value)): arr.append(val)

                            # define colors - 2 count+ -> green, [0,1] - blue
                            color = [0, 0, 255] if value < int(self.comboBox_SFM_2Dmap_Qxz_Threshold.currentText()) else [0, 255, 0]

                            self.spots_Qxz.append({'pos': (-Qx, Qz), 'pen': pg.mkPen(color[0], color[1], color[2])})

                if self.comboBox_SFM_2Dmap_Axes.currentText() == "Alpha_i vs. Alpha_f":
                    # calculate required number of pixels in Y axis
                    self.resolution_x_pix_deg = self.int_SFM_Detector_image.shape[0] / (max(self.int_SFM_Detector_image_Aif[0]) - min(self.int_SFM_Detector_image_Aif[0]))
                    self.resolution_y_pix = int(round((max(self.int_SFM_Detector_image_Aif[1]) - min(self.int_SFM_Detector_image_Aif[1])) * self.resolution_x_pix_deg))

                    grid_x, grid_y = np.mgrid[min(self.int_SFM_Detector_image_Aif[0]):max(self.int_SFM_Detector_image_Aif[0]):((max(self.int_SFM_Detector_image_Aif[0]) - min(self.int_SFM_Detector_image_Aif[0]))/len(self.th_list)), min(self.int_SFM_Detector_image_Aif[1]):max(self.int_SFM_Detector_image_Aif[1]):(max(self.int_SFM_Detector_image_Aif[1]) - min(self.int_SFM_Detector_image_Aif[1]))/self.resolution_y_pix]
                    self.res_Aif = griddata((self.int_SFM_Detector_image_Aif[0], self.int_SFM_Detector_image_Aif[1]), self.int_SFM_Detector_image_values_array, (grid_x, grid_y), method="linear", fill_value=float(0))
                    # create log array for log view
                    self.res_Aif_log = np.log10(np.where(self.res_Aif < 1, 0.1, self.res_Aif))

                # record params that we used for 2D maps calculation
                self.sfm_file_2d_calculated_params = [self.SFM_FILE, self.comboBox_SFM_2Dmap_Polarisation.currentText(), self.lineEdit_SFM_Detector_image_Roi_X_Left.text(), self.lineEdit_SFM_Detector_image_Roi_X_Right.text(), self.lineEdit_Instrument_Wavelength.text(), self.lineEdit_Instrument_Distance_sample_to_detector.text(), self.comboBox_SFM_2Dmap_Lower_number_of_points_by.currentText(), self.comboBox_SFM_2Dmap_Qxz_Threshold.currentText(), self.lineEdit_Instrument_Sample_curvature.text()]

        # plot
        if self.comboBox_SFM_2Dmap_Axes.currentText() == "Pixel vs. Point":

            image = self.int_SFM_Detector_image_log if self.comboBox_SFM_2Dmap_View_scale.currentText() == "Log" else self.int_SFM_Detector_image

            self.graphicsView_SFM_2Dmap.setImage(image, axes={'x': 1, 'y': 0}, levels=(0, np.max(image)), scale=(int(self.horizontalSlider_SFM_2Dmap_Rescale_image_x.value()), int(self.horizontalSlider_SFM_2Dmap_Rescale_image_y.value())))
            # add ROI rectangular
            spots_ROI = {'x':(int(self.lineEdit_SFM_Detector_image_Roi_X_Left.text()) * int(self.horizontalSlider_SFM_2Dmap_Rescale_image_x.value()), int(self.lineEdit_SFM_Detector_image_Roi_X_Right.text()) * int(self.horizontalSlider_SFM_2Dmap_Rescale_image_x.value()), int(self.lineEdit_SFM_Detector_image_Roi_X_Right.text()) * int(self.horizontalSlider_SFM_2Dmap_Rescale_image_x.value()), int(self.lineEdit_SFM_Detector_image_Roi_X_Left.text()) * int(self.horizontalSlider_SFM_2Dmap_Rescale_image_x.value()), int(self.lineEdit_SFM_Detector_image_Roi_X_Left.text()) * int(self.horizontalSlider_SFM_2Dmap_Rescale_image_x.value())), 'y':(0,0,self.int_SFM_Detector_image.shape[0] * int(self.horizontalSlider_SFM_2Dmap_Rescale_image_y.value()),self.int_SFM_Detector_image.shape[0] * int(self.horizontalSlider_SFM_2Dmap_Rescale_image_y.value()),0)}

            self.draw_roi_2D_map = pg.PlotDataItem(spots_ROI, pen=pg.mkPen(255, 255, 255), connect="all")
            self.graphicsView_SFM_2Dmap.addItem(self.draw_roi_2D_map)

        elif self.comboBox_SFM_2Dmap_Axes.currentText() == "Alpha_i vs. Alpha_f":
            image = self.res_Aif_log if self.comboBox_SFM_2Dmap_View_scale.currentText() == "Log" else self.res_Aif

            self.graphicsView_SFM_2Dmap.setImage(image, axes={'x': 0, 'y': 1}, levels=(0, np.max(image)))
            self.graphicsView_SFM_2Dmap.getImageItem().setRect(QtCore.QRectF(min(self.int_SFM_Detector_image_Aif[0]), min(self.int_SFM_Detector_image_Aif[1]), max(self.int_SFM_Detector_image_Aif[0]) - min(self.int_SFM_Detector_image_Aif[0]), max(self.int_SFM_Detector_image_Aif[1]) - min(self.int_SFM_Detector_image_Aif[1])))
            self.graphicsView_SFM_2Dmap.getView().enableAutoScale()

        elif self.comboBox_SFM_2Dmap_Axes.currentText() == "Qx vs. Qz":
            s0 = pg.ScatterPlotItem(spots=self.spots_Qxz, size=1)
            self.graphicsView_SFM_2Dmap_Qxz_Theta.addItem(s0)

        # hide Y axis in 2D map if "rescale image" is used. Reason - misleading scale
        for item in (self.graphicsView_SFM_2Dmap.view.getAxis("left"), self.graphicsView_SFM_2Dmap.view.getAxis("bottom")): item.setTicks(None)
        if self.horizontalSlider_SFM_2Dmap_Rescale_image_x.value() > 1: self.graphicsView_SFM_2Dmap.view.getAxis("bottom").setTicks([])
        if self.horizontalSlider_SFM_2Dmap_Rescale_image_y.value() > 1: self.graphicsView_SFM_2Dmap.view.getAxis("left").setTicks([])

    def export_2d_map(self):
        save_file_directory = self.lineEdit_Save_at.text() if self.lineEdit_Save_at.text() else self.current_dir

        if self.comboBox_SFM_2Dmap_Axes.currentText() == "Pixel vs. Point":
            with open(save_file_directory + self.SFM_FILE[self.SFM_FILE.rfind("/") + 1 : -3] + "_" + self.comboBox_SFM_2Dmap_Polarisation.currentText() + " 2D_map(Pixel vs. Point).dat", "w") as new_file_2d_map:
                for line in self.int_SFM_Detector_image:
                    for row in line: new_file_2d_map.write(str(row) + " ")
                    new_file_2d_map.write("\n")

        elif self.comboBox_SFM_2Dmap_Axes.currentText() == "Alpha_i vs. Alpha_f":
            with open(save_file_directory + self.SFM_FILE[self.SFM_FILE.rfind("/") + 1 : -3] + "_" + self.comboBox_SFM_2Dmap_Polarisation.currentText() + " 2D_map_(Alpha_i vs. Alpha_f)).dat", "w") as new_file_2d_map_Aif:
                # header
                new_file_2d_map_Aif.write("Alpha_i limits: " + str(min(self.int_SFM_Detector_image_Aif[0])) + " : " + str(max(self.int_SFM_Detector_image_Aif[0])) +
                                        "   Alpha_f limits: " + str(min(self.int_SFM_Detector_image_Aif[1])) + " : " + str(max(self.int_SFM_Detector_image_Aif[1])) + " degrees\n")
                for line in np.rot90(self.res_Aif):
                    for row in line: new_file_2d_map_Aif.write(str(row) + " ")
                    new_file_2d_map_Aif.write("\n")

        elif self.comboBox_SFM_2Dmap_Axes.currentText() in ["Qx vs. Qz"]:
            with open(save_file_directory + self.SFM_FILE[self.SFM_FILE.rfind("/") + 1 : -3] + "_" + self.comboBox_SFM_2Dmap_Polarisation.currentText() + " points_(Qx, Qz, intens).dat", "w") as new_file_2d_map_Qxz:
                for line in self.int_SFM_Detector_image_Qxz: new_file_2d_map_Qxz.write(str(line[0]) + " " + str(line[1]) + " " + str(line[2]) + "\n")

    def update_slits(self):

        roi_width = int(self.lineEdit_SFM_Detector_image_Roi_X_Right.text()) - int(self.lineEdit_SFM_Detector_image_Roi_X_Left.text())

        if not self.sender().objectName() == "lineEdit_SFM_Detector_image_Roi_bkg_X_Right":
            self.lineEdit_SFM_Detector_image_Roi_bkg_X_Left.setText(str(int(self.lineEdit_SFM_Detector_image_Roi_X_Left.text()) - 2 * roi_width))
            self.lineEdit_SFM_Detector_image_Roi_bkg_X_Right.setText(str(int(self.lineEdit_SFM_Detector_image_Roi_X_Left.text()) - roi_width))
        else: self.lineEdit_SFM_Detector_image_Roi_bkg_X_Left.setText(str(int(self.lineEdit_SFM_Detector_image_Roi_bkg_X_Right.text()) - roi_width))

        # record ROI coord for "Lock ROI" checkbox
        self.locked_roi = [[self.lineEdit_SFM_Detector_image_Roi_Y_Top.text() + ". ", self.lineEdit_SFM_Detector_image_Roi_Y_Bottom.text() + ". ", self.lineEdit_SFM_Detector_image_Roi_X_Left.text() + ". ", self.lineEdit_SFM_Detector_image_Roi_X_Right.text() + ". "], self.lineEdit_SFM_Detector_image_Roi_bkg_X_Right.text()]

        self.draw_det_image()
        self.load_SFM_Reflectivity_preview()
        self.draw_2D_map()

    def color_det_image(self):
        if self.comboBox_SFM_Detector_image_Color_scheme.currentText() == "White / Black": self.color_det_image = np.array([[0, 0, 0, 255], [255, 255, 255, 255], [255, 255, 255, 255]], dtype=np.ubyte)
        elif self.comboBox_SFM_Detector_image_Color_scheme.currentText() == "Green / Blue": self.color_det_image = np.array([[0, 0, 255, 255], [255, 0, 0, 255], [0, 255, 0, 255]], dtype=np.ubyte)
        self.draw_det_image()
    ##<--

if __name__ == "__main__":
    QtWidgets.QApplication.setStyle("Fusion")
    app = QtWidgets.QApplication(sys.argv)
    prog = GUI()
    prog.show()
    sys.exit(app.exec_())

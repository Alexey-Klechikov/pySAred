from PyQt5 import QtCore, QtGui, QtWidgets
import h5py, numpy, os, sys
import pyqtgraph as pg
from scipy.interpolate import griddata

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class Ui_MainWindow(QtGui.QMainWindow):

    ##--> define user interface elements
    def setupUi(self, MainWindow):

        # Fonts
        font_headline = QtGui.QFont()
        font_headline.setPointSize(12)
        font_headline.setBold(True)

        font_button = QtGui.QFont()
        font_button.setPointSize(11)
        font_button.setBold(True)

        font_graphs = QtGui.QFont()
        font_graphs.setPixelSize(12)
        font_graphs.setBold(False)

        font_ee = QtGui.QFont()
        font_ee.setPointSize(10)
        font_ee.setBold(False)

        # Main Window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1180, 700)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1180, 700))
        MainWindow.setMaximumSize(QtCore.QSize(1180, 700))
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowNestedDocks|QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        MainWindow.setWindowTitle("pySAred")
        MainWindow.setIconSize(QtCore.QSize(30, 30))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Block: .h5 files
        self.label_Files_Scans = QtWidgets.QLabel(self.centralwidget)
        self.label_Files_Scans.setGeometry(QtCore.QRect(15, 5, 200, 20))
        self.label_Files_Scans.setFont(font_headline)
        self.label_Files_Scans.setObjectName("label_Files_Scans")
        self.label_Files_Scans.setText(".h5 files")

        self.groupBox_Data = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Data.setGeometry(QtCore.QRect(10, 10, 280, 667))
        self.groupBox_Data.setFont(font_ee)
        self.groupBox_Data.setTitle("")
        self.groupBox_Data.setObjectName("groupBox_Data")
        self.label_Data_files = QtWidgets.QLabel(self.groupBox_Data)
        self.label_Data_files.setGeometry(QtCore.QRect(110, 20, 121, 21))
        self.label_Data_files.setFont(font_headline)
        self.label_Data_files.setObjectName("label_Data_files")
        self.label_Data_files.setText("Data files")
        self.tableWidget_Scans = QtWidgets.QTableWidget(self.groupBox_Data)
        self.tableWidget_Scans.setFont(font_ee)
        self.tableWidget_Scans.setGeometry(QtCore.QRect(10, 42, 260, 338))
        self.tableWidget_Scans.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_Scans.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_Scans.setAutoScroll(True)
        self.tableWidget_Scans.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.tableWidget_Scans.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_Scans.setObjectName("tableWidget_Scans")
        self.tableWidget_Scans.setColumnCount(4)
        self.tableWidget_Scans.setRowCount(0)
        headers_table_scans = ["Scan", "DB", "Scan_file_full_path"]
        for i in range(0,3):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_Scans.setHorizontalHeaderItem(i, item)
            self.tableWidget_Scans.horizontalHeaderItem(i).setText(headers_table_scans[i])
        self.tableWidget_Scans.horizontalHeader().setVisible(True)
        self.tableWidget_Scans.verticalHeader().setVisible(False)
        self.tableWidget_Scans.setColumnWidth(0, 200)
        self.tableWidget_Scans.setColumnWidth(1, int(self.tableWidget_Scans.width()) - int(self.tableWidget_Scans.columnWidth(0)) - 2)
        self.tableWidget_Scans.setColumnWidth(2, 0)
        self.pushButton_Delete_scans = QtWidgets.QPushButton(self.groupBox_Data)
        self.pushButton_Delete_scans.setGeometry(QtCore.QRect(10, 384, 81, 20))
        self.pushButton_Delete_scans.setFont(font_ee)
        self.pushButton_Delete_scans.setObjectName("pushButton_Delete_scans")
        self.pushButton_Delete_scans.setText("Delete scans")
        self.pushButton_Import_scans = QtWidgets.QPushButton(self.groupBox_Data)
        self.pushButton_Import_scans.setGeometry(QtCore.QRect(189, 384, 81, 20))
        self.pushButton_Import_scans.setFont(font_ee)
        self.pushButton_Import_scans.setObjectName("pushButton_Import_scans")
        self.pushButton_Import_scans.setText("Import scans")

        self.label_DB_files = QtWidgets.QLabel(self.groupBox_Data)
        self.label_DB_files.setGeometry(QtCore.QRect(78, 412, 191, 23))
        self.label_DB_files.setFont(font_headline)
        self.label_DB_files.setObjectName("label_DB_files")
        self.label_DB_files.setText("Direct Beam files")
        self.checkBox_Rearrange_DB_after = QtWidgets.QCheckBox(self.groupBox_Data)
        self.checkBox_Rearrange_DB_after.setGeometry(QtCore.QRect(10, 432, 210, 20))
        self.checkBox_Rearrange_DB_after.setFont(font_ee)
        self.checkBox_Rearrange_DB_after.setObjectName("checkBox_Rearrange_DB_after")
        self.checkBox_Rearrange_DB_after.setText("DB's were measured after the scans")
        self.tableWidget_DB = QtWidgets.QTableWidget(self.groupBox_Data)
        self.tableWidget_DB.setFont(font_ee)
        self.tableWidget_DB.setGeometry(QtCore.QRect(10, 452, 260, 183))
        self.tableWidget_DB.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_DB.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_DB.setAutoScroll(True)
        self.tableWidget_DB.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.tableWidget_DB.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_DB.setObjectName("tableWidget_DB")
        self.tableWidget_DB.setColumnCount(2)
        self.tableWidget_DB.setRowCount(0)
        headers_table_db = ["Scan", "Path"]
        for i in range(0, 2):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_DB.setHorizontalHeaderItem(i, item)
            self.tableWidget_DB.horizontalHeaderItem(i).setText(headers_table_db[i])
        self.tableWidget_DB.horizontalHeader().setVisible(False)
        self.tableWidget_DB.verticalHeader().setVisible(False)
        self.tableWidget_DB.setColumnWidth(0, self.tableWidget_DB.width())
        self.tableWidget_DB.setColumnWidth(1, 0)
        self.tableWidget_DB.setSortingEnabled(True)
        self.pushButton_Delete_DB = QtWidgets.QPushButton(self.groupBox_Data)
        self.pushButton_Delete_DB.setGeometry(QtCore.QRect(10, 639, 81, 20))
        self.pushButton_Delete_DB.setFont(font_ee)
        self.pushButton_Delete_DB.setObjectName("pushButton_Delete_DB")
        self.pushButton_Delete_DB.setText("Delete DB")
        self.pushButton_Import_DB = QtWidgets.QPushButton(self.groupBox_Data)
        self.pushButton_Import_DB.setGeometry(QtCore.QRect(189, 639, 81, 20))
        self.pushButton_Import_DB.setFont(font_ee)
        self.pushButton_Import_DB.setObjectName("pushButton_Import_DB")
        self.pushButton_Import_DB.setText("Import DB")

        # Block: Sample
        self.label_Sample = QtWidgets.QLabel(self.centralwidget)
        self.label_Sample.setGeometry(QtCore.QRect(305, 5, 200, 20))
        self.label_Sample.setFont(font_headline)
        self.label_Sample.setObjectName("label_Sample")
        self.label_Sample.setText("Sample")
        self.groupBox_Sample_len = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Sample_len.setGeometry(QtCore.QRect(300, 10, 282, 47))
        self.groupBox_Sample_len.setFont(font_ee)
        self.groupBox_Sample_len.setTitle("")
        self.groupBox_Sample_len.setObjectName("groupBox_Sample_len")
        self.label_Sample_len = QtWidgets.QLabel(self.groupBox_Sample_len)
        self.label_Sample_len.setGeometry(QtCore.QRect(10, 24, 131, 16))
        self.label_Sample_len.setFont(font_ee)
        self.label_Sample_len.setObjectName("label_Sample_len")
        self.label_Sample_len.setText("Sample length (mm)")
        self.lineEdit_Sample_len = QtWidgets.QLineEdit(self.groupBox_Sample_len)
        self.lineEdit_Sample_len.setGeometry(QtCore.QRect(192, 22, 83, 21))
        self.lineEdit_Sample_len.setObjectName("lineEdit_Sample_len")
        self.lineEdit_Sample_len.setText("50")

        # Block: Reductions and Instrument settings
        self.label_Reductions = QtWidgets.QLabel(self.centralwidget)
        self.label_Reductions.setGeometry(QtCore.QRect(305, 65, 200, 16))
        self.label_Reductions.setFont(font_headline)
        self.label_Reductions.setObjectName("label_Reductions")
        self.label_Reductions.setText("Reductions")
        self.tabWidget_Reductions = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_Reductions.setGeometry(QtCore.QRect(300, 87, 281, 226))
        self.tabWidget_Reductions.setFont(font_ee)
        self.tabWidget_Reductions.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget_Reductions.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget_Reductions.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget_Reductions.setObjectName("tabWidget_Reductions")

        # Tab: Reductions
        self.tab_Reductions = QtWidgets.QWidget()
        self.tab_Reductions.setObjectName("tab_Reductions")
        self.checkBox_Reductions_Divide_by_monitor_or_time = QtWidgets.QCheckBox(self.tab_Reductions)
        self.checkBox_Reductions_Divide_by_monitor_or_time.setGeometry(QtCore.QRect(10, 10, 131, 18))
        self.checkBox_Reductions_Divide_by_monitor_or_time.setFont(font_ee)
        self.checkBox_Reductions_Divide_by_monitor_or_time.setObjectName("checkBox_Reductions_Divide_by_monitor_or_time")
        self.checkBox_Reductions_Divide_by_monitor_or_time.setText("Divide by")
        self.comboBox_Reductions_Divide_by_monitor_or_time = QtWidgets.QComboBox(self.tab_Reductions)
        self.comboBox_Reductions_Divide_by_monitor_or_time.setGeometry(QtCore.QRect(80, 9, 70, 20))
        self.comboBox_Reductions_Divide_by_monitor_or_time.setObjectName("comboBox_Reductions_Divide_by_monitor_or_time")
        self.comboBox_Reductions_Divide_by_monitor_or_time.setFont(font_ee)
        self.comboBox_Reductions_Divide_by_monitor_or_time.addItem("monitor")
        self.comboBox_Reductions_Divide_by_monitor_or_time.addItem("time")

        self.checkBox_Reductions_Normalize_by_DB = QtWidgets.QCheckBox(self.tab_Reductions)
        self.checkBox_Reductions_Normalize_by_DB.setGeometry(QtCore.QRect(10, 35, 181, 18))
        self.checkBox_Reductions_Normalize_by_DB.setFont(font_ee)
        self.checkBox_Reductions_Normalize_by_DB.setObjectName("checkBox_Reductions_Normalize_by_DB")
        self.checkBox_Reductions_Normalize_by_DB.setText("Normalize by direct beam")
        # User will need Attenuator only with DB. Otherwice I hide this option and replace with Scale factor
        self.checkBox_Reductions_Attenuator_DB = QtWidgets.QCheckBox(self.tab_Reductions)
        self.checkBox_Reductions_Attenuator_DB.setGeometry(QtCore.QRect(10, 60, 161, 18))
        self.checkBox_Reductions_Attenuator_DB.setFont(font_ee)
        self.checkBox_Reductions_Attenuator_DB.setChecked(True)
        self.checkBox_Reductions_Attenuator_DB.setObjectName("checkBox_Reductions_Attenuator_DB")
        self.checkBox_Reductions_Attenuator_DB.setText("Direct beam attenuator")
        self.checkBox_Reductions_Attenuator_DB.setVisible(False)
        self.lineEdit_Reductions_Attenuator_DB = QtWidgets.QLineEdit(self.tab_Reductions)
        self.lineEdit_Reductions_Attenuator_DB.setGeometry(QtCore.QRect(30, 85, 221, 20))
        self.lineEdit_Reductions_Attenuator_DB.setFont(font_ee)
        self.lineEdit_Reductions_Attenuator_DB.setText("")
        self.lineEdit_Reductions_Attenuator_DB.setObjectName("lineEdit_Reductions_Attenuator_DB")
        self.lineEdit_Reductions_Attenuator_DB.setPlaceholderText("Attenuator correction factor [default 10]")
        self.lineEdit_Reductions_Attenuator_DB.setVisible(False)
        self.checkBox_Reductions_Scale_factor = QtWidgets.QCheckBox(self.tab_Reductions)
        self.checkBox_Reductions_Scale_factor.setGeometry(QtCore.QRect(10, 60, 161, 18))
        self.checkBox_Reductions_Scale_factor.setFont(font_ee)
        self.checkBox_Reductions_Scale_factor.setChecked(False)
        self.checkBox_Reductions_Scale_factor.setObjectName("checkBox_Reductions_Scale_factor")
        self.checkBox_Reductions_Scale_factor.setText("Scale factor")
        self.lineEdit_Reductions_Scale_factor = QtWidgets.QLineEdit(self.tab_Reductions)
        self.lineEdit_Reductions_Scale_factor.setGeometry(QtCore.QRect(30, 85, 221, 20))
        self.lineEdit_Reductions_Scale_factor.setFont(font_ee)
        self.lineEdit_Reductions_Scale_factor.setObjectName("lineEdit_Reductions_Scale_factor")
        self.lineEdit_Reductions_Scale_factor.setPlaceholderText("Divide reflectivity curve by [default 10]")

        self.checkBox_Reductions_Subtract_bkg = QtWidgets.QCheckBox(self.tab_Reductions)
        self.checkBox_Reductions_Subtract_bkg.setGeometry(QtCore.QRect(10, 115, 231, 18))
        self.checkBox_Reductions_Subtract_bkg.setFont(font_ee)
        self.checkBox_Reductions_Subtract_bkg.setObjectName("checkBox_Reductions_Subtract_bkg")
        self.checkBox_Reductions_Subtract_bkg.setText("Subtract background (using 1 ROI)")
        self.lineEdit_Reductions_Subtract_bkg_Skip = QtWidgets.QLineEdit(self.tab_Reductions)
        self.lineEdit_Reductions_Subtract_bkg_Skip.setGeometry(QtCore.QRect(30, 140, 221, 20))
        self.lineEdit_Reductions_Subtract_bkg_Skip.setFont(font_ee)
        self.lineEdit_Reductions_Subtract_bkg_Skip.setObjectName("lineEdit_Reductions_Subtract_bkg_Skip")
        self.lineEdit_Reductions_Subtract_bkg_Skip.setPlaceholderText("Skip background corr. at Qz < [default 0]")
        self.checkBox_Reductions_Overillumination_correction = QtWidgets.QCheckBox(self.tab_Reductions)
        self.checkBox_Reductions_Overillumination_correction.setGeometry(QtCore.QRect(10, 170, 181, 18))
        self.checkBox_Reductions_Overillumination_correction.setFont(font_ee)
        self.checkBox_Reductions_Overillumination_correction.setObjectName("checkBox_Reductions_Overillumination_correction")
        self.checkBox_Reductions_Overillumination_correction.setText("Overillumination correction")
        self.tabWidget_Reductions.addTab(self.tab_Reductions, "")
        self.tabWidget_Reductions.setTabText(0, "Reductions")

        # Tab: Instrument settings
        self.tab_Instrument_settings = QtWidgets.QWidget()
        self.tab_Instrument_settings.setObjectName("tab_Instrument_settings")
        self.label_Instrument_Wavelength = QtWidgets.QLabel(self.tab_Instrument_settings)
        self.label_Instrument_Wavelength.setGeometry(QtCore.QRect(10, 10, 111, 16))
        self.label_Instrument_Wavelength.setFont(font_ee)
        self.label_Instrument_Wavelength.setObjectName("label_Instrument_Wavelength")
        self.label_Instrument_Wavelength.setText("Wavelength (A)")
        self.lineEdit_Instrument_Wavelength = QtWidgets.QLineEdit(self.tab_Instrument_settings)
        self.lineEdit_Instrument_Wavelength.setGeometry(QtCore.QRect(220, 10, 41, 20))
        self.lineEdit_Instrument_Wavelength.setFont(font_ee)
        self.lineEdit_Instrument_Wavelength.setObjectName("lineEdit_Instrument_Wavelength")
        self.lineEdit_Instrument_Wavelength.setText("5.2")
        self.label_Instrument_Wavelength_resolution = QtWidgets.QLabel(self.tab_Instrument_settings)
        self.label_Instrument_Wavelength_resolution.setGeometry(QtCore.QRect(10, 35, 271, 16))
        self.label_Instrument_Wavelength_resolution.setFont(font_ee)
        self.label_Instrument_Wavelength_resolution.setObjectName("label_Instrument_Wavelength_resolution")
        self.label_Instrument_Wavelength_resolution.setText("Wavelength resolution (d_lambda/lambda)")
        self.lineEdit_Instrument_Wavelength_resolution = QtWidgets.QLineEdit(self.tab_Instrument_settings)
        self.lineEdit_Instrument_Wavelength_resolution.setGeometry(QtCore.QRect(220, 35, 41, 20))
        self.lineEdit_Instrument_Wavelength_resolution.setFont(font_ee)
        self.lineEdit_Instrument_Wavelength_resolution.setObjectName("lineEdit_Instrument_Wavelength_resolution")
        self.lineEdit_Instrument_Wavelength_resolution.setText("0.007")
        self.label_Instrument_Distance_s1_to_sample = QtWidgets.QLabel(self.tab_Instrument_settings)
        self.label_Instrument_Distance_s1_to_sample.setGeometry(QtCore.QRect(10, 60, 241, 16))
        self.label_Instrument_Distance_s1_to_sample.setFont(font_ee)
        self.label_Instrument_Distance_s1_to_sample.setObjectName("label_Instrument_Distance_s1_to_sample")
        self.label_Instrument_Distance_s1_to_sample.setText("Mono_slit to Samplle distance (mm)")
        self.lineEdit_Instrument_Distance_s1_to_sample = QtWidgets.QLineEdit(self.tab_Instrument_settings)
        self.lineEdit_Instrument_Distance_s1_to_sample.setGeometry(QtCore.QRect(220, 60, 41, 20))
        self.lineEdit_Instrument_Distance_s1_to_sample.setFont(font_ee)
        self.lineEdit_Instrument_Distance_s1_to_sample.setObjectName("lineEdit_Instrument_Distance_s1_to_sample")
        self.lineEdit_Instrument_Distance_s1_to_sample.setText("2350")
        self.label_Instrument_Distance_s2_to_sample = QtWidgets.QLabel(self.tab_Instrument_settings)
        self.label_Instrument_Distance_s2_to_sample.setGeometry(QtCore.QRect(10, 85, 241, 16))
        self.label_Instrument_Distance_s2_to_sample.setFont(font_ee)
        self.label_Instrument_Distance_s2_to_sample.setObjectName("label_Instrument_Distance_s2_to_sample")
        self.label_Instrument_Distance_s2_to_sample.setText("Sample_slit to Sample distance (mm)")
        self.lineEdit_Instrument_Distance_s2_to_sample = QtWidgets.QLineEdit(self.tab_Instrument_settings)
        self.lineEdit_Instrument_Distance_s2_to_sample.setGeometry(QtCore.QRect(220, 85, 41, 20))
        self.lineEdit_Instrument_Distance_s2_to_sample.setFont(font_ee)
        self.lineEdit_Instrument_Distance_s2_to_sample.setObjectName("lineEdit_Instrument_Distance_s2_to_sample")
        self.lineEdit_Instrument_Distance_s2_to_sample.setText("195")
        self.label_Instrument_Distance_sample_to_detector = QtWidgets.QLabel(self.tab_Instrument_settings)
        self.label_Instrument_Distance_sample_to_detector.setGeometry(QtCore.QRect(10, 110, 241, 16))
        self.label_Instrument_Distance_sample_to_detector.setFont(font_ee)
        self.label_Instrument_Distance_sample_to_detector.setObjectName("label_Instrument_Distance_sample_to_detector")
        self.label_Instrument_Distance_sample_to_detector.setText("Samplle to Detector distance (mm)")
        self.lineEdit_Instrument_Distance_sample_to_detector = QtWidgets.QLineEdit(self.tab_Instrument_settings)
        self.lineEdit_Instrument_Distance_sample_to_detector.setGeometry(QtCore.QRect(220, 110, 41, 20))
        self.lineEdit_Instrument_Distance_sample_to_detector.setFont(font_ee)
        self.lineEdit_Instrument_Distance_sample_to_detector.setObjectName("lineEdit_Instrument_Distance_sample_to_detector")
        self.lineEdit_Instrument_Distance_sample_to_detector.setText("2500")
        '''
        self.label_Instrument_Offset_th = QtWidgets.QLabel(self.tab_Instrument_settings)
        self.label_Instrument_Offset_th.setGeometry(QtCore.QRect(10, 150, 241, 16))
        self.label_Instrument_Offset_th.setFont(font_ee)
        self.label_Instrument_Offset_th.setObjectName("label_Instrument_Offset_th")
        self.label_Instrument_Offset_th.setText("th offset (deg) (SFM only)")
        self.lineEdit_Instrument_Offset_th = QtWidgets.QLineEdit(self.tab_Instrument_settings)
        self.lineEdit_Instrument_Offset_th.setGeometry(QtCore.QRect(220, 150, 41, 20))
        self.lineEdit_Instrument_Offset_th.setFont(font_ee)
        self.lineEdit_Instrument_Offset_th.setObjectName("lineEdit_Instrument_Offset_th")
        self.lineEdit_Instrument_Offset_th.setText("0")
        '''
        self.label_Instrument_Offset_full = QtWidgets.QLabel(self.tab_Instrument_settings)
        self.label_Instrument_Offset_full.setGeometry(QtCore.QRect(10, 175, 241, 16))
        self.label_Instrument_Offset_full.setFont(font_ee)
        self.label_Instrument_Offset_full.setObjectName("label_Instrument_Offset_full")
        self.label_Instrument_Offset_full.setText("Full scan offset (th - deg) (SFM only)")
        self.lineEdit_Instrument_Offset_full = QtWidgets.QLineEdit(self.tab_Instrument_settings)
        self.lineEdit_Instrument_Offset_full.setGeometry(QtCore.QRect(220, 175, 41, 20))
        self.lineEdit_Instrument_Offset_full.setFont(font_ee)
        self.lineEdit_Instrument_Offset_full.setObjectName("lineEdit_Instrument_Offset_full")
        self.lineEdit_Instrument_Offset_full.setText("0")
        self.tabWidget_Reductions.addTab(self.tab_Instrument_settings, "")
        self.tabWidget_Reductions.setTabText(1, "Instrument settings")

        # Tab: Export options
        self.tab_Export_options = QtWidgets.QWidget()
        self.tab_Export_options.setObjectName("tab_Export_options")
        self.checkBox_Export_Add_resolution_column = QtWidgets.QCheckBox(self.tab_Export_options)
        self.checkBox_Export_Add_resolution_column.setGeometry(QtCore.QRect(10, 10, 250, 18))
        self.checkBox_Export_Add_resolution_column.setFont(font_ee)
        self.checkBox_Export_Add_resolution_column.setChecked(True)
        self.checkBox_Export_Add_resolution_column.setObjectName("checkBox_Export_Add_resolution_column")
        self.checkBox_Export_Add_resolution_column.setText("Include ang. resolution column in the output file")
        self.checkBox_Export_Resolution_like_sared = QtWidgets.QCheckBox(self.tab_Export_options)
        self.checkBox_Export_Resolution_like_sared.setGeometry(QtCore.QRect(30, 35, 250, 18))
        self.checkBox_Export_Resolution_like_sared.setFont(font_ee)
        self.checkBox_Export_Resolution_like_sared.setChecked(True)
        self.checkBox_Export_Resolution_like_sared.setObjectName("checkBox_Export_Resolution_like_sared")
        self.checkBox_Export_Resolution_like_sared.setText("Calculate ang. resolution in 'Sared' way")
        self.checkBox_Export_Remove_zeros = QtWidgets.QCheckBox(self.tab_Export_options)
        self.checkBox_Export_Remove_zeros.setGeometry(QtCore.QRect(10, 60, 250, 18))
        self.checkBox_Export_Remove_zeros.setFont(font_ee)
        self.checkBox_Export_Remove_zeros.setChecked(False)
        self.checkBox_Export_Remove_zeros.setObjectName("checkBox_Export_Remove_zeros")
        self.checkBox_Export_Remove_zeros.setText("Remove zeros from reduced files")
        self.tabWidget_Reductions.addTab(self.tab_Export_options, "")
        self.tabWidget_Reductions.setTabText(2, "Export")

        # Block: Save reduced files at
        self.label_Save_at = QtWidgets.QLabel(self.centralwidget)
        self.label_Save_at.setGeometry(QtCore.QRect(305, 320, 200, 20))
        self.label_Save_at.setFont(font_headline)
        self.label_Save_at.setObjectName("label_Save_at")
        self.label_Save_at.setText("Save reduced files at")
        self.groupBox_Save_at = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Save_at.setGeometry(QtCore.QRect(299, 325, 282, 48))
        self.groupBox_Save_at.setFont(font_ee)
        self.groupBox_Save_at.setTitle("")
        self.groupBox_Save_at.setObjectName("groupBox_Save_at")
        self.lineEdit_Save_at = QtWidgets.QLineEdit(self.groupBox_Save_at)
        self.lineEdit_Save_at.setGeometry(QtCore.QRect(10, 22, 225, 22))
        self.lineEdit_Save_at.setFont(font_ee)
        self.lineEdit_Save_at.setObjectName("lineEdit_Save_at")
        self.lineEdit_Save_at.setText(self.current_dir)
        self.toolButton_Save_at = QtWidgets.QToolButton(self.groupBox_Save_at)
        self.toolButton_Save_at.setGeometry(QtCore.QRect(248, 22, 27, 22))
        self.toolButton_Save_at.setObjectName("toolButton_Save_at")
        self.toolButton_Save_at.setText("...")

        # Button: Clear
        self.pushButton_Clear = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Clear.setGeometry(QtCore.QRect(300, 380, 88, 30))
        self.pushButton_Clear.setFont(font_button)
        self.pushButton_Clear.setObjectName("pushButton_Clear")
        self.pushButton_Clear.setText("Clear all")

        # Button: Reduce all
        self.pushButton_Reduce_all = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Reduce_all.setGeometry(QtCore.QRect(493, 380, 88, 30))
        self.pushButton_Reduce_all.setFont(font_button)
        self.pushButton_Reduce_all.setObjectName("pushButton_Reduce_all")
        self.pushButton_Reduce_all.setText("Reduce all")

        # Errors
        self.label_Error_sample_len_missing = QtWidgets.QLabel(self.centralwidget)
        self.label_Error_sample_len_missing.setGeometry(QtCore.QRect(360, 420, 181, 31))
        self.label_Error_sample_len_missing.setFont(font_button)
        self.label_Error_sample_len_missing.setObjectName("label_Error_sample_len_missing")
        self.label_Error_sample_len_missing.setVisible(False)
        self.label_Error_sample_len_missing.setText("Sample length is missing")
        self.label_Error_sample_len_missing.setStyleSheet("color:rgb(255,0,0)")
        self.label_Error_DB_missing = QtWidgets.QLabel(self.centralwidget)
        self.label_Error_DB_missing.setGeometry(QtCore.QRect(355, 450, 181, 31))
        self.label_Error_DB_missing.setFont(font_button)
        self.label_Error_DB_missing.setObjectName("label_Error_DB_missing")
        self.label_Error_DB_missing.setVisible(False)
        self.label_Error_DB_missing.setText("Direct beam file is missing")
        self.label_Error_DB_missing.setStyleSheet("color:rgb(255,0,0)")
        self.label_Error_DB_wrong = QtWidgets.QLabel(self.centralwidget)
        self.label_Error_DB_wrong.setGeometry(QtCore.QRect(365, 420, 240, 51))
        self.label_Error_DB_wrong.setFont(font_button)
        self.label_Error_DB_wrong.setObjectName("label_Error_DB_wrong")
        self.label_Error_DB_wrong.setVisible(False)
        self.label_Error_DB_wrong.setStyleSheet("color:rgb(255,0,0)")
        self.label_Error_Save_at_missing = QtWidgets.QLabel(self.centralwidget)
        self.label_Error_Save_at_missing.setGeometry(QtCore.QRect(360, 435, 181, 31))
        self.label_Error_Save_at_missing.setFont(font_button)
        self.label_Error_Save_at_missing.setObjectName("label_Error_Save_at_missing")
        self.label_Error_Save_at_missing.setVisible(False)
        self.label_Error_Save_at_missing.setText("Define 'Save at' directory")
        self.label_Error_Save_at_missing.setStyleSheet("color:rgb(255,0,0)")
        self.label_Error_wrong_roi_input = QtWidgets.QLabel(self.centralwidget)
        self.label_Error_wrong_roi_input.setGeometry(QtCore.QRect(360, 435, 181, 31))
        self.label_Error_wrong_roi_input.setFont(font_button)
        self.label_Error_wrong_roi_input.setObjectName("label_Error_wrong_roi_input")
        self.label_Error_wrong_roi_input.setVisible(False)
        self.label_Error_wrong_roi_input.setText("Recheck your ROI input")
        self.label_Error_wrong_roi_input.setStyleSheet("color:rgb(255,0,0)")

        # Block: Recheck following files in SFM
        self.label_Recheck_files_in_SFM = QtWidgets.QLabel(self.centralwidget)
        self.label_Recheck_files_in_SFM.setGeometry(QtCore.QRect(305, 490, 250, 20))
        self.label_Recheck_files_in_SFM.setFont(font_headline)
        self.label_Recheck_files_in_SFM.setObjectName("label_Recheck_files_in_SFM")
        self.label_Recheck_files_in_SFM.setText("Recheck following files in SFM")
        self.groupBox_Recheck_files_in_SFM = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Recheck_files_in_SFM.setGeometry(QtCore.QRect(299, 497, 282, 180))
        self.groupBox_Recheck_files_in_SFM.setFont(font_ee)
        self.groupBox_Recheck_files_in_SFM.setTitle("")
        self.groupBox_Recheck_files_in_SFM.setObjectName("groupBox_Recheck_files_in_SFM")
        self.listWidget_Recheck_files_in_SFM = QtWidgets.QListWidget(self.groupBox_Recheck_files_in_SFM)
        self.listWidget_Recheck_files_in_SFM.setGeometry(QtCore.QRect(10, 27, 262, 145))
        self.listWidget_Recheck_files_in_SFM.setObjectName("listWidget_Recheck_files_in_SFM")

        # Block: Single File Mode
        self.label_SFM = QtWidgets.QLabel(self.centralwidget)
        self.label_SFM.setGeometry(QtCore.QRect(596, 5, 200, 20))
        self.label_SFM.setFont(font_headline)
        self.label_SFM.setObjectName("label_SFM")
        self.label_SFM.setText("Single File Mode (SFM)")
        self.groupBox_SFM_Scan = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_SFM_Scan.setGeometry(QtCore.QRect(591, 10, 472, 48))
        self.groupBox_SFM_Scan.setTitle("")
        self.groupBox_SFM_Scan.setObjectName("groupBoxScan")
        self.label_SFM_Scan = QtWidgets.QLabel(self.groupBox_SFM_Scan)
        self.label_SFM_Scan.setGeometry(QtCore.QRect(10, 23, 47, 20))
        self.label_SFM_Scan.setObjectName("label_SFM_Scan")
        self.label_SFM_Scan.setText("Scan")
        self.label_SFM_Scan.setFont(font_ee)
        self.comboBox_SFM_Scan = QtWidgets.QComboBox(self.groupBox_SFM_Scan)
        self.comboBox_SFM_Scan.setGeometry(QtCore.QRect(40, 23, 425, 20))
        self.comboBox_SFM_Scan.setObjectName("comboBoxScan")
        self.comboBox_SFM_Scan.setFont(font_ee)
        pg.setConfigOption('background', (255, 255, 255))
        pg.setConfigOption('foreground', 'k')

        # Button: Reduce SFM
        self.pushButton_Reduce_SFM = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Reduce_SFM.setGeometry(QtCore.QRect(1070, 28, 100, 30))
        self.pushButton_Reduce_SFM.setFont(font_button)
        self.pushButton_Reduce_SFM.setObjectName("pushButton_Reduce_SFM")
        self.pushButton_Reduce_SFM.setText("Reduce SFM")

        # Block: Detector Images and Reflectivity preview
        self.tabWidget_SFM = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_SFM.setGeometry(QtCore.QRect(592, 65, 578, 613))
        self.tabWidget_SFM.setFont(font_ee)
        self.tabWidget_SFM.setObjectName("tabWidget_SFM")

        # Tab: Detector images
        linedit_size_X = 30
        linedit_size_Y = 18
        self.tab_SFM_Detector_image = QtWidgets.QWidget()
        self.tab_SFM_Detector_image.setObjectName("tabdetector_image")
        self.graphicsView_SFM_Detector_image_Roi = pg.PlotWidget(self.tab_SFM_Detector_image, viewBox=pg.ViewBox())
        self.graphicsView_SFM_Detector_image_Roi.setGeometry(QtCore.QRect(0, 450, 577, 90))
        self.graphicsView_SFM_Detector_image_Roi.setObjectName("graphicsView_SFM_Detector_image_Roi")
        self.graphicsView_SFM_Detector_image_Roi.hideAxis("left")
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

        self.label_SFM_Detector_image_Point_number = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.label_SFM_Detector_image_Point_number.setFont(font_ee)
        self.label_SFM_Detector_image_Point_number.setGeometry(QtCore.QRect(10, 8, 70, 16))
        self.label_SFM_Detector_image_Point_number.setObjectName("label_SFM_Detector_image_Point_number")
        self.label_SFM_Detector_image_Point_number.setText("Point number")
        self.comboBox_SFM_Detector_image_Point_number = QtWidgets.QComboBox(self.tab_SFM_Detector_image)
        self.comboBox_SFM_Detector_image_Point_number.setFont(font_ee)
        self.comboBox_SFM_Detector_image_Point_number.setGeometry(QtCore.QRect(80, 7, 65, 20))
        self.comboBox_SFM_Detector_image_Point_number.setObjectName("comboBox_SFM_Detector_image_Point_number")
        self.label_SFM_Detector_image_Polarisation = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.label_SFM_Detector_image_Polarisation.setFont(font_ee)
        self.label_SFM_Detector_image_Polarisation.setGeometry(QtCore.QRect(155, 8, 60, 16))
        self.label_SFM_Detector_image_Polarisation.setObjectName("label_SFM_Detector_image_Polarisation")
        self.label_SFM_Detector_image_Polarisation.setText("Polarisation")
        self.comboBox_SFM_Detector_image_Polarisation = QtWidgets.QComboBox(self.tab_SFM_Detector_image)
        self.comboBox_SFM_Detector_image_Polarisation.setFont(font_ee)
        self.comboBox_SFM_Detector_image_Polarisation.setGeometry(QtCore.QRect(215, 7, 40, 20))
        self.comboBox_SFM_Detector_image_Polarisation.setObjectName("comboBox_SFM_Detector_image_Polarisation")
        self.label_SFM_Detector_image_Color_scheme = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.label_SFM_Detector_image_Color_scheme.setFont(font_ee)
        self.label_SFM_Detector_image_Color_scheme.setGeometry(QtCore.QRect(268, 8, 60, 16))
        self.label_SFM_Detector_image_Color_scheme.setObjectName("label_SFM_Detector_image_Color_scheme")
        self.label_SFM_Detector_image_Color_scheme.setText("Colors")
        self.comboBox_SFM_Detector_image_Color_scheme = QtWidgets.QComboBox(self.tab_SFM_Detector_image)
        self.comboBox_SFM_Detector_image_Color_scheme.setFont(font_ee)
        self.comboBox_SFM_Detector_image_Color_scheme.setGeometry(QtCore.QRect(305, 7, 90, 20))
        self.comboBox_SFM_Detector_image_Color_scheme.setObjectName("comboBox_SFM_Detector_image_Color_scheme")
        self.comboBox_SFM_Detector_image_Color_scheme.addItem("Green / Blue")
        self.comboBox_SFM_Detector_image_Color_scheme.addItem("White / Black")
        self.pushButton_SFM_Detector_image_Show_integrated_roi = QtWidgets.QPushButton(self.tab_SFM_Detector_image)
        self.pushButton_SFM_Detector_image_Show_integrated_roi.setGeometry(QtCore.QRect(445, 7, 120, 20))
        self.pushButton_SFM_Detector_image_Show_integrated_roi.setFont(font_button)
        self.pushButton_SFM_Detector_image_Show_integrated_roi.setObjectName("pushButton_SFM_Detector_image_Show_integrated_roi")
        self.pushButton_SFM_Detector_image_Show_integrated_roi.setText("Integrated ROI")
        self.label_SFM_Detector_image_Slits = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.label_SFM_Detector_image_Slits.setFont(font_ee)
        self.label_SFM_Detector_image_Slits.setGeometry(QtCore.QRect(385, 565, 51, 16))
        self.label_SFM_Detector_image_Slits.setObjectName("label_SFM_Detector_image_Slits")
        self.label_SFM_Detector_image_Slits.setText("Slits (mm):")
        self.label_SFM_Detector_image_Slits_s1hg = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.label_SFM_Detector_image_Slits_s1hg.setFont(font_ee)
        self.label_SFM_Detector_image_Slits_s1hg.setGeometry(QtCore.QRect(440, 565, 41, 16))
        self.label_SFM_Detector_image_Slits_s1hg.setObjectName("label_SFM_Detector_image_Slits_s1hg")
        self.label_SFM_Detector_image_Slits_s1hg.setText("s1hg")
        self.lineEdit_SFM_Detector_image_Slits_s1hg = QtWidgets.QLineEdit(self.tab_SFM_Detector_image)
        self.lineEdit_SFM_Detector_image_Slits_s1hg.setFont(font_ee)
        self.lineEdit_SFM_Detector_image_Slits_s1hg.setGeometry(QtCore.QRect(470, 565, linedit_size_X, linedit_size_Y))
        self.lineEdit_SFM_Detector_image_Slits_s1hg.setObjectName("lineEdit_SFM_Detector_image_Slits_s1hg")
        self.lineEdit_SFM_Detector_image_Slits_s1hg.setEnabled(False)
        self.lineEdit_SFM_Detector_image_Slits_s1hg.setStyleSheet("color:rgb(0,0,0)")
        self.label_SFM_Detector_image_Slits_s2hg = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.label_SFM_Detector_image_Slits_s2hg.setFont(font_ee)
        self.label_SFM_Detector_image_Slits_s2hg.setGeometry(QtCore.QRect(505, 565, 30, 16))
        self.label_SFM_Detector_image_Slits_s2hg.setObjectName("label_SFM_Detector_image_Slits_s2hg")
        self.label_SFM_Detector_image_Slits_s2hg.setText("s2hg")
        self.lineEdit_SFM_Detector_image_Slits_s2hg = QtWidgets.QLineEdit(self.tab_SFM_Detector_image)
        self.lineEdit_SFM_Detector_image_Slits_s2hg.setFont(font_ee)
        self.lineEdit_SFM_Detector_image_Slits_s2hg.setGeometry(QtCore.QRect(535, 565, linedit_size_X, linedit_size_Y))
        self.lineEdit_SFM_Detector_image_Slits_s2hg.setObjectName("lineEdit_SFM_Detector_image_Slits_s2hg")
        self.lineEdit_SFM_Detector_image_Slits_s2hg.setEnabled(False)
        self.lineEdit_SFM_Detector_image_Slits_s2hg.setStyleSheet("color:rgb(0,0,0)")
        self.label_SFM_Detector_image_Time = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.label_SFM_Detector_image_Time.setFont(font_ee)
        self.label_SFM_Detector_image_Time.setGeometry(QtCore.QRect(385, 545, 71, 16))
        self.label_SFM_Detector_image_Time.setObjectName("label_SFM_Detector_image_Time")
        self.label_SFM_Detector_image_Time.setText("Time (s):")
        self.lineEdit_SFM_Detector_image_Time = QtWidgets.QLineEdit(self.tab_SFM_Detector_image)
        self.lineEdit_SFM_Detector_image_Time.setFont(font_ee)
        self.lineEdit_SFM_Detector_image_Time.setGeometry(QtCore.QRect(470, 545, linedit_size_X, linedit_size_Y))
        self.lineEdit_SFM_Detector_image_Time.setObjectName("lineEdit_SFM_Detector_image_Time")
        self.lineEdit_SFM_Detector_image_Time.setEnabled(False)
        self.lineEdit_SFM_Detector_image_Time.setStyleSheet("color:rgb(0,0,0)")
        self.label_SFM_Detector_image_Roi = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.label_SFM_Detector_image_Roi.setFont(font_ee)
        self.label_SFM_Detector_image_Roi.setGeometry(QtCore.QRect(10, 545, 31, 16))
        self.label_SFM_Detector_image_Roi.setObjectName("label_SFM_Detector_image_Roi")
        self.label_SFM_Detector_image_Roi.setText("ROI:  ")
        self.label_SFM_Detector_image_Roi_X_Left = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.label_SFM_Detector_image_Roi_X_Left.setFont(font_ee)
        self.label_SFM_Detector_image_Roi_X_Left.setGeometry(QtCore.QRect(40, 545, 51, 16))
        self.label_SFM_Detector_image_Roi_X_Left.setObjectName("label_SFM_Detector_image_Roi_X_Left")
        self.label_SFM_Detector_image_Roi_X_Left.setText("left")
        self.lineEdit_SFM_Detector_image_Roi_X_Left = QtWidgets.QLineEdit(self.tab_SFM_Detector_image)
        self.lineEdit_SFM_Detector_image_Roi_X_Left.setFont(font_ee)
        self.lineEdit_SFM_Detector_image_Roi_X_Left.setGeometry(QtCore.QRect(75, 545, linedit_size_X, linedit_size_Y))
        self.lineEdit_SFM_Detector_image_Roi_X_Left.setObjectName("lineEdit_SFM_Detector_image_Roi_X_Left")
        self.label_SFM_Detector_image_Roi_X_Right = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.label_SFM_Detector_image_Roi_X_Right.setFont(font_ee)
        self.label_SFM_Detector_image_Roi_X_Right.setGeometry(QtCore.QRect(115, 545, 51, 16))
        self.label_SFM_Detector_image_Roi_X_Right.setObjectName("label_SFM_Detector_image_Roi_X_Right")
        self.label_SFM_Detector_image_Roi_X_Right.setText("right")
        self.lineEdit_SFM_Detector_image_Roi_X_Right = QtWidgets.QLineEdit(self.tab_SFM_Detector_image)
        self.lineEdit_SFM_Detector_image_Roi_X_Right.setFont(font_ee)
        self.lineEdit_SFM_Detector_image_Roi_X_Right.setGeometry(QtCore.QRect(140, 545, linedit_size_X, linedit_size_Y))
        self.lineEdit_SFM_Detector_image_Roi_X_Right.setObjectName("lineEdit_SFM_Detector_image_Roi_X_Right")
        self.label_SFM_Detector_image_Roi_Y_Bottom = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.label_SFM_Detector_image_Roi_Y_Bottom.setFont(font_ee)
        self.label_SFM_Detector_image_Roi_Y_Bottom.setGeometry(QtCore.QRect(40, 565, 51, 16))
        self.label_SFM_Detector_image_Roi_Y_Bottom.setObjectName("label_SFM_Detector_image_Roi_Y_Bottom")
        self.label_SFM_Detector_image_Roi_Y_Bottom.setText("bottom")
        self.lineEdit_SFM_Detector_image_Roi_Y_Bottom = QtWidgets.QLineEdit(self.tab_SFM_Detector_image)
        self.lineEdit_SFM_Detector_image_Roi_Y_Bottom.setFont(font_ee)
        self.lineEdit_SFM_Detector_image_Roi_Y_Bottom.setGeometry(QtCore.QRect(75, 565, linedit_size_X, linedit_size_Y))
        self.lineEdit_SFM_Detector_image_Roi_Y_Bottom.setObjectName("lineEdit_SFM_Detector_image_Roi_Y_Bottom")
        self.label_SFM_Detector_image_Roi_Y_Top = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.label_SFM_Detector_image_Roi_Y_Top.setFont(font_ee)
        self.label_SFM_Detector_image_Roi_Y_Top.setGeometry(QtCore.QRect(115, 565, 51, 16))
        self.label_SFM_Detector_image_Roi_Y_Top.setObjectName("label_SFM_Detector_image_Roi_Y_Top")
        self.label_SFM_Detector_image_Roi_Y_Top.setText("top")
        self.lineEdit_SFM_Detector_image_Roi_Y_Top = QtWidgets.QLineEdit(self.tab_SFM_Detector_image)
        self.lineEdit_SFM_Detector_image_Roi_Y_Top.setFont(font_ee)
        self.lineEdit_SFM_Detector_image_Roi_Y_Top.setGeometry(QtCore.QRect(140, 565, linedit_size_X, linedit_size_Y))
        self.lineEdit_SFM_Detector_image_Roi_Y_Top.setObjectName("lineEdit_SFM_Detector_image_Roi_Y_Top")
        self.label_SFM_Detector_image_Roi_bkg = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.label_SFM_Detector_image_Roi_bkg.setFont(font_ee)
        self.label_SFM_Detector_image_Roi_bkg.setGeometry(QtCore.QRect(190, 545, 47, 16))
        self.label_SFM_Detector_image_Roi_bkg.setObjectName("label_SFM_Detector_image_Roi_bkg")
        self.label_SFM_Detector_image_Roi_bkg.setText("ROI BKG:")
        self.label_SFM_Detector_image_Roi_bkg_X_Left = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.label_SFM_Detector_image_Roi_bkg_X_Left.setFont(font_ee)
        self.label_SFM_Detector_image_Roi_bkg_X_Left.setGeometry(QtCore.QRect(240, 545, 51, 16))
        self.label_SFM_Detector_image_Roi_bkg_X_Left.setObjectName("label_SFM_Detector_image_Roi_bkg_X_Left")
        self.label_SFM_Detector_image_Roi_bkg_X_Left.setText("left")
        self.lineEdit_SFM_Detector_image_Roi_bkg_X_Left = QtWidgets.QLineEdit(self.tab_SFM_Detector_image)
        self.lineEdit_SFM_Detector_image_Roi_bkg_X_Left.setFont(font_ee)
        self.lineEdit_SFM_Detector_image_Roi_bkg_X_Left.setGeometry(QtCore.QRect(275, 545, linedit_size_X, linedit_size_Y))
        self.lineEdit_SFM_Detector_image_Roi_bkg_X_Left.setObjectName("lineEdit_SFM_Detector_image_Roi_bkg_X_Left")
        self.lineEdit_SFM_Detector_image_Roi_bkg_X_Left.setEnabled(False)
        self.lineEdit_SFM_Detector_image_Roi_bkg_X_Left.setStyleSheet("color:rgb(0,0,0)")
        self.label_SFM_Detector_image_Roi_bkg_X_Right = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.label_SFM_Detector_image_Roi_bkg_X_Right.setFont(font_ee)
        self.label_SFM_Detector_image_Roi_bkg_X_Right.setGeometry(QtCore.QRect(315, 545, 51, 16))
        self.label_SFM_Detector_image_Roi_bkg_X_Right.setObjectName("label_SFM_Detector_image_Roi_bkg_X_Right")
        self.label_SFM_Detector_image_Roi_bkg_X_Right.setText("right")
        self.lineEdit_SFM_Detector_image_Roi_bkg_X_Right = QtWidgets.QLineEdit(self.tab_SFM_Detector_image)
        self.lineEdit_SFM_Detector_image_Roi_bkg_X_Right.setFont(font_ee)
        self.lineEdit_SFM_Detector_image_Roi_bkg_X_Right.setGeometry(QtCore.QRect(340, 545, linedit_size_X, linedit_size_Y))
        self.lineEdit_SFM_Detector_image_Roi_bkg_X_Right.setObjectName("lineEdit_SFM_Detector_image_Roi_bkg_X_Right")
        self.label_SFM_Detector_image_Roi_bkg_Y_Bottom = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.label_SFM_Detector_image_Roi_bkg_Y_Bottom.setFont(font_ee)
        self.label_SFM_Detector_image_Roi_bkg_Y_Bottom.setGeometry(QtCore.QRect(240, 565, 51, 16))
        self.label_SFM_Detector_image_Roi_bkg_Y_Bottom.setObjectName("label_SFM_Detector_image_Roi_bkg_Y_Bottom")
        self.label_SFM_Detector_image_Roi_bkg_Y_Bottom.setText("bottom")
        self.lineEdit_SFM_Detector_image_Roi_bkg_Y_Bottom = QtWidgets.QLineEdit(self.tab_SFM_Detector_image)
        self.lineEdit_SFM_Detector_image_Roi_bkg_Y_Bottom.setFont(font_ee)
        self.lineEdit_SFM_Detector_image_Roi_bkg_Y_Bottom.setGeometry(QtCore.QRect(275, 565, linedit_size_X, linedit_size_Y))
        self.lineEdit_SFM_Detector_image_Roi_bkg_Y_Bottom.setObjectName("lineEdit_SFM_Detector_image_Roi_bkg_Y_Bottom")
        self.lineEdit_SFM_Detector_image_Roi_bkg_Y_Bottom.setEnabled(False)
        self.lineEdit_SFM_Detector_image_Roi_bkg_Y_Bottom.setStyleSheet("color:rgb(0,0,0)")
        self.label_SFM_Detector_image_Roi_bkg_Y_Top = QtWidgets.QLabel(self.tab_SFM_Detector_image)
        self.label_SFM_Detector_image_Roi_bkg_Y_Top.setFont(font_ee)
        self.label_SFM_Detector_image_Roi_bkg_Y_Top.setGeometry(QtCore.QRect(315, 565, 51, 16))
        self.label_SFM_Detector_image_Roi_bkg_Y_Top.setObjectName("label_SFM_Detector_image_Roi_bkg_Y_Top")
        self.label_SFM_Detector_image_Roi_bkg_Y_Top.setText("top")
        self.lineEdit_SFM_Detector_image_Roi_bkg_Y_Top = QtWidgets.QLineEdit(self.tab_SFM_Detector_image)
        self.lineEdit_SFM_Detector_image_Roi_bkg_Y_Top.setFont(font_ee)
        self.lineEdit_SFM_Detector_image_Roi_bkg_Y_Top.setGeometry(QtCore.QRect(340, 565, linedit_size_X, linedit_size_Y))
        self.lineEdit_SFM_Detector_image_Roi_bkg_Y_Top.setObjectName("lineEdit_SFM_Detector_image_Roi_bkg_Y_Top")
        self.lineEdit_SFM_Detector_image_Roi_bkg_Y_Top.setEnabled(False)
        self.lineEdit_SFM_Detector_image_Roi_bkg_Y_Top.setStyleSheet("color:rgb(0,0,0)")

        self.tabWidget_SFM.addTab(self.tab_SFM_Detector_image, "")
        self.tabWidget_SFM.setTabText(self.tabWidget_SFM.indexOf(self.tab_SFM_Detector_image), "Detector Image")

        # Tab: Reflectivity preview
        self.tab_SFM_Reflectivity_preview = QtWidgets.QWidget()
        self.tab_SFM_Reflectivity_preview.setObjectName("tabreflectivity_preview")
        self.graphicsView_SFM_Reflectivity_preview = pg.PlotWidget(self.tab_SFM_Reflectivity_preview)
        self.graphicsView_SFM_Reflectivity_preview.setGeometry(QtCore.QRect(0, 20, 577, 540))
        self.graphicsView_SFM_Reflectivity_preview.setObjectName("graphicsView_SFM_Reflectivity_preview")
        self.graphicsView_SFM_Reflectivity_preview.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_SFM_Reflectivity_preview.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_SFM_Reflectivity_preview.getAxis("left").tickFont = font_graphs
        self.graphicsView_SFM_Reflectivity_preview.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_SFM_Reflectivity_preview.showAxis("top")
        self.graphicsView_SFM_Reflectivity_preview.getAxis("top").setTicks([])
        self.graphicsView_SFM_Reflectivity_preview.showAxis("right")
        self.graphicsView_SFM_Reflectivity_preview.getAxis("right").setTicks([])
        self.checkBox_SFM_Reflectivity_preview_Show_overillumination = QtWidgets.QCheckBox(self.tab_SFM_Reflectivity_preview)
        self.checkBox_SFM_Reflectivity_preview_Show_overillumination.setFont(font_ee)
        self.checkBox_SFM_Reflectivity_preview_Show_overillumination.setGeometry(QtCore.QRect(10, 7, 150, 18))
        self.checkBox_SFM_Reflectivity_preview_Show_overillumination.setObjectName("checkBox_SFM_Reflectivity_preview_Show_overillumination")
        self.checkBox_SFM_Reflectivity_preview_Show_overillumination.setText("Show Overillumination")
        self.comboBox_SFM_Reflectivity_preview_Plot_axis = QtWidgets.QComboBox(self.tab_SFM_Reflectivity_preview)
        self.comboBox_SFM_Reflectivity_preview_Plot_axis.setFont(font_ee)
        self.comboBox_SFM_Reflectivity_preview_Plot_axis.setGeometry(QtCore.QRect(380, 7, 185, 20))
        self.comboBox_SFM_Reflectivity_preview_Plot_axis.setObjectName("comboBoxreflectivity_preview_Plot_axis")
        self.comboBox_SFM_Reflectivity_preview_Plot_axis.addItem("Reflectivity (log) vs Angle (Qz)")
        self.comboBox_SFM_Reflectivity_preview_Plot_axis.addItem("Reflectivity (lin) vs Angle (Qz)")
        self.comboBox_SFM_Reflectivity_preview_Plot_axis.addItem("Reflectivity (log) vs Angle (deg)")
        self.comboBox_SFM_Reflectivity_preview_Plot_axis.addItem("Reflectivity (lin) vs Angle (deg)")
        self.checkBox_SFM_Reflectivity_preview_Include_errorbars = QtWidgets.QCheckBox(self.tab_SFM_Reflectivity_preview)
        self.checkBox_SFM_Reflectivity_preview_Include_errorbars.setFont(font_ee)
        self.checkBox_SFM_Reflectivity_preview_Include_errorbars.setGeometry(QtCore.QRect(10, 565, 111, 18))
        self.checkBox_SFM_Reflectivity_preview_Include_errorbars.setObjectName("checkBox_SFM_Reflectivity_preview_Include_errorbars")
        self.checkBox_SFM_Reflectivity_preview_Include_errorbars.setText("Include Error Bars")
        self.label_SFM_Reflectivity_preview_Skip_points_Left = QtWidgets.QLabel(self.tab_SFM_Reflectivity_preview)
        self.label_SFM_Reflectivity_preview_Skip_points_Left.setFont(font_ee)
        self.label_SFM_Reflectivity_preview_Skip_points_Left.setGeometry(QtCore.QRect(372, 565, 100, 16))
        self.label_SFM_Reflectivity_preview_Skip_points_Left.setObjectName("label_SFM_Reflectivity_preview_Skip_points_Left")
        self.label_SFM_Reflectivity_preview_Skip_points_Left.setText("Points to skip:  left")
        self.lineEdit_SFM_Reflectivity_preview_Skip_points_Left = QtWidgets.QLineEdit(self.tab_SFM_Reflectivity_preview)
        self.lineEdit_SFM_Reflectivity_preview_Skip_points_Left.setFont(font_ee)
        self.lineEdit_SFM_Reflectivity_preview_Skip_points_Left.setGeometry(QtCore.QRect(470, 565, linedit_size_X, linedit_size_Y))
        self.lineEdit_SFM_Reflectivity_preview_Skip_points_Left.setObjectName("lineEditreflectivity_preview_Skip_points_Left")
        self.lineEdit_SFM_Reflectivity_preview_Skip_points_Left.setText("0")
        self.label_SFM_Reflectivity_preview_Skip_points_Right = QtWidgets.QLabel(self.tab_SFM_Reflectivity_preview)
        self.label_SFM_Reflectivity_preview_Skip_points_Right.setFont(font_ee)
        self.label_SFM_Reflectivity_preview_Skip_points_Right.setGeometry(QtCore.QRect(510, 565, 80, 16))
        self.label_SFM_Reflectivity_preview_Skip_points_Right.setObjectName("label_SFM_Reflectivity_preview_Skip_points_Right")
        self.label_SFM_Reflectivity_preview_Skip_points_Right.setText("right")
        self.lineEdit_SFM_Reflectivity_preview_Skip_points_Right = QtWidgets.QLineEdit(self.tab_SFM_Reflectivity_preview)
        self.lineEdit_SFM_Reflectivity_preview_Skip_points_Right.setFont(font_ee)
        self.lineEdit_SFM_Reflectivity_preview_Skip_points_Right.setGeometry(QtCore.QRect(535, 565, linedit_size_X, linedit_size_Y))
        self.lineEdit_SFM_Reflectivity_preview_Skip_points_Right.setObjectName("lineEditreflectivity_preview_Skip_points_Right")
        self.lineEdit_SFM_Reflectivity_preview_Skip_points_Right.setText("0")
        self.tabWidget_SFM.addTab(self.tab_SFM_Reflectivity_preview, "")
        self.tabWidget_SFM.setTabText(self.tabWidget_SFM.indexOf(self.tab_SFM_Reflectivity_preview), "Reflectivity preview")

        # Tab: 2D Map
        self.tab_2Dmap = QtWidgets.QWidget()
        self.tab_2Dmap.setObjectName("tab_2Dmap")
        # scaling options are different for different views
        # scale for "Pixel vs Points view" and "Alpha I vs Alpha f"
        self.label_SFM_2Dmap_Highlight = QtWidgets.QLabel(self.tab_2Dmap)
        self.label_SFM_2Dmap_Highlight.setFont(font_ee)
        self.label_SFM_2Dmap_Highlight.setGeometry(QtCore.QRect(5, 8, 50, 16))
        self.label_SFM_2Dmap_Highlight.setObjectName("label_SFM_2Dmap_Highlight")
        self.label_SFM_2Dmap_Highlight.setText("Highlight")
        self.horizontalSlider_SFM_2Dmap_Highlight = QtWidgets.QSlider(self.tab_2Dmap)
        self.horizontalSlider_SFM_2Dmap_Highlight.setGeometry(QtCore.QRect(55, 7, 190, 22))
        self.horizontalSlider_SFM_2Dmap_Highlight.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_SFM_2Dmap_Highlight.setObjectName("horizontalSlider_SFM_2Dmap_Highlight")
        self.horizontalSlider_SFM_2Dmap_Highlight.setMinimum(0)
        self.horizontalSlider_SFM_2Dmap_Highlight.setMaximum(1000)
        self.horizontalSlider_SFM_2Dmap_Highlight.setValue(40)
        # "scale" for "Qx vs Qz"
        self.label_SFM_2Dmap_Qxz_Threshold = QtWidgets.QLabel(self.tab_2Dmap)
        self.label_SFM_2Dmap_Qxz_Threshold.setFont(font_ee)
        self.label_SFM_2Dmap_Qxz_Threshold.setGeometry(QtCore.QRect(5, 8, 220, 16))
        self.label_SFM_2Dmap_Qxz_Threshold.setObjectName("label_SFM_2Dmap_Qxz_Threshold")
        self.label_SFM_2Dmap_Qxz_Threshold.setText("Threshold for the view (number of neutrons):")
        self.label_SFM_2Dmap_Qxz_Threshold.setVisible(False)
        self.comboBox_SFM_2Dmap_Qxz_Threshold = QtWidgets.QComboBox(self.tab_2Dmap)
        self.comboBox_SFM_2Dmap_Qxz_Threshold.setFont(font_ee)
        self.comboBox_SFM_2Dmap_Qxz_Threshold.setGeometry(QtCore.QRect(230, 7, 40, 20))
        self.comboBox_SFM_2Dmap_Qxz_Threshold.setObjectName("comboBox2dmap_Qxz_threshold")
        self.comboBox_SFM_2Dmap_Qxz_Threshold.addItem("1")
        self.comboBox_SFM_2Dmap_Qxz_Threshold.addItem("2")
        self.comboBox_SFM_2Dmap_Qxz_Threshold.addItem("5")
        self.comboBox_SFM_2Dmap_Qxz_Threshold.addItem("10")
        self.comboBox_SFM_2Dmap_Qxz_Threshold.setVisible(False)
        self.label_SFM_2Dmap_Polarisation = QtWidgets.QLabel(self.tab_2Dmap)
        self.label_SFM_2Dmap_Polarisation.setFont(font_ee)
        self.label_SFM_2Dmap_Polarisation.setGeometry(QtCore.QRect(284, 8, 71, 16))
        self.label_SFM_2Dmap_Polarisation.setObjectName("label_SFM_2Dmap_Polarisation")
        self.label_SFM_2Dmap_Polarisation.setText("Polarisation")
        self.comboBox_SFM_2Dmap_Polarisation = QtWidgets.QComboBox(self.tab_2Dmap)
        self.comboBox_SFM_2Dmap_Polarisation.setFont(font_ee)
        self.comboBox_SFM_2Dmap_Polarisation.setGeometry(QtCore.QRect(344, 7, 40, 20))
        self.comboBox_SFM_2Dmap_Polarisation.setObjectName("comboBox2dmap_polarisation")
        self.label_SFM_2Dmap_Axes = QtWidgets.QLabel(self.tab_2Dmap)
        self.label_SFM_2Dmap_Axes.setFont(font_ee)
        self.label_SFM_2Dmap_Axes.setGeometry(QtCore.QRect(405, 8, 71, 16))
        self.label_SFM_2Dmap_Axes.setObjectName("label_SFM_2Dmap_Axes")
        self.label_SFM_2Dmap_Axes.setText("Axes")
        self.comboBox_SFM_2Dmap_Axes = QtWidgets.QComboBox(self.tab_2Dmap)
        self.comboBox_SFM_2Dmap_Axes.setFont(font_ee)
        self.comboBox_SFM_2Dmap_Axes.setGeometry(QtCore.QRect(435, 7, 130, 20))
        self.comboBox_SFM_2Dmap_Axes.setObjectName("comboBox2dmap_axes")
        self.comboBox_SFM_2Dmap_Axes.addItem("Pixel vs. Point")
        self.comboBox_SFM_2Dmap_Axes.addItem("Alpha_i vs. Alpha_f")
        self.comboBox_SFM_2Dmap_Axes.addItem("Qx vs. Qz")
        self.graphicsView_SFM_2Dmap = pg.ImageView(self.tab_2Dmap, view=pg.PlotItem())
        self.graphicsView_SFM_2Dmap.setGeometry(QtCore.QRect(0, 30, 577, 522))
        self.graphicsView_SFM_2Dmap.setObjectName("graphicsView_SFM_2Dmap")
        self.graphicsView_SFM_2Dmap.ui.menuBtn.hide()
        self.graphicsView_SFM_2Dmap.ui.roiBtn.hide()
        self.graphicsView_SFM_2Dmap.ui.histogram.hide()
        colmap = pg.ColorMap(numpy.array([0.0,0.1,1.0]), numpy.array([[0,0,0,255],[255,128,0,255],[255,255,0,255]], dtype=numpy.ubyte))
        self.graphicsView_SFM_2Dmap.setColorMap(colmap)
        self.graphicsView_SFM_2Dmap.view.showAxis("left")
        self.graphicsView_SFM_2Dmap.view.showAxis("bottom")
        self.graphicsView_SFM_2Dmap.view.showAxis("top")
        self.graphicsView_SFM_2Dmap.view.getAxis("top").setTicks([])
        self.graphicsView_SFM_2Dmap.view.showAxis("right")
        self.graphicsView_SFM_2Dmap.view.getAxis("right").setTicks([])
        self.graphicsView_SFM_2Dmap.getView().getViewBox().invertY(b=False)

        # 2D map for "Qx vs Qz" is a plot, compared to "Pixel vs Points" which is Image.
        # I rescale graphicsView_SFM_2Dmap_Qxz_Theta to show/hide it
        self.graphicsView_SFM_2Dmap_Qxz_Theta = pg.PlotWidget(self.tab_2Dmap)
        self.graphicsView_SFM_2Dmap_Qxz_Theta.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.graphicsView_SFM_2Dmap_Qxz_Theta.setObjectName("graphicsView_SFM_2Dmap_Qxz_Theta")
        self.graphicsView_SFM_2Dmap_Qxz_Theta.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_SFM_2Dmap_Qxz_Theta.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_SFM_2Dmap_Qxz_Theta.getAxis("left").tickFont = font_graphs
        self.graphicsView_SFM_2Dmap_Qxz_Theta.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_SFM_2Dmap_Qxz_Theta.showAxis("top")
        self.graphicsView_SFM_2Dmap_Qxz_Theta.getAxis("top").setTicks([])
        self.graphicsView_SFM_2Dmap_Qxz_Theta.showAxis("right")
        self.graphicsView_SFM_2Dmap_Qxz_Theta.getAxis("right").setTicks([])
        self.label_SFM_2Dmap_Qxz_Lower_number_of_points_by = QtWidgets.QLabel(self.tab_2Dmap)
        self.label_SFM_2Dmap_Qxz_Lower_number_of_points_by.setFont(font_ee)
        self.label_SFM_2Dmap_Qxz_Lower_number_of_points_by.setGeometry(QtCore.QRect(5, 561, 211, 16))
        self.label_SFM_2Dmap_Qxz_Lower_number_of_points_by.setObjectName("label_SFM_2Dmap_Qxz_Lower_number_of_points_by")
        self.label_SFM_2Dmap_Qxz_Lower_number_of_points_by.setText("Lower the number of points by factor")
        self.label_SFM_2Dmap_Qxz_Lower_number_of_points_by.setVisible(False)
        self.comboBox_SFM_2Dmap_Qxz_Lower_number_of_points_by = QtWidgets.QComboBox(self.tab_2Dmap)
        self.comboBox_SFM_2Dmap_Qxz_Lower_number_of_points_by.setFont(font_ee)
        self.comboBox_SFM_2Dmap_Qxz_Lower_number_of_points_by.setGeometry(QtCore.QRect(195, 560, 40, 20))
        self.comboBox_SFM_2Dmap_Qxz_Lower_number_of_points_by.setObjectName("comboBox2dmap_Qxz_Lower_number_of_points_by")
        self.comboBox_SFM_2Dmap_Qxz_Lower_number_of_points_by.addItem("5")
        self.comboBox_SFM_2Dmap_Qxz_Lower_number_of_points_by.addItem("4")
        self.comboBox_SFM_2Dmap_Qxz_Lower_number_of_points_by.addItem("3")
        self.comboBox_SFM_2Dmap_Qxz_Lower_number_of_points_by.addItem("2")
        self.comboBox_SFM_2Dmap_Qxz_Lower_number_of_points_by.addItem("1")
        self.comboBox_SFM_2Dmap_Qxz_Lower_number_of_points_by.setVisible(False)
        self.label_SFM_2Dmap_Rescale_image_x = QtWidgets.QLabel(self.tab_2Dmap)
        self.label_SFM_2Dmap_Rescale_image_x.setFont(font_ee)
        self.label_SFM_2Dmap_Rescale_image_x.setGeometry(QtCore.QRect(5, 561, 80, 16))
        self.label_SFM_2Dmap_Rescale_image_x.setObjectName("label_SFM_2Dmap_Rescale_image_x")
        self.label_SFM_2Dmap_Rescale_image_x.setText("Rescale image: x")
        self.horizontalSlider_SFM_2Dmap_Rescale_image_x = QtWidgets.QSlider(self.tab_2Dmap)
        self.horizontalSlider_SFM_2Dmap_Rescale_image_x.setGeometry(QtCore.QRect(90, 560, 80, 22))
        self.horizontalSlider_SFM_2Dmap_Rescale_image_x.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_SFM_2Dmap_Rescale_image_x.setObjectName("horizontalSlider_SFM_2Dmap_Rescale_image_x")
        self.horizontalSlider_SFM_2Dmap_Rescale_image_x.setMinimum(1)
        self.horizontalSlider_SFM_2Dmap_Rescale_image_x.setMaximum(15)
        self.horizontalSlider_SFM_2Dmap_Rescale_image_x.setValue(1)
        self.label_SFM_2Dmap_Rescale_image_y = QtWidgets.QLabel(self.tab_2Dmap)
        self.label_SFM_2Dmap_Rescale_image_y.setFont(font_ee)
        self.label_SFM_2Dmap_Rescale_image_y.setGeometry(QtCore.QRect(180, 561, 20, 16))
        self.label_SFM_2Dmap_Rescale_image_y.setObjectName("label_SFM_2Dmap_Rescale_image_y")
        self.label_SFM_2Dmap_Rescale_image_y.setText("y")
        self.horizontalSlider_SFM_2Dmap_Rescale_image_y = QtWidgets.QSlider(self.tab_2Dmap)
        self.horizontalSlider_SFM_2Dmap_Rescale_image_y.setGeometry(QtCore.QRect(190, 560, 80, 22))
        self.horizontalSlider_SFM_2Dmap_Rescale_image_y.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_SFM_2Dmap_Rescale_image_y.setObjectName("horizontalSlider_SFM_2Dmap_Rescale_image_y")
        self.horizontalSlider_SFM_2Dmap_Rescale_image_y.setMinimum(1)
        self.horizontalSlider_SFM_2Dmap_Rescale_image_y.setMaximum(15)
        self.horizontalSlider_SFM_2Dmap_Rescale_image_y.setValue(1)
        self.pushButton_SFM_2Dmap_export = QtWidgets.QPushButton(self.tab_2Dmap)
        self.pushButton_SFM_2Dmap_export.setGeometry(QtCore.QRect(445, 555, 120, 25))
        self.pushButton_SFM_2Dmap_export.setFont(font_button)
        self.pushButton_SFM_2Dmap_export.setObjectName("pushButton_SFM_2Dmap_export")
        self.pushButton_SFM_2Dmap_export.setText("Export 2D map")
        self.tabWidget_SFM.addTab(self.tab_2Dmap, "")
        self.tabWidget_SFM.setTabText(self.tabWidget_SFM.indexOf(self.tab_2Dmap), "2D map")

        # StatusBar
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # MenuBar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 21))
        self.menubar.setObjectName("menu_bar")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        self.menu_Help.setTitle("Help")
        MainWindow.setMenuBar(self.menubar)
        self.action_Algorithm_info = QtWidgets.QAction(MainWindow)
        self.action_Algorithm_info.setObjectName("action_Algorithm_info")
        self.action_Algorithm_info.setText("Algorithm info")
        self.action_Version = QtWidgets.QAction(MainWindow)
        self.action_Version.setObjectName("action_Version")
        self.menu_Help.addAction(self.action_Algorithm_info)
        self.menu_Help.addAction(self.action_Version)
        self.action_Version.setText("V1.4.2")
        self.menubar.addAction(self.menu_Help.menuAction())

        self.tabWidget_Reductions.setCurrentIndex(0)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    ##<--

class GUI(Ui_MainWindow):

    # MAC_Win diff
    current_dir = ""
    for i in sys.argv[0].split("/")[:-4]:
        current_dir += i + "/"

    def __init__(self):

        super(GUI, self).__init__()
        self.setupUi(self)

        # Other parameters

        # current file in Single File Mode
        self.SFM_FILE = ""
        self.sfm_file_already_analized = ""
        self.sfm_file_2d_calculated_params = []
        self.psd_uu_sfm = []
        self.psd_du_sfm = []
        self.psd_ud_sfm = []
        self.psd_dd_sfm = []

        # current th point
        self.current_th = ""

        # write calculated overillumination coefficients into library
        self.overill_coeff_lib = {}

        # Write DB info into library
        self.DB_INFO = {}
        self.db_already_analized = []

        # ROI frames
        self.draw_roi = []
        self.draw_roi_2D_map = []

        # Recalc intens if Y roi is changed
        self.old_roi_coord_Y = []
        self.draw_roi_int = []

        # Trigger to switch the detector image view
        self.show_det_int_trigger = True

        # Alpha_i vs Alpha_f array
        self.res_Aif = []

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

        # Triggers: ComboBoxes
        self.comboBox_SFM_Detector_image_Point_number.currentIndexChanged.connect(self.draw_det_image)
        self.comboBox_SFM_Detector_image_Polarisation.currentIndexChanged.connect(self.draw_det_image)
        self.comboBox_SFM_Scan.currentIndexChanged.connect(self.load_SFM_Detector_images)
        self.comboBox_SFM_Scan.currentIndexChanged.connect(self.load_SFM_Reflectivity_preview)
        self.comboBox_SFM_Reflectivity_preview_Plot_axis.currentIndexChanged.connect(self.load_SFM_Reflectivity_preview)
        self.comboBox_SFM_2Dmap_Qxz_Threshold.currentIndexChanged.connect(self.draw_2D_map)
        self.comboBox_SFM_2Dmap_Polarisation.currentIndexChanged.connect(self.draw_2D_map)
        self.comboBox_SFM_2Dmap_Axes.currentIndexChanged.connect(self.draw_2D_map)
        self.comboBox_SFM_Scan.currentIndexChanged.connect(self.draw_2D_map)
        self.comboBox_SFM_2Dmap_Qxz_Lower_number_of_points_by.currentIndexChanged.connect(self.draw_2D_map)
        self.comboBox_SFM_Detector_image_Color_scheme.currentIndexChanged.connect(self.color_det_image)
        self.comboBox_Reductions_Divide_by_monitor_or_time.currentIndexChanged.connect(self.db_analaze)
        self.comboBox_Reductions_Divide_by_monitor_or_time.currentIndexChanged.connect(self.load_SFM_Reflectivity_preview)

        # Triggers: CheckBoxes
        self.checkBox_Reductions_Divide_by_monitor_or_time.stateChanged.connect(self.load_SFM_Reflectivity_preview)
        self.checkBox_Reductions_Normalize_by_DB.stateChanged.connect(self.load_SFM_Reflectivity_preview)
        self.checkBox_Reductions_Attenuator_DB.stateChanged.connect(self.load_SFM_Reflectivity_preview)
        self.checkBox_Reductions_Overillumination_correction.stateChanged.connect(self.load_SFM_Reflectivity_preview)
        self.checkBox_Reductions_Subtract_bkg.stateChanged.connect(self.load_SFM_Reflectivity_preview)
        self.checkBox_SFM_Reflectivity_preview_Show_overillumination.stateChanged.connect(self.load_SFM_Reflectivity_preview)
        self.checkBox_SFM_Reflectivity_preview_Include_errorbars.stateChanged.connect(self.load_SFM_Reflectivity_preview)
        self.checkBox_Rearrange_DB_after.stateChanged.connect(self.load_SFM_Reflectivity_preview)
        self.checkBox_Rearrange_DB_after.stateChanged.connect(self.db_assign)
        self.checkBox_Reductions_Scale_factor.stateChanged.connect(self.load_SFM_Reflectivity_preview)

        # Triggers: Sliders
        self.horizontalSlider_SFM_2Dmap_Highlight.valueChanged.connect(self.draw_2D_map)
        self.horizontalSlider_SFM_2Dmap_Rescale_image_x.valueChanged.connect(self.draw_2D_map)
        self.horizontalSlider_SFM_2Dmap_Rescale_image_y.valueChanged.connect(self.draw_2D_map)

    ##--> menu options
    def menu_info(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowIcon(QtGui.QIcon(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "\icon.png"))
        msgBox.setText("pySAred " + self.action_Version.text() + "\n\n"
                       "Alexey.Klechikov@gmail.com\n\n"
                       "Check new version at https://github.com/Alexey-Klechikov/pySAred/releases")
        msgBox.exec_()

    def menu_algorithm(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowIcon(QtGui.QIcon(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "\icon.png"))
        msgBox.setText("1) Area for background estimation is automatically set to the same size as ROI.\n\n"
                       "2) File can appear in \"Recheck following files in Single File Mode\" if peak of its intensity (around Qz 0.015) is not in the middle of ROI.\n\n"
                       "3) Trapezoid beam form is used for overillumination correction.\n\n"
                       "4) Files are exported as Qz, I, dI, (dQz)\n\n"
                       "5) Button 'Reduce all' will export all Data files with no changes applied in the SFM block. \n\n"
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
                for j in range(0, 3):
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget_Scans.setItem(self.tableWidget_Scans.rowCount()-1, j, item)
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
                for j in range(0, 2):
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget_DB.setItem(self.tableWidget_DB.rowCount()-1, j, item)
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

        self.lineEdit_Save_at.setText(str(saveAt))
        if not str(saveAt)[-1] == "/": self.lineEdit_Save_at.setText(str(saveAt) + "/")

    def button_reduce_all(self):

        self.listWidget_Recheck_files_in_SFM.clear()

        if self.lineEdit_Reductions_Subtract_bkg_Skip.text(): skip_bkg = float(self.lineEdit_Reductions_Subtract_bkg_Skip.text())
        else: skip_bkg = 0

        if self.lineEdit_Save_at.text():  save_file_directory = self.lineEdit_Save_at.text()
        else: save_file_directory = self.current_dir

        if self.checkBox_Reductions_Overillumination_correction.isChecked() and self.lineEdit_Sample_len.text() == "":
            self.statusbar.showMessage("Sample length is missing")
            return
        else:
            sample_len = 999
            if self.lineEdit_Sample_len.text(): sample_len = self.lineEdit_Sample_len.text()

        if self.checkBox_Reductions_Normalize_by_DB.isChecked():
            if self.tableWidget_DB.rowCount() == 0:
                self.label_Error_DB_missing.setVisible(True)
                return

            if self.checkBox_Reductions_Attenuator_DB.isChecked():
                db_atten_factor = 10
                if not self.lineEdit_Reductions_Attenuator_DB.text() == "":
                    db_atten_factor = float(self.lineEdit_Reductions_Attenuator_DB.text())
            else:
                db_atten_factor = 1

        # iterate through table with scans
        for i in range(0, self.tableWidget_Scans.rowCount()):
            file_name = self.tableWidget_Scans.item(i, 2).text()[
                        self.tableWidget_Scans.item(i, 2).text().rfind("/") + 1: -3]

            # find full name DB file if there are several of them
            if self.checkBox_Reductions_Normalize_by_DB.isChecked(): FILE_DB = self.tableWidget_Scans.item(i, 1).text()
            else: FILE_DB = ""

            with h5py.File(self.tableWidget_Scans.item(i, 2).text(), 'r') as FILE:

                INSTRUMENT = FILE[list(FILE.keys())[0]].get("instrument")
                MOTOR_DATA = numpy.array(INSTRUMENT.get('motors').get('data')).T
                SCALERS_DATA = numpy.array(INSTRUMENT.get('scalers').get('data')).T

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

                    original_roi_coord = numpy.array(INSTRUMENT.get('scalers').get('roi').get("roi"))

                    scan_intens = INSTRUMENT.get("detectors").get(str(detector)).get('data')[:,
                                      int(original_roi_coord[0]): int(original_roi_coord[1]), :].sum(axis=1)

                    new_file = open(
                        save_file_directory + file_name + "_" + str(detector) + " (" + FILE_DB + ")" + ".dat", "w")

                    # iterate through th points
                    for index, th in enumerate(th_list):

                        # analize integrated intensity for ROI
                        if len(scan_intens.shape) == 1: Intens = scan_intens[index]
                        elif len(scan_intens.shape) == 2: Intens = sum(scan_intens[index][int(original_roi_coord[2]): int(original_roi_coord[3])])

                        if Intens == 0 and self.checkBox_Export_Remove_zeros.isChecked(): continue

                        if Intens == 0: Intens_err = 1
                        else: Intens_err = numpy.sqrt(Intens)

                        # read motors
                        Qz = (4 * numpy.pi / float(self.lineEdit_Instrument_Wavelength.text())) * numpy.sin(numpy.radians(th))
                        s1hg = s1hg_list[index]
                        s2hg = s2hg_list[index]

                        if self.comboBox_Reductions_Divide_by_monitor_or_time.currentText() == "monitor": monitor = monitor_list[index]
                        elif self.comboBox_Reductions_Divide_by_monitor_or_time.currentText() == "time": monitor = time_list[index]

                        # check if we are not in a middle of ROI in Qz approx 0.02)
                        if round(Qz, 3) > 0.015 and round(Qz, 3) < 0.03 and check_this_file == 0:
                            scan_data_0_015 = scan_intens[index][int(original_roi_coord[2]): int(original_roi_coord[3])]

                            if not max(scan_data_0_015) == max(scan_data_0_015[round((len(scan_data_0_015) / 3)):-round(
                                    (len(scan_data_0_015) / 3))]):
                                self.listWidget_Recheck_files_in_SFM.addItem(file_name)
                                check_this_file = 1

                        coeff = self.overillumination_correct_coeff(s1hg, s2hg, round(th, 4))
                        FWHM_proj = coeff[1]

                        if not self.checkBox_Reductions_Overillumination_correction.isChecked():
                            overill_corr = 1
                        else:
                            overill_corr = coeff[0]

                        # calculate resolution in Sared way or better
                        if self.checkBox_Export_Resolution_like_sared.isChecked():
                            Resolution = numpy.sqrt(((2 * numpy.pi / float(self.lineEdit_Instrument_Wavelength.text())) ** 2) * (
                                    (numpy.cos(numpy.radians(th))) ** 2) * (0.68 ** 2) * ((s1hg ** 2) + (s2hg ** 2)) / (
                                                                (float(
                                                                    self.lineEdit_Instrument_Distance_s1_to_sample.text()) - float(
                                                                    self.lineEdit_Instrument_Distance_s2_to_sample.text())) ** 2) + (
                                                            (float(self.lineEdit_Instrument_Wavelength_resolution.text()) ** 2) * (Qz ** 2)))
                        else:
                            if FWHM_proj == s2hg:
                                Resolution = numpy.sqrt(
                                    ((2 * numpy.pi / float(self.lineEdit_Instrument_Wavelength.text())) ** 2) * (
                                            (numpy.cos(numpy.radians(th))) ** 2) * (0.68 ** 2) * (
                                                (s1hg ** 2) + (s2hg ** 2)) / ((float(
                                        self.lineEdit_Instrument_Distance_s1_to_sample.text()) - float(
                                        self.lineEdit_Instrument_Distance_s2_to_sample.text())) ** 2) + (
                                                (float(self.lineEdit_Instrument_Wavelength_resolution.text()) ** 2) * (Qz ** 2)))
                            else:
                                Resolution = numpy.sqrt(
                                    ((2 * numpy.pi / float(self.lineEdit_Instrument_Wavelength.text())) ** 2) * (
                                            (numpy.cos(numpy.radians(th))) ** 2) * (0.68 ** 2) * (
                                            (s1hg ** 2) + (FWHM_proj ** 2)) / (
                                            float(self.lineEdit_Instrument_Distance_s1_to_sample.text()) ** 2) + (
                                            (float(self.lineEdit_Instrument_Wavelength_resolution.text()) ** 2) * (Qz ** 2)))

                        # I cite Gunnar in here "We are now saving dQ as sigma rather than FWHM for genx"
                        Resolution = Resolution / (2 * numpy.sqrt(2 * numpy.log(2)))

                        # minus background, divide by monitor, overillumination correct + calculate errors
                        if self.checkBox_Reductions_Subtract_bkg.isChecked() and Qz > skip_bkg:
                            Intens_bkg = sum(scan_intens[index][
                                             int(original_roi_coord[2]) - 2 * (int(original_roi_coord[3]) - int(original_roi_coord[2])): int(original_roi_coord[2]) - (
                                                         int(original_roi_coord[3]) - int(original_roi_coord[2]))])

                            if Intens_bkg > 0:
                                Intens_err = numpy.sqrt(Intens + Intens_bkg)
                                Intens = Intens - Intens_bkg

                        if self.checkBox_Reductions_Divide_by_monitor_or_time.isChecked():

                            if self.comboBox_Reductions_Divide_by_monitor_or_time.currentText() == "monitor":
                                monitor = monitor_list[index]
                                if Intens == 0: Intens_err = Intens_err / monitor
                                else: Intens_err = (Intens / monitor) * numpy.sqrt((Intens_err / Intens) ** 2 + (1 / monitor))
                            elif self.comboBox_Reductions_Divide_by_monitor_or_time.currentText() == "time":
                                monitor = time_list[index]
                                Intens_err = Intens_err / monitor

                            Intens = Intens / monitor

                        if self.checkBox_Reductions_Overillumination_correction.isChecked():
                            Intens_err = Intens_err / overill_corr
                            Intens = Intens / overill_corr

                        if self.checkBox_Reductions_Normalize_by_DB.isChecked():
                            try:
                                db_intens = float(
                                    self.DB_INFO[str(FILE_DB) + ";" + str(s1hg) + ";" + str(s2hg)].split(";")[0]) * db_atten_factor
                                db_err = overill_corr * float(
                                    self.DB_INFO[str(FILE_DB) + ";" + str(s1hg) + ";" + str(s2hg)].split(";")[1]) * self.db_atten_factor

                                if Intens == 0: Intens_err += db_err
                                else: Intens_err = (Intens / db_intens) * numpy.sqrt((db_err / db_intens) ** 2 + (Intens_err / Intens) ** 2)

                                Intens = Intens / db_intens
                            except:
                                if check_this_file == 0:
                                    self.listWidget_Recheck_files_in_SFM.addItem(file_name)
                                    check_this_file = 1

                            self.checkBox_Reductions_Scale_factor.setChecked(False)

                        if self.checkBox_Reductions_Scale_factor.isChecked():
                            Intens_err = Intens_err / self.scale_factor
                            Intens = Intens / self.scale_factor

                        # skip the first point
                        if index == 0: continue

                        if Intens == 0 and self.checkBox_Export_Remove_zeros.isChecked(): continue

                        new_file.write(str(Qz) + ' ' + str(Intens) + ' ' + str(Intens_err) + ' ')
                        if self.checkBox_Export_Add_resolution_column.isChecked(): new_file.write(str(Resolution))
                        new_file.write('\n')

                    # close files
                    new_file.close()

                    # check if file is empty - then comment inside
                    if os.stat(save_file_directory + file_name + "_" + str(detector) + " (" + FILE_DB + ")" + ".dat").st_size == 0:
                        with open(save_file_directory + file_name + "_" + str(detector) + " (" + FILE_DB + ")" + ".dat", "w") as empty_file:
                            empty_file.write("All points are either zeros or negatives.")

        self.statusbar.showMessage(str(self.tableWidget_Scans.rowCount()) + " files reduced, " + str(
            self.listWidget_Recheck_files_in_SFM.count()) + " file(s) might need extra care.")

    def button_reduce_sfm(self):

        if self.lineEdit_Save_at.text(): save_file_directory = self.lineEdit_Save_at.text()
        else: save_file_directory = self.current_dir

        # polarisation order - uu, dd, ud, du
        detector = ["uu", "du", "ud", "dd"]

        for i in range(0, len(self.sfm_Export_Qz)):

            if self.checkBox_Reductions_Normalize_by_DB.isChecked():
                sfm_db_file_export = self.SFM_DB_FILE
            else: sfm_db_file_export = ""

            with open(save_file_directory + self.SFM_FILE[self.SFM_FILE.rfind("/") + 1 : -3] + "_" + str(detector[i]) + " (" + sfm_db_file_export + ")" + " SFM.dat", "w") as new_file:
                for j in range(0, len(self.sfm_Export_Qz[i])):
                    if self.sfm_Export_Qz[i][j] == 0: continue
                    if self.sfm_Export_I[i][j] == 0 and self.checkBox_Export_Remove_zeros.isChecked(): continue
                    new_file.write(str(self.sfm_Export_Qz[i][j]) + ' ' + str(self.sfm_Export_I[i][j]) + ' ' + str(self.sfm_Export_dI[i][j]) + ' ')
                    if self.checkBox_Export_Add_resolution_column.isChecked(): new_file.write(str(self.sfm_Export_Resolution[i][j]))
                    new_file.write('\n')

            # close new file
            new_file.close()

        self.statusbar.showMessage(self.SFM_FILE[self.SFM_FILE.rfind("/") + 1:] + " file is reduced in SFM.")

    def button_Clear(self):

        self.comboBox_SFM_Scan.clear()
        self.listWidget_Recheck_files_in_SFM.clear()
        self.graphicsView_SFM_Detector_image.clear()
        self.graphicsView_SFM_2Dmap.clear()
        self.graphicsView_SFM_Reflectivity_preview.getPlotItem().clear()
        self.comboBox_SFM_Detector_image_Point_number.clear()
        self.comboBox_SFM_Detector_image_Polarisation.clear()
        self.comboBox_SFM_2Dmap_Polarisation.clear()
        for i in range(self.tableWidget_Scans.rowCount(), -1, -1):
            self.tableWidget_Scans.removeRow(i)
        for i in range(self.tableWidget_DB.rowCount(), -1, -1):
            self.tableWidget_DB.removeRow(i)
    ##<--

    ##--> extra functions to shorten the code
    def overillumination_correct_coeff(self, s1hg, s2hg, th):

        # Check for Sample Length input
        try:
            sample_len = float(self.lineEdit_Sample_len.text())
        except:
            return [1, s2hg]

        config = str(s1hg) + " " + str(s2hg) + " " + str(th) + " " + str(sample_len)

        # check if we already calculated overillumination for current configuration
        if config in self.overill_coeff_lib:
            coeff = self.overill_coeff_lib[config]
        else:
            coeff = [0, 0]

            # for trapezoid beam - find (half of) widest beam width (OC) and flat region (OB) with max intensity
            if s1hg > s2hg:
                OB = ((float(self.lineEdit_Instrument_Distance_s1_to_sample.text()) * (s2hg - s1hg)) / (2 * (float(self.lineEdit_Instrument_Distance_s1_to_sample.text()) - float(self.lineEdit_Instrument_Distance_s2_to_sample.text())))) + s1hg / 2
                OC = ((float(self.lineEdit_Instrument_Distance_s1_to_sample.text()) * (s2hg + s1hg)) / (2 * (float(self.lineEdit_Instrument_Distance_s1_to_sample.text()) - float(self.lineEdit_Instrument_Distance_s2_to_sample.text())))) - s1hg / 2
            elif s1hg < s2hg:
                OB = ((s2hg * float(self.lineEdit_Instrument_Distance_s1_to_sample.text())) - (s1hg * float(self.lineEdit_Instrument_Distance_s2_to_sample.text()))) / (2 * (float(self.lineEdit_Instrument_Distance_s1_to_sample.text()) - float(self.lineEdit_Instrument_Distance_s2_to_sample.text())))
                OC = (float(self.lineEdit_Instrument_Distance_s1_to_sample.text()) / (float(self.lineEdit_Instrument_Distance_s1_to_sample.text()) - float(self.lineEdit_Instrument_Distance_s2_to_sample.text()))) * (s2hg + s1hg) / 2 - (s1hg / 2)
            elif s1hg == s2hg:
                OB = s1hg / 2
                OC = s1hg * (float(self.lineEdit_Instrument_Distance_s1_to_sample.text()) / (float(self.lineEdit_Instrument_Distance_s1_to_sample.text()) - float(self.lineEdit_Instrument_Distance_s2_to_sample.text())) - 1 / 2)

            BC = OC - OB
            AO = 1 / (OB + OC)  # normalized height of trapezoid

            FWHM_beam = BC/2 + OB # half of the beam FWHM

            sample_len_relative = float(sample_len) * numpy.sin(numpy.radians(numpy.fabs(th)))  # projection of sample surface on the beam

            # "coeff" represents how much of total beam intensity illuminates the sample
            if sample_len_relative / 2 >= OC:
                coeff[0] = 1
            else:  # check if we use only middle part of the beam or trapezoid "shoulders" also
                if sample_len_relative / 2 > OB:
                    coeff[0] = 1 - ((OC - sample_len_relative / 2) * AO)  # 1 - 2 trimmed triangles
                elif sample_len_relative / 2 <= OB:
                    coeff[0] = 1 - (BC * AO) - ((OB - sample_len_relative / 2) * 2 * AO)  # 1 - 2 squares and 2 trimmed triangles

            # for the beam resolution calcultion we check how much of the beam FHWM we cover by the sample
            if sample_len_relative / 2 >= FWHM_beam:
                coeff[1] = s2hg

            else:
                coeff[1] = sample_len_relative

            self.overill_coeff_lib[config] = coeff

        return coeff

    def db_analaze(self):

        self.DB_INFO = {}

        for i in range(0, self.tableWidget_DB.rowCount()):
            with h5py.File(self.tableWidget_DB.item(i,1).text(), 'r') as FILE_DB:
                INSTRUMENT = FILE_DB[list(FILE_DB.keys())[0]].get("instrument")
                MOTOR_DATA = numpy.array(INSTRUMENT.get('motors').get('data')).T
                SCALERS_DATA = numpy.array(INSTRUMENT.get('scalers').get('data')).T

                for index, motor in enumerate(INSTRUMENT.get('motors').get('SPEC_motor_mnemonics')):
                    if "'th'" in str(motor):
                        th_list = MOTOR_DATA[index]
                    elif "'s1hg'" in str(motor):
                        s1hg_list = MOTOR_DATA[index]
                    elif "'s2hg'" in str(motor):
                        s2hg_list = MOTOR_DATA[index]

                for index, scaler in enumerate(INSTRUMENT.get('scalers').get('SPEC_counter_mnemonics')):
                    if "'mon0'" in str(scaler): monitor_list = SCALERS_DATA[index]
                    elif "'roi'" in str(scaler): intens_list = SCALERS_DATA[index]
                    elif "'sec'" in str(scaler): time_list = SCALERS_DATA[index]

                if self.comboBox_Reductions_Divide_by_monitor_or_time.currentText() == "monitor": monitor = monitor_list
                elif self.comboBox_Reductions_Divide_by_monitor_or_time.currentText() == "time": monitor = time_list

                for j in range(0, len(th_list)):
                    db_intens = float(intens_list[j]) / float(monitor[j])
                    db_err = db_intens * numpy.sqrt(1/float(intens_list[j]) + 1/float(monitor[j]))

                    scan_and_slits = self.tableWidget_DB.item(i, 0).text()[:5] + ";" + str(s1hg_list[j]) + ";" + str(s2hg_list[j])

                    self.DB_INFO[scan_and_slits] = str(db_intens) + ";" + str(db_err)

        if self.tableWidget_DB.rowCount() == 0:
            return
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

        self.comboBox_SFM_Detector_image_Point_number.clear()
        self.comboBox_SFM_Detector_image_Polarisation.clear()
        self.comboBox_SFM_2Dmap_Polarisation.clear()

        # we need to find full path for the SFM file from the table
        for i in range(0, self.tableWidget_Scans.rowCount()):
            if self.tableWidget_Scans.item(i, 0).text() == self.comboBox_SFM_Scan.currentText():
                self.SFM_FILE = self.tableWidget_Scans.item(i, 2).text()
                #self.sfm_file_scan_num = int(self.tableWidget_Scans.item(i, 0).text()[:5])

        with h5py.File(self.SFM_FILE, 'r') as FILE:

            SCAN = FILE[list(FILE.keys())[0]]
            original_roi_coord = numpy.array(SCAN.get("instrument").get('scalers').get('roi').get("roi"))
            roi_width = int(original_roi_coord[3]) - int(original_roi_coord[2])

            self.lineEdit_SFM_Detector_image_Roi_X_Left.setText(str(original_roi_coord[2])[:-2])
            self.lineEdit_SFM_Detector_image_Roi_X_Right.setText(str(original_roi_coord[3])[:-2])
            self.lineEdit_SFM_Detector_image_Roi_Y_Bottom.setText(str(original_roi_coord[1])[:-2])
            self.lineEdit_SFM_Detector_image_Roi_Y_Top.setText(str(original_roi_coord[0])[:-2])
            self.lineEdit_SFM_Detector_image_Roi_bkg_X_Left.setText(str(int(original_roi_coord[2]) - 2 * roi_width))
            self.lineEdit_SFM_Detector_image_Roi_bkg_X_Right.setText(str(int(original_roi_coord[2]) - roi_width))
            self.lineEdit_SFM_Detector_image_Roi_bkg_Y_Bottom.setText(str(original_roi_coord[1])[:-2])
            self.lineEdit_SFM_Detector_image_Roi_bkg_Y_Top.setText(str(original_roi_coord[0])[:-2])

            for index, th in enumerate(SCAN.get("instrument").get('motors').get('th').get("value")):
                if str(th)[0:5] in ("-0.00", "0.00"): continue

                self.comboBox_SFM_Detector_image_Point_number.addItem(str(round(th, 3)))

            if len(SCAN.get("ponos").get('data')) == 1:
                self.comboBox_SFM_Detector_image_Polarisation.addItem("uu")
                self.comboBox_SFM_2Dmap_Polarisation.addItem("uu")
            for polarisation in SCAN.get("ponos").get('data'):
                if polarisation not in ("data_du", "data_uu", "data_dd", "data_ud"): continue
                if numpy.any(numpy.array(SCAN.get("ponos").get('data').get(polarisation))):
                    self.comboBox_SFM_Detector_image_Polarisation.addItem(str(polarisation)[-2:])
                    self.comboBox_SFM_2Dmap_Polarisation.addItem(str(polarisation)[-2:])

            self.comboBox_SFM_Detector_image_Polarisation.setCurrentIndex(0)
            self.comboBox_SFM_2Dmap_Polarisation.setCurrentIndex(0)

    def draw_det_image(self):

        if self.comboBox_SFM_Detector_image_Polarisation.currentText() == "" or self.comboBox_SFM_Detector_image_Point_number.currentText() == "": return

        self.graphicsView_SFM_Detector_image.clear()
        self.graphicsView_SFM_Detector_image_Roi.clear()

        if self.SFM_FILE == "": return
        with h5py.File(self.SFM_FILE, 'r') as FILE:

            self.current_th = self.comboBox_SFM_Detector_image_Point_number.currentText()

            INSTRUMENT = FILE[list(FILE.keys())[0]].get("instrument")
            MOTOR_DATA = numpy.array(INSTRUMENT.get('motors').get('data')).T
            SCALERS_DATA = numpy.array(INSTRUMENT.get('scalers').get('data')).T

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

                if i == "psd": scan_psd = "psd"
                else: scan_psd = "psd_" + self.comboBox_SFM_Detector_image_Polarisation.currentText()

            detector_images = INSTRUMENT.get('detectors').get(scan_psd).get('data')

            for index, th in enumerate(self.th_list):
                # check th
                if self.current_th == str(round(th, 3)):
                    self.lineEdit_SFM_Detector_image_Slits_s1hg.setText(str(self.s1hg_list[index]))
                    self.lineEdit_SFM_Detector_image_Slits_s2hg.setText(str(self.s2hg_list[index]))
                    self.lineEdit_SFM_Detector_image_Time.setText(str(time_list[index]))

                    # seems to be a bug in numpy arrays imported from hdf5 files. Problem is solved after I subtract ZEROs array with the same dimentions.
                    detector_image = detector_images[index]
                    detector_image = numpy.around(detector_image, decimals=0).astype(int)
                    detector_image = numpy.subtract(detector_image, numpy.zeros((detector_image.shape[0], detector_image.shape[1])))
                    # integrate detector image with respect to ROI Y coordinates
                    detector_image_int = detector_image[int(self.lineEdit_SFM_Detector_image_Roi_Y_Top.text()): int(self.lineEdit_SFM_Detector_image_Roi_Y_Bottom.text()), :].sum(axis=0).astype(int)

                    self.graphicsView_SFM_Detector_image.setImage(detector_image, axes={'x':1, 'y':0}, levels=(0,0.1))
                    self.graphicsView_SFM_Detector_image_Roi.addItem(pg.PlotCurveItem(y = detector_image_int, pen=pg.mkPen(color=(0, 0, 0), width=2), brush=pg.mkBrush(color=(255, 0, 0), width=3)))

                    if self.comboBox_SFM_Detector_image_Color_scheme.currentText() == "White / Black":
                        self.color_det_image = numpy.array([[0, 0, 0, 255], [255, 255, 255, 255], [255, 255, 255, 255]],
                                                        dtype=numpy.ubyte)
                    elif self.comboBox_SFM_Detector_image_Color_scheme.currentText() == "Green / Blue":
                        self.color_det_image = numpy.array([[0, 0, 255, 255], [255, 0, 0, 255], [0, 255, 0, 255]],
                                                           dtype=numpy.ubyte)
                    pos = numpy.array([0.0, 0.1, 1.0])

                    colmap = pg.ColorMap(pos, self.color_det_image)
                    self.graphicsView_SFM_Detector_image.setColorMap(colmap)

                    # add ROI rectangular
                    spots_ROI_det_int = []
                    if self.draw_roi:
                        self.graphicsView_SFM_Detector_image.removeItem(self.draw_roi)

                    # add ROI rectangular
                    spots_ROI_det_view = {'x': (int(self.lineEdit_SFM_Detector_image_Roi_X_Left.text()), int(self.lineEdit_SFM_Detector_image_Roi_X_Right.text()), int(self.lineEdit_SFM_Detector_image_Roi_X_Right.text()), int(self.lineEdit_SFM_Detector_image_Roi_X_Left.text()), int(self.lineEdit_SFM_Detector_image_Roi_X_Left.text())),
                                 'y': (int(self.lineEdit_SFM_Detector_image_Roi_Y_Top.text()), int(self.lineEdit_SFM_Detector_image_Roi_Y_Top.text()), int(self.lineEdit_SFM_Detector_image_Roi_Y_Bottom.text()), int(self.lineEdit_SFM_Detector_image_Roi_Y_Bottom.text()), int(self.lineEdit_SFM_Detector_image_Roi_Y_Top.text()))}

                    self.draw_roi = pg.PlotDataItem(spots_ROI_det_view, pen=pg.mkPen(255, 255, 255), connect="all")
                    self.graphicsView_SFM_Detector_image.addItem(self.draw_roi)

                    if self.draw_roi_int:
                        self.graphicsView_SFM_Detector_image_Roi.removeItem(self.draw_roi_int)

                    for i in range(0, detector_image_int.max()):
                        spots_ROI_det_int.append({'x': int(self.lineEdit_SFM_Detector_image_Roi_X_Left.text()), 'y': i})
                        spots_ROI_det_int.append({'x': int(self.lineEdit_SFM_Detector_image_Roi_X_Right.text()), 'y': i})

                    self.draw_roi_int = pg.ScatterPlotItem(spots=spots_ROI_det_int, size=1, pen=pg.mkPen(255, 0, 0))
                    self.graphicsView_SFM_Detector_image_Roi.addItem(self.draw_roi_int)

                    break

        # Show "integrated roi" part
        if self.sender().objectName() == "pushButton_SFM_Detector_image_Show_integrated_roi":

            if self.show_det_int_trigger:
                self.graphicsView_SFM_Detector_image.setGeometry(QtCore.QRect(0, 30, 577, 420))
                self.show_det_int_trigger = False
            else:
                self.graphicsView_SFM_Detector_image.setGeometry(QtCore.QRect(0, 30, 577, 510))
                self.show_det_int_trigger = True

    def load_SFM_Reflectivity_preview(self):

        self.graphicsView_SFM_Reflectivity_preview.getPlotItem().clear()
        skip_bkg = 0

        self.sfm_Export_Qz = []
        self.sfm_Export_I = []
        self.sfm_Export_dI = []
        self.sfm_Export_Resolution = []

        # change interface (Scale factor, DB correction, DB attenuator)
        if self.checkBox_Reductions_Normalize_by_DB.isChecked():
            self.checkBox_Reductions_Attenuator_DB.setHidden(False)
            self.lineEdit_Reductions_Attenuator_DB.setHidden(False)
            self.checkBox_Reductions_Scale_factor.setHidden(True)
            self.lineEdit_Reductions_Scale_factor.setHidden(True)
            self.checkBox_Reductions_Scale_factor.setChecked(False)
        else:
            self.checkBox_Reductions_Attenuator_DB.setHidden(True)
            self.lineEdit_Reductions_Attenuator_DB.setHidden(True)
            self.checkBox_Reductions_Scale_factor.setHidden(False)
            self.lineEdit_Reductions_Scale_factor.setHidden(False)

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

        if self.checkBox_Reductions_Scale_factor.isChecked():
            self.scale_factor = 10
            if not self.lineEdit_Reductions_Scale_factor.text() == "":
                self.scale_factor = float(self.lineEdit_Reductions_Scale_factor.text())
        else: self.scale_factor = 1

        if self.checkBox_Reductions_Attenuator_DB.isChecked():
            self.db_atten_factor = 10
            if not self.lineEdit_Reductions_Attenuator_DB.text() == "":
                self.db_atten_factor = float(self.lineEdit_Reductions_Attenuator_DB.text())
        else: self.db_atten_factor = 1

        if self.lineEdit_Reductions_Subtract_bkg_Skip.text(): skip_bkg = float(self.lineEdit_Reductions_Subtract_bkg_Skip.text())

        for i in range(0, self.tableWidget_Scans.rowCount()):
            if self.tableWidget_Scans.item(i, 0).text() == self.comboBox_SFM_Scan.currentText():
                self.SFM_FILE = self.tableWidget_Scans.item(i, 2).text()
                self.SFM_DB_FILE = self.tableWidget_Scans.item(i, 1).text()

        with h5py.File(self.SFM_FILE, 'r') as FILE:

            INSTRUMENT = FILE[list(FILE.keys())[0]].get("instrument")
            PONOS = FILE[list(FILE.keys())[0]].get("ponos")
            MOTOR_DATA = numpy.array(INSTRUMENT.get('motors').get('data')).T
            SCALERS_DATA = numpy.array(INSTRUMENT.get('scalers').get('data')).T

            roi_coord_Y = [int(self.lineEdit_SFM_Detector_image_Roi_Y_Top.text()), int(self.lineEdit_SFM_Detector_image_Roi_Y_Bottom.text())]
            roi_coord_X = [int(self.lineEdit_SFM_Detector_image_Roi_X_Left.text()), int(self.lineEdit_SFM_Detector_image_Roi_X_Right.text())]
            roi_coord_X_BKG = [int(self.lineEdit_SFM_Detector_image_Roi_bkg_X_Left.text()), int(self.lineEdit_SFM_Detector_image_Roi_bkg_X_Right.text())]

            if not roi_coord_Y == self.old_roi_coord_Y:
                self.sfm_file_already_analized = ""

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
                if not self.SFM_FILE == self.sfm_file_already_analized:
                    if "pnr" in list(FILE[list(FILE.keys())[0]]):
                        if str(scan) == "data_du": self.psd_du_sfm = INSTRUMENT.get("detectors").get("psd_du").get('data')[:, int(roi_coord_Y[0]): int(roi_coord_Y[1]), :].sum(axis=1)
                        elif str(scan) == "data_uu": self.psd_uu_sfm = INSTRUMENT.get("detectors").get("psd_uu").get('data')[:, int(roi_coord_Y[0]): int(roi_coord_Y[1]), :].sum(axis=1)
                        elif str(scan) == "data_ud": self.psd_ud_sfm = INSTRUMENT.get("detectors").get("psd_ud").get('data')[:, int(roi_coord_Y[0]): int(roi_coord_Y[1]), :].sum(axis=1)
                        elif str(scan) == "data_dd": self.psd_dd_sfm = INSTRUMENT.get("detectors").get("psd_dd").get('data')[:, int(roi_coord_Y[0]): int(roi_coord_Y[1]), :].sum(axis=1)
                    else: self.psd_uu_sfm = INSTRUMENT.get("detectors").get("psd").get('data')[:, int(roi_coord_Y[0]) : int(roi_coord_Y[1]), :].sum(axis=1)

            self.sfm_file_already_analized = self.SFM_FILE

            for color_index, scan_intens_sfm in enumerate([self.psd_uu_sfm, self.psd_du_sfm, self.psd_ud_sfm, self.psd_dd_sfm]):

                sfm_Export_Qz_one_pol = []
                sfm_Export_I_one_pol = []
                sfm_Export_dI_one_pol = []
                sfm_Export_Resolution_one_pol = []

                plot_I = []
                plot_angle = []
                plot_dI_err_bottom = []
                plot_dI_err_top = []
                plot_overillumination = []

                if scan_intens_sfm == []: continue

                if color_index == 0: # ++
                    color = [0, 0, 0]
                    monitor_data = [monitor_list if numpy.count_nonzero(monitor_uu_list) == 0 else monitor_uu_list][0]
                elif color_index == 1: # -+
                    color = [0, 0, 255]
                    monitor_data = monitor_du_list
                elif color_index == 2: # --
                    color = [0, 255, 0]
                    monitor_data = monitor_ud_list
                elif color_index == 3: # --
                    color = [255, 0, 0]
                    monitor_data = monitor_dd_list

                for index, th in enumerate(self.th_list):

                    try: # Full offset. If "text" cant be converted to "float" - ignore the field
                        th = th - float(self.lineEdit_Instrument_Offset_full.text())
                    except:
                        th = th

                    # read motors
                    Qz = (4 * numpy.pi / float(self.lineEdit_Instrument_Wavelength.text())) * numpy.sin(numpy.radians(th))
                    s1hg = self.s1hg_list[index]
                    s2hg = self.s2hg_list[index]
                    monitor = monitor_data[index]

                    if not self.checkBox_Reductions_Overillumination_correction.isChecked():
                        overill_corr = 1
                        overill_corr_plot = self.overillumination_correct_coeff(s1hg, s2hg, round(th, 4))[0]
                    else:
                        overill_corr, FWHM_proj = self.overillumination_correct_coeff(s1hg, s2hg, round(th, 4))
                        overill_corr_plot = overill_corr

                    # calculate resolution in Sared way or better
                    if self.checkBox_Export_Resolution_like_sared.isChecked():
                        Resolution = numpy.sqrt(((2 * numpy.pi / float(self.lineEdit_Instrument_Wavelength.text())) ** 2) * (
                                (numpy.cos(numpy.radians(th))) ** 2) * (0.68 ** 2) * ((s1hg ** 2) + (s2hg ** 2)) / (
                                                        (float(
                                                            self.lineEdit_Instrument_Distance_s1_to_sample.text()) - float(
                                                            self.lineEdit_Instrument_Distance_s2_to_sample.text())) ** 2) + (
                                                        (float(self.lineEdit_Instrument_Wavelength_resolution.text()) ** 2) * (Qz ** 2)))
                    else:
                        if FWHM_proj == s2hg:
                            Resolution = numpy.sqrt(
                                ((2 * numpy.pi / float(self.lineEdit_Instrument_Wavelength.text())) ** 2) * (
                                        (numpy.cos(numpy.radians(th))) ** 2) * (0.68 ** 2) * (
                                        (s1hg ** 2) + (s2hg ** 2)) / ((float(
                                    self.lineEdit_Instrument_Distance_s1_to_sample.text()) - float(
                                    self.lineEdit_Instrument_Distance_s2_to_sample.text())) ** 2) + (
                                        (float(self.lineEdit_Instrument_Wavelength_resolution.text()) ** 2) * (Qz ** 2)))
                        else:
                            Resolution = numpy.sqrt(
                                ((2 * numpy.pi / float(self.lineEdit_Instrument_Wavelength.text())) ** 2) * (
                                        (numpy.cos(numpy.radians(th))) ** 2) * (0.68 ** 2) * (
                                        (s1hg ** 2) + (FWHM_proj ** 2)) / (
                                        float(self.lineEdit_Instrument_Distance_s1_to_sample.text()) ** 2) + (
                                        (float(self.lineEdit_Instrument_Wavelength_resolution.text()) ** 2) * (Qz ** 2)))

                    # I cite Gunnar in here "We are now saving dQ as sigma rather than FWHM for genx"
                    Resolution = Resolution / (2 * numpy.sqrt(2 * numpy.log(2)))

                    # analize integrated intensity for ROI
                    Intens = sum(scan_intens_sfm[index][roi_coord_X[0]: roi_coord_X[1]])
                    Intens_bkg = sum(scan_intens_sfm[index][roi_coord_X_BKG[0] : roi_coord_X_BKG[1]])

                    # minus background, divide by monitor, overillumination correct + calculate errors
                    if not Intens > 0: Intens = 0
                    # I want to avoid error==0 if intens==0
                    if Intens == 0: Intens_err = 1
                    else: Intens_err = numpy.sqrt(Intens)

                    if self.checkBox_Reductions_Subtract_bkg.isChecked() and Qz > skip_bkg:
                        if Intens_bkg > 0:
                            Intens_err = numpy.sqrt(Intens + Intens_bkg)
                            Intens = Intens - Intens_bkg

                    if self.checkBox_Reductions_Divide_by_monitor_or_time.isChecked():

                        if self.comboBox_Reductions_Divide_by_monitor_or_time.currentText() == "monitor":
                            monitor = monitor_list[index]
                            if Intens == 0: Intens_err = Intens_err / monitor
                            else: Intens_err = (Intens / monitor) * numpy.sqrt((Intens_err / Intens) ** 2 + (1 / monitor))
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
                            Intens_err = (Intens / db_intens) * numpy.sqrt((db_err / db_intens) ** 2 + (Intens_err / Intens) ** 2)
                            Intens = Intens / db_intens
                            self.label_Error_DB_wrong.setVisible(False)
                        except:
                            # if we try DB file without neccesary slits combination measured - show error message + redraw reflectivity_preview
                            self.label_Error_DB_wrong.setVisible(True)
                            self.label_Error_DB_wrong.setText("Choose another DB file \n for this SFM data file.")
                            self.checkBox_Reductions_Normalize_by_DB.setCheckState(0)

                    if self.checkBox_Reductions_Scale_factor.isChecked():
                        Intens_err = Intens_err / self.scale_factor
                        Intens = Intens / self.scale_factor

                    try:
                        show_first = int(self.lineEdit_SFM_Reflectivity_preview_Skip_points_Left.text())
                        show_last = len(self.th_list) - int(self.lineEdit_SFM_Reflectivity_preview_Skip_points_Right.text())
                    except:
                        show_first = 0
                        show_last = len(self.th_list)

                    if not Intens < 0 and index < show_last and index > show_first:
                        # I need this for "Reduce SFM" option. First - store one pol.
                        sfm_Export_Qz_one_pol.append(Qz)
                        sfm_Export_I_one_pol.append(Intens)
                        sfm_Export_dI_one_pol.append(Intens_err)
                        sfm_Export_Resolution_one_pol.append(Resolution)

                        if Intens > 0:
                            plot_I.append(numpy.log10(Intens))
                            plot_angle.append(Qz)
                            plot_dI_err_top.append(abs(numpy.log10(Intens + Intens_err) - numpy.log10(Intens)))

                            plot_overillumination.append(overill_corr_plot)

                            if Intens > Intens_err: plot_dI_err_bottom.append(numpy.log10(Intens) - numpy.log10(Intens - Intens_err))
                            else: plot_dI_err_bottom.append(0)

                        if self.comboBox_SFM_Reflectivity_preview_Plot_axis.currentText() in ("Reflectivity (lin) vs Angle (Qz)", "Reflectivity (lin) vs Angle (deg)"):
                            plot_I.pop()
                            plot_I.append(Intens)
                            plot_dI_err_top.pop()
                            plot_dI_err_top.append(Intens_err)
                            plot_dI_err_bottom.pop()
                            plot_dI_err_bottom.append(Intens_err)

                        if self.comboBox_SFM_Reflectivity_preview_Plot_axis.currentText() in ("Reflectivity (lin) vs Angle (deg)", "Reflectivity (log) vs Angle (deg)"):
                            plot_angle.pop()
                            plot_angle.append(th)

                # I need this for "Reduse SFM" option. Second - combine all shown pol in one list variable.
                # polarisations are uu, dd, ud, du
                self.sfm_Export_Qz.append(sfm_Export_Qz_one_pol)
                self.sfm_Export_I.append(sfm_Export_I_one_pol)
                self.sfm_Export_dI.append(sfm_Export_dI_one_pol)
                self.sfm_Export_Resolution.append(sfm_Export_Resolution_one_pol)

                if self.checkBox_SFM_Reflectivity_preview_Include_errorbars.isChecked():
                    s1 = pg.ErrorBarItem(x=numpy.array(plot_angle), y=numpy.array(plot_I), top=numpy.array(plot_dI_err_top), bottom=numpy.array(plot_dI_err_bottom), pen=pg.mkPen(color[0], color[1], color[2]), brush=pg.mkBrush(color[0], color[1], color[2]))
                    self.graphicsView_SFM_Reflectivity_preview.addItem(s1)

                s2 = pg.ScatterPlotItem(x=plot_angle, y=plot_I, symbol="o", size=4, pen=pg.mkPen(color[0], color[1], color[2]), brush=pg.mkBrush(color[0], color[1], color[2]))
                self.graphicsView_SFM_Reflectivity_preview.addItem(s2)

                if self.checkBox_SFM_Reflectivity_preview_Show_overillumination.isChecked():
                    s3 = pg.PlotCurveItem(x=plot_angle, y=plot_overillumination,
                                            pen=pg.mkPen(color=(255, 0, 0), width=1),
                                            brush=pg.mkBrush(color=(255, 0, 0), width=1) )
                    self.graphicsView_SFM_Reflectivity_preview.addItem(s3)

    def draw_2D_map(self):

        self.int_SFM_Detector_image = []

        self.graphicsView_SFM_2Dmap_Qxz_Theta.clear()
        self.graphicsView_SFM_2Dmap.clear()

        # change interface if for different views
        if self.comboBox_SFM_2Dmap_Axes.currentText() == "Pixel vs. Point":
            self.graphicsView_SFM_2Dmap_Qxz_Theta.setGeometry(QtCore.QRect(0, 0, 0, 0))
            self.label_SFM_2Dmap_Highlight.setVisible(True)
            self.horizontalSlider_SFM_2Dmap_Highlight.setVisible(True)
            self.label_SFM_2Dmap_Rescale_image_x.setVisible(True)
            self.label_SFM_2Dmap_Rescale_image_y.setVisible(True)
            self.horizontalSlider_SFM_2Dmap_Rescale_image_x.setVisible(True)
            self.horizontalSlider_SFM_2Dmap_Rescale_image_y.setVisible(True)
            self.label_SFM_2Dmap_Qxz_Lower_number_of_points_by.setVisible(False)
            self.comboBox_SFM_2Dmap_Qxz_Lower_number_of_points_by.setVisible(False)
            self.label_SFM_2Dmap_Qxz_Threshold.setVisible(False)
            self.comboBox_SFM_2Dmap_Qxz_Threshold.setVisible(False)
        elif self.comboBox_SFM_2Dmap_Axes.currentText() == "Qx vs. Qz":
            self.graphicsView_SFM_2Dmap_Qxz_Theta.setGeometry(QtCore.QRect(0, 30, 577, 520))
            self.label_SFM_2Dmap_Qxz_Lower_number_of_points_by.setVisible(True)
            self.comboBox_SFM_2Dmap_Qxz_Lower_number_of_points_by.setVisible(True)
            self.label_SFM_2Dmap_Qxz_Threshold.setVisible(True)
            self.comboBox_SFM_2Dmap_Qxz_Threshold.setVisible(True)
            self.label_SFM_2Dmap_Rescale_image_x.setVisible(False)
            self.label_SFM_2Dmap_Rescale_image_y.setVisible(False)
            self.horizontalSlider_SFM_2Dmap_Rescale_image_x.setVisible(False)
            self.horizontalSlider_SFM_2Dmap_Rescale_image_y.setVisible(False)
            self.label_SFM_2Dmap_Highlight.setVisible(False)
            self.horizontalSlider_SFM_2Dmap_Highlight.setVisible(False)
        elif self.comboBox_SFM_2Dmap_Axes.currentText() == "Alpha_i vs. Alpha_f":
            self.graphicsView_SFM_2Dmap_Qxz_Theta.setGeometry(QtCore.QRect(0, 0, 0, 0))
            self.label_SFM_2Dmap_Highlight.setVisible(True)
            self.horizontalSlider_SFM_2Dmap_Highlight.setVisible(True)
            self.label_SFM_2Dmap_Rescale_image_x.setVisible(False)
            self.label_SFM_2Dmap_Rescale_image_y.setVisible(False)
            self.horizontalSlider_SFM_2Dmap_Rescale_image_x.setVisible(False)
            self.horizontalSlider_SFM_2Dmap_Rescale_image_y.setVisible(False)
            self.label_SFM_2Dmap_Qxz_Lower_number_of_points_by.setVisible(False)
            self.comboBox_SFM_2Dmap_Qxz_Lower_number_of_points_by.setVisible(False)
            self.label_SFM_2Dmap_Qxz_Threshold.setVisible(False)
            self.comboBox_SFM_2Dmap_Qxz_Threshold.setVisible(False)


        if self.SFM_FILE == "": return

        # start over if we selected nes SFM scan
        if not self.sfm_file_2d_calculated_params == [] and not self.sfm_file_2d_calculated_params[0] == self.SFM_FILE:
            self.comboBox_SFM_2Dmap_Axes.setCurrentIndex(0)
            self.sfm_file_2d_calculated_params = []
            self.res_Aif = []

        try:
            self.graphicsView_SFM_2Dmap.removeItem(self.draw_roi_2D_map)
        except: 1

        # load selected integrated detector image
        if self.comboBox_SFM_2Dmap_Polarisation.count() == 1:
            self.int_SFM_Detector_image = self.psd_uu_sfm
        else:
            if self.comboBox_SFM_2Dmap_Polarisation.currentText() == "uu":
                self.int_SFM_Detector_image = self.psd_uu_sfm
            elif self.comboBox_SFM_2Dmap_Polarisation.currentText() == "du":
                self.int_SFM_Detector_image = self.psd_du_sfm
            elif self.comboBox_SFM_2Dmap_Polarisation.currentText() == "ud":
                self.int_SFM_Detector_image = self.psd_ud_sfm
            elif self.comboBox_SFM_2Dmap_Polarisation.currentText() == "dd":
                self.int_SFM_Detector_image = self.psd_dd_sfm

        if self.int_SFM_Detector_image == []: return

        # Pixel to Angle conversion for "Qx vs Qz" and "alpha_i vs alpha_f" 2d maps
        if self.comboBox_SFM_2Dmap_Axes.currentText() in ["Qx vs. Qz", "Alpha_i vs. Alpha_f"]:
            # recalculate only if something was changed
            if self.res_Aif == [] or not self.sfm_file_2d_calculated_params == [self.SFM_FILE, self.comboBox_SFM_2Dmap_Polarisation.currentText(),
                                              self.lineEdit_SFM_Detector_image_Roi_X_Left.text(), self.lineEdit_SFM_Detector_image_Roi_X_Right.text(),
                                              self.lineEdit_Instrument_Wavelength.text(), self.lineEdit_Instrument_Distance_sample_to_detector.text(),
                                              self.comboBox_SFM_2Dmap_Qxz_Lower_number_of_points_by.currentText(), self.comboBox_SFM_2Dmap_Qxz_Threshold.currentText()]:
                self.spots_Qxz = []
                self.int_SFM_Detector_image_Qxz = []
                self.int_SFM_Detector_image_Aif = [[],[]]
                self.int_SFM_Detector_image_values_array = []

                roi_middle = round((self.int_SFM_Detector_image.shape[1] - float(self.lineEdit_SFM_Detector_image_Roi_X_Left.text()) +
                                    self.int_SFM_Detector_image.shape[1] - float(self.lineEdit_SFM_Detector_image_Roi_X_Right.text())) / 2)
                mm_per_pix = 300 / self.int_SFM_Detector_image.shape[1]

                # we need to flip the detector (X) for correct calculation
                for theta_i, tth_i, det_image_i in zip(self.th_list, self.tth_list, numpy.flip(self.int_SFM_Detector_image, 1)):
                    for pixel_num, value in enumerate(det_image_i):
                        # Reduce number of points to draw (to save RAM)
                        if pixel_num % int(self.comboBox_SFM_2Dmap_Qxz_Lower_number_of_points_by.currentText()) == 0:
                            # theta F in deg
                            theta_f = tth_i - theta_i
                            # calculate delta theta F in deg
                            delta_theta_F_mm = (pixel_num - roi_middle) * mm_per_pix
                            delta_theta_F_deg = numpy.degrees(
                                numpy.arctan(delta_theta_F_mm / float(self.lineEdit_Instrument_Distance_sample_to_detector.text())))
                            # final theta F in deg for the point
                            theta_f += delta_theta_F_deg
                            # convert to Q
                            Qx = (2 * numpy.pi / float(self.lineEdit_Instrument_Wavelength.text())) * (
                                        numpy.cos(numpy.radians(theta_f)) - numpy.cos(numpy.radians(theta_i)))
                            Qz = (2 * numpy.pi / float(self.lineEdit_Instrument_Wavelength.text())) * (
                                        numpy.sin(numpy.radians(theta_f)) + numpy.sin(numpy.radians(theta_i)))

                            self.int_SFM_Detector_image_Qxz.append([Qx, Qz, value])

                            self.int_SFM_Detector_image_Aif[0].append(theta_i)
                            self.int_SFM_Detector_image_Aif[1].append(theta_f)
                            self.int_SFM_Detector_image_values_array.append(value)

                            # define colors - 2 count+ -> green, [0,1] - blue
                            if value < int(self.comboBox_SFM_2Dmap_Qxz_Threshold.currentText()): color = [0, 0, 255]
                            else: color = [0, 255, 0]

                            self.spots_Qxz.append({'pos': (-Qx, Qz), 'pen': pg.mkPen(color[0], color[1], color[2])})

                if self.comboBox_SFM_2Dmap_Axes.currentText() == "Alpha_i vs. Alpha_f":
                    # calculate required number of pixels in Y axis
                    self.resolution_x_pix_deg = self.int_SFM_Detector_image.shape[0] / (max(self.int_SFM_Detector_image_Aif[0]) - min(self.int_SFM_Detector_image_Aif[0]))
                    self.resolution_y_pix = int(round((max(self.int_SFM_Detector_image_Aif[1]) - min(self.int_SFM_Detector_image_Aif[1])) * self.resolution_x_pix_deg))

                    grid_x, grid_y = numpy.mgrid[min(self.int_SFM_Detector_image_Aif[0]):max(self.int_SFM_Detector_image_Aif[0]):((max(self.int_SFM_Detector_image_Aif[0]) - min(self.int_SFM_Detector_image_Aif[0]))/len(self.th_list)), min(self.int_SFM_Detector_image_Aif[1]):max(self.int_SFM_Detector_image_Aif[1]):(max(self.int_SFM_Detector_image_Aif[1]) - min(self.int_SFM_Detector_image_Aif[1]))/self.resolution_y_pix]
                    self.res_Aif = griddata((self.int_SFM_Detector_image_Aif[0], self.int_SFM_Detector_image_Aif[1]), self.int_SFM_Detector_image_values_array, (grid_x, grid_y), method="linear", fill_value=float(0))

                # record params that we used for 2D maps calculation
                self.sfm_file_2d_calculated_params = [self.SFM_FILE, self.comboBox_SFM_2Dmap_Polarisation.currentText(),
                                                      self.lineEdit_SFM_Detector_image_Roi_X_Left.text(), self.lineEdit_SFM_Detector_image_Roi_X_Right.text(),
                                                      self.lineEdit_Instrument_Wavelength.text(), self.lineEdit_Instrument_Distance_sample_to_detector.text(),
                                                      self.comboBox_SFM_2Dmap_Qxz_Lower_number_of_points_by.currentText(), self.comboBox_SFM_2Dmap_Qxz_Threshold.currentText()]

        # plot
        if self.comboBox_SFM_2Dmap_Axes.currentText() == "Pixel vs. Point":
            self.graphicsView_SFM_2Dmap.setImage(self.int_SFM_Detector_image, axes={'x': 1, 'y': 0}, levels=(0, 0.1),
                                           scale=(int(self.horizontalSlider_SFM_2Dmap_Rescale_image_x.value()), int(self.horizontalSlider_SFM_2Dmap_Rescale_image_y.value())))
            # add ROI rectangular
            spots_ROI = {'x':(int(self.lineEdit_SFM_Detector_image_Roi_X_Left.text()) * int(self.horizontalSlider_SFM_2Dmap_Rescale_image_x.value()), int(self.lineEdit_SFM_Detector_image_Roi_X_Right.text()) * int(self.horizontalSlider_SFM_2Dmap_Rescale_image_x.value()), int(self.lineEdit_SFM_Detector_image_Roi_X_Right.text()) * int(self.horizontalSlider_SFM_2Dmap_Rescale_image_x.value()), int(self.lineEdit_SFM_Detector_image_Roi_X_Left.text()) * int(self.horizontalSlider_SFM_2Dmap_Rescale_image_x.value()), int(self.lineEdit_SFM_Detector_image_Roi_X_Left.text()) * int(self.horizontalSlider_SFM_2Dmap_Rescale_image_x.value())), 'y':(0,0,self.int_SFM_Detector_image.shape[0] * int(self.horizontalSlider_SFM_2Dmap_Rescale_image_y.value()),self.int_SFM_Detector_image.shape[0] * int(self.horizontalSlider_SFM_2Dmap_Rescale_image_y.value()),0)}

            self.draw_roi_2D_map = pg.PlotDataItem(spots_ROI, pen=pg.mkPen(255, 255, 255), connect="all")
            self.graphicsView_SFM_2Dmap.addItem(self.draw_roi_2D_map)

        elif self.comboBox_SFM_2Dmap_Axes.currentText() == "Alpha_i vs. Alpha_f":
            self.graphicsView_SFM_2Dmap.setImage(self.res_Aif, axes={'x': 0, 'y': 1}, levels=(0, 0.1))
            self.graphicsView_SFM_2Dmap.getImageItem().setRect(QtCore.QRectF(min(self.int_SFM_Detector_image_Aif[0]), min(self.int_SFM_Detector_image_Aif[1]), abs(min(self.int_SFM_Detector_image_Aif[0])) + abs(max(self.int_SFM_Detector_image_Aif[0])), abs(min(self.int_SFM_Detector_image_Aif[1])) + abs(max(self.int_SFM_Detector_image_Aif[1]))))
            self.graphicsView_SFM_2Dmap.getView().enableAutoScale()

        elif self.comboBox_SFM_2Dmap_Axes.currentText() == "Qx vs. Qz":
            s0 = pg.ScatterPlotItem(spots=self.spots_Qxz, size=1)
            self.graphicsView_SFM_2Dmap_Qxz_Theta.addItem(s0)

        self.graphicsView_SFM_2Dmap.ui.histogram.setHistogramRange(0, self.horizontalSlider_SFM_2Dmap_Highlight.value())
        self.graphicsView_SFM_2Dmap.ui.histogram.setLevels(0, self.horizontalSlider_SFM_2Dmap_Highlight.value())

    def export_2d_map(self):
        if self.lineEdit_Save_at.text(): save_file_directory = self.lineEdit_Save_at.text()
        else: save_file_directory = self.current_dir

        if self.comboBox_SFM_2Dmap_Axes.currentText() == "Pixel vs. Point":
            with open(save_file_directory + self.SFM_FILE[self.SFM_FILE.rfind("/") + 1 : -3] + "_" + self.comboBox_SFM_2Dmap_Polarisation.currentText() + " 2D_map(Pixel vs. Point).dat", "w") as new_file_2d_map:
                for line in self.int_SFM_Detector_image:
                    for row in line:
                        new_file_2d_map.write(str(row) + " ")
                    new_file_2d_map.write("\n")

        elif self.comboBox_SFM_2Dmap_Axes.currentText() == "Alpha_i vs. Alpha_f":
            with open(save_file_directory + self.SFM_FILE[self.SFM_FILE.rfind("/") + 1 : -3] + "_" + self.comboBox_SFM_2Dmap_Polarisation.currentText() + " 2D_map_(Alpha_i vs. Alpha_f)).dat", "w") as new_file_2d_map_Aif:
                # header
                new_file_2d_map_Aif.write("Alpha_i limits: " + str(min(self.int_SFM_Detector_image_Aif[0])) + " : " + str(max(self.int_SFM_Detector_image_Aif[0])) +
                                        "   Alpha_f limits: " + str(min(self.int_SFM_Detector_image_Aif[1])) + " : " + str(max(self.int_SFM_Detector_image_Aif[1])) + " degrees\n")
                for line in numpy.rot90(self.res_Aif):
                    for row in line:
                        new_file_2d_map_Aif.write(str(row) + " ")
                    new_file_2d_map_Aif.write("\n")

        elif self.comboBox_SFM_2Dmap_Axes.currentText() in ["Qx vs. Qz"]:
            with open(save_file_directory + self.SFM_FILE[self.SFM_FILE.rfind("/") + 1 : -3] + "_" + self.comboBox_SFM_2Dmap_Polarisation.currentText() + " points_(Qx, Qz, intens).dat", "w") as new_file_2d_map_Qxz:
                for line in self.int_SFM_Detector_image_Qxz:
                    new_file_2d_map_Qxz.write(str(line[0]) + " " + str(line[1]) + " " + str(line[2]))
                    new_file_2d_map_Qxz.write("\n")

    def update_slits(self):
        roi_width = int(self.lineEdit_SFM_Detector_image_Roi_X_Right.text()) - int(self.lineEdit_SFM_Detector_image_Roi_X_Left.text())
        self.lineEdit_SFM_Detector_image_Roi_bkg_X_Left.setText(str(int(self.lineEdit_SFM_Detector_image_Roi_bkg_X_Right.text()) - roi_width))

        self.lineEdit_SFM_Detector_image_Roi_bkg_Y_Bottom.setText(str(int(self.lineEdit_SFM_Detector_image_Roi_Y_Bottom.text())))
        self.lineEdit_SFM_Detector_image_Roi_bkg_Y_Top.setText(str(int(self.lineEdit_SFM_Detector_image_Roi_Y_Top.text())))

        self.draw_det_image()
        self.load_SFM_Reflectivity_preview()

        self.draw_2D_map()

    def color_det_image(self):
        if self.comboBox_SFM_Detector_image_Color_scheme.currentText() == "White / Black":
            self.color_det_image = numpy.array([[0, 0, 0, 255], [255, 255, 255, 255], [255, 255, 255, 255]], dtype=numpy.ubyte)
        elif self.comboBox_SFM_Detector_image_Color_scheme.currentText() == "Green / Blue":
            self.color_det_image = numpy.array([[0, 0, 255, 255], [255, 0, 0, 255], [0, 255, 0, 255]], dtype=numpy.ubyte)

        self.draw_det_image()
    ##<--

if __name__ == "__main__":
    QtWidgets.QApplication.setStyle("Fusion")
    app = QtWidgets.QApplication(sys.argv)
    prog = GUI()
    prog.show()
    sys.exit(app.exec_())

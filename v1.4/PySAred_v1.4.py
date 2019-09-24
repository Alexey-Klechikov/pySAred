from PyQt5 import QtCore, QtGui, QtWidgets
import h5py, numpy, os
import pyqtgraph as pg
from scipy.interpolate import griddata

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class Ui_MainWindow(QtGui.QMainWindow):

    ##--> define user interface elements
    def setupUi(self, MainWindow):

        # Fonts
        font_headline = QtGui.QFont()
        font_headline.setPointSize(11)
        font_headline.setBold(True)

        font_button = QtGui.QFont()
        font_button.setPointSize(10)
        font_button.setBold(True)

        font_graphs = QtGui.QFont()
        font_graphs.setPixelSize(12)
        font_graphs.setBold(False)

        font_graphs_2 = QtGui.QFont()
        font_graphs_2.setPixelSize(1)
        font_graphs_2.setBold(False)

        font_ee = QtGui.QFont()
        font_ee.setPointSize(8)
        font_ee.setBold(False)

        # Main Window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1180, 720)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1180, 720))
        MainWindow.setMaximumSize(QtCore.QSize(1180, 720))
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowNestedDocks|QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        MainWindow.setWindowTitle("pySAred")
        MainWindow.setWindowIcon(QtGui.QIcon(self.current_dir + "icon.png"))
        MainWindow.setIconSize(QtCore.QSize(30, 30))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Block: .h5 files
        self.label_h5_files = QtWidgets.QLabel(self.centralwidget)
        self.label_h5_files.setGeometry(QtCore.QRect(15, 5, 200, 20))
        self.label_h5_files.setFont(font_headline)
        self.label_h5_files.setObjectName("label_h5_files")
        self.label_h5_files.setText(".h5 files")

        self.groupBox_data = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_data.setGeometry(QtCore.QRect(10, 10, 280, 667))
        self.groupBox_data.setFont(font_ee)
        self.groupBox_data.setTitle("")
        self.groupBox_data.setObjectName("groupBox_data")
        self.label_data_files = QtWidgets.QLabel(self.groupBox_data)
        self.label_data_files.setGeometry(QtCore.QRect(110, 20, 121, 21))
        self.label_data_files.setFont(font_headline)
        self.label_data_files.setObjectName("label_data_files")
        self.label_data_files.setText("Data files")
        self.tableWidget_scans = QtWidgets.QTableWidget(self.groupBox_data)
        self.tableWidget_scans.setFont(font_ee)
        self.tableWidget_scans.setGeometry(QtCore.QRect(10, 42, 260, 338))
        self.tableWidget_scans.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_scans.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_scans.setAutoScroll(True)
        self.tableWidget_scans.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.tableWidget_scans.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_scans.setObjectName("tableWidget_scans")
        self.tableWidget_scans.setColumnCount(4)
        self.tableWidget_scans.setRowCount(0)
        for i in range(0,3):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_scans.setHorizontalHeaderItem(i, item)
        self.tableWidget_scans.horizontalHeader().setVisible(True)
        self.tableWidget_scans.verticalHeader().setVisible(False)
        item = self.tableWidget_scans.horizontalHeaderItem(0)
        item.setText("Scan")
        item = self.tableWidget_scans.horizontalHeaderItem(1)
        item.setText("DB")
        item = self.tableWidget_scans.horizontalHeaderItem(2)
        item.setText("Scan_file_full_path")
        self.tableWidget_scans.setColumnWidth(0, 200)
        self.tableWidget_scans.setColumnWidth(1, int(self.tableWidget_scans.width()) - int(self.tableWidget_scans.columnWidth(0)) - 2)
        self.tableWidget_scans.setColumnWidth(2, 0)
        self.pushButton_delete_scans = QtWidgets.QPushButton(self.groupBox_data)
        self.pushButton_delete_scans.setGeometry(QtCore.QRect(10, 384, 81, 20))
        self.pushButton_delete_scans.setFont(font_ee)
        self.pushButton_delete_scans.setObjectName("pushButton_delete_scans")
        self.pushButton_delete_scans.setText("Delete scans")
        self.pushButton_import_scans = QtWidgets.QPushButton(self.groupBox_data)
        self.pushButton_import_scans.setGeometry(QtCore.QRect(189, 384, 81, 20))
        self.pushButton_import_scans.setFont(font_ee)
        self.pushButton_import_scans.setObjectName("pushButton_import_scans")
        self.pushButton_import_scans.setText("Import scans")

        self.label_db_files = QtWidgets.QLabel(self.groupBox_data)
        self.label_db_files.setGeometry(QtCore.QRect(78, 412, 191, 23))
        self.label_db_files.setFont(font_headline)
        self.label_db_files.setObjectName("label_db_files")
        self.label_db_files.setText("Direct Beam files")
        self.checkBox_db_rearr_after = QtWidgets.QCheckBox(self.groupBox_data)
        self.checkBox_db_rearr_after.setGeometry(QtCore.QRect(10, 432, 210, 20))
        self.checkBox_db_rearr_after.setFont(font_ee)
        self.checkBox_db_rearr_after.setObjectName("checkBox_db_rearr_after")
        self.checkBox_db_rearr_after.setText("DB's were measured after the scans")
        self.tableWidget_db = QtWidgets.QTableWidget(self.groupBox_data)
        self.tableWidget_db.setFont(font_ee)
        self.tableWidget_db.setGeometry(QtCore.QRect(10, 452, 260, 183))
        self.tableWidget_db.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_db.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_db.setAutoScroll(True)
        self.tableWidget_db.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.tableWidget_db.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_db.setObjectName("tableWidget_db")
        self.tableWidget_db.setColumnCount(2)
        self.tableWidget_db.setRowCount(0)
        for i in range(0, 2):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_db.setHorizontalHeaderItem(i, item)
        self.tableWidget_db.horizontalHeader().setVisible(False)
        self.tableWidget_db.verticalHeader().setVisible(False)
        item = self.tableWidget_db.horizontalHeaderItem(0)
        item.setText("Scan")
        item = self.tableWidget_db.horizontalHeaderItem(1)
        item.setText("Path")
        self.tableWidget_db.setColumnWidth(0, self.tableWidget_db.width())
        self.tableWidget_db.setColumnWidth(1, 0)
        self.tableWidget_db.setSortingEnabled(True)
        self.pushButton_delete_db = QtWidgets.QPushButton(self.groupBox_data)
        self.pushButton_delete_db.setGeometry(QtCore.QRect(10, 639, 81, 20))
        self.pushButton_delete_db.setFont(font_ee)
        self.pushButton_delete_db.setObjectName("pushButton_delete_db")
        self.pushButton_delete_db.setText("Delete DB")
        self.pushButton_import_db = QtWidgets.QPushButton(self.groupBox_data)
        self.pushButton_import_db.setGeometry(QtCore.QRect(189, 639, 81, 20))
        self.pushButton_import_db.setFont(font_ee)
        self.pushButton_import_db.setObjectName("pushButton_import_db")
        self.pushButton_import_db.setText("Import DB")

        # Block: Sample
        self.label_sample = QtWidgets.QLabel(self.centralwidget)
        self.label_sample.setGeometry(QtCore.QRect(305, 5, 200, 20))
        self.label_sample.setFont(font_headline)
        self.label_sample.setObjectName("label_sample")
        self.label_sample.setText("Sample")
        self.groupBox_sample_len = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_sample_len.setGeometry(QtCore.QRect(300, 10, 282, 47))
        self.groupBox_sample_len.setFont(font_ee)
        self.groupBox_sample_len.setTitle("")
        self.groupBox_sample_len.setObjectName("groupBox_sample_len")
        self.label_sample_len = QtWidgets.QLabel(self.groupBox_sample_len)
        self.label_sample_len.setGeometry(QtCore.QRect(10, 24, 131, 16))
        self.label_sample_len.setFont(font_ee)
        self.label_sample_len.setObjectName("label_sample_len")
        self.label_sample_len.setText("Sample length (mm)")
        self.lineEdit_sample_len = QtWidgets.QLineEdit(self.groupBox_sample_len)
        self.lineEdit_sample_len.setGeometry(QtCore.QRect(192, 22, 83, 21))
        self.lineEdit_sample_len.setObjectName("lineEdit_sample_len")
        self.lineEdit_sample_len.setText("50")

        # Block: Reductions and Instrument settings
        self.label_reductions = QtWidgets.QLabel(self.centralwidget)
        self.label_reductions.setGeometry(QtCore.QRect(305, 65, 200, 16))
        self.label_reductions.setFont(font_headline)
        self.label_reductions.setObjectName("label_reductions")
        self.label_reductions.setText("Reductions")
        self.tabWidget_settings_re_in_ex = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_settings_re_in_ex.setGeometry(QtCore.QRect(300, 87, 281, 226))
        self.tabWidget_settings_re_in_ex.setFont(font_ee)
        self.tabWidget_settings_re_in_ex.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget_settings_re_in_ex.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget_settings_re_in_ex.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget_settings_re_in_ex.setObjectName("tabWidget_settings_re_in_ex")

        # Tab: Reductions
        self.tab_reductions = QtWidgets.QWidget()
        self.tab_reductions.setObjectName("tab_reductions")
        self.checkBox_red_devide_by_monitor = QtWidgets.QCheckBox(self.tab_reductions)
        self.checkBox_red_devide_by_monitor.setGeometry(QtCore.QRect(10, 10, 131, 18))
        self.checkBox_red_devide_by_monitor.setFont(font_ee)
        self.checkBox_red_devide_by_monitor.setObjectName("checkBox_red_devide_by_monitor")
        self.checkBox_red_devide_by_monitor.setText("Devide by monitor")
        self.checkBox_red_normalize_by_db = QtWidgets.QCheckBox(self.tab_reductions)
        self.checkBox_red_normalize_by_db.setGeometry(QtCore.QRect(10, 35, 181, 18))
        self.checkBox_red_normalize_by_db.setFont(font_ee)
        self.checkBox_red_normalize_by_db.setObjectName("checkBox_red_normalize_by_db")
        self.checkBox_red_normalize_by_db.setText("Normalize by direct beam")
        self.checkBox_red_db_attenuator = QtWidgets.QCheckBox(self.tab_reductions)
        self.checkBox_red_db_attenuator.setGeometry(QtCore.QRect(10, 60, 161, 18))
        self.checkBox_red_db_attenuator.setFont(font_ee)
        self.checkBox_red_db_attenuator.setChecked(False)
        self.checkBox_red_db_attenuator.setObjectName("checkBox_red_db_attenuator")
        self.checkBox_red_db_attenuator.setText("Direct beam attenuator")
        self.lineEdit_red_db_attenuator_factor = QtWidgets.QLineEdit(self.tab_reductions)
        self.lineEdit_red_db_attenuator_factor.setGeometry(QtCore.QRect(30, 85, 221, 20))
        self.lineEdit_red_db_attenuator_factor.setFont(font_ee)
        self.lineEdit_red_db_attenuator_factor.setText("")
        self.lineEdit_red_db_attenuator_factor.setObjectName("lineEdit_red_db_attenuator_factor")
        self.lineEdit_red_db_attenuator_factor.setPlaceholderText("Attenuator correction [default 10.4]")
        self.checkBox_red_subtract_bkg = QtWidgets.QCheckBox(self.tab_reductions)
        self.checkBox_red_subtract_bkg.setGeometry(QtCore.QRect(10, 115, 231, 18))
        self.checkBox_red_subtract_bkg.setFont(font_ee)
        self.checkBox_red_subtract_bkg.setObjectName("checkBox_red_subtract_bkg")
        self.checkBox_red_subtract_bkg.setText("Subtract background (using 1 ROI)")
        self.lineEdit_red_subtract_bkg_skip = QtWidgets.QLineEdit(self.tab_reductions)
        self.lineEdit_red_subtract_bkg_skip.setGeometry(QtCore.QRect(30, 140, 221, 20))
        self.lineEdit_red_subtract_bkg_skip.setFont(font_ee)
        self.lineEdit_red_subtract_bkg_skip.setObjectName("lineEdit_red_subtract_bkg_skip")
        self.lineEdit_red_subtract_bkg_skip.setPlaceholderText("Skip background corr. at Qz < [default 0]")
        self.checkBox_red_overillumination_correction = QtWidgets.QCheckBox(self.tab_reductions)
        self.checkBox_red_overillumination_correction.setGeometry(QtCore.QRect(10, 170, 181, 18))
        self.checkBox_red_overillumination_correction.setFont(font_ee)
        self.checkBox_red_overillumination_correction.setObjectName("checkBox_red_overillumination_correction")
        self.checkBox_red_overillumination_correction.setText("Overillumination correction")
        self.tabWidget_settings_re_in_ex.addTab(self.tab_reductions, "")
        self.tabWidget_settings_re_in_ex.setTabText(0, "Reductions")

        # Tab: Instrument settings
        self.tab_instrument_settings = QtWidgets.QWidget()
        self.tab_instrument_settings.setObjectName("tab_instrument_settings")
        self.label_instr_wavelength = QtWidgets.QLabel(self.tab_instrument_settings)
        self.label_instr_wavelength.setGeometry(QtCore.QRect(10, 10, 111, 16))
        self.label_instr_wavelength.setFont(font_ee)
        self.label_instr_wavelength.setObjectName("label_instr_wavelength")
        self.label_instr_wavelength.setText("Wavelength (A)")
        self.lineEdit_instr_wavelength = QtWidgets.QLineEdit(self.tab_instrument_settings)
        self.lineEdit_instr_wavelength.setGeometry(QtCore.QRect(220, 10, 41, 20))
        self.lineEdit_instr_wavelength.setFont(font_ee)
        self.lineEdit_instr_wavelength.setObjectName("lineEdit_instr_wavelength")
        self.lineEdit_instr_wavelength.setText("5.2")
        self.label_instr_wavelength_resolution = QtWidgets.QLabel(self.tab_instrument_settings)
        self.label_instr_wavelength_resolution.setGeometry(QtCore.QRect(10, 35, 271, 16))
        self.label_instr_wavelength_resolution.setFont(font_ee)
        self.label_instr_wavelength_resolution.setObjectName("label_instr_wavelength_resolution")
        self.label_instr_wavelength_resolution.setText("Wavelength resolution (d_lambda/lambda)")
        self.lineEdit_instr_wavelength_resolution = QtWidgets.QLineEdit(self.tab_instrument_settings)
        self.lineEdit_instr_wavelength_resolution.setGeometry(QtCore.QRect(220, 35, 41, 20))
        self.lineEdit_instr_wavelength_resolution.setFont(font_ee)
        self.lineEdit_instr_wavelength_resolution.setObjectName("lineEdit_instr_wavelength_resolution")
        self.lineEdit_instr_wavelength_resolution.setText("0.007")
        self.label_instr_s1_to_sample_dist = QtWidgets.QLabel(self.tab_instrument_settings)
        self.label_instr_s1_to_sample_dist.setGeometry(QtCore.QRect(10, 60, 241, 16))
        self.label_instr_s1_to_sample_dist.setFont(font_ee)
        self.label_instr_s1_to_sample_dist.setObjectName("label_instr_s1_to_sample_dist")
        self.label_instr_s1_to_sample_dist.setText("Mono_slit to Samplle distance (mm)")
        self.lineEdit_instr_s1_to_sample_dist = QtWidgets.QLineEdit(self.tab_instrument_settings)
        self.lineEdit_instr_s1_to_sample_dist.setGeometry(QtCore.QRect(220, 60, 41, 20))
        self.lineEdit_instr_s1_to_sample_dist.setFont(font_ee)
        self.lineEdit_instr_s1_to_sample_dist.setObjectName("lineEdit_instr_s1_to_sample_dist")
        self.lineEdit_instr_s1_to_sample_dist.setText("2350")
        self.label_instr_s2_to_sample_dist = QtWidgets.QLabel(self.tab_instrument_settings)
        self.label_instr_s2_to_sample_dist.setGeometry(QtCore.QRect(10, 85, 241, 16))
        self.label_instr_s2_to_sample_dist.setFont(font_ee)
        self.label_instr_s2_to_sample_dist.setObjectName("label_instr_s2_to_sample_dist")
        self.label_instr_s2_to_sample_dist.setText("Sample_slit to Sample distance (mm)")
        self.lineEdit_instr_s2_to_sample_dist = QtWidgets.QLineEdit(self.tab_instrument_settings)
        self.lineEdit_instr_s2_to_sample_dist.setGeometry(QtCore.QRect(220, 85, 41, 20))
        self.lineEdit_instr_s2_to_sample_dist.setFont(font_ee)
        self.lineEdit_instr_s2_to_sample_dist.setObjectName("lineEdit_instr_s2_to_sample_dist")
        self.lineEdit_instr_s2_to_sample_dist.setText("195")
        self.label_instr_sample_to_det_dist = QtWidgets.QLabel(self.tab_instrument_settings)
        self.label_instr_sample_to_det_dist.setGeometry(QtCore.QRect(10, 110, 241, 16))
        self.label_instr_sample_to_det_dist.setFont(font_ee)
        self.label_instr_sample_to_det_dist.setObjectName("label_instr_sample_to_det_dist")
        self.label_instr_sample_to_det_dist.setText("Samplle to Detector distance (mm)")
        self.lineEdit_instr_sample_to_det_dist = QtWidgets.QLineEdit(self.tab_instrument_settings)
        self.lineEdit_instr_sample_to_det_dist.setGeometry(QtCore.QRect(220, 110, 41, 20))
        self.lineEdit_instr_sample_to_det_dist.setFont(font_ee)
        self.lineEdit_instr_sample_to_det_dist.setObjectName("lineEdit_instr_sample_to_det_dist")
        self.lineEdit_instr_sample_to_det_dist.setText("2500")
        '''
        self.label_instr_th_offset = QtWidgets.QLabel(self.tab_instrument_settings)
        self.label_instr_th_offset.setGeometry(QtCore.QRect(10, 150, 241, 16))
        self.label_instr_th_offset.setFont(font_ee)
        self.label_instr_th_offset.setObjectName("label_instr_th_offset")
        self.label_instr_th_offset.setText("th offset (deg) (SFM only)")
        self.lineEdit_instr_th_offset = QtWidgets.QLineEdit(self.tab_instrument_settings)
        self.lineEdit_instr_th_offset.setGeometry(QtCore.QRect(220, 150, 41, 20))
        self.lineEdit_instr_th_offset.setFont(font_ee)
        self.lineEdit_instr_th_offset.setObjectName("lineEdit_instr_th_offset")
        self.lineEdit_instr_th_offset.setText("0")
        '''
        self.label_instr_full_scan_offset = QtWidgets.QLabel(self.tab_instrument_settings)
        self.label_instr_full_scan_offset.setGeometry(QtCore.QRect(10, 175, 241, 16))
        self.label_instr_full_scan_offset.setFont(font_ee)
        self.label_instr_full_scan_offset.setObjectName("label_instr_full_scan_offset")
        self.label_instr_full_scan_offset.setText("Full scan offset (th - deg) (SFM only)")
        self.lineEdit_instr_full_scan_offset = QtWidgets.QLineEdit(self.tab_instrument_settings)
        self.lineEdit_instr_full_scan_offset.setGeometry(QtCore.QRect(220, 175, 41, 20))
        self.lineEdit_instr_full_scan_offset.setFont(font_ee)
        self.lineEdit_instr_full_scan_offset.setObjectName("lineEdit_instr_full_scan_offset")
        self.lineEdit_instr_full_scan_offset.setText("0")
        self.tabWidget_settings_re_in_ex.addTab(self.tab_instrument_settings, "")
        self.tabWidget_settings_re_in_ex.setTabText(1, "Instrument settings")

        # Tab: Export options
        self.tab_export_options = QtWidgets.QWidget()
        self.tab_export_options.setObjectName("tab_export_options")
        self.checkBox_export_add_resolution_column = QtWidgets.QCheckBox(self.tab_export_options)
        self.checkBox_export_add_resolution_column.setGeometry(QtCore.QRect(10, 10, 250, 18))
        self.checkBox_export_add_resolution_column.setFont(font_ee)
        self.checkBox_export_add_resolution_column.setChecked(True)
        self.checkBox_export_add_resolution_column.setObjectName("checkBox_export_add_resolution_column")
        self.checkBox_export_add_resolution_column.setText("Include ang. resolution column in the output file")
        self.checkBox_export_resolution_like_sared = QtWidgets.QCheckBox(self.tab_export_options)
        self.checkBox_export_resolution_like_sared.setGeometry(QtCore.QRect(30, 35, 250, 18))
        self.checkBox_export_resolution_like_sared.setFont(font_ee)
        self.checkBox_export_resolution_like_sared.setChecked(True)
        self.checkBox_export_resolution_like_sared.setObjectName("checkBox_export_resolution_like_sared")
        self.checkBox_export_resolution_like_sared.setText("Calculate ang. resolution in 'Sared' way")
        self.checkBox_export_remove_zeros = QtWidgets.QCheckBox(self.tab_export_options)
        self.checkBox_export_remove_zeros.setGeometry(QtCore.QRect(10, 60, 250, 18))
        self.checkBox_export_remove_zeros.setFont(font_ee)
        self.checkBox_export_remove_zeros.setChecked(False)
        self.checkBox_export_remove_zeros.setObjectName("checkBox_export_remove_zeros")
        self.checkBox_export_remove_zeros.setText("Remove zeros from reduced files")
        self.tabWidget_settings_re_in_ex.addTab(self.tab_export_options, "")
        self.tabWidget_settings_re_in_ex.setTabText(2, "Export")

        # Block: Save reduced files at
        self.label_save_at = QtWidgets.QLabel(self.centralwidget)
        self.label_save_at.setGeometry(QtCore.QRect(305, 320, 200, 20))
        self.label_save_at.setFont(font_headline)
        self.label_save_at.setObjectName("label_save_at")
        self.label_save_at.setText("Save reduced files at")
        self.groupBox_save_at = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_save_at.setGeometry(QtCore.QRect(299, 325, 282, 48))
        self.groupBox_save_at.setFont(font_ee)
        self.groupBox_save_at.setTitle("")
        self.groupBox_save_at.setObjectName("groupBox_save_at")
        self.lineEdit_save_at = QtWidgets.QLineEdit(self.groupBox_save_at)
        self.lineEdit_save_at.setGeometry(QtCore.QRect(10, 22, 225, 22))
        self.lineEdit_save_at.setFont(font_ee)
        self.lineEdit_save_at.setObjectName("lineEdit_save_at")
        self.lineEdit_save_at.setText(self.current_dir)
        self.toolButton_save_at = QtWidgets.QToolButton(self.groupBox_save_at)
        self.toolButton_save_at.setGeometry(QtCore.QRect(248, 22, 27, 22))
        self.toolButton_save_at.setObjectName("toolButton_save_at")
        self.toolButton_save_at.setText("...")

        # Button: Clear
        self.pushButton_clear = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_clear.setGeometry(QtCore.QRect(300, 380, 88, 30))
        self.pushButton_clear.setFont(font_button)
        self.pushButton_clear.setObjectName("pushButton_clear")
        self.pushButton_clear.setText("Clear all")

        # Button: Reduce all
        self.pushButton_reduce_all = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_reduce_all.setGeometry(QtCore.QRect(493, 380, 88, 30))
        self.pushButton_reduce_all.setFont(font_button)
        self.pushButton_reduce_all.setObjectName("pushButton_reduce_all")
        self.pushButton_reduce_all.setText("Reduce all")

        # Errors
        self.label_error_sample_len_missing = QtWidgets.QLabel(self.centralwidget)
        self.label_error_sample_len_missing.setGeometry(QtCore.QRect(360, 420, 181, 31))
        self.label_error_sample_len_missing.setFont(font_button)
        self.label_error_sample_len_missing.setObjectName("label_error_sample_len_missing")
        self.label_error_sample_len_missing.setVisible(False)
        self.label_error_sample_len_missing.setText("Sample length is missing")
        self.label_error_sample_len_missing.setStyleSheet("color:rgb(255,0,0)")
        self.label_error_db_missing = QtWidgets.QLabel(self.centralwidget)
        self.label_error_db_missing.setGeometry(QtCore.QRect(355, 450, 181, 31))
        self.label_error_db_missing.setFont(font_button)
        self.label_error_db_missing.setObjectName("label_error_db_missing")
        self.label_error_db_missing.setVisible(False)
        self.label_error_db_missing.setText("Direct beam file is missing")
        self.label_error_db_missing.setStyleSheet("color:rgb(255,0,0)")
        self.label_error_db_wrong = QtWidgets.QLabel(self.centralwidget)
        self.label_error_db_wrong.setGeometry(QtCore.QRect(365, 420, 240, 51))
        self.label_error_db_wrong.setFont(font_button)
        self.label_error_db_wrong.setObjectName("label_error_db_wrong")
        self.label_error_db_wrong.setVisible(False)
        self.label_error_db_wrong.setStyleSheet("color:rgb(255,0,0)")
        self.label_error_save_at_missing = QtWidgets.QLabel(self.centralwidget)
        self.label_error_save_at_missing.setGeometry(QtCore.QRect(360, 435, 181, 31))
        self.label_error_save_at_missing.setFont(font_button)
        self.label_error_save_at_missing.setObjectName("label_error_save_at_missing")
        self.label_error_save_at_missing.setVisible(False)
        self.label_error_save_at_missing.setText("Define 'Save at' directory")
        self.label_error_save_at_missing.setStyleSheet("color:rgb(255,0,0)")
        self.label_error_wrong_roi_input = QtWidgets.QLabel(self.centralwidget)
        self.label_error_wrong_roi_input.setGeometry(QtCore.QRect(360, 435, 181, 31))
        self.label_error_wrong_roi_input.setFont(font_button)
        self.label_error_wrong_roi_input.setObjectName("label_error_wrong_roi_input")
        self.label_error_wrong_roi_input.setVisible(False)
        self.label_error_wrong_roi_input.setText("Recheck your ROI input")
        self.label_error_wrong_roi_input.setStyleSheet("color:rgb(255,0,0)")

        # Block: Recheck following files in SFM
        self.label_recheck_in_sfm = QtWidgets.QLabel(self.centralwidget)
        self.label_recheck_in_sfm.setGeometry(QtCore.QRect(305, 490, 250, 20))
        self.label_recheck_in_sfm.setFont(font_headline)
        self.label_recheck_in_sfm.setObjectName("label_recheck_in_sfm")
        self.label_recheck_in_sfm.setText("Recheck following files in SFM")
        self.groupBox_recheck_files_in_sfm = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_recheck_files_in_sfm.setGeometry(QtCore.QRect(299, 497, 282, 180))
        self.groupBox_recheck_files_in_sfm.setFont(font_ee)
        self.groupBox_recheck_files_in_sfm.setTitle("")
        self.groupBox_recheck_files_in_sfm.setObjectName("groupBox_recheck_files_in_sfm")
        self.listWidget_recheck_files_in_sfm = QtWidgets.QListWidget(self.groupBox_recheck_files_in_sfm)
        self.listWidget_recheck_files_in_sfm.setGeometry(QtCore.QRect(10, 27, 262, 145))
        self.listWidget_recheck_files_in_sfm.setObjectName("listWidget_recheck_files_in_sfm")

        # Block: Single File Mode
        self.label_single_file_mode = QtWidgets.QLabel(self.centralwidget)
        self.label_single_file_mode.setGeometry(QtCore.QRect(596, 5, 200, 20))
        self.label_single_file_mode.setFont(font_headline)
        self.label_single_file_mode.setObjectName("label_single_file_mode")
        self.label_single_file_mode.setText("Single File Mode (SFM)")
        self.groupBox_single_file_mode_scan = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_single_file_mode_scan.setGeometry(QtCore.QRect(591, 10, 472, 48))
        self.groupBox_single_file_mode_scan.setTitle("")
        self.groupBox_single_file_mode_scan.setObjectName("groupBox_single_file_mode_scan")
        self.label_single_file_mode_scan = QtWidgets.QLabel(self.groupBox_single_file_mode_scan)
        self.label_single_file_mode_scan.setGeometry(QtCore.QRect(10, 23, 47, 20))
        self.label_single_file_mode_scan.setObjectName("label_single_file_mode_scan")
        self.label_single_file_mode_scan.setText("Scan")
        self.label_single_file_mode_scan.setFont(font_ee)
        self.comboBox_single_file_mode_scan = QtWidgets.QComboBox(self.groupBox_single_file_mode_scan)
        self.comboBox_single_file_mode_scan.setGeometry(QtCore.QRect(40, 23, 425, 20))
        self.comboBox_single_file_mode_scan.setObjectName("comboBox_single_file_mode_scan")
        self.comboBox_single_file_mode_scan.setFont(font_ee)
        pg.setConfigOption('background', (255, 255, 255))
        pg.setConfigOption('foreground', 'k')

        # Button: Reduce SFM
        self.pushButton_reduce_sfm_scan = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_reduce_sfm_scan.setGeometry(QtCore.QRect(1070, 28, 100, 30))
        self.pushButton_reduce_sfm_scan.setFont(font_button)
        self.pushButton_reduce_sfm_scan.setObjectName("pushButton_reduce_sfm_scan")
        self.pushButton_reduce_sfm_scan.setText("Reduce SFM")

        # Block: Detector Images and Reflectivity preview
        self.tabWidget_single_file_mode = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_single_file_mode.setGeometry(QtCore.QRect(592, 65, 578, 613))
        self.tabWidget_single_file_mode.setFont(font_ee)
        self.tabWidget_single_file_mode.setObjectName("tabWidget_single_file_mode")

        # Tab: Detector images
        linedit_size_X = 30
        linedit_size_Y = 18
        self.tab_sfm_detector_image = QtWidgets.QWidget()
        self.tab_sfm_detector_image.setObjectName("tab_sfm_detector_image")
        self.graphicsView_sfm_detector_roi = pg.PlotWidget(self.tab_sfm_detector_image)
        self.graphicsView_sfm_detector_roi.setGeometry(QtCore.QRect(0, 450, 577, 90))
        self.graphicsView_sfm_detector_roi.setObjectName("graphicsView_sfm_detector_roi")
        self.graphicsView_sfm_detector_roi.hideAxis("left")
        self.graphicsView_sfm_detector_roi.setMouseEnabled(y=False)
        self.graphicsView_sfm_detector_image = pg.ImageView(self.tab_sfm_detector_image)
        self.graphicsView_sfm_detector_image.setGeometry(QtCore.QRect(0, 30, 577, 510))
        self.graphicsView_sfm_detector_image.setObjectName("graphicsView_sfm_detector_image")
        self.graphicsView_sfm_detector_image.ui.histogram.hide()
        self.graphicsView_sfm_detector_image.ui.menuBtn.hide()
        self.graphicsView_sfm_detector_image.ui.roiBtn.hide()
        self.label_sfm_detector_image_point_number = QtWidgets.QLabel(self.tab_sfm_detector_image)
        self.label_sfm_detector_image_point_number.setFont(font_ee)
        self.label_sfm_detector_image_point_number.setGeometry(QtCore.QRect(10, 8, 70, 16))
        self.label_sfm_detector_image_point_number.setObjectName("label_sfm_detector_image_point_number")
        self.label_sfm_detector_image_point_number.setText("Point number")
        self.comboBox_sfm_detector_image_point_number = QtWidgets.QComboBox(self.tab_sfm_detector_image)
        self.comboBox_sfm_detector_image_point_number.setFont(font_ee)
        self.comboBox_sfm_detector_image_point_number.setGeometry(QtCore.QRect(80, 7, 65, 20))
        self.comboBox_sfm_detector_image_point_number.setObjectName("comboBox_sfm_detector_image_point_number")
        self.label_sfm_detector_image_polarisation = QtWidgets.QLabel(self.tab_sfm_detector_image)
        self.label_sfm_detector_image_polarisation.setFont(font_ee)
        self.label_sfm_detector_image_polarisation.setGeometry(QtCore.QRect(155, 8, 60, 16))
        self.label_sfm_detector_image_polarisation.setObjectName("label_sfm_detector_image_polarisation")
        self.label_sfm_detector_image_polarisation.setText("Polarisation")
        self.comboBox_sfm_detector_image_polarisation = QtWidgets.QComboBox(self.tab_sfm_detector_image)
        self.comboBox_sfm_detector_image_polarisation.setFont(font_ee)
        self.comboBox_sfm_detector_image_polarisation.setGeometry(QtCore.QRect(215, 7, 40, 20))
        self.comboBox_sfm_detector_image_polarisation.setObjectName("comboBox_sfm_detector_image_polarisation")
        self.label_sfm_detector_image_color_scheme = QtWidgets.QLabel(self.tab_sfm_detector_image)
        self.label_sfm_detector_image_color_scheme.setFont(font_ee)
        self.label_sfm_detector_image_color_scheme.setGeometry(QtCore.QRect(268, 8, 60, 16))
        self.label_sfm_detector_image_color_scheme.setObjectName("label_sfm_detector_image_color_scheme")
        self.label_sfm_detector_image_color_scheme.setText("Colors")
        self.comboBox_sfm_detector_image_color_scheme = QtWidgets.QComboBox(self.tab_sfm_detector_image)
        self.comboBox_sfm_detector_image_color_scheme.setFont(font_ee)
        self.comboBox_sfm_detector_image_color_scheme.setGeometry(QtCore.QRect(305, 7, 90, 20))
        self.comboBox_sfm_detector_image_color_scheme.setObjectName("comboBox_sfm_detector_image_color_scheme")
        self.comboBox_sfm_detector_image_color_scheme.addItem("Green / Blue")
        self.comboBox_sfm_detector_image_color_scheme.addItem("White / Black")
        self.pushButton_sfm_detector_image_show_int_roi = QtWidgets.QPushButton(self.tab_sfm_detector_image)
        self.pushButton_sfm_detector_image_show_int_roi.setGeometry(QtCore.QRect(445, 7, 120, 20))
        self.pushButton_sfm_detector_image_show_int_roi.setFont(font_button)
        self.pushButton_sfm_detector_image_show_int_roi.setObjectName("pushButton_sfm_detector_image_show_int_roi")
        self.pushButton_sfm_detector_image_show_int_roi.setText("Integrated ROI")
        self.label_sfm_detector_image_slits = QtWidgets.QLabel(self.tab_sfm_detector_image)
        self.label_sfm_detector_image_slits.setFont(font_ee)
        self.label_sfm_detector_image_slits.setGeometry(QtCore.QRect(385, 565, 51, 16))
        self.label_sfm_detector_image_slits.setObjectName("label_sfm_detector_image_slits")
        self.label_sfm_detector_image_slits.setText("Slits (mm):")
        self.label_sfm_detector_image_slits_s1hg = QtWidgets.QLabel(self.tab_sfm_detector_image)
        self.label_sfm_detector_image_slits_s1hg.setFont(font_ee)
        self.label_sfm_detector_image_slits_s1hg.setGeometry(QtCore.QRect(440, 565, 41, 16))
        self.label_sfm_detector_image_slits_s1hg.setObjectName("label_sfm_detector_image_slits_s1hg")
        self.label_sfm_detector_image_slits_s1hg.setText("s1hg")
        self.lineEdit_sfm_detector_image_slits_s1hg = QtWidgets.QLineEdit(self.tab_sfm_detector_image)
        self.lineEdit_sfm_detector_image_slits_s1hg.setFont(font_ee)
        self.lineEdit_sfm_detector_image_slits_s1hg.setGeometry(QtCore.QRect(470, 565, linedit_size_X, linedit_size_Y))
        self.lineEdit_sfm_detector_image_slits_s1hg.setObjectName("lineEdit_sfm_detector_image_slits_s1hg")
        self.lineEdit_sfm_detector_image_slits_s1hg.setEnabled(False)
        self.lineEdit_sfm_detector_image_slits_s1hg.setStyleSheet("color:rgb(0,0,0)")
        self.label_sfm_detector_image_slits_s2hg = QtWidgets.QLabel(self.tab_sfm_detector_image)
        self.label_sfm_detector_image_slits_s2hg.setFont(font_ee)
        self.label_sfm_detector_image_slits_s2hg.setGeometry(QtCore.QRect(505, 565, 30, 16))
        self.label_sfm_detector_image_slits_s2hg.setObjectName("label_sfm_detector_image_slits_s2hg")
        self.label_sfm_detector_image_slits_s2hg.setText("s2hg")
        self.lineEdit_sfm_detector_image_slits_s2hg = QtWidgets.QLineEdit(self.tab_sfm_detector_image)
        self.lineEdit_sfm_detector_image_slits_s2hg.setFont(font_ee)
        self.lineEdit_sfm_detector_image_slits_s2hg.setGeometry(QtCore.QRect(535, 565, linedit_size_X, linedit_size_Y))
        self.lineEdit_sfm_detector_image_slits_s2hg.setObjectName("lineEdit_sfm_detector_image_slits_s2hg")
        self.lineEdit_sfm_detector_image_slits_s2hg.setEnabled(False)
        self.lineEdit_sfm_detector_image_slits_s2hg.setStyleSheet("color:rgb(0,0,0)")
        self.label_sfm_detector_image_time = QtWidgets.QLabel(self.tab_sfm_detector_image)
        self.label_sfm_detector_image_time.setFont(font_ee)
        self.label_sfm_detector_image_time.setGeometry(QtCore.QRect(385, 545, 71, 16))
        self.label_sfm_detector_image_time.setObjectName("label_sfm_detector_image_time")
        self.label_sfm_detector_image_time.setText("Time (s):")
        self.lineEdit_sfm_detector_image_time = QtWidgets.QLineEdit(self.tab_sfm_detector_image)
        self.lineEdit_sfm_detector_image_time.setFont(font_ee)
        self.lineEdit_sfm_detector_image_time.setGeometry(QtCore.QRect(470, 545, linedit_size_X, linedit_size_Y))
        self.lineEdit_sfm_detector_image_time.setObjectName("lineEdit_sfm_detector_image_time")
        self.lineEdit_sfm_detector_image_time.setEnabled(False)
        self.lineEdit_sfm_detector_image_time.setStyleSheet("color:rgb(0,0,0)")
        self.label_sfm_detector_image_roi = QtWidgets.QLabel(self.tab_sfm_detector_image)
        self.label_sfm_detector_image_roi.setFont(font_ee)
        self.label_sfm_detector_image_roi.setGeometry(QtCore.QRect(10, 545, 31, 16))
        self.label_sfm_detector_image_roi.setObjectName("label_sfm_detector_image_roi")
        self.label_sfm_detector_image_roi.setText("ROI:  ")
        self.label_sfm_detector_image_roi_x_left = QtWidgets.QLabel(self.tab_sfm_detector_image)
        self.label_sfm_detector_image_roi_x_left.setFont(font_ee)
        self.label_sfm_detector_image_roi_x_left.setGeometry(QtCore.QRect(40, 545, 51, 16))
        self.label_sfm_detector_image_roi_x_left.setObjectName("label_sfm_detector_image_roi_x_left")
        self.label_sfm_detector_image_roi_x_left.setText("left")
        self.lineEdit_sfm_detector_image_roi_x_left = QtWidgets.QLineEdit(self.tab_sfm_detector_image)
        self.lineEdit_sfm_detector_image_roi_x_left.setFont(font_ee)
        self.lineEdit_sfm_detector_image_roi_x_left.setGeometry(QtCore.QRect(75, 545, linedit_size_X, linedit_size_Y))
        self.lineEdit_sfm_detector_image_roi_x_left.setObjectName("lineEdit_sfm_detector_image_roi_x_left")
        self.label_sfm_detector_image_roi_x_right = QtWidgets.QLabel(self.tab_sfm_detector_image)
        self.label_sfm_detector_image_roi_x_right.setFont(font_ee)
        self.label_sfm_detector_image_roi_x_right.setGeometry(QtCore.QRect(115, 545, 51, 16))
        self.label_sfm_detector_image_roi_x_right.setObjectName("label_sfm_detector_image_roi_x_right")
        self.label_sfm_detector_image_roi_x_right.setText("right")
        self.lineEdit_sfm_detector_image_roi_x_right = QtWidgets.QLineEdit(self.tab_sfm_detector_image)
        self.lineEdit_sfm_detector_image_roi_x_right.setFont(font_ee)
        self.lineEdit_sfm_detector_image_roi_x_right.setGeometry(QtCore.QRect(140, 545, linedit_size_X, linedit_size_Y))
        self.lineEdit_sfm_detector_image_roi_x_right.setObjectName("lineEdit_sfm_detector_image_roi_x_right")
        self.label_sfm_detector_image_roi_y_bottom = QtWidgets.QLabel(self.tab_sfm_detector_image)
        self.label_sfm_detector_image_roi_y_bottom.setFont(font_ee)
        self.label_sfm_detector_image_roi_y_bottom.setGeometry(QtCore.QRect(40, 565, 51, 16))
        self.label_sfm_detector_image_roi_y_bottom.setObjectName("label_sfm_detector_image_roi_y_bottom")
        self.label_sfm_detector_image_roi_y_bottom.setText("bottom")
        self.lineEdit_sfm_detector_image_roi_y_bottom = QtWidgets.QLineEdit(self.tab_sfm_detector_image)
        self.lineEdit_sfm_detector_image_roi_y_bottom.setFont(font_ee)
        self.lineEdit_sfm_detector_image_roi_y_bottom.setGeometry(QtCore.QRect(75, 565, linedit_size_X, linedit_size_Y))
        self.lineEdit_sfm_detector_image_roi_y_bottom.setObjectName("lineEdit_sfm_detector_image_roi_y_bottom")
        self.label_sfm_detector_image_roi_y_top = QtWidgets.QLabel(self.tab_sfm_detector_image)
        self.label_sfm_detector_image_roi_y_top.setFont(font_ee)
        self.label_sfm_detector_image_roi_y_top.setGeometry(QtCore.QRect(115, 565, 51, 16))
        self.label_sfm_detector_image_roi_y_top.setObjectName("label_sfm_detector_image_roi_y_top")
        self.label_sfm_detector_image_roi_y_top.setText("top")
        self.lineEdit_sfm_detector_image_roi_y_top = QtWidgets.QLineEdit(self.tab_sfm_detector_image)
        self.lineEdit_sfm_detector_image_roi_y_top.setFont(font_ee)
        self.lineEdit_sfm_detector_image_roi_y_top.setGeometry(QtCore.QRect(140, 565, linedit_size_X, linedit_size_Y))
        self.lineEdit_sfm_detector_image_roi_y_top.setObjectName("lineEdit_sfm_detector_image_roi_y_top")
        self.label_sfm_detector_image_roi_bkg = QtWidgets.QLabel(self.tab_sfm_detector_image)
        self.label_sfm_detector_image_roi_bkg.setFont(font_ee)
        self.label_sfm_detector_image_roi_bkg.setGeometry(QtCore.QRect(190, 545, 47, 16))
        self.label_sfm_detector_image_roi_bkg.setObjectName("label_sfm_detector_image_roi_bkg")
        self.label_sfm_detector_image_roi_bkg.setText("ROI BKG:")
        self.label_sfm_detector_image_roi_bkg_x_left = QtWidgets.QLabel(self.tab_sfm_detector_image)
        self.label_sfm_detector_image_roi_bkg_x_left.setFont(font_ee)
        self.label_sfm_detector_image_roi_bkg_x_left.setGeometry(QtCore.QRect(240, 545, 51, 16))
        self.label_sfm_detector_image_roi_bkg_x_left.setObjectName("label_sfm_detector_image_roi_bkg_x_left")
        self.label_sfm_detector_image_roi_bkg_x_left.setText("left")
        self.lineEdit_sfm_detector_image_roi_bkg_x_left = QtWidgets.QLineEdit(self.tab_sfm_detector_image)
        self.lineEdit_sfm_detector_image_roi_bkg_x_left.setFont(font_ee)
        self.lineEdit_sfm_detector_image_roi_bkg_x_left.setGeometry(QtCore.QRect(275, 545, linedit_size_X, linedit_size_Y))
        self.lineEdit_sfm_detector_image_roi_bkg_x_left.setObjectName("lineEdit_sfm_detector_image_roi_bkg_x_left")
        self.lineEdit_sfm_detector_image_roi_bkg_x_left.setEnabled(False)
        self.lineEdit_sfm_detector_image_roi_bkg_x_left.setStyleSheet("color:rgb(0,0,0)")
        self.label_sfm_detector_image_roi_bkg_x_right = QtWidgets.QLabel(self.tab_sfm_detector_image)
        self.label_sfm_detector_image_roi_bkg_x_right.setFont(font_ee)
        self.label_sfm_detector_image_roi_bkg_x_right.setGeometry(QtCore.QRect(315, 545, 51, 16))
        self.label_sfm_detector_image_roi_bkg_x_right.setObjectName("label_sfm_detector_image_roi_bkg_x_right")
        self.label_sfm_detector_image_roi_bkg_x_right.setText("right")
        self.lineEdit_sfm_detector_image_roi_bkg_x_right = QtWidgets.QLineEdit(self.tab_sfm_detector_image)
        self.lineEdit_sfm_detector_image_roi_bkg_x_right.setFont(font_ee)
        self.lineEdit_sfm_detector_image_roi_bkg_x_right.setGeometry(QtCore.QRect(340, 545, linedit_size_X, linedit_size_Y))
        self.lineEdit_sfm_detector_image_roi_bkg_x_right.setObjectName("lineEdit_sfm_detector_image_roi_bkg_x_right")
        self.label_sfm_detector_image_roi_bkg_y_bottom = QtWidgets.QLabel(self.tab_sfm_detector_image)
        self.label_sfm_detector_image_roi_bkg_y_bottom.setFont(font_ee)
        self.label_sfm_detector_image_roi_bkg_y_bottom.setGeometry(QtCore.QRect(240, 565, 51, 16))
        self.label_sfm_detector_image_roi_bkg_y_bottom.setObjectName("label_sfm_detector_image_roi_bkg_y_bottom")
        self.label_sfm_detector_image_roi_bkg_y_bottom.setText("bottom")
        self.lineEdit_sfm_detector_image_roi_bkg_y_bottom = QtWidgets.QLineEdit(self.tab_sfm_detector_image)
        self.lineEdit_sfm_detector_image_roi_bkg_y_bottom.setFont(font_ee)
        self.lineEdit_sfm_detector_image_roi_bkg_y_bottom.setGeometry(QtCore.QRect(275, 565, linedit_size_X, linedit_size_Y))
        self.lineEdit_sfm_detector_image_roi_bkg_y_bottom.setObjectName("lineEdit_sfm_detector_image_roi_bkg_y_bottom")
        self.lineEdit_sfm_detector_image_roi_bkg_y_bottom.setEnabled(False)
        self.lineEdit_sfm_detector_image_roi_bkg_y_bottom.setStyleSheet("color:rgb(0,0,0)")
        self.label_sfm_detector_image_roi_bkg_y_top = QtWidgets.QLabel(self.tab_sfm_detector_image)
        self.label_sfm_detector_image_roi_bkg_y_top.setFont(font_ee)
        self.label_sfm_detector_image_roi_bkg_y_top.setGeometry(QtCore.QRect(315, 565, 51, 16))
        self.label_sfm_detector_image_roi_bkg_y_top.setObjectName("label_sfm_detector_image_roi_bkg_y_top")
        self.label_sfm_detector_image_roi_bkg_y_top.setText("top")
        self.lineEdit_sfm_detector_image_roi_bkg_y_top = QtWidgets.QLineEdit(self.tab_sfm_detector_image)
        self.lineEdit_sfm_detector_image_roi_bkg_y_top.setFont(font_ee)
        self.lineEdit_sfm_detector_image_roi_bkg_y_top.setGeometry(QtCore.QRect(340, 565, linedit_size_X, linedit_size_Y))
        self.lineEdit_sfm_detector_image_roi_bkg_y_top.setObjectName("lineEdit_sfm_detector_image_roi_bkg_y_top")
        self.lineEdit_sfm_detector_image_roi_bkg_y_top.setEnabled(False)
        self.lineEdit_sfm_detector_image_roi_bkg_y_top.setStyleSheet("color:rgb(0,0,0)")

        self.tabWidget_single_file_mode.addTab(self.tab_sfm_detector_image, "")
        self.tabWidget_single_file_mode.setTabText(self.tabWidget_single_file_mode.indexOf(self.tab_sfm_detector_image), "Detector Image")

        # Tab: Reflectivity preview
        self.tab_sfm_reflectivity_preview = QtWidgets.QWidget()
        self.tab_sfm_reflectivity_preview.setObjectName("tab_sfm_reflectivity_preview")
        self.graphicsView_sfm_reflectivity_preview = pg.PlotWidget(self.tab_sfm_reflectivity_preview)
        self.graphicsView_sfm_reflectivity_preview.setGeometry(QtCore.QRect(0, 20, 577, 540))
        self.graphicsView_sfm_reflectivity_preview.setObjectName("graphicsView_sfm_reflectivity_preview")
        self.graphicsView_sfm_reflectivity_preview.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_sfm_reflectivity_preview.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_sfm_reflectivity_preview.getAxis("left").tickFont = font_graphs
        self.graphicsView_sfm_reflectivity_preview.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_sfm_reflectivity_preview.showAxis("top")
        self.graphicsView_sfm_reflectivity_preview.getAxis("top").tickFont = font_graphs_2
        self.graphicsView_sfm_reflectivity_preview.getAxis("top").setStyle(tickTextOffset=-2)
        self.graphicsView_sfm_reflectivity_preview.showAxis("right")
        self.graphicsView_sfm_reflectivity_preview.getAxis("right").tickFont = font_graphs_2
        self.graphicsView_sfm_reflectivity_preview.getAxis("right").setStyle(tickTextOffset=-2)
        self.checkBox_sfm_reflectivity_preview_show_overillumination = QtWidgets.QCheckBox(self.tab_sfm_reflectivity_preview)
        self.checkBox_sfm_reflectivity_preview_show_overillumination.setFont(font_ee)
        self.checkBox_sfm_reflectivity_preview_show_overillumination.setGeometry(QtCore.QRect(10, 7, 150, 18))
        self.checkBox_sfm_reflectivity_preview_show_overillumination.setObjectName("checkBox_sfm_reflectivity_preview_show_overillumination")
        self.checkBox_sfm_reflectivity_preview_show_overillumination.setText("Show Overillumination")
        self.comboBox_sfm_reflectivity_preview_plot_axis = QtWidgets.QComboBox(self.tab_sfm_reflectivity_preview)
        self.comboBox_sfm_reflectivity_preview_plot_axis.setFont(font_ee)
        self.comboBox_sfm_reflectivity_preview_plot_axis.setGeometry(QtCore.QRect(380, 7, 185, 20))
        self.comboBox_sfm_reflectivity_preview_plot_axis.setObjectName("comboBox_sfm_reflectivity_preview_plot_axis")
        self.comboBox_sfm_reflectivity_preview_plot_axis.addItem("Reflectivity (log) vs Angle (Qz)")
        self.comboBox_sfm_reflectivity_preview_plot_axis.addItem("Reflectivity (lin) vs Angle (Qz)")
        self.comboBox_sfm_reflectivity_preview_plot_axis.addItem("Reflectivity (log) vs Angle (deg)")
        self.comboBox_sfm_reflectivity_preview_plot_axis.addItem("Reflectivity (lin) vs Angle (deg)")
        self.checkBox_sfm_reflectivity_preview_incl_errorbars = QtWidgets.QCheckBox(self.tab_sfm_reflectivity_preview)
        self.checkBox_sfm_reflectivity_preview_incl_errorbars.setFont(font_ee)
        self.checkBox_sfm_reflectivity_preview_incl_errorbars.setGeometry(QtCore.QRect(10, 565, 111, 18))
        self.checkBox_sfm_reflectivity_preview_incl_errorbars.setObjectName("checkBox_sfm_reflectivity_preview_incl_errorbars")
        self.checkBox_sfm_reflectivity_preview_incl_errorbars.setText("Include Error Bars")
        self.label_sfm_reflectivity_preview_skip_points_left = QtWidgets.QLabel(self.tab_sfm_reflectivity_preview)
        self.label_sfm_reflectivity_preview_skip_points_left.setFont(font_ee)
        self.label_sfm_reflectivity_preview_skip_points_left.setGeometry(QtCore.QRect(372, 565, 100, 16))
        self.label_sfm_reflectivity_preview_skip_points_left.setObjectName("label_sfm_reflectivity_preview_skip_points_left")
        self.label_sfm_reflectivity_preview_skip_points_left.setText("Points to skip:  left")
        self.lineEdit_sfm_reflectivity_preview_skip_points_left = QtWidgets.QLineEdit(self.tab_sfm_reflectivity_preview)
        self.lineEdit_sfm_reflectivity_preview_skip_points_left.setFont(font_ee)
        self.lineEdit_sfm_reflectivity_preview_skip_points_left.setGeometry(QtCore.QRect(470, 565, linedit_size_X, linedit_size_Y))
        self.lineEdit_sfm_reflectivity_preview_skip_points_left.setObjectName("lineEdit_sfm_reflectivity_preview_skip_points_left")
        self.lineEdit_sfm_reflectivity_preview_skip_points_left.setText("0")
        self.label_sfm_reflectivity_preview_skip_points_right = QtWidgets.QLabel(self.tab_sfm_reflectivity_preview)
        self.label_sfm_reflectivity_preview_skip_points_right.setFont(font_ee)
        self.label_sfm_reflectivity_preview_skip_points_right.setGeometry(QtCore.QRect(510, 565, 80, 16))
        self.label_sfm_reflectivity_preview_skip_points_right.setObjectName("label_sfm_reflectivity_preview_skip_points_right")
        self.label_sfm_reflectivity_preview_skip_points_right.setText("right")
        self.lineEdit_sfm_reflectivity_preview_skip_points_right = QtWidgets.QLineEdit(self.tab_sfm_reflectivity_preview)
        self.lineEdit_sfm_reflectivity_preview_skip_points_right.setFont(font_ee)
        self.lineEdit_sfm_reflectivity_preview_skip_points_right.setGeometry(QtCore.QRect(535, 565, linedit_size_X, linedit_size_Y))
        self.lineEdit_sfm_reflectivity_preview_skip_points_right.setObjectName("lineEdit_sfm_reflectivity_preview_skip_points_right")
        self.lineEdit_sfm_reflectivity_preview_skip_points_right.setText("0")
        self.tabWidget_single_file_mode.addTab(self.tab_sfm_reflectivity_preview, "")
        self.tabWidget_single_file_mode.setTabText(self.tabWidget_single_file_mode.indexOf(self.tab_sfm_reflectivity_preview), "Reflectivity preview")

        # Tab: 2D Map
        self.tab_sfm_2dmap = QtWidgets.QWidget()
        self.tab_sfm_2dmap.setObjectName("tab_sfm_2dmap")
        # scaling options are different for different views
        # scale for "Pixel vs Points view" and "Alpha I vs Alpha f"
        self.label_sfm_2dmap_highlight = QtWidgets.QLabel(self.tab_sfm_2dmap)
        self.label_sfm_2dmap_highlight.setFont(font_ee)
        self.label_sfm_2dmap_highlight.setGeometry(QtCore.QRect(5, 8, 50, 16))
        self.label_sfm_2dmap_highlight.setObjectName("label_sfm_2dmap_highlight")
        self.label_sfm_2dmap_highlight.setText("Highlight")
        self.horizontalSlider_sfm_2dmap_highlight = QtWidgets.QSlider(self.tab_sfm_2dmap)
        self.horizontalSlider_sfm_2dmap_highlight.setGeometry(QtCore.QRect(55, 7, 190, 22))
        self.horizontalSlider_sfm_2dmap_highlight.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_sfm_2dmap_highlight.setObjectName("horizontalSlider_sfm_2dmap_highlight")
        self.horizontalSlider_sfm_2dmap_highlight.setMinimum(0)
        self.horizontalSlider_sfm_2dmap_highlight.setMaximum(1000)
        self.horizontalSlider_sfm_2dmap_highlight.setValue(40)
        # "scale" for "Qx vs Qz"
        self.label_sfm_2dmap_Qxz_threshold = QtWidgets.QLabel(self.tab_sfm_2dmap)
        self.label_sfm_2dmap_Qxz_threshold.setFont(font_ee)
        self.label_sfm_2dmap_Qxz_threshold.setGeometry(QtCore.QRect(5, 8, 220, 16))
        self.label_sfm_2dmap_Qxz_threshold.setObjectName("label_sfm_2dmap_Qxz_threshold")
        self.label_sfm_2dmap_Qxz_threshold.setText("Threshold for the view (number of neutrons):")
        self.label_sfm_2dmap_Qxz_threshold.setVisible(False)
        self.comboBox_sfm_2dmap_Qxz_threshold = QtWidgets.QComboBox(self.tab_sfm_2dmap)
        self.comboBox_sfm_2dmap_Qxz_threshold.setFont(font_ee)
        self.comboBox_sfm_2dmap_Qxz_threshold.setGeometry(QtCore.QRect(230, 7, 40, 20))
        self.comboBox_sfm_2dmap_Qxz_threshold.setObjectName("comboBox_sfm_2dmap_Qxz_threshold")
        self.comboBox_sfm_2dmap_Qxz_threshold.addItem("1")
        self.comboBox_sfm_2dmap_Qxz_threshold.addItem("2")
        self.comboBox_sfm_2dmap_Qxz_threshold.addItem("5")
        self.comboBox_sfm_2dmap_Qxz_threshold.addItem("10")
        self.comboBox_sfm_2dmap_Qxz_threshold.setVisible(False)
        self.label_sfm_2dmap_polarisation = QtWidgets.QLabel(self.tab_sfm_2dmap)
        self.label_sfm_2dmap_polarisation.setFont(font_ee)
        self.label_sfm_2dmap_polarisation.setGeometry(QtCore.QRect(284, 8, 71, 16))
        self.label_sfm_2dmap_polarisation.setObjectName("label_sfm_2dmap_polarisation")
        self.label_sfm_2dmap_polarisation.setText("Polarisation")
        self.comboBox_sfm_2dmap_polarisation = QtWidgets.QComboBox(self.tab_sfm_2dmap)
        self.comboBox_sfm_2dmap_polarisation.setFont(font_ee)
        self.comboBox_sfm_2dmap_polarisation.setGeometry(QtCore.QRect(344, 7, 40, 20))
        self.comboBox_sfm_2dmap_polarisation.setObjectName("comboBox_sfm_2dmap_polarisation")
        self.label_sfm_2dmap_axes = QtWidgets.QLabel(self.tab_sfm_2dmap)
        self.label_sfm_2dmap_axes.setFont(font_ee)
        self.label_sfm_2dmap_axes.setGeometry(QtCore.QRect(405, 8, 71, 16))
        self.label_sfm_2dmap_axes.setObjectName("label_sfm_2dmap_axes")
        self.label_sfm_2dmap_axes.setText("Axes")
        self.comboBox_sfm_2dmap_axes = QtWidgets.QComboBox(self.tab_sfm_2dmap)
        self.comboBox_sfm_2dmap_axes.setFont(font_ee)
        self.comboBox_sfm_2dmap_axes.setGeometry(QtCore.QRect(435, 7, 130, 20))
        self.comboBox_sfm_2dmap_axes.setObjectName("comboBox_sfm_2dmap_axes")
        self.comboBox_sfm_2dmap_axes.addItem("Pixel vs. Point")
        self.comboBox_sfm_2dmap_axes.addItem("Alpha_i vs. Alpha_f")
        self.comboBox_sfm_2dmap_axes.addItem("Qx vs. Qz")
        self.graphicsView_sfm_2dmap = pg.ImageView(self.tab_sfm_2dmap)
        self.graphicsView_sfm_2dmap.setGeometry(QtCore.QRect(0, 30, 577, 522))
        self.graphicsView_sfm_2dmap.setObjectName("graphicsView_sfm_2dmap")
        self.graphicsView_sfm_2dmap.ui.menuBtn.hide()
        self.graphicsView_sfm_2dmap.ui.roiBtn.hide()
        self.graphicsView_sfm_2dmap.ui.histogram.hide()
        colmap = pg.ColorMap(numpy.array([0.0,0.1,1.0]),
                             numpy.array([[0,0,0,255],[255,128,0,255],[255,255,0,255]], dtype=numpy.ubyte))
        self.graphicsView_sfm_2dmap.setColorMap(colmap)
        # 2D map for "Qx vs Qz" is a plot, compared to "Pixel vs Points" which is Image.
        # I rescale graphicsView_sfm_2dmap_Qxz_Theta to show/hide it
        self.graphicsView_sfm_2dmap_Qxz_Theta = pg.PlotWidget(self.tab_sfm_2dmap)
        self.graphicsView_sfm_2dmap_Qxz_Theta.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.graphicsView_sfm_2dmap_Qxz_Theta.setObjectName("graphicsView_sfm_2dmap_Qxz_Theta")
        self.graphicsView_sfm_2dmap_Qxz_Theta.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_sfm_2dmap_Qxz_Theta.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_sfm_2dmap_Qxz_Theta.getAxis("left").tickFont = font_graphs
        self.graphicsView_sfm_2dmap_Qxz_Theta.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_sfm_2dmap_Qxz_Theta.showAxis("top")
        self.graphicsView_sfm_2dmap_Qxz_Theta.getAxis("top").tickFont = font_graphs_2
        self.graphicsView_sfm_2dmap_Qxz_Theta.getAxis("top").setStyle(tickTextOffset=-2)
        self.graphicsView_sfm_2dmap_Qxz_Theta.showAxis("right")
        self.graphicsView_sfm_2dmap_Qxz_Theta.getAxis("right").tickFont = font_graphs_2
        self.graphicsView_sfm_2dmap_Qxz_Theta.getAxis("right").setStyle(tickTextOffset=-2)
        self.label_sfm_2dmap_Qxz_lower_number_of_points_by = QtWidgets.QLabel(self.tab_sfm_2dmap)
        self.label_sfm_2dmap_Qxz_lower_number_of_points_by.setFont(font_ee)
        self.label_sfm_2dmap_Qxz_lower_number_of_points_by.setGeometry(QtCore.QRect(5, 561, 211, 16))
        self.label_sfm_2dmap_Qxz_lower_number_of_points_by.setObjectName("label_sfm_2dmap_Qxz_lower_number_of_points_by")
        self.label_sfm_2dmap_Qxz_lower_number_of_points_by.setText("Lower the number of points by factor")
        self.label_sfm_2dmap_Qxz_lower_number_of_points_by.setVisible(False)
        self.comboBox_sfm_2dmap_Qxz_lower_number_of_points_by = QtWidgets.QComboBox(self.tab_sfm_2dmap)
        self.comboBox_sfm_2dmap_Qxz_lower_number_of_points_by.setFont(font_ee)
        self.comboBox_sfm_2dmap_Qxz_lower_number_of_points_by.setGeometry(QtCore.QRect(195, 560, 40, 20))
        self.comboBox_sfm_2dmap_Qxz_lower_number_of_points_by.setObjectName("comboBox_sfm_2dmap_Qxz_lower_number_of_points_by")
        self.comboBox_sfm_2dmap_Qxz_lower_number_of_points_by.addItem("5")
        self.comboBox_sfm_2dmap_Qxz_lower_number_of_points_by.addItem("4")
        self.comboBox_sfm_2dmap_Qxz_lower_number_of_points_by.addItem("3")
        self.comboBox_sfm_2dmap_Qxz_lower_number_of_points_by.addItem("2")
        self.comboBox_sfm_2dmap_Qxz_lower_number_of_points_by.addItem("1")
        self.comboBox_sfm_2dmap_Qxz_lower_number_of_points_by.setVisible(False)
        self.label_sfm_2dmap_rescale_image_x = QtWidgets.QLabel(self.tab_sfm_2dmap)
        self.label_sfm_2dmap_rescale_image_x.setFont(font_ee)
        self.label_sfm_2dmap_rescale_image_x.setGeometry(QtCore.QRect(5, 561, 80, 16))
        self.label_sfm_2dmap_rescale_image_x.setObjectName("label_sfm_2dmap_rescale_image_x")
        self.label_sfm_2dmap_rescale_image_x.setText("Rescale image: x")
        self.horizontalSlider_sfm_2dmap_rescale_image_x = QtWidgets.QSlider(self.tab_sfm_2dmap)
        self.horizontalSlider_sfm_2dmap_rescale_image_x.setGeometry(QtCore.QRect(90, 560, 80, 22))
        self.horizontalSlider_sfm_2dmap_rescale_image_x.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_sfm_2dmap_rescale_image_x.setObjectName("horizontalSlider_sfm_2dmap_rescale_image_x")
        self.horizontalSlider_sfm_2dmap_rescale_image_x.setMinimum(1)
        self.horizontalSlider_sfm_2dmap_rescale_image_x.setMaximum(15)
        self.horizontalSlider_sfm_2dmap_rescale_image_x.setValue(1)
        self.label_sfm_2dmap_rescale_image_y = QtWidgets.QLabel(self.tab_sfm_2dmap)
        self.label_sfm_2dmap_rescale_image_y.setFont(font_ee)
        self.label_sfm_2dmap_rescale_image_y.setGeometry(QtCore.QRect(180, 561, 20, 16))
        self.label_sfm_2dmap_rescale_image_y.setObjectName("label_sfm_2dmap_rescale_image_y")
        self.label_sfm_2dmap_rescale_image_y.setText("y")
        self.horizontalSlider_sfm_2dmap_rescale_image_y = QtWidgets.QSlider(self.tab_sfm_2dmap)
        self.horizontalSlider_sfm_2dmap_rescale_image_y.setGeometry(QtCore.QRect(190, 560, 80, 22))
        self.horizontalSlider_sfm_2dmap_rescale_image_y.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_sfm_2dmap_rescale_image_y.setObjectName("horizontalSlider_sfm_2dmap_rescale_image_y")
        self.horizontalSlider_sfm_2dmap_rescale_image_y.setMinimum(1)
        self.horizontalSlider_sfm_2dmap_rescale_image_y.setMaximum(15)
        self.horizontalSlider_sfm_2dmap_rescale_image_y.setValue(1)
        self.pushButton_sfm_2dmap_export = QtWidgets.QPushButton(self.tab_sfm_2dmap)
        self.pushButton_sfm_2dmap_export.setGeometry(QtCore.QRect(445, 555, 120, 25))
        self.pushButton_sfm_2dmap_export.setFont(font_button)
        self.pushButton_sfm_2dmap_export.setObjectName("pushButton_sfm_2dmap_export")
        self.pushButton_sfm_2dmap_export.setText("Export 2D map")
        self.tabWidget_single_file_mode.addTab(self.tab_sfm_2dmap, "")
        self.tabWidget_single_file_mode.setTabText(self.tabWidget_single_file_mode.indexOf(self.tab_sfm_2dmap), "2D map")

        # StatusBar
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # MenuBar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 21))
        self.menubar.setObjectName("menu_bar")
        self.menu_help = QtWidgets.QMenu(self.menubar)
        self.menu_help.setObjectName("menu_help")
        self.menu_help.setTitle("Help")
        MainWindow.setMenuBar(self.menubar)
        self.action_algorithm_info = QtWidgets.QAction(MainWindow)
        self.action_algorithm_info.setObjectName("action_algorithm_info")
        self.action_algorithm_info.setText("Algorithm info")
        self.action_version = QtWidgets.QAction(MainWindow)
        self.action_version.setObjectName("action_version")
        self.menu_help.addAction(self.action_algorithm_info)
        self.menu_help.addAction(self.action_version)
        self.action_version.setText("Version 1.4")
        self.menubar.addAction(self.menu_help.menuAction())

        self.tabWidget_settings_re_in_ex.setCurrentIndex(0)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    ##<--

class GUI(Ui_MainWindow):

    current_dir = os.getcwd().replace("\\", "/") + "/"

    def __init__(self):

        super(GUI, self).__init__()
        self.setupUi(self)

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

        # Actions on clicks
        self.pushButton_import_scans.clicked.connect(self.button_import_remove_scans)
        self.pushButton_delete_scans.clicked.connect(self.button_import_remove_scans)
        self.pushButton_import_db.clicked.connect(self.button_import_remove_db)
        self.pushButton_delete_db.clicked.connect(self.button_import_remove_db)
        self.toolButton_save_at.clicked.connect(self.button_SaveDir)
        self.pushButton_reduce_all.clicked.connect(self.button_reduce_all)
        self.pushButton_reduce_sfm_scan.clicked.connect(self.button_reduce_sfm_scan)
        self.pushButton_clear.clicked.connect(self.button_Clear)
        self.pushButton_sfm_2dmap_export.clicked.connect(self.export_2d_map)


        self.lineEdit_sfm_detector_image_roi_x_left.editingFinished.connect(self.update_slits)
        self.lineEdit_sfm_detector_image_roi_x_right.editingFinished.connect(self.update_slits)
        self.lineEdit_sfm_detector_image_roi_y_bottom.editingFinished.connect(self.update_slits)
        self.lineEdit_sfm_detector_image_roi_y_top.editingFinished.connect(self.update_slits)
        self.lineEdit_sfm_detector_image_roi_bkg_x_right.editingFinished.connect(self.update_slits)

        self.pushButton_sfm_detector_image_show_int_roi.clicked.connect(self.draw_det_image)
        self.comboBox_sfm_detector_image_point_number.currentIndexChanged.connect(self.draw_det_image)
        self.comboBox_sfm_detector_image_polarisation.currentIndexChanged.connect(self.draw_det_image)

        self.comboBox_single_file_mode_scan.currentIndexChanged.connect(self.load_detector_images)

        self.comboBox_single_file_mode_scan.currentIndexChanged.connect(self.load_reflectivity_preview)
        self.lineEdit_sample_len.editingFinished.connect(self.load_reflectivity_preview)
        self.checkBox_red_devide_by_monitor.stateChanged.connect(self.load_reflectivity_preview)
        self.checkBox_red_normalize_by_db.stateChanged.connect(self.load_reflectivity_preview)
        self.checkBox_red_db_attenuator.stateChanged.connect(self.load_reflectivity_preview)
        self.lineEdit_red_db_attenuator_factor.editingFinished.connect(self.load_reflectivity_preview)
        self.checkBox_red_overillumination_correction.stateChanged.connect(self.load_reflectivity_preview)
        self.lineEdit_red_subtract_bkg_skip.editingFinished.connect(self.load_reflectivity_preview)
        self.checkBox_red_subtract_bkg.stateChanged.connect(self.load_reflectivity_preview)
        self.checkBox_sfm_reflectivity_preview_show_overillumination.stateChanged.connect(self.load_reflectivity_preview)
        self.checkBox_sfm_reflectivity_preview_incl_errorbars.stateChanged.connect(self.load_reflectivity_preview)
        self.lineEdit_instr_wavelength.editingFinished.connect(self.load_reflectivity_preview)
        self.lineEdit_instr_wavelength_resolution.editingFinished.connect(self.load_reflectivity_preview)
        self.lineEdit_instr_s1_to_sample_dist.editingFinished.connect(self.load_reflectivity_preview)
        self.lineEdit_instr_s2_to_sample_dist.editingFinished.connect(self.load_reflectivity_preview)
        self.lineEdit_instr_full_scan_offset.editingFinished.connect(self.load_reflectivity_preview)
        self.lineEdit_sfm_reflectivity_preview_skip_points_right.editingFinished.connect(self.load_reflectivity_preview)
        self.lineEdit_sfm_reflectivity_preview_skip_points_left.editingFinished.connect(self.load_reflectivity_preview)
        self.checkBox_db_rearr_after.stateChanged.connect(self.load_reflectivity_preview)
        self.comboBox_sfm_reflectivity_preview_plot_axis.currentIndexChanged.connect(self.load_reflectivity_preview)

        self.comboBox_sfm_2dmap_Qxz_threshold.currentIndexChanged.connect(self.draw_2D_map)
        self.comboBox_sfm_2dmap_polarisation.currentIndexChanged.connect(self.draw_2D_map)
        self.horizontalSlider_sfm_2dmap_highlight.valueChanged.connect(self.draw_2D_map)
        self.horizontalSlider_sfm_2dmap_rescale_image_x.valueChanged.connect(self.draw_2D_map)
        self.horizontalSlider_sfm_2dmap_rescale_image_y.valueChanged.connect(self.draw_2D_map)
        self.comboBox_sfm_2dmap_axes.currentIndexChanged.connect(self.draw_2D_map)
        self.comboBox_single_file_mode_scan.currentIndexChanged.connect(self.draw_2D_map)
        self.lineEdit_instr_wavelength.editingFinished.connect(self.draw_2D_map)
        self.lineEdit_instr_sample_to_det_dist.editingFinished.connect(self.draw_2D_map)
        self.comboBox_sfm_2dmap_Qxz_lower_number_of_points_by.currentIndexChanged.connect(self.draw_2D_map)

        self.checkBox_db_rearr_after.stateChanged.connect(self.db_assign)

        self.action_version.triggered.connect(self.menu_info)
        self.action_algorithm_info.triggered.connect(self.menu_algorithm)

        self.comboBox_sfm_detector_image_color_scheme.currentIndexChanged.connect(self.color_det_image)

    ##--> Main window buttons
    def button_import_remove_scans(self):

        if self.sender().objectName() == "pushButton_import_scans":

            import_files = QtWidgets.QFileDialog().getOpenFileNames(None, "FileNames", self.current_dir, ".h5 (*.h5)")
            if import_files[0] == []: return
            # Next "Import scans" will open last dir
            self.current_dir = import_files[0][0][:import_files[0][0].rfind("/")]

            for FILE in import_files[0]:
                self.tableWidget_scans.insertRow(self.tableWidget_scans.rowCount())
                self.tableWidget_scans.setRowHeight(self.tableWidget_scans.rowCount()-1, 10)
                # File name (row 0) and full path (row 2)
                for j in range(0, 3):
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget_scans.setItem(self.tableWidget_scans.rowCount()-1, j, item)
                self.tableWidget_scans.item(self.tableWidget_scans.rowCount() - 1, 0).setText(FILE[FILE.rfind("/") + 1:])
                self.tableWidget_scans.item(self.tableWidget_scans.rowCount() - 1, 2).setText(FILE)

                # add file into SFM / Scan ComboBox
                self.comboBox_single_file_mode_scan.addItem(str(FILE[FILE.rfind("/") + 1:]))

                self.db_analaze()

                self.load_reflectivity_preview()

        if self.sender().objectName() == "pushButton_delete_scans":

            remove_files = self.tableWidget_scans.selectedItems()
            if not remove_files: return

            for FILE in remove_files:
                self.tableWidget_scans.removeRow(self.tableWidget_scans.row(FILE))

            # update SFM list
            self.comboBox_single_file_mode_scan.clear()

            for i in range(0, self.tableWidget_scans.rowCount()):
                # add file into SFM
                self.comboBox_single_file_mode_scan.addItem(self.tableWidget_scans.item(i, 2).text()[
                            self.tableWidget_scans.item(i, 2).text().rfind("/") + 1:])

    def button_import_remove_db(self):

        if self.sender().objectName() == "pushButton_import_db":

            import_files = QtWidgets.QFileDialog().getOpenFileNames(None, "FileNames", self.current_dir, ".h5 (*.h5)")
            if import_files[0] == []: return
            # Next "Import scans" will open last dir
            self.current_dir = import_files[0][0][:import_files[0][0].rfind("/")]

            # I couldnt make tablewidget sorting work when adding files to not empty table, so this is the solution for making the list of DB files sorted
            for i in range(self.tableWidget_db.rowCount()-1, -1, -1):
                import_files[0].append(self.tableWidget_db.item(i, 1).text())
                self.tableWidget_db.removeRow(i)

            for FILE in sorted(import_files[0]):
                self.tableWidget_db.insertRow(self.tableWidget_db.rowCount())
                self.tableWidget_db.setRowHeight(self.tableWidget_db.rowCount()-1, 10)
                # File name (row 0) and full path (row 2)
                for j in range(0, 2):
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget_db.setItem(self.tableWidget_db.rowCount()-1, j, item)
                self.tableWidget_db.item(self.tableWidget_db.rowCount() - 1, 0).setText(FILE[FILE.rfind("/") + 1:])
                self.tableWidget_db.item(self.tableWidget_db.rowCount() - 1, 1).setText(FILE)

            self.db_analaze()
            self.load_reflectivity_preview()

        elif self.sender().objectName() == "pushButton_delete_db":

            remove_files = self.tableWidget_db.selectedItems()
            if not remove_files: return

            for FILE in remove_files:
                self.tableWidget_db.removeRow(self.tableWidget_db.row(FILE))

            self.db_analaze()

    def button_SaveDir(self):

        saveAt = QtWidgets.QFileDialog().getExistingDirectory()
        if not saveAt: return

        self.lineEdit_save_at.setText(str(saveAt))
        if not str(saveAt)[-1] == "/": self.lineEdit_save_at.setText(str(saveAt) + "/")

    def button_reduce_all(self):

        self.listWidget_recheck_files_in_sfm.clear()

        if self.lineEdit_red_subtract_bkg_skip.text(): skip_bkg = float(self.lineEdit_red_subtract_bkg_skip.text())
        else: skip_bkg = 0

        if self.lineEdit_save_at.text():  save_file_directory = self.lineEdit_save_at.text()
        else: save_file_directory = self.current_dir

        if self.checkBox_red_overillumination_correction.isChecked() and self.lineEdit_sample_len.text() == "":
            self.statusbar.showMessage("Sample length is missing")
            return
        else:
            sample_len = 999
            if self.lineEdit_sample_len.text(): sample_len = self.lineEdit_sample_len.text()

        if self.checkBox_red_normalize_by_db.isChecked():
            if self.tableWidget_db.rowCount() == 0:
                self.label_error_db_missing.setVisible(True)
                return

            if self.checkBox_red_db_attenuator.isChecked():
                db_atten_factor = 10.4
                if not self.lineEdit_red_db_attenuator_factor.text() == "":
                    db_atten_factor = float(self.lineEdit_red_db_attenuator_factor.text())
            else:
                db_atten_factor = 1

        # iterate through table with scans
        for i in range(0, self.tableWidget_scans.rowCount()):
            file_name = self.tableWidget_scans.item(i, 2).text()[
                        self.tableWidget_scans.item(i, 2).text().rfind("/") + 1: -3]

            # find full name DB file if there are several of them
            if self.checkBox_red_normalize_by_db.isChecked(): FILE_DB = self.tableWidget_scans.item(i, 1).text()
            else: FILE_DB = ""

            with h5py.File(self.tableWidget_scans.item(i, 2).text(), 'r') as FILE:

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

                        if Intens == 0 and self.checkBox_export_remove_zeros.isChecked(): continue

                        if Intens == 0: Intens_err = 1
                        else: Intens_err = numpy.sqrt(Intens)

                        # read motors
                        Qz = (4 * numpy.pi / float(self.lineEdit_instr_wavelength.text())) * numpy.sin(numpy.radians(th))
                        s1hg = s1hg_list[index]
                        s2hg = s2hg_list[index]
                        monitor = monitor_list[index]

                        # check if we are not in a middle of ROI in Qz approx 0.02)
                        if round(Qz, 3) > 0.015 and round(Qz, 3) < 0.03 and check_this_file == 0:
                            scan_data_0_015 = scan_intens[index][int(original_roi_coord[2]): int(original_roi_coord[3])]

                            if not max(scan_data_0_015) == max(scan_data_0_015[round((len(scan_data_0_015) / 3)):-round(
                                    (len(scan_data_0_015) / 3))]):
                                self.listWidget_recheck_files_in_sfm.addItem(file_name)
                                check_this_file = 1

                        coeff = self.overillumination_correct_coeff(s1hg, s2hg, round(th, 4))
                        FWHM_proj = coeff[1]

                        if not self.checkBox_red_overillumination_correction.isChecked():
                            overill_corr = 1
                        else:
                            overill_corr = coeff[0]

                        # calculate resolution in Sared way or better
                        if self.checkBox_export_resolution_like_sared.isChecked():
                            Resolution = numpy.sqrt(((2 * numpy.pi / float(self.lineEdit_instr_wavelength.text())) ** 2) * (
                                    (numpy.cos(numpy.radians(th))) ** 2) * (0.68 ** 2) * ((s1hg ** 2) + (s2hg ** 2)) / (
                                                                (float(
                                                                    self.lineEdit_instr_s1_to_sample_dist.text()) - float(
                                                                    self.lineEdit_instr_s2_to_sample_dist.text())) ** 2) + (
                                                            (float(self.lineEdit_instr_wavelength_resolution.text()) ** 2) * (Qz ** 2)))
                        else:
                            if FWHM_proj == s2hg:
                                Resolution = numpy.sqrt(
                                    ((2 * numpy.pi / float(self.lineEdit_instr_wavelength.text())) ** 2) * (
                                            (numpy.cos(numpy.radians(th))) ** 2) * (0.68 ** 2) * (
                                                (s1hg ** 2) + (s2hg ** 2)) / ((float(
                                        self.lineEdit_instr_s1_to_sample_dist.text()) - float(
                                        self.lineEdit_instr_s2_to_sample_dist.text())) ** 2) + (
                                                (float(self.lineEdit_instr_wavelength_resolution.text()) ** 2) * (Qz ** 2)))
                            else:
                                Resolution = numpy.sqrt(
                                    ((2 * numpy.pi / float(self.lineEdit_instr_wavelength.text())) ** 2) * (
                                            (numpy.cos(numpy.radians(th))) ** 2) * (0.68 ** 2) * (
                                            (s1hg ** 2) + (FWHM_proj ** 2)) / (
                                            float(self.lineEdit_instr_s1_to_sample_dist.text()) ** 2) + (
                                            (float(self.lineEdit_instr_wavelength_resolution.text()) ** 2) * (Qz ** 2)))

                        # I cite Gunnar in here "We are now saving dQ as sigma rather than FWHM for genx"
                        Resolution = Resolution / (2 * numpy.sqrt(2 * numpy.log(2)))

                        # minus background, devide by monitor, overillumination correct + calculate errors
                        if self.checkBox_red_subtract_bkg.isChecked() and Qz > skip_bkg:
                            Intens_bkg = sum(scan_intens[index][
                                             int(original_roi_coord[2]) - 2 * (int(original_roi_coord[3]) - int(original_roi_coord[2])): int(original_roi_coord[2]) - (
                                                         int(original_roi_coord[3]) - int(original_roi_coord[2]))])

                            if Intens_bkg > 0:
                                Intens_err = numpy.sqrt(Intens + Intens_bkg)
                                Intens = Intens - Intens_bkg

                        if self.checkBox_red_devide_by_monitor.isChecked():
                            if Intens == 0: Intens_err = Intens_err / monitor
                            else: Intens_err = (Intens / monitor) * numpy.sqrt((Intens_err / Intens) ** 2 + (1 / monitor))
                            Intens = Intens / monitor

                        if self.checkBox_red_overillumination_correction.isChecked():
                            Intens_err = Intens_err / overill_corr
                            Intens = Intens / overill_corr

                        if self.checkBox_red_normalize_by_db.isChecked():
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
                                    self.listWidget_recheck_files_in_sfm.addItem(file_name)
                                    check_this_file = 1

                        # skip first point
                        if index == 1: continue

                        if Intens == 0 and self.checkBox_export_remove_zeros.isChecked(): continue

                        new_file.write(str(Qz) + ' ' + str(Intens) + ' ' + str(Intens_err) + ' ')
                        if self.checkBox_export_add_resolution_column.isChecked(): new_file.write(str(Resolution))
                        new_file.write('\n')

                    # close files
                    new_file.close()

                    # check if file is empty - then comment inside
                    if os.stat(save_file_directory + file_name + "_" + str(detector) + " (" + FILE_DB + ")" + ".dat").st_size == 0:
                        with open(save_file_directory + file_name + "_" + str(detector) + " (" + FILE_DB + ")" + ".dat", "w") as empty_file:
                            empty_file.write("All points are either zeros or negatives.")

        self.statusbar.showMessage(str(self.tableWidget_scans.rowCount()) + " files reduced, " + str(
            self.listWidget_recheck_files_in_sfm.count()) + " file(s) might need extra care.")

    def button_reduce_sfm_scan(self):

        if self.lineEdit_save_at.text(): save_file_directory = self.lineEdit_save_at.text()
        else: save_file_directory = self.current_dir

        # polarisation order - uu, dd, ud, du
        detector = ["uu", "du", "ud", "dd"]

        for i in range(0, len(self.sfm_export_Qz)):

            if self.checkBox_red_normalize_by_db.isChecked():
                sfm_db_file_export = self.SFM_DB_FILE
            else: sfm_db_file_export = ""

            with open(save_file_directory + self.SFM_FILE[self.SFM_FILE.rfind("/") + 1 : -3] + "_" + str(detector[i]) + " (" + sfm_db_file_export + ")" + " SFM.dat", "w") as new_file:
                for j in range(0, len(self.sfm_export_Qz[i])):
                    if self.sfm_export_Qz[i][j] == 0: continue
                    if self.sfm_export_I[i][j] == 0 and self.checkBox_export_remove_zeros.isChecked(): continue
                    new_file.write(str(self.sfm_export_Qz[i][j]) + ' ' + str(self.sfm_export_I[i][j]) + ' ' + str(self.sfm_export_dI[i][j]) + ' ')
                    if self.checkBox_export_add_resolution_column.isChecked(): new_file.write(str(self.sfm_export_Resolution[i][j]))
                    new_file.write('\n')

            # close new file
            new_file.close()

        self.statusbar.showMessage(self.SFM_FILE[self.SFM_FILE.rfind("/") + 1:] + " file is reduced in SFM.")

    def button_Clear(self):

        self.comboBox_single_file_mode_scan.clear()
        self.listWidget_recheck_files_in_sfm.clear()
        self.graphicsView_sfm_detector_image.clear()
        self.graphicsView_sfm_2dmap.clear()
        self.graphicsView_sfm_reflectivity_preview.getPlotItem().clear()
        self.comboBox_sfm_detector_image_point_number.clear()
        self.comboBox_sfm_detector_image_polarisation.clear()
        self.comboBox_sfm_2dmap_polarisation.clear()
        for i in range(self.tableWidget_scans.rowCount(), -1, -1):
            self.tableWidget_scans.removeRow(i)
        for i in range(self.tableWidget_db.rowCount(), -1, -1):
            self.tableWidget_db.removeRow(i)
    ##<--

    ##--> extra functions to shorten the code
    def overillumination_correct_coeff(self, s1hg, s2hg, th):

        # Check for Sample Length input
        try:
            sample_len = float(self.lineEdit_sample_len.text())
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
                OB = ((float(self.lineEdit_instr_s1_to_sample_dist.text()) * (s2hg - s1hg)) / (2 * (float(self.lineEdit_instr_s1_to_sample_dist.text()) - float(self.lineEdit_instr_s2_to_sample_dist.text())))) + s1hg / 2
                OC = ((float(self.lineEdit_instr_s1_to_sample_dist.text()) * (s2hg + s1hg)) / (2 * (float(self.lineEdit_instr_s1_to_sample_dist.text()) - float(self.lineEdit_instr_s2_to_sample_dist.text())))) - s1hg / 2
            elif s1hg < s2hg:
                OB = ((s2hg * float(self.lineEdit_instr_s1_to_sample_dist.text())) - (s1hg * float(self.lineEdit_instr_s2_to_sample_dist.text()))) / (2 * (float(self.lineEdit_instr_s1_to_sample_dist.text()) - float(self.lineEdit_instr_s2_to_sample_dist.text())))
                OC = (float(self.lineEdit_instr_s1_to_sample_dist.text()) / (float(self.lineEdit_instr_s1_to_sample_dist.text()) - float(self.lineEdit_instr_s2_to_sample_dist.text()))) * (s2hg + s1hg) / 2 - (s1hg / 2)
            elif s1hg == s2hg:
                OB = s1hg / 2
                OC = s1hg * (float(self.lineEdit_instr_s1_to_sample_dist.text()) / (float(self.lineEdit_instr_s1_to_sample_dist.text()) - float(self.lineEdit_instr_s2_to_sample_dist.text())) - 1 / 2)

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

        for i in range(0, self.tableWidget_db.rowCount()):
            with h5py.File(self.tableWidget_db.item(i,1).text(), 'r') as FILE_DB:
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
                    if "'mon0'" in str(scaler):
                        monitor_list = SCALERS_DATA[index]
                    elif "'roi'" in str(scaler):
                        intens_list = SCALERS_DATA[index]

                for j in range(0, len(th_list)):
                    db_intens = float(intens_list[j]) / float(monitor_list[j])
                    db_err = db_intens * numpy.sqrt(1/float(intens_list[j]) + 1/float(monitor_list[j]))

                    scan_and_slits = self.tableWidget_db.item(i, 0).text()[:5] + ";" + str(s1hg_list[j]) + ";" + str(s2hg_list[j])

                    self.DB_INFO[scan_and_slits] = str(db_intens) + ";" + str(db_err)

        if self.tableWidget_db.rowCount() == 0:
            return
        else: self.db_assign()

    def db_assign(self):
        db_list = []
        for db_scan_number in self.DB_INFO: db_list.append(db_scan_number.split(";")[0])

        for i in range(self.tableWidget_scans.rowCount()):
            scan_number = self.tableWidget_scans.item(i, 0).text()[:5]

            # find nearest DB file if there are several of them
            if len(db_list) == 0: FILE_DB = ""
            elif len(db_list) == 1: FILE_DB = db_list[0][:5]
            else:
                if self.checkBox_db_rearr_after.isChecked():
                    for j, db_scan in enumerate(db_list):
                        FILE_DB = db_scan[:5]
                        if int(db_scan[:5]) > int(scan_number[:5]): break
                else:
                    for j, db_scan in enumerate(reversed(db_list)):
                        FILE_DB = db_scan[:5]
                        if int(db_scan[:5]) < int(scan_number[:5]): break

            self.tableWidget_scans.item(i, 1).setText(FILE_DB)
    ##<--

    ##--> menu options
    def menu_info(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowIcon(QtGui.QIcon(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "\icon.png"))
        msgBox.setText( "pySAred. " + self.action_version.text() + "\n\n"
                        "Alexey.Klechikov@gmail.com\n\n"                                                                     
                        "Check new version at https://github.com/Alexey-Klechikov/pySAred/releases")
        msgBox.exec_()

    def menu_algorithm(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowIcon(QtGui.QIcon(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "\icon.png"))
        msgBox.setText( "1) Area for background estimation is automatically set to the same size as ROI.\n\n"
                        "2) File can appear in \"Recheck following files in Single File Mode\" if peak of its intensity (around Qz 0.015) is not in the middle of ROI.\n\n"
                        "3) Trapezoid beam form is used for overillumination correction.\n\n"
                        "4) Files are exported as Qz, I, dI, (dQz)\n\n"
                        "5) If there are more than 1 DB file, the one with nearest lower scan number will be used for reduction\n\n"
                        "6) Button 'Reduce all' will export all Data files with no changes applied in SFM block. \n\n"
                        )

        msgBox.exec_()
    ##<--

    ##--> SFM
    def load_detector_images(self):

        if self.comboBox_single_file_mode_scan.currentText() == "": return

        self.comboBox_sfm_detector_image_point_number.clear()
        self.comboBox_sfm_detector_image_polarisation.clear()
        self.comboBox_sfm_2dmap_polarisation.clear()

        # we need to find full path for the SFM file from the table
        for i in range(0, self.tableWidget_scans.rowCount()):
            if self.tableWidget_scans.item(i, 0).text() == self.comboBox_single_file_mode_scan.currentText():
                self.SFM_FILE = self.tableWidget_scans.item(i, 2).text()
                #self.sfm_file_scan_num = int(self.tableWidget_scans.item(i, 0).text()[:5])

        with h5py.File(self.SFM_FILE, 'r') as FILE:

            SCAN = FILE[list(FILE.keys())[0]]
            original_roi_coord = numpy.array(SCAN.get("instrument").get('scalers').get('roi').get("roi"))
            roi_width = int(original_roi_coord[3]) - int(original_roi_coord[2])

            self.lineEdit_sfm_detector_image_roi_x_left.setText(str(original_roi_coord[2])[:-2])
            self.lineEdit_sfm_detector_image_roi_x_right.setText(str(original_roi_coord[3])[:-2])
            self.lineEdit_sfm_detector_image_roi_y_bottom.setText(str(original_roi_coord[1])[:-2])
            self.lineEdit_sfm_detector_image_roi_y_top.setText(str(original_roi_coord[0])[:-2])
            self.lineEdit_sfm_detector_image_roi_bkg_x_left.setText(str(int(original_roi_coord[2]) - 2 * roi_width))
            self.lineEdit_sfm_detector_image_roi_bkg_x_right.setText(str(int(original_roi_coord[2]) - roi_width))
            self.lineEdit_sfm_detector_image_roi_bkg_y_bottom.setText(str(original_roi_coord[1])[:-2])
            self.lineEdit_sfm_detector_image_roi_bkg_y_top.setText(str(original_roi_coord[0])[:-2])

            for index, th in enumerate(SCAN.get("instrument").get('motors').get('th').get("value")):
                if str(th)[0:5] in ("-0.00", "0.00"): continue

                self.comboBox_sfm_detector_image_point_number.addItem(str(round(th, 3)))

            if len(SCAN.get("ponos").get('data')) == 1:
                self.comboBox_sfm_detector_image_polarisation.addItem("uu")
                self.comboBox_sfm_2dmap_polarisation.addItem("uu")
            for polarisation in SCAN.get("ponos").get('data'):
                if polarisation not in ("data_du", "data_uu", "data_dd", "data_ud"): continue
                if numpy.any(numpy.array(SCAN.get("ponos").get('data').get(polarisation))):
                    self.comboBox_sfm_detector_image_polarisation.addItem(str(polarisation)[-2:])
                    self.comboBox_sfm_2dmap_polarisation.addItem(str(polarisation)[-2:])

            self.comboBox_sfm_detector_image_polarisation.setCurrentIndex(0)
            self.comboBox_sfm_2dmap_polarisation.setCurrentIndex(0)

    def draw_det_image(self):

        if self.comboBox_sfm_detector_image_polarisation.currentText() == "" or self.comboBox_sfm_detector_image_point_number.currentText() == "": return

        self.graphicsView_sfm_detector_image.clear()
        self.graphicsView_sfm_detector_roi.clear()

        if self.SFM_FILE == "": return
        with h5py.File(self.SFM_FILE, 'r') as FILE:

            self.current_th = self.comboBox_sfm_detector_image_point_number.currentText()

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
                else: scan_psd = "psd_" + self.comboBox_sfm_detector_image_polarisation.currentText()

            detector_images = INSTRUMENT.get('detectors').get(scan_psd).get('data')

            for index, th in enumerate(self.th_list):
                # check th
                if self.current_th == str(round(th, 3)):
                    self.lineEdit_sfm_detector_image_slits_s1hg.setText(str(self.s1hg_list[index]))
                    self.lineEdit_sfm_detector_image_slits_s2hg.setText(str(self.s2hg_list[index]))
                    self.lineEdit_sfm_detector_image_time.setText(str(time_list[index]))

                    # seems to be a bug in numpy arrays imported from hdf5 files. Problem is solved after I subtract ZEROs array with the same dimentions.
                    detector_image = detector_images[index]
                    detector_image = numpy.around(detector_image, decimals=0).astype(int)
                    detector_image = numpy.subtract(detector_image, numpy.zeros((detector_image.shape[0], detector_image.shape[1])))
                    # integrate detector image with respect to ROI Y coordinates
                    detector_image_int = detector_image[int(self.lineEdit_sfm_detector_image_roi_y_top.text()): int(self.lineEdit_sfm_detector_image_roi_y_bottom.text()), :].sum(axis=0).astype(int)

                    self.graphicsView_sfm_detector_image.setImage(detector_image, axes={'x':1, 'y':0}, levels=(0,0.1))
                    self.graphicsView_sfm_detector_roi.addItem(pg.PlotCurveItem(y = detector_image_int, pen=pg.mkPen(color=(0, 0, 0), width=2), brush=pg.mkBrush(color=(255, 0, 0), width=3)))

                    if self.comboBox_sfm_detector_image_color_scheme.currentText() == "White / Black":
                        self.color_det_image = numpy.array([[0, 0, 0, 255], [255, 255, 255, 255], [255, 255, 255, 255]],
                                                        dtype=numpy.ubyte)
                    elif self.comboBox_sfm_detector_image_color_scheme.currentText() == "Green / Blue":
                        self.color_det_image = numpy.array([[0, 0, 255, 255], [255, 0, 0, 255], [0, 255, 0, 255]],
                                                           dtype=numpy.ubyte)
                    pos = numpy.array([0.0, 0.1, 1.0])

                    colmap = pg.ColorMap(pos, self.color_det_image)
                    self.graphicsView_sfm_detector_image.setColorMap(colmap)

                    # add ROI rectangular
                    spots_ROI_det_view = []
                    spots_ROI_det_int = []
                    if self.draw_roi:
                        self.graphicsView_sfm_detector_image.removeItem(self.draw_roi)

                    for i in range(int(self.lineEdit_sfm_detector_image_roi_y_top.text()), int(self.lineEdit_sfm_detector_image_roi_y_bottom.text())):
                        spots_ROI_det_view.append({'x': int(self.lineEdit_sfm_detector_image_roi_x_left.text()), 'y': i})
                        spots_ROI_det_view.append({'x': int(self.lineEdit_sfm_detector_image_roi_x_right.text()), 'y': i})

                    for i in range(int(self.lineEdit_sfm_detector_image_roi_x_left.text()), int(self.lineEdit_sfm_detector_image_roi_x_right.text())):
                        spots_ROI_det_view.append({'x': i, 'y': int(self.lineEdit_sfm_detector_image_roi_y_bottom.text())})
                        spots_ROI_det_view.append({'x': i, 'y': int(self.lineEdit_sfm_detector_image_roi_y_top.text())})

                    self.draw_roi = pg.ScatterPlotItem(spots=spots_ROI_det_view, size=0.5, pen=pg.mkPen(255, 255, 255))
                    self.graphicsView_sfm_detector_image.addItem(self.draw_roi)

                    if self.draw_roi_int:
                        self.graphicsView_sfm_detector_roi.removeItem(self.draw_roi_int)

                    for i in range(0, detector_image_int.max()):
                        spots_ROI_det_int.append({'x': int(self.lineEdit_sfm_detector_image_roi_x_left.text()), 'y': i})
                        spots_ROI_det_int.append({'x': int(self.lineEdit_sfm_detector_image_roi_x_right.text()), 'y': i})

                    self.draw_roi_int = pg.ScatterPlotItem(spots=spots_ROI_det_int, size=1, pen=pg.mkPen(255, 0, 0))
                    self.graphicsView_sfm_detector_roi.addItem(self.draw_roi_int)

                    break

        # Show "integrated roi" part
        if self.sender().objectName() == "pushButton_sfm_detector_image_show_int_roi":

            if self.show_det_int_trigger:
                self.graphicsView_sfm_detector_image.setGeometry(QtCore.QRect(0, 30, 577, 420))
                self.show_det_int_trigger = False
            else:
                self.graphicsView_sfm_detector_image.setGeometry(QtCore.QRect(0, 30, 577, 510))
                self.show_det_int_trigger = True

    def load_reflectivity_preview(self):

        self.graphicsView_sfm_reflectivity_preview.getPlotItem().clear()
        skip_bkg = 0

        self.sfm_export_Qz = []
        self.sfm_export_I = []
        self.sfm_export_dI = []
        self.sfm_export_Resolution = []

        if self.comboBox_single_file_mode_scan.currentText() == "": return
        self.label_error_sample_len_missing.setVisible(False)
        self.label_error_db_missing.setVisible(False)
        self.label_error_wrong_roi_input.setVisible(False)
        if not self.sender().objectName() == "checkBox_red_normalize_by_db":
            self.label_error_db_wrong.setVisible(False)

        if (self.checkBox_red_overillumination_correction.isChecked() or self.checkBox_sfm_reflectivity_preview_show_overillumination.isChecked()) and self.lineEdit_sample_len.text() == "":
            self.label_error_sample_len_missing.setVisible(True)
            return

        if self.checkBox_red_normalize_by_db.isChecked() and self.tableWidget_db.rowCount() == 0:
            self.label_error_db_missing.setVisible(True)
            return

        if int(self.lineEdit_sfm_detector_image_roi_x_left.text()) > int(self.lineEdit_sfm_detector_image_roi_x_right.text()) or int(self.lineEdit_sfm_detector_image_roi_y_bottom.text()) < int(self.lineEdit_sfm_detector_image_roi_y_top.text()) or int(self.lineEdit_sfm_detector_image_roi_bkg_x_left.text()) < 0:
            self.label_error_wrong_roi_input.setVisible(True)
            return

        if self.checkBox_red_db_attenuator.isChecked():
            self.db_atten_factor = 10.4
            if not self.lineEdit_red_db_attenuator_factor.text() == "":
                self.db_atten_factor = float(self.lineEdit_red_db_attenuator_factor.text())
        else: self.db_atten_factor = 1

        if self.lineEdit_red_subtract_bkg_skip.text(): skip_bkg = float(self.lineEdit_red_subtract_bkg_skip.text())

        for i in range(0, self.tableWidget_scans.rowCount()):
            if self.tableWidget_scans.item(i, 0).text() == self.comboBox_single_file_mode_scan.currentText():
                self.SFM_FILE = self.tableWidget_scans.item(i, 2).text()
                self.SFM_DB_FILE = self.tableWidget_scans.item(i, 1).text()

        with h5py.File(self.SFM_FILE, 'r') as FILE:

            INSTRUMENT = FILE[list(FILE.keys())[0]].get("instrument")
            PONOS = FILE[list(FILE.keys())[0]].get("ponos")
            MOTOR_DATA = numpy.array(INSTRUMENT.get('motors').get('data')).T
            SCALERS_DATA = numpy.array(INSTRUMENT.get('scalers').get('data')).T

            roi_coord_Y = [int(self.lineEdit_sfm_detector_image_roi_y_top.text()), int(self.lineEdit_sfm_detector_image_roi_y_bottom.text())]
            roi_coord_X = [int(self.lineEdit_sfm_detector_image_roi_x_left.text()), int(self.lineEdit_sfm_detector_image_roi_x_right.text())]
            roi_coord_X_BKG = [int(self.lineEdit_sfm_detector_image_roi_bkg_x_left.text()), int(self.lineEdit_sfm_detector_image_roi_bkg_x_right.text())]

            if not roi_coord_Y == self.old_roi_coord_Y:
                self.sfm_file_already_analized = ""

            self.old_roi_coord_Y = roi_coord_Y

            for index, scaler in enumerate(INSTRUMENT.get('scalers').get('SPEC_counter_mnemonics')):
                if "'mon0'" in str(scaler): monitor_list = SCALERS_DATA[index]
                elif "'m1'" in str(scaler): monitor_uu_list = SCALERS_DATA[index]
                elif "'m2'" in str(scaler): monitor_dd_list = SCALERS_DATA[index]
                elif "'m3'" in str(scaler): monitor_du_list = SCALERS_DATA[index]
                elif "'m4'" in str(scaler): monitor_ud_list = SCALERS_DATA[index]

            if not self.SFM_FILE == self.sfm_file_already_analized:
                self.psd_uu_sfm = self.psd_dd_sfm = self.psd_ud_sfm = self.psd_du_sfm = []

            # get or create 2-dimentional intensity array for each polarisation
            for scan in PONOS.get('data'):

                # avoid reSUM of intensity after each action
                if not self.SFM_FILE == self.sfm_file_already_analized:
                    if "pnr" in list(FILE[list(FILE.keys())[0]]):
                        if str(scan) == "data_du":
                            self.psd_du_sfm = INSTRUMENT.get("detectors").get("psd_du").get('data')[:,
                                  int(roi_coord_Y[0]): int(roi_coord_Y[1]), :].sum(axis=1)
                        elif str(scan) == "data_uu":
                            self.psd_uu_sfm = INSTRUMENT.get("detectors").get("psd_uu").get('data')[:,
                                  int(roi_coord_Y[0]): int(roi_coord_Y[1]), :].sum(axis=1)
                        elif str(scan) == "data_ud":
                            self.psd_ud_sfm = INSTRUMENT.get("detectors").get("psd_ud").get('data')[:,
                                  int(roi_coord_Y[0]): int(roi_coord_Y[1]), :].sum(axis=1)
                        elif str(scan) == "data_dd":
                            self.psd_dd_sfm = INSTRUMENT.get("detectors").get("psd_dd").get('data')[:,
                                  int(roi_coord_Y[0]): int(roi_coord_Y[1]), :].sum(axis=1)
                    else:
                        self.psd_uu_sfm = INSTRUMENT.get("detectors").get("psd").get('data')[:, int(roi_coord_Y[0]) : int(roi_coord_Y[1]), :].sum(axis=1)

            self.sfm_file_already_analized = self.SFM_FILE

            for color_index, scan_intens_sfm in enumerate([self.psd_uu_sfm, self.psd_du_sfm, self.psd_ud_sfm, self.psd_dd_sfm]):

                sfm_export_Qz_one_pol = []
                sfm_export_I_one_pol = []
                sfm_export_dI_one_pol = []
                sfm_export_Resolution_one_pol = []

                plot_I = []
                plot_angle = []
                plot_dI_err_bottom = []
                plot_dI_err_top = []
                plot_overillumination = []

                if scan_intens_sfm == []: continue

                if color_index == 0: # ++
                    color = [0, 0, 0]
                    if numpy.count_nonzero(monitor_uu_list) == 0: monitor_data = monitor_list
                    else: monitor_data = monitor_uu_list
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
                        th = th - float(self.lineEdit_instr_full_scan_offset.text())
                    except:
                        th = th

                    # read motors
                    Qz = (4 * numpy.pi / float(self.lineEdit_instr_wavelength.text())) * numpy.sin(numpy.radians(th))
                    s1hg = self.s1hg_list[index]
                    s2hg = self.s2hg_list[index]
                    monitor = monitor_data[index]

                    if not self.checkBox_red_overillumination_correction.isChecked():
                        overill_corr = 1
                        overill_corr_plot = self.overillumination_correct_coeff(s1hg, s2hg, round(th, 4))[0]
                    else:
                        overill_corr, FWHM_proj = self.overillumination_correct_coeff(s1hg, s2hg, round(th, 4))
                        overill_corr_plot = overill_corr

                    # calculate resolution in Sared way or better
                    if self.checkBox_export_resolution_like_sared.isChecked():
                        Resolution = numpy.sqrt(((2 * numpy.pi / float(self.lineEdit_instr_wavelength.text())) ** 2) * (
                                (numpy.cos(numpy.radians(th))) ** 2) * (0.68 ** 2) * ((s1hg ** 2) + (s2hg ** 2)) / (
                                                        (float(
                                                            self.lineEdit_instr_s1_to_sample_dist.text()) - float(
                                                            self.lineEdit_instr_s2_to_sample_dist.text())) ** 2) + (
                                                        (float(self.lineEdit_instr_wavelength_resolution.text()) ** 2) * (Qz ** 2)))
                    else:
                        if FWHM_proj == s2hg:
                            Resolution = numpy.sqrt(
                                ((2 * numpy.pi / float(self.lineEdit_instr_wavelength.text())) ** 2) * (
                                        (numpy.cos(numpy.radians(th))) ** 2) * (0.68 ** 2) * (
                                        (s1hg ** 2) + (s2hg ** 2)) / ((float(
                                    self.lineEdit_instr_s1_to_sample_dist.text()) - float(
                                    self.lineEdit_instr_s2_to_sample_dist.text())) ** 2) + (
                                        (float(self.lineEdit_instr_wavelength_resolution.text()) ** 2) * (Qz ** 2)))
                        else:
                            Resolution = numpy.sqrt(
                                ((2 * numpy.pi / float(self.lineEdit_instr_wavelength.text())) ** 2) * (
                                        (numpy.cos(numpy.radians(th))) ** 2) * (0.68 ** 2) * (
                                        (s1hg ** 2) + (FWHM_proj ** 2)) / (
                                        float(self.lineEdit_instr_s1_to_sample_dist.text()) ** 2) + (
                                        (float(self.lineEdit_instr_wavelength_resolution.text()) ** 2) * (Qz ** 2)))

                    # I cite Gunnar in here "We are now saving dQ as sigma rather than FWHM for genx"
                    Resolution = Resolution / (2 * numpy.sqrt(2 * numpy.log(2)))

                    # analize integrated intensity for ROI
                    Intens = sum(scan_intens_sfm[index][roi_coord_X[0]: roi_coord_X[1]])
                    Intens_bkg = sum(scan_intens_sfm[index][roi_coord_X_BKG[0] : roi_coord_X_BKG[1]])

                    # minus background, devide by monitor, overillumination correct + calculate errors
                    if not Intens > 0: Intens = 0
                        # I want to avoid error==0 if intens==0
                    if Intens == 0: Intens_err = 1
                    else: Intens_err = numpy.sqrt(Intens)

                    if self.checkBox_red_subtract_bkg.isChecked() and Qz > skip_bkg:
                        if Intens_bkg > 0:
                            Intens_err = numpy.sqrt(Intens + Intens_bkg)
                            Intens = Intens - Intens_bkg

                    if self.checkBox_red_devide_by_monitor.isChecked():
                        if Intens == 0:  Intens_err = Intens_err / monitor
                        else: Intens_err = (Intens / monitor) * numpy.sqrt((Intens_err / Intens) ** 2 + (1 / monitor))
                        Intens = Intens / monitor

                    if self.checkBox_red_overillumination_correction.isChecked() and overill_corr > 0:
                        Intens_err = Intens_err / overill_corr
                        Intens = Intens / overill_corr

                    if self.checkBox_red_normalize_by_db.isChecked():
                        try:
                            db_intens = float(self.DB_INFO[self.SFM_DB_FILE + ";" + str(s1hg) + ";" + str(s2hg)].split(";")[0]) * self.db_atten_factor
                            db_err = overill_corr * float(self.DB_INFO[self.SFM_DB_FILE + ";" + str(s1hg) + ";" + str(s2hg)].split(";")[1]) * self.db_atten_factor
                            Intens_err = (Intens / db_intens) * numpy.sqrt((db_err / db_intens) ** 2 + (Intens_err / Intens) ** 2)
                            Intens = Intens / db_intens
                            self.label_error_db_wrong.setVisible(False)
                        except:
                            # if we try DB file without neccesary slits combination measured - show error message + redraw reflectivity_preview
                            self.label_error_db_wrong.setVisible(True)
                            self.label_error_db_wrong.setText("Choose another DB file \n for this SFM data file.")
                            self.checkBox_red_normalize_by_db.setCheckState(0)

                    try:
                        show_first = int(self.lineEdit_sfm_reflectivity_preview_skip_points_left.text())
                        show_last = len(self.th_list) - int(self.lineEdit_sfm_reflectivity_preview_skip_points_right.text())
                    except:
                        show_first = 0
                        show_last = len(self.th_list)

                    if not Intens < 0 and index < show_last and index > show_first:
                        # I need this for "Reduce SFM" option. First - store one pol.
                        sfm_export_Qz_one_pol.append(Qz)
                        sfm_export_I_one_pol.append(Intens)
                        sfm_export_dI_one_pol.append(Intens_err)
                        sfm_export_Resolution_one_pol.append(Resolution)

                        if Intens > 0:
                            plot_I.append(numpy.log10(Intens))
                            plot_angle.append(Qz)
                            plot_dI_err_top.append(abs(numpy.log10(Intens + Intens_err) - numpy.log10(Intens)))

                            plot_overillumination.append(overill_corr_plot)

                            if Intens > Intens_err: plot_dI_err_bottom.append(numpy.log10(Intens) - numpy.log10(Intens - Intens_err))
                            else: plot_dI_err_bottom.append(0)

                        if self.comboBox_sfm_reflectivity_preview_plot_axis.currentText() in ("Reflectivity (lin) vs Angle (Qz)", "Reflectivity (lin) vs Angle (deg)"):
                            plot_I.pop()
                            plot_I.append(Intens)
                            plot_dI_err_top.pop()
                            plot_dI_err_top.append(Intens_err)
                            plot_dI_err_bottom.pop()
                            plot_dI_err_bottom.append(Intens_err)

                        if self.comboBox_sfm_reflectivity_preview_plot_axis.currentText() in ("Reflectivity (lin) vs Angle (deg)", "Reflectivity (log) vs Angle (deg)"):
                            plot_angle.pop()
                            plot_angle.append(th)

                # I need this for "Reduse SFM" option. Second - combine all shown pol in one list variable.
                # polarisations are uu, dd, ud, du
                self.sfm_export_Qz.append(sfm_export_Qz_one_pol)
                self.sfm_export_I.append(sfm_export_I_one_pol)
                self.sfm_export_dI.append(sfm_export_dI_one_pol)
                self.sfm_export_Resolution.append(sfm_export_Resolution_one_pol)

                if self.checkBox_sfm_reflectivity_preview_incl_errorbars.isChecked():
                    s1 = pg.ErrorBarItem(x=numpy.array(plot_angle), y=numpy.array(plot_I), top=numpy.array(plot_dI_err_top), bottom=numpy.array(plot_dI_err_bottom), pen=pg.mkPen(color[0], color[1], color[2]), brush=pg.mkBrush(color[0], color[1], color[2]))
                    self.graphicsView_sfm_reflectivity_preview.addItem(s1)

                s2 = pg.ScatterPlotItem(x=plot_angle, y=plot_I, symbol="o", size=3, pen=pg.mkPen(color[0], color[1], color[2]), brush=pg.mkBrush(color[0], color[1], color[2]))
                self.graphicsView_sfm_reflectivity_preview.addItem(s2)

                if self.checkBox_sfm_reflectivity_preview_show_overillumination.isChecked():
                    s3 = pg.PlotCurveItem(x=plot_angle, y=plot_overillumination,
                                            pen=pg.mkPen(color=(255, 0, 0), width=3),
                                            brush=pg.mkBrush(color=(255, 0, 0), width=3) )
                    self.graphicsView_sfm_reflectivity_preview.addItem(s3)

    def draw_2D_map(self):

        self.int_detector_image = []

        self.graphicsView_sfm_2dmap_Qxz_Theta.clear()
        self.graphicsView_sfm_2dmap.clear()

        # change interface if for different views
        if self.comboBox_sfm_2dmap_axes.currentText() == "Pixel vs. Point":
            self.graphicsView_sfm_2dmap_Qxz_Theta.setGeometry(QtCore.QRect(0, 0, 0, 0))
            self.label_sfm_2dmap_highlight.setVisible(True)
            self.horizontalSlider_sfm_2dmap_highlight.setVisible(True)
            self.label_sfm_2dmap_rescale_image_x.setVisible(True)
            self.label_sfm_2dmap_rescale_image_y.setVisible(True)
            self.horizontalSlider_sfm_2dmap_rescale_image_x.setVisible(True)
            self.horizontalSlider_sfm_2dmap_rescale_image_y.setVisible(True)
            self.label_sfm_2dmap_Qxz_lower_number_of_points_by.setVisible(False)
            self.comboBox_sfm_2dmap_Qxz_lower_number_of_points_by.setVisible(False)
            self.label_sfm_2dmap_Qxz_threshold.setVisible(False)
            self.comboBox_sfm_2dmap_Qxz_threshold.setVisible(False)
        elif self.comboBox_sfm_2dmap_axes.currentText() == "Qx vs. Qz":
            self.graphicsView_sfm_2dmap_Qxz_Theta.setGeometry(QtCore.QRect(0, 30, 577, 520))
            self.label_sfm_2dmap_Qxz_lower_number_of_points_by.setVisible(True)
            self.comboBox_sfm_2dmap_Qxz_lower_number_of_points_by.setVisible(True)
            self.label_sfm_2dmap_Qxz_threshold.setVisible(True)
            self.comboBox_sfm_2dmap_Qxz_threshold.setVisible(True)
            self.label_sfm_2dmap_rescale_image_x.setVisible(False)
            self.label_sfm_2dmap_rescale_image_y.setVisible(False)
            self.horizontalSlider_sfm_2dmap_rescale_image_x.setVisible(False)
            self.horizontalSlider_sfm_2dmap_rescale_image_y.setVisible(False)
            self.label_sfm_2dmap_highlight.setVisible(False)
            self.horizontalSlider_sfm_2dmap_highlight.setVisible(False)
        elif self.comboBox_sfm_2dmap_axes.currentText() == "Alpha_i vs. Alpha_f":
            self.graphicsView_sfm_2dmap_Qxz_Theta.setGeometry(QtCore.QRect(0, 0, 0, 0))
            self.label_sfm_2dmap_highlight.setVisible(True)
            self.horizontalSlider_sfm_2dmap_highlight.setVisible(True)
            self.label_sfm_2dmap_rescale_image_x.setVisible(True)
            self.label_sfm_2dmap_rescale_image_y.setVisible(True)
            self.horizontalSlider_sfm_2dmap_rescale_image_x.setVisible(True)
            self.horizontalSlider_sfm_2dmap_rescale_image_y.setVisible(True)
            self.label_sfm_2dmap_Qxz_lower_number_of_points_by.setVisible(False)
            self.comboBox_sfm_2dmap_Qxz_lower_number_of_points_by.setVisible(False)
            self.label_sfm_2dmap_Qxz_threshold.setVisible(False)
            self.comboBox_sfm_2dmap_Qxz_threshold.setVisible(False)

        if self.SFM_FILE == "": return

        # start over if we selected nes SFM scan
        if not self.sfm_file_2d_calculated_params == [] and not self.sfm_file_2d_calculated_params[0] == self.SFM_FILE:
            self.comboBox_sfm_2dmap_axes.setCurrentIndex(0)
            self.sfm_file_2d_calculated_params = []
            self.res_Aif = []

        try:
            self.graphicsView_sfm_2dmap.removeItem(self.draw_roi_2D_map)
        except: 1

        # load selected integrated detector image
        if self.comboBox_sfm_2dmap_polarisation.count() == 1:
            self.int_detector_image = self.psd_uu_sfm
        else:
            if self.comboBox_sfm_2dmap_polarisation.currentText() == "uu":
                self.int_detector_image = self.psd_uu_sfm
            elif self.comboBox_sfm_2dmap_polarisation.currentText() == "du":
                self.int_detector_image = self.psd_du_sfm
            elif self.comboBox_sfm_2dmap_polarisation.currentText() == "ud":
                self.int_detector_image = self.psd_ud_sfm
            elif self.comboBox_sfm_2dmap_polarisation.currentText() == "dd":
                self.int_detector_image = self.psd_dd_sfm

        if self.int_detector_image == []: return

        # Pixel to Angle conversion for "Qx vs Qz" and "alpha_i vs alpha_f" 2d maps
        if self.comboBox_sfm_2dmap_axes.currentText() in ["Qx vs. Qz", "Alpha_i vs. Alpha_f"]:
            # recalculate only if something was changed
            if self.res_Aif == [] or not self.sfm_file_2d_calculated_params == [self.SFM_FILE, self.comboBox_sfm_2dmap_polarisation.currentText(),
                                              self.lineEdit_sfm_detector_image_roi_x_left.text(), self.lineEdit_sfm_detector_image_roi_x_right.text(),
                                              self.lineEdit_instr_wavelength.text(), self.lineEdit_instr_sample_to_det_dist.text(),
                                              self.comboBox_sfm_2dmap_Qxz_lower_number_of_points_by.currentText(), self.comboBox_sfm_2dmap_Qxz_threshold.currentText()]:
                self.spots_Qxz = []
                self.int_detector_image_Qxz = []
                self.int_detector_image_Aif = [[],[]]
                self.int_detector_image_values_array = []

                roi_middle = round((self.int_detector_image.shape[1] - float(self.lineEdit_sfm_detector_image_roi_x_left.text()) +
                                    self.int_detector_image.shape[1] - float(self.lineEdit_sfm_detector_image_roi_x_right.text())) / 2)
                mm_per_pix = 300 / self.int_detector_image.shape[1]

                # we need to flip the detector (X) for correct calculation
                for theta_i, tth_i, det_image_i in zip(self.th_list, self.tth_list, numpy.flip(self.int_detector_image, 1)):
                    for pixel_num, value in enumerate(det_image_i):
                        # Reduce number of points to draw (to save RAM)
                        if pixel_num % int(self.comboBox_sfm_2dmap_Qxz_lower_number_of_points_by.currentText()) == 0:
                            # theta F in deg
                            theta_f = tth_i - theta_i
                            # calculate delta theta F in deg
                            delta_theta_F_mm = (pixel_num - roi_middle) * mm_per_pix
                            delta_theta_F_deg = numpy.degrees(
                                numpy.arctan(delta_theta_F_mm / float(self.lineEdit_instr_sample_to_det_dist.text())))
                            # final theta F in deg for the point
                            theta_f += delta_theta_F_deg
                            # convert to Q
                            Qx = (2 * numpy.pi / float(self.lineEdit_instr_wavelength.text())) * (
                                        numpy.cos(numpy.radians(theta_f)) - numpy.cos(numpy.radians(theta_i)))
                            Qz = (2 * numpy.pi / float(self.lineEdit_instr_wavelength.text())) * (
                                        numpy.sin(numpy.radians(theta_f)) + numpy.sin(numpy.radians(theta_i)))

                            self.int_detector_image_Qxz.append([Qx, Qz, value])

                            self.int_detector_image_Aif[0].append(theta_i)
                            self.int_detector_image_Aif[1].append(theta_f)
                            self.int_detector_image_values_array.append(value)

                            # define colors - 2 count+ -> green, [0,1] - blue
                            if value < int(self.comboBox_sfm_2dmap_Qxz_threshold.currentText()): color = [0, 0, 255]
                            else: color = [0, 255, 0]

                            self.spots_Qxz.append({'pos': (-Qx, Qz), 'pen': pg.mkPen(color[0], color[1], color[2])})

                if self.comboBox_sfm_2dmap_axes.currentText() == "Alpha_i vs. Alpha_f":
                    # calculate required number of pixels in Y axis
                    self.resolution_x_pix_deg = self.int_detector_image.shape[0] / (max(self.int_detector_image_Aif[0]) - min(self.int_detector_image_Aif[0]))
                    self.resolution_y_pix = int(round((max(self.int_detector_image_Aif[1]) - min(self.int_detector_image_Aif[1])) * self.resolution_x_pix_deg))

                    grid_x, grid_y = numpy.mgrid[min(self.int_detector_image_Aif[0]):max(self.int_detector_image_Aif[0]):((max(self.int_detector_image_Aif[0]) - min(self.int_detector_image_Aif[0]))/len(self.th_list)), min(self.int_detector_image_Aif[1]):max(self.int_detector_image_Aif[1]):(max(self.int_detector_image_Aif[1]) - min(self.int_detector_image_Aif[1]))/self.resolution_y_pix]
                    self.res_Aif = griddata((self.int_detector_image_Aif[0], self.int_detector_image_Aif[1]), self.int_detector_image_values_array, (grid_x, grid_y), method="linear", fill_value=float(0))

                # record params that we used for 2D maps calculation
                self.sfm_file_2d_calculated_params = [self.SFM_FILE, self.comboBox_sfm_2dmap_polarisation.currentText(),
                                                      self.lineEdit_sfm_detector_image_roi_x_left.text(), self.lineEdit_sfm_detector_image_roi_x_right.text(),
                                                      self.lineEdit_instr_wavelength.text(), self.lineEdit_instr_sample_to_det_dist.text(),
                                                      self.comboBox_sfm_2dmap_Qxz_lower_number_of_points_by.currentText(), self.comboBox_sfm_2dmap_Qxz_threshold.currentText()]

        # plot
        if self.comboBox_sfm_2dmap_axes.currentText() == "Pixel vs. Point":
            self.graphicsView_sfm_2dmap.setImage(numpy.flip(self.int_detector_image, axis=0), axes={'x': 1, 'y': 0}, levels=(0, 0.1),
                                           scale=(int(self.horizontalSlider_sfm_2dmap_rescale_image_x.value()), int(self.horizontalSlider_sfm_2dmap_rescale_image_y.value())))
            # add ROI rectangular
            spots_ROI = []

            for i in range(int(self.int_detector_image.shape[0])):
                spots_ROI.append({'y': i * int(self.horizontalSlider_sfm_2dmap_rescale_image_y.value()),
                                  'x': int(self.lineEdit_sfm_detector_image_roi_x_left.text()) * int(
                                      self.horizontalSlider_sfm_2dmap_rescale_image_x.value())})
                spots_ROI.append({'y': i * int(self.horizontalSlider_sfm_2dmap_rescale_image_y.value()),
                                  'x': int(self.lineEdit_sfm_detector_image_roi_x_right.text()) * int(
                                      self.horizontalSlider_sfm_2dmap_rescale_image_x.value())})

            self.draw_roi_2D_map = pg.ScatterPlotItem(spots=spots_ROI, size=1.5, pen=pg.mkPen(255, 255, 255))
            self.graphicsView_sfm_2dmap.addItem(self.draw_roi_2D_map)
        elif self.comboBox_sfm_2dmap_axes.currentText() == "Alpha_i vs. Alpha_f":
            self.graphicsView_sfm_2dmap.setImage(numpy.flip(self.res_Aif, axis=1), axes={'x': 0, 'y': 1}, levels=(0, 0.1),
                                            scale=(int(self.horizontalSlider_sfm_2dmap_rescale_image_x.value()), int(self.horizontalSlider_sfm_2dmap_rescale_image_y.value())))
        elif self.comboBox_sfm_2dmap_axes.currentText() == "Qx vs. Qz":
            s0 = pg.ScatterPlotItem(spots=self.spots_Qxz, size=1)
            self.graphicsView_sfm_2dmap_Qxz_Theta.addItem(s0)

        self.graphicsView_sfm_2dmap.ui.histogram.setHistogramRange(0, self.horizontalSlider_sfm_2dmap_highlight.value())
        self.graphicsView_sfm_2dmap.ui.histogram.setLevels(0, self.horizontalSlider_sfm_2dmap_highlight.value())

    def export_2d_map(self):
        if self.lineEdit_save_at.text(): save_file_directory = self.lineEdit_save_at.text()
        else: save_file_directory = self.current_dir

        if self.comboBox_sfm_2dmap_axes.currentText() == "Pixel vs. Point":
            with open(save_file_directory + self.SFM_FILE[self.SFM_FILE.rfind("/") + 1 : -3] + "_" + self.comboBox_sfm_2dmap_polarisation.currentText() + " 2D_map(Pixel vs. Point).dat", "w") as new_file_2d_map:
                for line in self.int_detector_image:
                    for row in line:
                        new_file_2d_map.write(str(row) + " ")
                    new_file_2d_map.write("\n")

        elif self.comboBox_sfm_2dmap_axes.currentText() == "Alpha_i vs. Alpha_f":
            with open(save_file_directory + self.SFM_FILE[self.SFM_FILE.rfind("/") + 1 : -3] + "_" + self.comboBox_sfm_2dmap_polarisation.currentText() + " 2D_map_(Alpha_i vs. Alpha_f)).dat", "w") as new_file_2d_map_Aif:
                # header
                new_file_2d_map_Aif.write("Alpha_i limits: " + str(min(self.int_detector_image_Aif[0])) + " : " + str(max(self.int_detector_image_Aif[0])) +
                                        ".   Alpha_f limits: " + str(min(self.int_detector_image_Aif[1])) + " : " + str(max(self.int_detector_image_Aif[1])) + " degrees\n")
                for line in numpy.rot90(self.res_Aif):
                    for row in line:
                        new_file_2d_map_Aif.write(str(row) + " ")
                    new_file_2d_map_Aif.write("\n")

        elif self.comboBox_sfm_2dmap_axes.currentText() in ["Qx vs. Qz"]:
            with open(save_file_directory + self.SFM_FILE[self.SFM_FILE.rfind("/") + 1 : -3] + "_" + self.comboBox_sfm_2dmap_polarisation.currentText() + " points_(Qx, Qz, intens).dat", "w") as new_file_2d_map_Qxz:
                for line in self.int_detector_image_Qxz:
                    new_file_2d_map_Qxz.write(str(line[0]) + " " + str(line[1]) + " " + str(line[2]))
                    new_file_2d_map_Qxz.write("\n")

    def update_slits(self):
        roi_width = int(self.lineEdit_sfm_detector_image_roi_x_right.text()) - int(self.lineEdit_sfm_detector_image_roi_x_left.text())
        self.lineEdit_sfm_detector_image_roi_bkg_x_left.setText(str(int(self.lineEdit_sfm_detector_image_roi_bkg_x_right.text()) - roi_width))

        self.lineEdit_sfm_detector_image_roi_bkg_y_bottom.setText(str(int(self.lineEdit_sfm_detector_image_roi_y_bottom.text())))
        self.lineEdit_sfm_detector_image_roi_bkg_y_top.setText(str(int(self.lineEdit_sfm_detector_image_roi_y_top.text())))

        self.draw_det_image()
        self.load_reflectivity_preview()

    def color_det_image(self):
        if self.comboBox_sfm_detector_image_color_scheme.currentText() == "White / Black":
            self.color_det_image = numpy.array([[0, 0, 0, 255], [255, 255, 255, 255], [255, 255, 255, 255]], dtype=numpy.ubyte)
        elif self.comboBox_sfm_detector_image_color_scheme.currentText() == "Green / Blue":
            self.color_det_image = numpy.array([[0, 0, 255, 255], [255, 0, 0, 255], [0, 255, 0, 255]], dtype=numpy.ubyte)

        self.draw_det_image()
    ##<--

if __name__ == "__main__":
    import sys
    QtWidgets.QApplication.setStyle("Fusion")
    app = QtWidgets.QApplication(sys.argv)
    prog = GUI()
    prog.show()
    sys.exit(app.exec_())

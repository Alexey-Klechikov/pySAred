from PyQt5 import QtCore, QtGui, QtWidgets
import h5py, numpy, os
import pyqtgraph as pg
import pyqtgraph.exporters as image_exporter

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
        MainWindow.setWindowIcon(QtGui.QIcon(self.current_dir + "\icon.png"))
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
        self.tableWidget_Scans = QtWidgets.QTableWidget(self.groupBox_data)
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
        for i in range(0,4):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_Scans.setHorizontalHeaderItem(i, item)
        self.tableWidget_Scans.horizontalHeader().setVisible(True)
        self.tableWidget_Scans.verticalHeader().setVisible(False)
        item = self.tableWidget_Scans.horizontalHeaderItem(0)
        item.setText("Scan")
        # I removed ROI column, so I will remove the column from here when I see its really not necessary to have
        item = self.tableWidget_Scans.horizontalHeaderItem(1)
        item.setText("ROI")
        item = self.tableWidget_Scans.horizontalHeaderItem(2)
        item.setText("DB")
        item = self.tableWidget_Scans.horizontalHeaderItem(3)
        item.setText("Scan_file_full_path")
        self.tableWidget_Scans.setColumnWidth(0, 200)
        self.tableWidget_Scans.setColumnWidth(1, 0)
        self.tableWidget_Scans.setColumnWidth(2, int(self.tableWidget_Scans.width()) - int(self.tableWidget_Scans.columnWidth(0)) - int(self.tableWidget_Scans.columnWidth(1)) - 2)
        self.tableWidget_Scans.setColumnWidth(3, 0)
        self.pushButton_DeleteImportScans = QtWidgets.QPushButton(self.groupBox_data)
        self.pushButton_DeleteImportScans.setGeometry(QtCore.QRect(10, 384, 81, 20))
        self.pushButton_DeleteImportScans.setFont(font_ee)
        self.pushButton_DeleteImportScans.setObjectName("pushButton_DeleteImportScans")
        self.pushButton_DeleteImportScans.setText("Delete scans")
        self.pushButton_importScans = QtWidgets.QPushButton(self.groupBox_data)
        self.pushButton_importScans.setGeometry(QtCore.QRect(189, 384, 81, 20))
        self.pushButton_importScans.setFont(font_ee)
        self.pushButton_importScans.setObjectName("pushButton_importScans")
        self.pushButton_importScans.setText("Import scans")
        self.label_db = QtWidgets.QLabel(self.groupBox_data)
        self.label_db.setGeometry(QtCore.QRect(78, 412, 191, 23))
        self.label_db.setFont(font_headline)
        self.label_db.setObjectName("label_db")
        self.label_db.setText("Direct Beam files")
        self.checkBox_db_arrangement_after = QtWidgets.QCheckBox(self.groupBox_data)
        self.checkBox_db_arrangement_after.setGeometry(QtCore.QRect(10, 432, 210, 20))
        self.checkBox_db_arrangement_after.setFont(font_ee)
        self.checkBox_db_arrangement_after.setObjectName("checkBox_db_arrangement_after")
        self.checkBox_db_arrangement_after.setText("DB's were measured after the scans")
        self.tableWidget_DB = QtWidgets.QTableWidget(self.groupBox_data)
        self.tableWidget_DB.setFont(font_ee)
        self.tableWidget_DB.setGeometry(QtCore.QRect(10, 452, 260, 183))
        self.tableWidget_DB.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_DB.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_DB.setAutoScroll(True)
        self.tableWidget_DB.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.tableWidget_DB.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_DB.setObjectName("tableWidget_db")
        self.tableWidget_DB.setColumnCount(2)
        self.tableWidget_DB.setRowCount(0)
        for i in range(0, 2):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_DB.setHorizontalHeaderItem(i, item)
        self.tableWidget_DB.horizontalHeader().setVisible(False)
        self.tableWidget_DB.verticalHeader().setVisible(False)
        item = self.tableWidget_DB.horizontalHeaderItem(0)
        item.setText("Scan")
        item = self.tableWidget_DB.horizontalHeaderItem(1)
        item.setText("Path")
        self.tableWidget_DB.setColumnWidth(0, self.tableWidget_DB.width())
        self.tableWidget_DB.setColumnWidth(1, 0)
        self.tableWidget_DB.setSortingEnabled(True)
        self.pushButton_DeleteImportDB = QtWidgets.QPushButton(self.groupBox_data)
        self.pushButton_DeleteImportDB.setGeometry(QtCore.QRect(10, 639, 81, 20))
        self.pushButton_DeleteImportDB.setFont(font_ee)
        self.pushButton_DeleteImportDB.setObjectName("pushButton_DeleteImportDB")
        self.pushButton_DeleteImportDB.setText("Delete DB")
        self.pushButton_ImportDB = QtWidgets.QPushButton(self.groupBox_data)
        self.pushButton_ImportDB.setGeometry(QtCore.QRect(189, 639, 81, 20))
        self.pushButton_ImportDB.setFont(font_ee)
        self.pushButton_ImportDB.setObjectName("pushButton_ImportDB")
        self.pushButton_ImportDB.setText("Import DB")

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
        self.lineEdit_SampleLength = QtWidgets.QLineEdit(self.groupBox_sample_len)
        self.lineEdit_SampleLength.setGeometry(QtCore.QRect(192, 22, 83, 21))
        self.lineEdit_SampleLength.setObjectName("lineEdit_SampleLength")
        self.lineEdit_SampleLength.setText("50")

        # Block: Reductions and Instrument settings
        self.label_reductions = QtWidgets.QLabel(self.centralwidget)
        self.label_reductions.setGeometry(QtCore.QRect(305, 65, 200, 16))
        self.label_reductions.setFont(font_headline)
        self.label_reductions.setObjectName("label_reductions")
        self.label_reductions.setText("Reductions")
        self.tabWidget_red_instr_exp = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_red_instr_exp.setGeometry(QtCore.QRect(300, 87, 281, 226))
        self.tabWidget_red_instr_exp.setFont(font_ee)
        self.tabWidget_red_instr_exp.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget_red_instr_exp.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget_red_instr_exp.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget_red_instr_exp.setObjectName("tabWidget_red_instr_exp")

        # Tab: Reductions
        self.tab_reduct = QtWidgets.QWidget()
        self.tab_reduct.setObjectName("tab_reduct")
        self.checkBox_DevideByMon = QtWidgets.QCheckBox(self.tab_reduct)
        self.checkBox_DevideByMon.setGeometry(QtCore.QRect(10, 10, 131, 18))
        self.checkBox_DevideByMon.setFont(font_ee)
        self.checkBox_DevideByMon.setObjectName("checkBox_DevideByMon")
        self.checkBox_DevideByMon.setText("Devide by monitor")
        self.checkBox_NormDB = QtWidgets.QCheckBox(self.tab_reduct)
        self.checkBox_NormDB.setGeometry(QtCore.QRect(10, 35, 181, 18))
        self.checkBox_NormDB.setFont(font_ee)
        self.checkBox_NormDB.setObjectName("checkBox_NormDB")
        self.checkBox_NormDB.setText("Normalise by direct beam")
        self.checkBox_DBatten = QtWidgets.QCheckBox(self.tab_reduct)
        self.checkBox_DBatten.setGeometry(QtCore.QRect(10, 60, 161, 18))
        self.checkBox_DBatten.setFont(font_ee)
        self.checkBox_DBatten.setChecked(True)
        self.checkBox_DBatten.setObjectName("checkBox_DBatten")
        self.checkBox_DBatten.setText("Direct beam attenuator")
        self.lineEdit_AttenCorrFactor = QtWidgets.QLineEdit(self.tab_reduct)
        self.lineEdit_AttenCorrFactor.setGeometry(QtCore.QRect(30, 85, 221, 20))
        self.lineEdit_AttenCorrFactor.setFont(font_ee)
        self.lineEdit_AttenCorrFactor.setText("")
        self.lineEdit_AttenCorrFactor.setObjectName("lineEdit_AttenCorrFactor")
        self.lineEdit_AttenCorrFactor.setPlaceholderText("Attenuator correction [default 10.4]")
        self.checkBox_SubtrBKG = QtWidgets.QCheckBox(self.tab_reduct)
        self.checkBox_SubtrBKG.setGeometry(QtCore.QRect(10, 115, 231, 18))
        self.checkBox_SubtrBKG.setFont(font_ee)
        self.checkBox_SubtrBKG.setObjectName("checkBox_SubtrBKG")
        self.checkBox_SubtrBKG.setText("Subtract background (using 1 ROI)")
        self.lineEdit_SkipSubtrBKG = QtWidgets.QLineEdit(self.tab_reduct)
        self.lineEdit_SkipSubtrBKG.setGeometry(QtCore.QRect(30, 140, 221, 20))
        self.lineEdit_SkipSubtrBKG.setFont(font_ee)
        self.lineEdit_SkipSubtrBKG.setObjectName("lineEdit_SkipSubtrBKG")
        self.lineEdit_SkipSubtrBKG.setPlaceholderText("Skip background corr. at Qz < [default 0]")
        self.checkBox_OverillCorr = QtWidgets.QCheckBox(self.tab_reduct)
        self.checkBox_OverillCorr.setGeometry(QtCore.QRect(10, 170, 181, 18))
        self.checkBox_OverillCorr.setFont(font_ee)
        self.checkBox_OverillCorr.setObjectName("checkBox_OverillCorr")
        self.checkBox_OverillCorr.setText("Overillumination correction")
        self.tabWidget_red_instr_exp.addTab(self.tab_reduct, "")
        self.tabWidget_red_instr_exp.setTabText(0, "Reductions")

        # Tab: Instrument settings
        self.tab_instr = QtWidgets.QWidget()
        self.tab_instr.setObjectName("tab_instr")
        self.label_wavelength = QtWidgets.QLabel(self.tab_instr)
        self.label_wavelength.setGeometry(QtCore.QRect(10, 10, 111, 16))
        self.label_wavelength.setFont(font_ee)
        self.label_wavelength.setObjectName("label_wavelength")
        self.label_wavelength.setText("Wavelength (A)")
        self.lineEdit_wavelength = QtWidgets.QLineEdit(self.tab_instr)
        self.lineEdit_wavelength.setGeometry(QtCore.QRect(220, 10, 41, 20))
        self.lineEdit_wavelength.setFont(font_ee)
        self.lineEdit_wavelength.setObjectName("lineEdit_wavelength")
        self.lineEdit_wavelength.setText("5.2")
        self.label_wavel_resol = QtWidgets.QLabel(self.tab_instr)
        self.label_wavel_resol.setGeometry(QtCore.QRect(10, 35, 271, 16))
        self.label_wavel_resol.setFont(font_ee)
        self.label_wavel_resol.setObjectName("label_wavel_resol")
        self.label_wavel_resol.setText("Wavelength resolution (d_lambda/lambda)")
        self.lineEdit_wavel_resol = QtWidgets.QLineEdit(self.tab_instr)
        self.lineEdit_wavel_resol.setGeometry(QtCore.QRect(220, 35, 41, 20))
        self.lineEdit_wavel_resol.setFont(font_ee)
        self.lineEdit_wavel_resol.setObjectName("lineEdit_wavel_resol")
        self.lineEdit_wavel_resol.setText("0.007")
        self.label_s1_sample_dist = QtWidgets.QLabel(self.tab_instr)
        self.label_s1_sample_dist.setGeometry(QtCore.QRect(10, 60, 241, 16))
        self.label_s1_sample_dist.setFont(font_ee)
        self.label_s1_sample_dist.setObjectName("label_s1_sample_dist")
        self.label_s1_sample_dist.setText("Mono_slit to Samplle distance (mm)")
        self.lineEdit_s1_sample_dist = QtWidgets.QLineEdit(self.tab_instr)
        self.lineEdit_s1_sample_dist.setGeometry(QtCore.QRect(220, 60, 41, 20))
        self.lineEdit_s1_sample_dist.setFont(font_ee)
        self.lineEdit_s1_sample_dist.setObjectName("lineEdit_s1_sample_dist")
        self.lineEdit_s1_sample_dist.setText("2350")
        self.label_s2_sample_dist = QtWidgets.QLabel(self.tab_instr)
        self.label_s2_sample_dist.setGeometry(QtCore.QRect(10, 85, 241, 16))
        self.label_s2_sample_dist.setFont(font_ee)
        self.label_s2_sample_dist.setObjectName("label_s2_sample_dist")
        self.label_s2_sample_dist.setText("Sample_slit to Sample distance (mm)")
        self.lineEdit_s2_sample_dist = QtWidgets.QLineEdit(self.tab_instr)
        self.lineEdit_s2_sample_dist.setGeometry(QtCore.QRect(220, 85, 41, 20))
        self.lineEdit_s2_sample_dist.setFont(font_ee)
        self.lineEdit_s2_sample_dist.setObjectName("lineEdit_s2_sample_dist")
        self.lineEdit_s2_sample_dist.setText("195")
        self.label_sample_det_dist = QtWidgets.QLabel(self.tab_instr)
        self.label_sample_det_dist.setGeometry(QtCore.QRect(10, 110, 241, 16))
        self.label_sample_det_dist.setFont(font_ee)
        self.label_sample_det_dist.setObjectName("label_sample_det_dist")
        self.label_sample_det_dist.setText("Samplle to Detector distance (mm)")
        self.lineEdit_sample_det_dist = QtWidgets.QLineEdit(self.tab_instr)
        self.lineEdit_sample_det_dist.setGeometry(QtCore.QRect(220, 110, 41, 20))
        self.lineEdit_sample_det_dist.setFont(font_ee)
        self.lineEdit_sample_det_dist.setObjectName("lineEdit_sample_det_dist")
        self.lineEdit_sample_det_dist.setText("2500")
        '''
        self.label_th_offset = QtWidgets.QLabel(self.tab_instr)
        self.label_th_offset.setGeometry(QtCore.QRect(10, 150, 241, 16))
        self.label_th_offset.setFont(font_ee)
        self.label_th_offset.setObjectName("label_th_offset")
        self.label_th_offset.setText("th offset (deg) (SFM only)")
        self.lineEdit_th_offset = QtWidgets.QLineEdit(self.tab_instr)
        self.lineEdit_th_offset.setGeometry(QtCore.QRect(220, 150, 41, 20))
        self.lineEdit_th_offset.setFont(font_ee)
        self.lineEdit_th_offset.setObjectName("lineEdit_sample_det_dist")
        self.lineEdit_th_offset.setText("0")
        '''
        self.label_full_scan_offset = QtWidgets.QLabel(self.tab_instr)
        self.label_full_scan_offset.setGeometry(QtCore.QRect(10, 175, 241, 16))
        self.label_full_scan_offset.setFont(font_ee)
        self.label_full_scan_offset.setObjectName("label_full_scan_offset")
        self.label_full_scan_offset.setText("Full scan offset (th - deg) (SFM only)")
        self.lineEdit_full_scan_offset = QtWidgets.QLineEdit(self.tab_instr)
        self.lineEdit_full_scan_offset.setGeometry(QtCore.QRect(220, 175, 41, 20))
        self.lineEdit_full_scan_offset.setFont(font_ee)
        self.lineEdit_full_scan_offset.setObjectName("lineEdit_full_scan_offset")
        self.lineEdit_full_scan_offset.setText("0")
        self.tabWidget_red_instr_exp.addTab(self.tab_instr, "")
        self.tabWidget_red_instr_exp.setTabText(1, "Instrument settings")

        # Tab: Export options
        self.tab_export_options = QtWidgets.QWidget()
        self.tab_export_options.setObjectName("tab_export_options")
        self.checkBox_add_resolution_column = QtWidgets.QCheckBox(self.tab_export_options)
        self.checkBox_add_resolution_column.setGeometry(QtCore.QRect(10, 10, 250, 18))
        self.checkBox_add_resolution_column.setFont(font_ee)
        self.checkBox_add_resolution_column.setChecked(True)
        self.checkBox_add_resolution_column.setObjectName("checkBox_add_resolution_column")
        self.checkBox_add_resolution_column.setText("Include ang. resolution column in the output file")
        self.checkBox_resol_sared = QtWidgets.QCheckBox(self.tab_export_options)
        self.checkBox_resol_sared.setGeometry(QtCore.QRect(30, 35, 250, 18))
        self.checkBox_resol_sared.setFont(font_ee)
        self.checkBox_resol_sared.setChecked(True)
        self.checkBox_resol_sared.setObjectName("checkBox_resol_sared")
        self.checkBox_resol_sared.setText("Calculate ang. resolution in 'Sared' way")

        self.checkBox_remove_zeros = QtWidgets.QCheckBox(self.tab_export_options)
        self.checkBox_remove_zeros.setGeometry(QtCore.QRect(10, 60, 250, 18))
        self.checkBox_remove_zeros.setFont(font_ee)
        self.checkBox_remove_zeros.setChecked(False)
        self.checkBox_remove_zeros.setObjectName("checkBox_remove_zeros")
        self.checkBox_remove_zeros.setText("Remove zeros from reduced files")

        self.tabWidget_red_instr_exp.addTab(self.tab_export_options, "")
        self.tabWidget_red_instr_exp.setTabText(2, "Export")

        # Block: Save reduced files at
        self.label_save_at = QtWidgets.QLabel(self.centralwidget)
        self.label_save_at.setGeometry(QtCore.QRect(305, 320, 200, 20))
        self.label_save_at.setFont(font_headline)
        self.label_save_at.setObjectName("label_save_at")
        self.label_save_at.setText("Save reduced files at")
        self.groupBox_save_at = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_save_at.setGeometry(QtCore.QRect(300, 325, 282, 48))
        self.groupBox_save_at.setFont(font_ee)
        self.groupBox_save_at.setTitle("")
        self.groupBox_save_at.setObjectName("groupBox_save_at")
        self.lineEdit_saveAt = QtWidgets.QLineEdit(self.groupBox_save_at)
        self.lineEdit_saveAt.setGeometry(QtCore.QRect(10, 22, 225, 22))
        self.lineEdit_saveAt.setFont(font_ee)
        self.lineEdit_saveAt.setObjectName("lineEdit_saveAt")
        self.lineEdit_saveAt.setPlaceholderText(self.current_dir)
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
        self.pushButton_start_all = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start_all.setGeometry(QtCore.QRect(494, 380, 88, 30))
        self.pushButton_start_all.setFont(font_button)
        self.pushButton_start_all.setObjectName("pushButton_start_all")
        self.pushButton_start_all.setText("Reduce all")

        # Errors
        self.label_sample_len_missing = QtWidgets.QLabel(self.centralwidget)
        self.label_sample_len_missing.setGeometry(QtCore.QRect(360, 420, 181, 31))
        self.label_sample_len_missing.setFont(font_button)
        self.label_sample_len_missing.setObjectName("label_sample_len_missing")
        self.label_sample_len_missing.setVisible(False)
        self.label_sample_len_missing.setText("Sample length is missing")
        self.label_sample_len_missing.setStyleSheet("color:rgb(255,0,0)")
        self.label_DB_missing = QtWidgets.QLabel(self.centralwidget)
        self.label_DB_missing.setGeometry(QtCore.QRect(355, 450, 181, 31))
        self.label_DB_missing.setFont(font_button)
        self.label_DB_missing.setObjectName("label_DB_missing")
        self.label_DB_missing.setVisible(False)
        self.label_DB_missing.setText("Direct beam file is missing")
        self.label_DB_missing.setStyleSheet("color:rgb(255,0,0)")
        self.label_wrong_roi_input = QtWidgets.QLabel(self.centralwidget)
        self.label_wrong_roi_input.setGeometry(QtCore.QRect(360, 435, 181, 31))
        self.label_wrong_roi_input.setFont(font_button)
        self.label_wrong_roi_input.setObjectName("label_wrong_roi_input")
        self.label_wrong_roi_input.setVisible(False)
        self.label_wrong_roi_input.setText("Recheck your ROI input")
        self.label_wrong_roi_input.setStyleSheet("color:rgb(255,0,0)")

        # Block: Recheck following files in SFM
        self.label_recheck_with_sared = QtWidgets.QLabel(self.centralwidget)
        self.label_recheck_with_sared.setGeometry(QtCore.QRect(305, 490, 250, 20))
        self.label_recheck_with_sared.setFont(font_headline)
        self.label_recheck_with_sared.setObjectName("label_recheck_with_sared")
        self.label_recheck_with_sared.setText("Recheck following files in SFM")
        self.groupBox_recheck_files = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_recheck_files.setGeometry(QtCore.QRect(300, 497, 282, 180))
        self.groupBox_recheck_files.setFont(font_ee)
        self.groupBox_recheck_files.setTitle("")
        self.groupBox_recheck_files.setObjectName("groupBox_recheck_files")
        self.listWidget_filesToCheck = QtWidgets.QListWidget(self.groupBox_recheck_files)
        self.listWidget_filesToCheck.setGeometry(QtCore.QRect(10, 27, 262, 145))
        self.listWidget_filesToCheck.setObjectName("listWidget_filesToCheck")

        # Block: Single File Mode
        self.label_SFM = QtWidgets.QLabel(self.centralwidget)
        self.label_SFM.setGeometry(QtCore.QRect(596, 5, 200, 20))
        self.label_SFM.setFont(font_headline)
        self.label_SFM.setObjectName("label_SFM")
        self.label_SFM.setText("Single File Mode (SFM)")
        self.groupBox_load_scan = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_load_scan.setGeometry(QtCore.QRect(591, 10, 472, 48))
        self.groupBox_load_scan.setTitle("")
        self.groupBox_load_scan.setObjectName("groupBox_load_scan")
        self.label_scan = QtWidgets.QLabel(self.groupBox_load_scan)
        self.label_scan.setGeometry(QtCore.QRect(10, 23, 47, 20))
        self.label_scan.setObjectName("label_scan")
        self.label_scan.setText("Scan")
        self.label_scan.setFont(font_ee)
        self.comboBox_scan = QtWidgets.QComboBox(self.groupBox_load_scan)
        self.comboBox_scan.setGeometry(QtCore.QRect(40, 23, 425, 20))
        self.comboBox_scan.setObjectName("comboBox_scan")
        self.comboBox_scan.setFont(font_ee)
        pg.setConfigOption('background', (255, 255, 255))
        pg.setConfigOption('foreground', 'k')

        # Button: Reduce SFM
        self.pushButton_start_sfm = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start_sfm.setGeometry(QtCore.QRect(1070, 28, 100, 30))
        self.pushButton_start_sfm.setFont(font_button)
        self.pushButton_start_sfm.setObjectName("pushButton_start_sfm")
        self.pushButton_start_sfm.setText("Reduce SFM")

        # Block: Detector Images and Reflectivity preview
        self.tabWidget_SFM = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_SFM.setGeometry(QtCore.QRect(592, 65, 578, 613))
        self.tabWidget_SFM.setFont(font_ee)
        self.tabWidget_SFM.setObjectName("tabWidget_SFM")

        # Tab: Detector images
        linedit_size_X = 30
        linedit_size_Y = 18
        self.tab_det_images = QtWidgets.QWidget()
        self.tab_det_images.setObjectName("tab_det_images")
        self.graphicsView_det_integr = pg.PlotWidget(self.tab_det_images)
        self.graphicsView_det_integr.setGeometry(QtCore.QRect(0, 450, 577, 90))
        self.graphicsView_det_integr.setObjectName("graphicsView_det_integr")
        self.graphicsView_det_integr.hideAxis("left")
        self.graphicsView_det_integr.setMouseEnabled(y=False)
        self.graphicsView_det_images = pg.ImageView(self.tab_det_images)
        self.graphicsView_det_images.setGeometry(QtCore.QRect(0, 30, 577, 510))
        self.graphicsView_det_images.setObjectName("graphicsView_det_images")
        self.graphicsView_det_images.ui.histogram.hide()
        self.graphicsView_det_images.ui.menuBtn.hide()
        self.graphicsView_det_images.ui.roiBtn.hide()
        self.label_point_number = QtWidgets.QLabel(self.tab_det_images)
        self.label_point_number.setFont(font_ee)
        self.label_point_number.setGeometry(QtCore.QRect(10, 8, 70, 16))
        self.label_point_number.setObjectName("label_point_number")
        self.label_point_number.setText("Point number")
        self.comboBox_point_number = QtWidgets.QComboBox(self.tab_det_images)
        self.comboBox_point_number.setFont(font_ee)
        self.comboBox_point_number.setGeometry(QtCore.QRect(80, 7, 55, 20))
        self.comboBox_point_number.setObjectName("comboBox_point_number")
        self.label_polarisation = QtWidgets.QLabel(self.tab_det_images)
        self.label_polarisation.setFont(font_ee)
        self.label_polarisation.setGeometry(QtCore.QRect(155, 8, 60, 16))
        self.label_polarisation.setObjectName("label_polarisation")
        self.label_polarisation.setText("Polarisation")
        self.comboBox_polarisation = QtWidgets.QComboBox(self.tab_det_images)
        self.comboBox_polarisation.setFont(font_ee)
        self.comboBox_polarisation.setGeometry(QtCore.QRect(215, 7, 40, 20))
        self.comboBox_polarisation.setObjectName("comboBox_polarisation")
        self.label_color_scheme = QtWidgets.QLabel(self.tab_det_images)
        self.label_color_scheme.setFont(font_ee)
        self.label_color_scheme.setGeometry(QtCore.QRect(268, 8, 60, 16))
        self.label_color_scheme.setObjectName("label_color_scheme")
        self.label_color_scheme.setText("Colors")
        self.comboBox_colors_cheme = QtWidgets.QComboBox(self.tab_det_images)
        self.comboBox_colors_cheme.setFont(font_ee)
        self.comboBox_colors_cheme.setGeometry(QtCore.QRect(305, 7, 90, 20))
        self.comboBox_colors_cheme.setObjectName("comboBox_colors_cheme")
        self.pushButton_det_int_show = QtWidgets.QPushButton(self.tab_det_images)
        self.pushButton_det_int_show.setGeometry(QtCore.QRect(445, 7, 120, 20))
        self.pushButton_det_int_show.setFont(font_button)
        self.pushButton_det_int_show.setObjectName("pushButton_det_int_show")
        self.pushButton_det_int_show.setText("Integrated ROI")

        self.label_slits = QtWidgets.QLabel(self.tab_det_images)
        self.label_slits.setFont(font_ee)
        self.label_slits.setGeometry(QtCore.QRect(385, 565, 51, 16))
        self.label_slits.setObjectName("label_slits")
        self.label_slits.setText("Slits (mm):")
        self.label_slit_s1hg = QtWidgets.QLabel(self.tab_det_images)
        self.label_slit_s1hg.setFont(font_ee)
        self.label_slit_s1hg.setGeometry(QtCore.QRect(440, 565, 41, 16))
        self.label_slit_s1hg.setObjectName("label_slit_s1hg")
        self.label_slit_s1hg.setText("s1hg")
        self.lineEdit_slits_s1hg = QtWidgets.QLineEdit(self.tab_det_images)
        self.lineEdit_slits_s1hg.setFont(font_ee)
        self.lineEdit_slits_s1hg.setGeometry(QtCore.QRect(470, 565, linedit_size_X, linedit_size_Y))
        self.lineEdit_slits_s1hg.setObjectName("lineEdit_slits_s1hg")
        self.lineEdit_slits_s1hg.setEnabled(False)
        self.lineEdit_slits_s1hg.setStyleSheet("color:rgb(0,0,0)")
        self.label_slit_s2hg = QtWidgets.QLabel(self.tab_det_images)
        self.label_slit_s2hg.setFont(font_ee)
        self.label_slit_s2hg.setGeometry(QtCore.QRect(505, 565, 30, 16))
        self.label_slit_s2hg.setObjectName("label_slit_s2hg")
        self.label_slit_s2hg.setText("s2hg")
        self.lineEdit_slits_s2hg = QtWidgets.QLineEdit(self.tab_det_images)
        self.lineEdit_slits_s2hg.setFont(font_ee)
        self.lineEdit_slits_s2hg.setGeometry(QtCore.QRect(535, 565, linedit_size_X, linedit_size_Y))
        self.lineEdit_slits_s2hg.setObjectName("lineEdit_slits_s2hg")
        self.lineEdit_slits_s2hg.setEnabled(False)
        self.lineEdit_slits_s2hg.setStyleSheet("color:rgb(0,0,0)")
        self.label_time = QtWidgets.QLabel(self.tab_det_images)
        self.label_time.setFont(font_ee)
        self.label_time.setGeometry(QtCore.QRect(385, 545, 71, 16))
        self.label_time.setObjectName("label_time")
        self.label_time.setText("Time (s):")
        self.lineEdit_time = QtWidgets.QLineEdit(self.tab_det_images)
        self.lineEdit_time.setFont(font_ee)
        self.lineEdit_time.setGeometry(QtCore.QRect(470, 545, linedit_size_X, linedit_size_Y))
        self.lineEdit_time.setObjectName("lineEdit_time")
        self.lineEdit_time.setEnabled(False)
        self.lineEdit_time.setStyleSheet("color:rgb(0,0,0)")
        self.label_ROI = QtWidgets.QLabel(self.tab_det_images)
        self.label_ROI.setFont(font_ee)
        self.label_ROI.setGeometry(QtCore.QRect(10, 545, 31, 16))
        self.label_ROI.setObjectName("label_ROI")
        self.label_ROI.setText("ROI:  ")
        self.label_ROI_x_left = QtWidgets.QLabel(self.tab_det_images)
        self.label_ROI_x_left.setFont(font_ee)
        self.label_ROI_x_left.setGeometry(QtCore.QRect(40, 545, 51, 16))
        self.label_ROI_x_left.setObjectName("label_ROI_x_left")
        self.label_ROI_x_left.setText("left")
        self.lineEdit_ROI_x_left = QtWidgets.QLineEdit(self.tab_det_images)
        self.lineEdit_ROI_x_left.setFont(font_ee)
        self.lineEdit_ROI_x_left.setGeometry(QtCore.QRect(75, 545, linedit_size_X, linedit_size_Y))
        self.lineEdit_ROI_x_left.setObjectName("lineEdit_ROI_x_left")
        self.label_ROI_x_right = QtWidgets.QLabel(self.tab_det_images)
        self.label_ROI_x_right.setFont(font_ee)
        self.label_ROI_x_right.setGeometry(QtCore.QRect(115, 545, 51, 16))
        self.label_ROI_x_right.setObjectName("label_ROI_x_right")
        self.label_ROI_x_right.setText("right")
        self.lineEdit_ROI_x_right = QtWidgets.QLineEdit(self.tab_det_images)
        self.lineEdit_ROI_x_right.setFont(font_ee)
        self.lineEdit_ROI_x_right.setGeometry(QtCore.QRect(140, 545, linedit_size_X, linedit_size_Y))
        self.lineEdit_ROI_x_right.setObjectName("lineEdit_ROI_x_right")
        self.label_ROI_y_bottom = QtWidgets.QLabel(self.tab_det_images)
        self.label_ROI_y_bottom.setFont(font_ee)
        self.label_ROI_y_bottom.setGeometry(QtCore.QRect(40, 565, 51, 16))
        self.label_ROI_y_bottom.setObjectName("label_ROI_y_bottom")
        self.label_ROI_y_bottom.setText("bottom")
        self.lineEdit_ROI_y_bottom = QtWidgets.QLineEdit(self.tab_det_images)
        self.lineEdit_ROI_y_bottom.setFont(font_ee)
        self.lineEdit_ROI_y_bottom.setGeometry(QtCore.QRect(75, 565, linedit_size_X, linedit_size_Y))
        self.lineEdit_ROI_y_bottom.setObjectName("lineEdit_ROI_y_bottom")
        self.label_ROI_y_top = QtWidgets.QLabel(self.tab_det_images)
        self.label_ROI_y_top.setFont(font_ee)
        self.label_ROI_y_top.setGeometry(QtCore.QRect(115, 565, 51, 16))
        self.label_ROI_y_top.setObjectName("label_ROI_y_top")
        self.label_ROI_y_top.setText("top")
        self.lineEdit_ROI_y_top = QtWidgets.QLineEdit(self.tab_det_images)
        self.lineEdit_ROI_y_top.setFont(font_ee)
        self.lineEdit_ROI_y_top.setGeometry(QtCore.QRect(140, 565, linedit_size_X, linedit_size_Y))
        self.lineEdit_ROI_y_top.setObjectName("lineEdit_ROI_y_top")

        self.label_ROI_BKG = QtWidgets.QLabel(self.tab_det_images)
        self.label_ROI_BKG.setFont(font_ee)
        self.label_ROI_BKG.setGeometry(QtCore.QRect(190, 545, 47, 16))
        self.label_ROI_BKG.setObjectName("label_ROI_BKG")
        self.label_ROI_BKG.setText("ROI BKG:")
        self.label_ROI_BKG_x_left = QtWidgets.QLabel(self.tab_det_images)
        self.label_ROI_BKG_x_left.setFont(font_ee)
        self.label_ROI_BKG_x_left.setGeometry(QtCore.QRect(240, 545, 51, 16))
        self.label_ROI_BKG_x_left.setObjectName("label_ROI_BKG_x_left")
        self.label_ROI_BKG_x_left.setText("left")
        self.lineEdit_ROI_BKG_x_left = QtWidgets.QLineEdit(self.tab_det_images)
        self.lineEdit_ROI_BKG_x_left.setFont(font_ee)
        self.lineEdit_ROI_BKG_x_left.setGeometry(QtCore.QRect(275, 545, linedit_size_X, linedit_size_Y))
        self.lineEdit_ROI_BKG_x_left.setObjectName("lineEdit_ROI_BKG_x_left")
        self.lineEdit_ROI_BKG_x_left.setEnabled(False)
        self.lineEdit_ROI_BKG_x_left.setStyleSheet("color:rgb(0,0,0)")
        self.label_ROI_BKG_x_right = QtWidgets.QLabel(self.tab_det_images)
        self.label_ROI_BKG_x_right.setFont(font_ee)
        self.label_ROI_BKG_x_right.setGeometry(QtCore.QRect(315, 545, 51, 16))
        self.label_ROI_BKG_x_right.setObjectName("label_ROI_BKG_x_right")
        self.label_ROI_BKG_x_right.setText("right")
        self.lineEdit_ROI_BKG_x_right = QtWidgets.QLineEdit(self.tab_det_images)
        self.lineEdit_ROI_BKG_x_right.setFont(font_ee)
        self.lineEdit_ROI_BKG_x_right.setGeometry(QtCore.QRect(340, 545, linedit_size_X, linedit_size_Y))
        self.lineEdit_ROI_BKG_x_right.setObjectName("lineEdit_ROI_BKG_x_right")
        self.label_ROI_BKG_y_bottom = QtWidgets.QLabel(self.tab_det_images)
        self.label_ROI_BKG_y_bottom.setFont(font_ee)
        self.label_ROI_BKG_y_bottom.setGeometry(QtCore.QRect(240, 565, 51, 16))
        self.label_ROI_BKG_y_bottom.setObjectName("label_ROI_BKG_y_bottom")
        self.label_ROI_BKG_y_bottom.setText("bottom")
        self.lineEdit_ROI_BKG_y_bottom = QtWidgets.QLineEdit(self.tab_det_images)
        self.lineEdit_ROI_BKG_y_bottom.setFont(font_ee)
        self.lineEdit_ROI_BKG_y_bottom.setGeometry(QtCore.QRect(275, 565, linedit_size_X, linedit_size_Y))
        self.lineEdit_ROI_BKG_y_bottom.setObjectName("lineEdit_ROI_BKG_y_bottom")
        self.lineEdit_ROI_BKG_y_bottom.setEnabled(False)
        self.lineEdit_ROI_BKG_y_bottom.setStyleSheet("color:rgb(0,0,0)")
        self.label_ROI_BKG_y_top = QtWidgets.QLabel(self.tab_det_images)
        self.label_ROI_BKG_y_top.setFont(font_ee)
        self.label_ROI_BKG_y_top.setGeometry(QtCore.QRect(315, 565, 51, 16))
        self.label_ROI_BKG_y_top.setObjectName("label_ROI_BKG_y_top")
        self.label_ROI_BKG_y_top.setText("top")
        self.lineEdit_ROI_BKG_y_top = QtWidgets.QLineEdit(self.tab_det_images)
        self.lineEdit_ROI_BKG_y_top.setFont(font_ee)
        self.lineEdit_ROI_BKG_y_top.setGeometry(QtCore.QRect(340, 565, linedit_size_X, linedit_size_Y))
        self.lineEdit_ROI_BKG_y_top.setObjectName("lineEdit_ROI_BKG_y_top")
        self.lineEdit_ROI_BKG_y_top.setEnabled(False)
        self.lineEdit_ROI_BKG_y_top.setStyleSheet("color:rgb(0,0,0)")

        self.tabWidget_SFM.addTab(self.tab_det_images, "")
        self.tabWidget_SFM.setTabText(self.tabWidget_SFM.indexOf(self.tab_det_images), "Detector Images")

        # Tab: Reflectivity preview
        self.tab_refl_preview = QtWidgets.QWidget()
        self.tab_refl_preview.setObjectName("tab_refl_preview")
        self.graphicsView_refl_profile = pg.PlotWidget(self.tab_refl_preview)
        self.graphicsView_refl_profile.setGeometry(QtCore.QRect(0, 20, 577, 540))
        self.graphicsView_refl_profile.setObjectName("graphicsView_refl_profile")
        self.graphicsView_refl_profile.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_refl_profile.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_refl_profile.getAxis("left").tickFont = font_graphs
        self.graphicsView_refl_profile.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_refl_profile.showAxis("top")
        self.graphicsView_refl_profile.getAxis("top").tickFont = font_graphs_2
        self.graphicsView_refl_profile.getAxis("top").setStyle(tickTextOffset=-2)
        self.graphicsView_refl_profile.showAxis("right")
        self.graphicsView_refl_profile.getAxis("right").tickFont = font_graphs_2
        self.graphicsView_refl_profile.getAxis("right").setStyle(tickTextOffset=-2)
        self.checkBox_show_overillumination = QtWidgets.QCheckBox(self.tab_refl_preview)
        self.checkBox_show_overillumination.setFont(font_ee)
        self.checkBox_show_overillumination.setGeometry(QtCore.QRect(10, 7, 150, 18))
        self.checkBox_show_overillumination.setObjectName("checkBox_show_overillumination")
        self.checkBox_show_overillumination.setText("Show Overillumination")
        self.comboBox_plot_axis = QtWidgets.QComboBox(self.tab_refl_preview)
        self.comboBox_plot_axis.setFont(font_ee)
        self.comboBox_plot_axis.setGeometry(QtCore.QRect(380, 7, 185, 20))
        self.comboBox_plot_axis.setObjectName("comboBox_plot_axis")
        self.comboBox_plot_axis.addItem("Reflectivity (log) vs Angle (Qz)")
        self.comboBox_plot_axis.addItem("Reflectivity (lin) vs Angle (Qz)")
        self.comboBox_plot_axis.addItem("Reflectivity (log) vs Angle (deg)")
        self.comboBox_plot_axis.addItem("Reflectivity (lin) vs Angle (deg)")
        self.checkBox_incl_errorbars = QtWidgets.QCheckBox(self.tab_refl_preview)
        self.checkBox_incl_errorbars.setFont(font_ee)
        self.checkBox_incl_errorbars.setGeometry(QtCore.QRect(10, 565, 111, 18))
        self.checkBox_incl_errorbars.setObjectName("checkBox_incl_errorbars")
        self.checkBox_incl_errorbars.setText("Include Error Bars")
        self.label_skip_first_points = QtWidgets.QLabel(self.tab_refl_preview)
        self.label_skip_first_points.setFont(font_ee)
        self.label_skip_first_points.setGeometry(QtCore.QRect(372, 565, 100, 16))
        self.label_skip_first_points.setObjectName("label_skip_first_points")
        self.label_skip_first_points.setText("Points to skip:  left")
        self.lineEdit_skip_first_points = QtWidgets.QLineEdit(self.tab_refl_preview)
        self.lineEdit_skip_first_points.setFont(font_ee)
        self.lineEdit_skip_first_points.setGeometry(QtCore.QRect(470, 565, linedit_size_X, linedit_size_Y))
        self.lineEdit_skip_first_points.setObjectName("lineEdit_skip_first_points")
        self.lineEdit_skip_first_points.setText("0")
        self.label_skip_last_points = QtWidgets.QLabel(self.tab_refl_preview)
        self.label_skip_last_points.setFont(font_ee)
        self.label_skip_last_points.setGeometry(QtCore.QRect(510, 565, 80, 16))
        self.label_skip_last_points.setObjectName("label_skip_last_points")
        self.label_skip_last_points.setText("right")
        self.lineEdit_skip_last_points = QtWidgets.QLineEdit(self.tab_refl_preview)
        self.lineEdit_skip_last_points.setFont(font_ee)
        self.lineEdit_skip_last_points.setGeometry(QtCore.QRect(535, 565, linedit_size_X, linedit_size_Y))
        self.lineEdit_skip_last_points.setObjectName("lineEdit_skip_last_points")
        self.lineEdit_skip_last_points.setText("0")
        self.tabWidget_SFM.addTab(self.tab_refl_preview, "")
        self.tabWidget_SFM.setTabText(self.tabWidget_SFM.indexOf(self.tab_refl_preview), "Reflectivity preview")

        # Tab: 2D Map
        self.tab_map = QtWidgets.QWidget()
        self.tab_map.setObjectName("tab_map")
        # scaling options are different for different views "horizontalSlider" for "Pizel vs Point" and "comboBox" for "Qx vs Qz"
        self.horizontalSlider_scale = QtWidgets.QSlider(self.tab_map)
        self.horizontalSlider_scale.setGeometry(QtCore.QRect(5, 7, 150, 22))
        self.horizontalSlider_scale.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_scale.setObjectName("horizontalSlider_scale")
        self.horizontalSlider_scale.setMinimum(0)
        self.horizontalSlider_scale.setMaximum(1000)
        self.horizontalSlider_scale.setValue(40)
        self.label_scale = QtWidgets.QLabel(self.tab_map)
        self.label_scale.setFont(font_ee)
        self.label_scale.setGeometry(QtCore.QRect(5, 8, 121, 16))
        self.label_scale.setObjectName("label_polarisation")
        self.label_scale.setText("Decrease pts number by")
        self.label_scale.setVisible(False)
        self.comboBox_scale = QtWidgets.QComboBox(self.tab_map)
        self.comboBox_scale.setFont(font_ee)
        self.comboBox_scale.setGeometry(QtCore.QRect(130, 7, 40, 20))
        self.comboBox_scale.setObjectName("comboBox_polarisation")
        self.comboBox_scale.addItem("5")
        self.comboBox_scale.addItem("4")
        self.comboBox_scale.addItem("3")
        self.comboBox_scale.addItem("2")
        self.comboBox_scale.addItem("1")
        self.comboBox_scale.setVisible(False)
        self.label_polarisation_2d_map = QtWidgets.QLabel(self.tab_map)
        self.label_polarisation_2d_map.setFont(font_ee)
        self.label_polarisation_2d_map.setGeometry(QtCore.QRect(184, 8, 71, 16))
        self.label_polarisation_2d_map.setObjectName("label_polarisation")
        self.label_polarisation_2d_map.setText("Polarisation")
        self.comboBox_polarisation_2d_map = QtWidgets.QComboBox(self.tab_map)
        self.comboBox_polarisation_2d_map.setFont(font_ee)
        self.comboBox_polarisation_2d_map.setGeometry(QtCore.QRect(244, 7, 40, 20))
        self.comboBox_polarisation_2d_map.setObjectName("comboBox_polarisation")
        self.label_axis = QtWidgets.QLabel(self.tab_map)
        self.label_axis.setFont(font_ee)
        self.label_axis.setGeometry(QtCore.QRect(300, 8, 71, 16))
        self.label_axis.setObjectName("label_axis")
        self.label_axis.setText("Axis")
        self.comboBox_axis = QtWidgets.QComboBox(self.tab_map)
        self.comboBox_axis.setFont(font_ee)
        self.comboBox_axis.setGeometry(QtCore.QRect(325, 7, 110, 20))
        self.comboBox_axis.setObjectName("comboBox_axis")
        self.comboBox_axis.addItem("Pixel vs. Point")
        self.comboBox_axis.addItem("Theta vs. 2Theta")
        self.comboBox_axis.addItem("Qx vs. Qz")
        self.pushButton_refresh_2d_map = QtWidgets.QPushButton(self.tab_map)
        self.pushButton_refresh_2d_map.setGeometry(QtCore.QRect(450, 7, 120, 20))
        self.pushButton_refresh_2d_map.setFont(font_button)
        self.pushButton_refresh_2d_map.setObjectName("pushButton_refresh_2d_map")
        self.pushButton_refresh_2d_map.setText("Refresh 2D map")
        self.graphicsView_map = pg.ImageView(self.tab_map)
        self.graphicsView_map.setGeometry(QtCore.QRect(0, 30, 577, 522))
        self.graphicsView_map.setObjectName("graphicsView_map")
        self.graphicsView_map.ui.menuBtn.hide()
        self.graphicsView_map.ui.roiBtn.hide()
        self.graphicsView_map.ui.histogram.hide()
        colmap = pg.ColorMap(numpy.array([0.0,0.1,1.0]),
                             numpy.array([[0,0,0,255],[255,128,0,255],[255,255,0,255]], dtype=numpy.ubyte))
        self.graphicsView_map.setColorMap(colmap)
        # 2D map for "Qx vs Qz" is a plot, compared to "Pixel vs Points" which is Image.
        # I rescale graphicsView_map_Qxz_Theta to show/hide it
        self.graphicsView_map_Qxz_Theta = pg.PlotWidget(self.tab_map)
        self.graphicsView_map_Qxz_Theta.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.graphicsView_map_Qxz_Theta.setObjectName("graphicsView_map_Qxz_Theta")
        self.graphicsView_map_Qxz_Theta.getAxis("bottom").tickFont = font_graphs
        self.graphicsView_map_Qxz_Theta.getAxis("bottom").setStyle(tickTextOffset=10)
        self.graphicsView_map_Qxz_Theta.getAxis("left").tickFont = font_graphs
        self.graphicsView_map_Qxz_Theta.getAxis("left").setStyle(tickTextOffset=10)
        self.graphicsView_map_Qxz_Theta.showAxis("top")
        self.graphicsView_map_Qxz_Theta.getAxis("top").tickFont = font_graphs_2
        self.graphicsView_map_Qxz_Theta.getAxis("top").setStyle(tickTextOffset=-2)
        self.graphicsView_map_Qxz_Theta.showAxis("right")
        self.graphicsView_map_Qxz_Theta.getAxis("right").tickFont = font_graphs_2
        self.graphicsView_map_Qxz_Theta.getAxis("right").setStyle(tickTextOffset=-2)
        self.pushButton_export_2d_map = QtWidgets.QPushButton(self.tab_map)
        self.pushButton_export_2d_map.setGeometry(QtCore.QRect(450, 555, 120, 25))
        self.pushButton_export_2d_map.setFont(font_button)
        self.pushButton_export_2d_map.setObjectName("pushButton_export_2d_map")
        self.pushButton_export_2d_map.setText("Export 2D map")

        self.tabWidget_SFM.addTab(self.tab_map, "")
        self.tabWidget_SFM.setTabText(self.tabWidget_SFM.indexOf(self.tab_map), "2D map")

        # StatusBar
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # MenuBar
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1000, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuHelp.setTitle("Help")
        MainWindow.setMenuBar(self.menuBar)
        self.actionAlgorithm_info = QtWidgets.QAction(MainWindow)
        self.actionAlgorithm_info.setObjectName("actionAlgorithm_info")
        self.actionAlgorithm_info.setText("Algorithm info")
        self.actionVersion = QtWidgets.QAction(MainWindow)
        self.actionVersion.setObjectName("actionVersion")
        self.menuHelp.addAction(self.actionAlgorithm_info)
        self.menuHelp.addAction(self.actionVersion)
        self.actionVersion.setText("Version 1.4")
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.tabWidget_red_instr_exp.setCurrentIndex(0)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    ##<--

class GUI(Ui_MainWindow):

    current_dir = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

    def __init__(self):

        super(GUI, self).__init__()
        self.setupUi(self)

        # current file in Single File Mode
        self.SFM_file = ""
        self.SFM_file_already_analized = ""
        self.I_uu_sfm = []
        self.I_du_sfm = []
        self.I_ud_sfm = []
        self.I_dd_sfm = []

        # current th point
        self.current_th = ""

        # write calculated overillumination coefficients into library
        self.overill_coeff_lib = {}

        # Write DB info into library
        self.DB_info = {}
        self.DB_already_analized = []

        # ROI frames
        self.draw_roi = []
        self.draw_roi_2D_map = []

        # Recalc intens if Y roi is changed
        self.old_roi_coord_Y = []
        self.draw_roi_int = []

        # Trigger to switch the detector image view
        self.show_det_int_trigger = True

        # Actions on clicks
        self.pushButton_importScans.clicked.connect(self.button_ImportScans)
        self.pushButton_DeleteImportScans.clicked.connect(self.button_DeleteScans)
        self.pushButton_ImportDB.clicked.connect(self.button_ImportDB)
        self.pushButton_DeleteImportDB.clicked.connect(self.button_DeleteDB)
        self.toolButton_save_at.clicked.connect(self.button_SaveDir)
        self.pushButton_start_all.clicked.connect(self.button_Start_all)
        self.pushButton_start_sfm.clicked.connect(self.button_Start_sfm)
        self.pushButton_clear.clicked.connect(self.button_Clear)
        self.pushButton_export_2d_map.clicked.connect(self.export_2d_map)
        self.pushButton_det_int_show.clicked.connect(self.show_det_int)
        self.pushButton_refresh_2d_map.clicked.connect(self.draw_2D_map)

        self.lineEdit_ROI_x_left.editingFinished.connect(self.update_slits)
        self.lineEdit_ROI_x_right.editingFinished.connect(self.update_slits)
        self.lineEdit_ROI_y_bottom.editingFinished.connect(self.update_slits)
        self.lineEdit_ROI_y_top.editingFinished.connect(self.update_slits)
        self.lineEdit_ROI_BKG_x_right.editingFinished.connect(self.update_slits)

        self.comboBox_point_number.currentIndexChanged.connect(self.change_pol_or_ang)
        self.comboBox_polarisation.currentIndexChanged.connect(self.change_pol_or_ang)
        self.comboBox_polarisation_2d_map.currentIndexChanged.connect(self.draw_2D_map)
        self.horizontalSlider_scale.valueChanged.connect(self.draw_2D_map)
        self.comboBox_axis.currentIndexChanged.connect(self.draw_2D_map)
        self.comboBox_scan.currentIndexChanged.connect(self.load_detector_images)
        self.comboBox_scan.currentIndexChanged.connect(self.load_reflectivity_preview)
        self.comboBox_scan.currentIndexChanged.connect(self.draw_2D_map)
        self.lineEdit_SampleLength.textChanged.connect(self.load_reflectivity_preview)
        self.checkBox_DevideByMon.stateChanged.connect(self.load_reflectivity_preview)
        self.checkBox_NormDB.stateChanged.connect(self.load_reflectivity_preview)
        self.checkBox_DBatten.stateChanged.connect(self.load_reflectivity_preview)
        self.lineEdit_AttenCorrFactor.textChanged.connect(self.load_reflectivity_preview)
        self.checkBox_OverillCorr.stateChanged.connect(self.load_reflectivity_preview)
        self.lineEdit_SkipSubtrBKG.textChanged.connect(self.load_reflectivity_preview)
        self.checkBox_SubtrBKG.stateChanged.connect(self.load_reflectivity_preview)
        self.checkBox_show_overillumination.stateChanged.connect(self.load_reflectivity_preview)
        self.checkBox_incl_errorbars.stateChanged.connect(self.load_reflectivity_preview)
        self.lineEdit_wavelength.textChanged.connect(self.load_reflectivity_preview)
        self.lineEdit_wavel_resol.textChanged.connect(self.load_reflectivity_preview)
        self.lineEdit_s1_sample_dist.textChanged.connect(self.load_reflectivity_preview)
        self.lineEdit_s2_sample_dist.textChanged.connect(self.load_reflectivity_preview)
        self.lineEdit_full_scan_offset.textChanged.connect(self.load_reflectivity_preview)
        self.lineEdit_skip_last_points.textChanged.connect(self.load_reflectivity_preview)
        self.lineEdit_skip_first_points.textChanged.connect(self.load_reflectivity_preview)
        self.checkBox_db_arrangement_after.stateChanged.connect(self.assignDB)
        self.checkBox_db_arrangement_after.stateChanged.connect(self.load_reflectivity_preview)

        self.actionVersion.triggered.connect(self.menu_info)
        self.actionAlgorithm_info.triggered.connect(self.menu_algorithm)

        self.comboBox_colors_cheme.addItem("Green / Blue")
        self.comboBox_colors_cheme.addItem("White / Black")
        self.comboBox_colors_cheme.currentIndexChanged.connect(self.color_det_image)
        self.comboBox_plot_axis.currentIndexChanged.connect(self.load_reflectivity_preview)
        self.comboBox_scale.currentIndexChanged.connect(self.draw_2D_map)

    ##--> Main window buttons
    def button_ImportScans(self):
        import_files = QtWidgets.QFileDialog().getOpenFileNames(None, "FileNames", self.current_dir, ".h5 (*.h5)")
        if import_files[0] == []: return
        # Next "Import scans" will open last dir
        self.current_dir = import_files[0][0][:import_files[0][0].rfind("/")]

        for file in import_files[0]:
            self.tableWidget_Scans.insertRow(self.tableWidget_Scans.rowCount())
            self.tableWidget_Scans.setRowHeight(self.tableWidget_Scans.rowCount()-1, 10)
            # File name (row 0) and full path (row 2)
            for j in range(0, 4):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget_Scans.setItem(self.tableWidget_Scans.rowCount()-1, j, item)
            self.tableWidget_Scans.item(self.tableWidget_Scans.rowCount() - 1, 0).setText(file[file.rfind("/") + 1:])
            self.tableWidget_Scans.item(self.tableWidget_Scans.rowCount() - 1, 3).setText(file)

            # add file into SFM / Scan ComboBox
            self.comboBox_scan.addItem(str(file[file.rfind("/") + 1:]))

            self.analazeDB()

            self.load_reflectivity_preview()

    def button_DeleteScans(self):
        remove_files = self.tableWidget_Scans.selectedItems()
        if not remove_files: return

        for file in remove_files:
            self.tableWidget_Scans.removeRow(self.tableWidget_Scans.row(file))

        # update SFM list
        self.comboBox_scan.clear()

        for i in range(0, self.tableWidget_Scans.rowCount()):
            # add file into SFM
            self.comboBox_scan.addItem(self.tableWidget_Scans.item(i, 3).text()[
                        self.tableWidget_Scans.item(i, 3).text().rfind("/") + 1:])

    def button_ImportDB(self):
        import_files = QtWidgets.QFileDialog().getOpenFileNames(None, "FileNames", self.current_dir, ".h5 (*.h5)")
        if import_files[0] == []: return
        # Next "Import scans" will open last dir
        self.current_dir = import_files[0][0][:import_files[0][0].rfind("/")]

        # I couldnt make tablewidget sorting work when adding files to not empty table, so this is the solution for making the list of DB files sorted
        for i in range(self.tableWidget_DB.rowCount()-1, -1, -1):
            import_files[0].append(self.tableWidget_DB.item(i, 1).text())
            self.tableWidget_DB.removeRow(i)

        for file in sorted(import_files[0]):
            self.tableWidget_DB.insertRow(self.tableWidget_DB.rowCount())
            self.tableWidget_DB.setRowHeight(self.tableWidget_DB.rowCount()-1, 10)
            # File name (row 0) and full path (row 2)
            for j in range(0, 2):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget_DB.setItem(self.tableWidget_DB.rowCount()-1, j, item)
            self.tableWidget_DB.item(self.tableWidget_DB.rowCount() - 1, 0).setText(file[file.rfind("/") + 1:])
            self.tableWidget_DB.item(self.tableWidget_DB.rowCount() - 1, 1).setText(file)

        self.analazeDB()
        self.load_reflectivity_preview()

    def button_DeleteDB(self):
        remove_files = self.tableWidget_DB.selectedItems()
        if not remove_files: return

        for file in remove_files:
            self.tableWidget_DB.removeRow(self.tableWidget_DB.row(file))

        self.analazeDB()

    def button_SaveDir(self):
        saveAt = QtWidgets.QFileDialog().getExistingDirectory()
        if not saveAt: return

        self.lineEdit_saveAt.setText(str(saveAt))
        if not str(saveAt)[-1] == "/": self.lineEdit_saveAt.setText(str(saveAt) + "/")

    def button_Start_all(self):

        self.listWidget_filesToCheck.clear()

        if self.lineEdit_SkipSubtrBKG.text(): skip_BKG = float(self.lineEdit_SkipSubtrBKG.text())
        else: skip_BKG = 0

        save_file_directory = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + '/'
        if self.lineEdit_saveAt.text(): save_file_directory = self.lineEdit_saveAt.text()

        if self.checkBox_OverillCorr.isChecked() and self.lineEdit_SampleLength.text() == "":
            self.statusbar.showMessage("Sample length is missing")
            return
        else:
            sample_len = 999
            if self.lineEdit_SampleLength.text(): sample_len = self.lineEdit_SampleLength.text()

        if self.checkBox_NormDB.isChecked():
            if self.tableWidget_DB.rowCount() == 0:
                self.label_DB_missing.setVisible(True)
                return

            if self.checkBox_DBatten.isChecked():
                DB_atten_factor = 10.4
                if not self.lineEdit_AttenCorrFactor.text() == "":
                    DB_atten_factor = float(self.lineEdit_AttenCorrFactor.text())
            else:
                DB_atten_factor = 1

        # iterate through table with scans
        for i in range(0, self.tableWidget_Scans.rowCount()):
            file_name = self.tableWidget_Scans.item(i, 3).text()[
                        self.tableWidget_Scans.item(i, 3).text().rfind("/") + 1: -3]

            # find full name DB file if there are several of them
            if self.checkBox_NormDB.isChecked(): DB_file_scan = self.tableWidget_Scans.item(i, 2).text()
            else: DB_file_scan = ""

            with h5py.File(self.tableWidget_Scans.item(i, 3).text(), 'r') as file:

                scan_data_instr = file[list(file.keys())[0]].get("instrument")
                motors_data = numpy.array(scan_data_instr.get('motors').get('data')).T
                scalers_data = numpy.array(scan_data_instr.get('scalers').get('data')).T

                for index, motor in enumerate(scan_data_instr.get('motors').get('SPEC_motor_mnemonics')):
                    if "'th'" in str(motor): th_motor_data = motors_data[index]
                    elif "'s1hg'" in str(motor): s1hg_motor_data = motors_data[index]
                    elif "'s2hg'" in str(motor): s2hg_motor_data = motors_data[index]

                check_this_file = 0

                # check if we have several polarisations
                for detector in scan_data_instr.get('detectors'):
                    if str(detector) not in ("psd", "psd_du", "psd_uu", "psd_ud", "psd_dd"): continue

                    for index, scaler in enumerate(scan_data_instr.get('scalers').get('SPEC_counter_mnemonics')):
                        if "'mon0'" in str(scaler) and str(detector) == "psd": monitor_scalers_data = scalers_data[index]
                        elif "'m1'" in str(scaler) and str(detector) == "psd_uu": monitor_scalers_data = scalers_data[index]
                        elif "'m2'" in str(scaler) and str(detector) == "psd_dd": monitor_scalers_data = scalers_data[index]
                        elif "'m3'" in str(scaler) and str(detector) == "psd_du": monitor_scalers_data = scalers_data[index]
                        elif "'m4'" in str(scaler) and str(detector) == "psd_ud": monitor_scalers_data = scalers_data[index]

                    original_roi_coord = numpy.array(scan_data_instr.get('scalers').get('roi').get("roi"))


                    scan_intens = scan_data_instr.get("detectors").get(str(detector)).get('data')[:,
                                      int(original_roi_coord[0]): int(original_roi_coord[1]), :].sum(axis=1)

                    new_file = open(
                        save_file_directory + file_name + "_" + str(detector) + " (" + DB_file_scan + ")" + ".dat", "w")

                    # iterate through th points
                    for index, th in enumerate(th_motor_data):

                        # analize integrated intensity for ROI
                        if len(scan_intens.shape) == 1: Intens = scan_intens[index]
                        elif len(scan_intens.shape) == 2: Intens = sum(scan_intens[index][int(original_roi_coord[2]): int(original_roi_coord[3])])

                        if Intens == 0 and self.checkBox_remove_zeros.isChecked(): continue

                        if Intens == 0: Intens_err = 1
                        else: Intens_err = numpy.sqrt(Intens)

                        # read motors
                        Qz = (4 * numpy.pi / float(self.lineEdit_wavelength.text())) * numpy.sin(numpy.radians(th))
                        s1hg = s1hg_motor_data[index]
                        s2hg = s2hg_motor_data[index]
                        monitor = monitor_scalers_data[index]

                        # check if we are not in a middle of ROI in Qz approx 0.02)
                        if round(Qz, 3) == 0.015 and check_this_file == 0:
                            scan_data_0_015 = scan_intens[index][int(original_roi_coord[2]): int(original_roi_coord[3])]

                            if not max(scan_data_0_015) == max(scan_data_0_015[round((len(scan_data_0_015) / 3)):-round(
                                    (len(scan_data_0_015) / 3))]):
                                self.listWidget_filesToCheck.addItem(file_name)
                                check_this_file = 1

                        coeff = self.overillumination_correct_coeff(s1hg, s2hg, round(th, 4))
                        FWHM_proj = coeff[1]

                        if not self.checkBox_OverillCorr.isChecked():
                            overill_corr = 1
                        else:
                            overill_corr = coeff[0]

                        # calculate resolution in Sared way or better
                        if self.checkBox_resol_sared.isChecked():
                            Resolution = numpy.sqrt(((2 * numpy.pi / float(self.lineEdit_wavelength.text())) ** 2) * (
                                    (numpy.cos(numpy.radians(th))) ** 2) * (0.68 ** 2) * ((s1hg ** 2) + (s2hg ** 2)) / (
                                                                (float(
                                                                    self.lineEdit_s1_sample_dist.text()) - float(
                                                                    self.lineEdit_s2_sample_dist.text())) ** 2) + (
                                                            (float(self.lineEdit_wavel_resol.text()) ** 2) * (Qz ** 2)))
                        else:
                            if FWHM_proj == s2hg:
                                Resolution = numpy.sqrt(
                                    ((2 * numpy.pi / float(self.lineEdit_wavelength.text())) ** 2) * (
                                            (numpy.cos(numpy.radians(th))) ** 2) * (0.68 ** 2) * (
                                                (s1hg ** 2) + (s2hg ** 2)) / ((float(
                                        self.lineEdit_s1_sample_dist.text()) - float(
                                        self.lineEdit_s2_sample_dist.text())) ** 2) + (
                                                (float(self.lineEdit_wavel_resol.text()) ** 2) * (Qz ** 2)))
                            else:
                                Resolution = numpy.sqrt(
                                    ((2 * numpy.pi / float(self.lineEdit_wavelength.text())) ** 2) * (
                                            (numpy.cos(numpy.radians(th))) ** 2) * (0.68 ** 2) * (
                                            (s1hg ** 2) + (FWHM_proj ** 2)) / (
                                            float(self.lineEdit_s1_sample_dist.text()) ** 2) + (
                                            (float(self.lineEdit_wavel_resol.text()) ** 2) * (Qz ** 2)))

                        # I cite Gunnar in here "We are now saving dQ as sigma rather than FWHM for genx"
                        Resolution = Resolution / (2 * numpy.sqrt(2 * numpy.log(2)))

                        # minus background, devide by monitor, overillumination correct + calculate errors
                        if self.checkBox_SubtrBKG.isChecked() and Qz > skip_BKG:
                            Intens_bkg = sum(scan_intens[index][
                                             int(original_roi_coord[2]) - 2 * (int(original_roi_coord[3]) - int(original_roi_coord[2])): int(original_roi_coord[2]) - (
                                                         int(original_roi_coord[3]) - int(original_roi_coord[2]))])

                            if Intens_bkg > 0:
                                Intens_err = numpy.sqrt(Intens + Intens_bkg)
                                Intens = Intens - Intens_bkg

                        if self.checkBox_DevideByMon.isChecked():
                            if Intens == 0: Intens_err = Intens_err / monitor
                            else: Intens_err = (Intens / monitor) * numpy.sqrt((Intens_err / Intens) ** 2 + (1 / monitor))
                            Intens = Intens / monitor

                        if self.checkBox_OverillCorr.isChecked():
                            Intens_err = Intens_err / overill_corr
                            Intens = Intens / overill_corr

                        if self.checkBox_NormDB.isChecked():
                            DB_intens = float(
                                self.DB_info[str(DB_file_scan) + ";" + str(s1hg) + ";" + str(s2hg)].split(";")[0]) * DB_atten_factor
                            DB_err = overill_corr * float(
                                self.DB_info[str(DB_file_scan) + ";" + str(s1hg) + ";" + str(s2hg)].split(";")[1]) * self.DB_atten_factor

                            if Intens == 0: Intens_err += DB_err
                            else: Intens_err = (Intens / DB_intens) * numpy.sqrt((DB_err / DB_intens) ** 2 + (Intens_err / Intens) ** 2)

                            Intens = Intens / DB_intens

                        # skip first point
                        if index == 1: continue

                        if Intens == 0 and self.checkBox_remove_zeros.isChecked(): continue

                        new_file.write(str(Qz) + ' ' + str(Intens) + ' ' + str(Intens_err) + ' ')
                        if self.checkBox_add_resolution_column.isChecked(): new_file.write(str(Resolution))
                        new_file.write('\n')

                    # close files
                    new_file.close()

                    # check if file is empty - then comment inside
                    if os.stat(save_file_directory + file_name + "_" + str(detector) + " (" + DB_file_scan + ")" + ".dat").st_size == 0:
                        with open(save_file_directory + file_name + "_" + str(detector) + " (" + DB_file_scan + ")" + ".dat", "w") as empty_file:
                            empty_file.write("All points are either zeros or negatives.")

        self.statusbar.showMessage(str(self.tableWidget_Scans.rowCount()) + " files reduced, " + str(
            self.listWidget_filesToCheck.count()) + " files might need extra care.")

    def button_Start_sfm(self):

        # polarisation order - uu, dd, ud, du
        detector = ["uu", "du", "ud", "dd"]

        for i in range(0, len(self.SFM_export_Qz)):

            if self.checkBox_NormDB.isChecked():
                SFM_DB_file_export = self.SFM_DB_file
            else: SFM_DB_file_export = ""

            with open(self.lineEdit_saveAt.text() + self.SFM_file[self.SFM_file.rfind("/") + 1 : -3] + "_" + str(detector[i]) + " (" + SFM_DB_file_export + ")" + " SFM.dat", "w") as new_file:
                for j in range(0, len(self.SFM_export_Qz[i])):
                    if self.SFM_export_Qz[i][j] == 0: continue
                    if self.SFM_export_I[i][j] == 0 and self.checkBox_remove_zeros.isChecked(): continue
                    new_file.write(str(self.SFM_export_Qz[i][j]) + ' ' + str(self.SFM_export_I[i][j]) + ' ' + str(self.SFM_export_dI[i][j]) + ' ')
                    if self.checkBox_add_resolution_column.isChecked(): new_file.write(str(self.SFM_export_Resolution[i][j]))
                    new_file.write('\n')

            # close new file
            new_file.close()

        self.statusbar.showMessage(self.SFM_file[self.SFM_file.rfind("/") + 1:] + " file is reduced in SFM.")

    def button_Clear(self):

        self.comboBox_scan.clear()
        self.listWidget_filesToCheck.clear()
        self.graphicsView_det_images.clear()
        self.graphicsView_map.clear()
        self.graphicsView_refl_profile.getPlotItem().clear()
        self.comboBox_point_number.clear()
        self.comboBox_polarisation.clear()
        self.comboBox_polarisation_2d_map.clear()
        for i in range(self.tableWidget_Scans.rowCount(), -1, -1):
            self.tableWidget_Scans.removeRow(i)
        for i in range(self.tableWidget_DB.rowCount(), -1, -1):
            self.tableWidget_DB.removeRow(i)
    ##<--

    ##--> extra functions to shorten the code
    def overillumination_correct_coeff(self, s1hg, s2hg, th):

        # Check for Sample Length input
        try:
            sample_len = float(self.lineEdit_SampleLength.text())
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
                OB = ((float(self.lineEdit_s1_sample_dist.text()) * (s2hg - s1hg)) / (2 * (float(self.lineEdit_s1_sample_dist.text()) - float(self.lineEdit_s2_sample_dist.text())))) + s1hg / 2
                OC = ((float(self.lineEdit_s1_sample_dist.text()) * (s2hg + s1hg)) / (2 * (float(self.lineEdit_s1_sample_dist.text()) - float(self.lineEdit_s2_sample_dist.text())))) - s1hg / 2
            elif s1hg < s2hg:
                OB = ((s2hg * float(self.lineEdit_s1_sample_dist.text())) - (s1hg * float(self.lineEdit_s2_sample_dist.text()))) / (2 * (float(self.lineEdit_s1_sample_dist.text()) - float(self.lineEdit_s2_sample_dist.text())))
                OC = (float(self.lineEdit_s1_sample_dist.text()) / (float(self.lineEdit_s1_sample_dist.text()) - float(self.lineEdit_s2_sample_dist.text()))) * (s2hg + s1hg) / 2 - (s1hg / 2)
            elif s1hg == s2hg:
                OB = s1hg / 2
                OC = s1hg * (float(self.lineEdit_s1_sample_dist.text()) / (float(self.lineEdit_s1_sample_dist.text()) - float(self.lineEdit_s2_sample_dist.text())) - 1 / 2)

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

    def analazeDB(self):

        self.DB_info = {}

        for i in range(0, self.tableWidget_DB.rowCount()):
            with h5py.File(self.tableWidget_DB.item(i,1).text(), 'r') as file_db:
                scan_data_instr = file_db[list(file_db.keys())[0]].get("instrument")
                motors_data = numpy.array(scan_data_instr.get('motors').get('data')).T
                scalers_data = numpy.array(scan_data_instr.get('scalers').get('data')).T

                for index, motor in enumerate(scan_data_instr.get('motors').get('SPEC_motor_mnemonics')):
                    if "'th'" in str(motor):
                        th_motor_data = motors_data[index]
                    elif "'s1hg'" in str(motor):
                        s1hg_motor_data = motors_data[index]
                    elif "'s2hg'" in str(motor):
                        s2hg_motor_data = motors_data[index]

                for index, scaler in enumerate(scan_data_instr.get('scalers').get('SPEC_counter_mnemonics')):
                    if "'mon0'" in str(scaler):
                        monitor_scalers_data = scalers_data[index]
                    elif "'roi'" in str(scaler):
                        intens_scalers_data = scalers_data[index]

                for j in range(0, len(th_motor_data)):
                    DB_intens = float(intens_scalers_data[j]) / float(monitor_scalers_data[j])
                    DB_err = DB_intens * numpy.sqrt(1/float(intens_scalers_data[j]) + 1/float(monitor_scalers_data[j]))

                    scan_and_slits = self.tableWidget_DB.item(i, 0).text()[:5] + ";" + str(s1hg_motor_data[j]) + ";" + str(s2hg_motor_data[j])

                    DB_intens_and_err = str(DB_intens) + ";" + str(DB_err)
                    self.DB_info[scan_and_slits] = DB_intens_and_err

        if self.tableWidget_DB.rowCount() == 0:
            return
        else: self.assignDB()

    def assignDB(self):
        db_list = []
        for db_scan_number in self.DB_info: db_list.append(db_scan_number.split(";")[0])

        for i in range(self.tableWidget_Scans.rowCount()):
            scan_number = self.tableWidget_Scans.item(i, 0).text()[:5]

            # find nearest DB file if there are several of them
            if len(db_list) == 0: DB_file_scan = ""
            elif len(db_list) == 1: DB_file_scan = db_list[0][:5]
            else:
                if self.checkBox_db_arrangement_after.isChecked():
                    for j, db_scan in enumerate(db_list):
                        DB_file_scan = db_scan[:5]
                        if int(db_scan[:5]) > int(scan_number[:5]): break
                else:
                    for j, db_scan in enumerate(reversed(db_list)):
                        DB_file_scan = db_scan[:5]
                        if int(db_scan[:5]) < int(scan_number[:5]): break

            self.tableWidget_Scans.item(i, 2).setText(DB_file_scan)
    ##<--

    ##--> menu options
    def menu_info(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowIcon(QtGui.QIcon(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "\icon.png"))
        msgBox.setText( "pySAred. " + self.actionVersion.text() + "\n\n"
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

        if self.comboBox_scan.currentText() == "": return

        self.comboBox_point_number.clear()
        self.comboBox_polarisation.clear()
        self.comboBox_polarisation_2d_map.clear()

        # we need to find full path for the SFM file from the table
        for i in range(0, self.tableWidget_Scans.rowCount()):
            if self.tableWidget_Scans.item(i, 0).text() == self.comboBox_scan.currentText():
                self.SFM_file = self.tableWidget_Scans.item(i, 3).text()
                self.SFM_file_scan_num = int(self.tableWidget_Scans.item(i, 0).text()[:5])

        with h5py.File(self.SFM_file, 'r') as file:

            scan_data = file[list(file.keys())[0]]
            original_roi_coord = numpy.array(scan_data.get("instrument").get('scalers').get('roi').get("roi"))
            roi_width = int(original_roi_coord[3]) - int(original_roi_coord[2])

            self.lineEdit_ROI_x_left.setText(str(original_roi_coord[2])[:-2])
            self.lineEdit_ROI_x_right.setText(str(original_roi_coord[3])[:-2])
            self.lineEdit_ROI_y_bottom.setText(str(original_roi_coord[1])[:-2])
            self.lineEdit_ROI_y_top.setText(str(original_roi_coord[0])[:-2])
            self.lineEdit_ROI_BKG_x_left.setText(str(int(original_roi_coord[2]) - 2 * roi_width))
            self.lineEdit_ROI_BKG_x_right.setText(str(int(original_roi_coord[2]) - roi_width))
            self.lineEdit_ROI_BKG_y_bottom.setText(str(original_roi_coord[1])[:-2])
            self.lineEdit_ROI_BKG_y_top.setText(str(original_roi_coord[0])[:-2])

            for index, th in enumerate(scan_data.get("instrument").get('motors').get('th').get("value")):
                if str(th)[0:5] in ("-0.00", "0.00"): continue

                self.comboBox_point_number.addItem(str(round(th, 3)))

            if len(scan_data.get("ponos").get('data')) == 1:
                self.comboBox_polarisation.addItem("uu")
                self.comboBox_polarisation_2d_map.addItem("uu")
            for polarisation in scan_data.get("ponos").get('data'):
                if polarisation not in ("data_du", "data_uu", "data_dd", "data_ud"): continue
                if numpy.any(numpy.array(scan_data.get("ponos").get('data').get(polarisation))):
                    self.comboBox_polarisation.addItem(str(polarisation)[-2:])
                    self.comboBox_polarisation_2d_map.addItem(str(polarisation)[-2:])

            self.comboBox_polarisation.setCurrentIndex(0)
            self.comboBox_polarisation_2d_map.setCurrentIndex(0)

    def draw_det_image(self):

        self.graphicsView_det_images.clear()
        self.graphicsView_det_integr.clear()

        if self.SFM_file == "": return
        with h5py.File(self.SFM_file, 'r') as file:

            self.current_th = self.comboBox_point_number.currentText()

            scan_data_instr = file[list(file.keys())[0]].get("instrument")
            motors_data = numpy.array(scan_data_instr.get('motors').get('data')).T
            scalers_data = numpy.array(scan_data_instr.get('scalers').get('data')).T

            for index, motor in enumerate(scan_data_instr.get('motors').get('SPEC_motor_mnemonics')):
                if "'th'" in str(motor): self.th_motor_data = motors_data[index]
                elif "'tth'" in str(motor): self.tth_motor_data = motors_data[index]
                elif "'s1hg'" in str(motor): self.s1hg_motor_data = motors_data[index]
                elif "'s2hg'" in str(motor): self.s2hg_motor_data = motors_data[index]

            for index, scaler in enumerate(scan_data_instr.get('scalers').get('SPEC_counter_mnemonics')):
                if "'sec'" in str(scaler):
                    time_scalers_data = scalers_data[index]
                    break

            for i in scan_data_instr.get('detectors'):
                if i not in ("psd", "psd_uu", "psd_dd", "psd_du", "psd_ud"): continue

                if i == "psd": scan_psd = "psd"
                else: scan_psd = "psd_" + self.comboBox_polarisation.currentText()

            detector_images = scan_data_instr.get('detectors').get(scan_psd).get('data')

            for index, th in enumerate(self.th_motor_data):
                # check th
                if self.current_th == str(round(th, 3)):
                    self.lineEdit_slits_s1hg.setText(str(self.s1hg_motor_data[index]))
                    self.lineEdit_slits_s2hg.setText(str(self.s2hg_motor_data[index]))
                    self.lineEdit_time.setText(str(time_scalers_data[index]))

                    # seems to be a bug in numpy arrays imported from hdf5 files. Problem is solved after I subtract ZEROs array with the same dimentions.
                    detector_image = detector_images[index]
                    detector_image = numpy.around(detector_image, decimals=0).astype(int)
                    detector_image = numpy.subtract(detector_image, numpy.zeros((detector_image.shape[0], detector_image.shape[1])))
                    # integrate detector image with respect to ROI Y coordinates
                    detector_image_int = detector_image[int(self.lineEdit_ROI_y_top.text()): int(self.lineEdit_ROI_y_bottom.text()), :].sum(axis=0).astype(int)

                    self.graphicsView_det_images.setImage(detector_image, axes={'x':1, 'y':0}, levels=(0,0.1))
                    self.graphicsView_det_integr.addItem(pg.PlotCurveItem(y = detector_image_int, pen=pg.mkPen(color=(0, 0, 0), width=2), brush=pg.mkBrush(color=(255, 0, 0), width=3)))

                    if self.comboBox_colors_cheme.currentText() == "White / Black":
                        self.color_det_image = numpy.array([[0, 0, 0, 255], [255, 255, 255, 255], [255, 255, 255, 255]],
                                                        dtype=numpy.ubyte)
                    elif self.comboBox_colors_cheme.currentText() == "Green / Blue":
                        self.color_det_image = numpy.array([[0, 0, 255, 255], [255, 0, 0, 255], [0, 255, 0, 255]],
                                                           dtype=numpy.ubyte)
                    pos = numpy.array([0.0, 0.1, 1.0])

                    colmap = pg.ColorMap(pos, self.color_det_image)
                    self.graphicsView_det_images.setColorMap(colmap)

                    # add ROI rectangular
                    spots_ROI_det_view = []
                    spots_ROI_det_int = []
                    if self.draw_roi:
                        self.graphicsView_det_images.removeItem(self.draw_roi)

                    for i in range(int(self.lineEdit_ROI_y_top.text()), int(self.lineEdit_ROI_y_bottom.text())):
                        spots_ROI_det_view.append({'x': int(self.lineEdit_ROI_x_left.text()), 'y': i})
                        spots_ROI_det_view.append({'x': int(self.lineEdit_ROI_x_right.text()), 'y': i})

                    for i in range(int(self.lineEdit_ROI_x_left.text()), int(self.lineEdit_ROI_x_right.text())):
                        spots_ROI_det_view.append({'x': i, 'y': int(self.lineEdit_ROI_y_bottom.text())})
                        spots_ROI_det_view.append({'x': i, 'y': int(self.lineEdit_ROI_y_top.text())})

                    self.draw_roi = pg.ScatterPlotItem(spots=spots_ROI_det_view, size=0.5, pen=pg.mkPen(255, 255, 255))
                    self.graphicsView_det_images.addItem(self.draw_roi)

                    if self.draw_roi_int:
                        self.graphicsView_det_integr.removeItem(self.draw_roi_int)

                    for i in range(0, detector_image_int.max()):
                        spots_ROI_det_int.append({'x': int(self.lineEdit_ROI_x_left.text()), 'y': i})
                        spots_ROI_det_int.append({'x': int(self.lineEdit_ROI_x_right.text()), 'y': i})

                    self.draw_roi_int = pg.ScatterPlotItem(spots=spots_ROI_det_int, size=1, pen=pg.mkPen(255, 0, 0))
                    self.graphicsView_det_integr.addItem(self.draw_roi_int)

                    break

    def show_det_int(self):
        if self.show_det_int_trigger:
            self.graphicsView_det_images.setGeometry(QtCore.QRect(0, 30, 577, 420))
            self.show_det_int_trigger = False
        else:
            self.graphicsView_det_images.setGeometry(QtCore.QRect(0, 30, 577, 510))
            self.show_det_int_trigger = True

    def load_reflectivity_preview(self):

        self.graphicsView_refl_profile.getPlotItem().clear()
        skip_BKG = 0

        self.SFM_export_Qz = []
        self.SFM_export_I = []
        self.SFM_export_dI = []
        self.SFM_export_Resolution = []

        if self.comboBox_scan.currentText() == "": return

        self.label_sample_len_missing.setVisible(False)
        self.label_DB_missing.setVisible(False)
        self.label_wrong_roi_input.setVisible(False)

        if (self.checkBox_OverillCorr.isChecked() or self.checkBox_show_overillumination.isChecked()) and self.lineEdit_SampleLength.text() == "":
            self.label_sample_len_missing.setVisible(True)
            return

        if self.checkBox_NormDB.isChecked() and self.tableWidget_DB.rowCount() == 0:
            self.label_DB_missing.setVisible(True)
            return

        if int(self.lineEdit_ROI_x_left.text()) > int(self.lineEdit_ROI_x_right.text()) or int(self.lineEdit_ROI_y_bottom.text()) < int(self.lineEdit_ROI_y_top.text()) or int(self.lineEdit_ROI_BKG_x_left.text()) < 0:
            self.label_wrong_roi_input.setVisible(True)
            return

        if self.checkBox_DBatten.isChecked():
            self.DB_atten_factor = 10.4
            if not self.lineEdit_AttenCorrFactor.text() == "":
                self.DB_atten_factor = float(self.lineEdit_AttenCorrFactor.text())
        else: self.DB_atten_factor = 1

        if self.lineEdit_SkipSubtrBKG.text(): skip_BKG = float(self.lineEdit_SkipSubtrBKG.text())

        for i in range(0, self.tableWidget_Scans.rowCount()):
            if self.tableWidget_Scans.item(i, 0).text() == self.comboBox_scan.currentText():
                self.SFM_file = self.tableWidget_Scans.item(i, 3).text()
                self.SFM_DB_file = self.tableWidget_Scans.item(i, 2).text()

        with h5py.File(self.SFM_file, 'r') as file:

            scan_data_instr = file[list(file.keys())[0]].get("instrument")
            scan_data_ponos = file[list(file.keys())[0]].get("ponos")
            motors_data = numpy.array(scan_data_instr.get('motors').get('data')).T
            scalers_data = numpy.array(scan_data_instr.get('scalers').get('data')).T

            roi_coord_Y = [int(self.lineEdit_ROI_y_top.text()), int(self.lineEdit_ROI_y_bottom.text())]
            roi_coord_X = [int(self.lineEdit_ROI_x_left.text()), int(self.lineEdit_ROI_x_right.text())]
            roi_coord_X_BKG = [int(self.lineEdit_ROI_BKG_x_left.text()), int(self.lineEdit_ROI_BKG_x_right.text())]

            if not roi_coord_Y == self.old_roi_coord_Y:
                self.SFM_file_already_analized = ""

            self.old_roi_coord_Y = roi_coord_Y

            for index, scaler in enumerate(scan_data_instr.get('scalers').get('SPEC_counter_mnemonics')):
                if "'mon0'" in str(scaler): monitor_scalers_data = scalers_data[index]
                elif "'m1'" in str(scaler): monitor_uu_scalers_data = scalers_data[index]
                elif "'m2'" in str(scaler): monitor_dd_scalers_data = scalers_data[index]
                elif "'m3'" in str(scaler): monitor_du_scalers_data = scalers_data[index]
                elif "'m4'" in str(scaler): monitor_ud_scalers_data = scalers_data[index]

            if not self.SFM_file == self.SFM_file_already_analized:
                self.I_uu_sfm = self.I_dd_sfm = self.I_ud_sfm = self.I_du_sfm = []

            # get or create 2-dimentional intensity array for each polarisation
            for scan in scan_data_ponos.get('data'):

                # avoid reSUM of intensity after each action
                if not self.SFM_file == self.SFM_file_already_analized:
                    if "pnr" in list(file[list(file.keys())[0]]):
                        if str(scan) == "data_du":
                            self.I_du_sfm = scan_data_instr.get("detectors").get("psd_du").get('data')[:,
                                  int(roi_coord_Y[0]): int(roi_coord_Y[1]), :].sum(axis=1)
                        elif str(scan) == "data_uu":
                            self.I_uu_sfm = scan_data_instr.get("detectors").get("psd_uu").get('data')[:,
                                  int(roi_coord_Y[0]): int(roi_coord_Y[1]), :].sum(axis=1)
                        elif str(scan) == "data_ud":
                            self.I_ud_sfm = scan_data_instr.get("detectors").get("psd_ud").get('data')[:,
                                  int(roi_coord_Y[0]): int(roi_coord_Y[1]), :].sum(axis=1)
                        elif str(scan) == "data_dd":
                            self.I_dd_sfm = scan_data_instr.get("detectors").get("psd_dd").get('data')[:,
                                  int(roi_coord_Y[0]): int(roi_coord_Y[1]), :].sum(axis=1)
                    else:
                        self.I_uu_sfm = scan_data_instr.get("detectors").get("psd").get('data')[:, int(roi_coord_Y[0]) : int(roi_coord_Y[1]), :].sum(axis=1)

            self.SFM_file_already_analized = self.SFM_file

            for color_index, scan_intens_sfm in enumerate([self.I_uu_sfm, self.I_du_sfm, self.I_ud_sfm, self.I_dd_sfm]):

                SFM_export_Qz_one_pol = []
                SFM_export_I_one_pol = []
                SFM_export_dI_one_pol = []
                SFM_export_Resolution_one_pol = []

                plot_I = []
                plot_angle = []
                plot_dI_err_bottom = []
                plot_dI_err_top = []
                plot_overillumination = []

                if scan_intens_sfm == []: continue

                if color_index == 0: # ++
                    color = [0, 0, 0]
                    if numpy.count_nonzero(monitor_uu_scalers_data) == 0: monitor_data = monitor_scalers_data
                    else: monitor_data = monitor_uu_scalers_data
                elif color_index == 1: # -+
                    color = [0, 0, 255]
                    monitor_data = monitor_du_scalers_data
                elif color_index == 2: # --
                    color = [0, 255, 0]
                    monitor_data = monitor_ud_scalers_data
                elif color_index == 3: # --
                    color = [255, 0, 0]
                    monitor_data = monitor_dd_scalers_data

                for index, th in enumerate(self.th_motor_data):

                    try: # Full offset. If "text" cant be converted to "float" - ignore the field
                        th = th - float(self.lineEdit_full_scan_offset.text())
                    except:
                        th = th

                    # read motors
                    Qz = (4 * numpy.pi / float(self.lineEdit_wavelength.text())) * numpy.sin(numpy.radians(th))
                    s1hg = self.s1hg_motor_data[index]
                    s2hg = self.s2hg_motor_data[index]
                    monitor = monitor_data[index]

                    if not self.checkBox_OverillCorr.isChecked():
                        overill_corr = 1
                        overill_corr_plot = self.overillumination_correct_coeff(s1hg, s2hg, round(th, 4))[0]
                    else:
                        overill_corr, FWHM_proj = self.overillumination_correct_coeff(s1hg, s2hg, round(th, 4))
                        overill_corr_plot = overill_corr

                    # calculate resolution in Sared way or better
                    if self.checkBox_resol_sared.isChecked():
                        Resolution = numpy.sqrt(((2 * numpy.pi / float(self.lineEdit_wavelength.text())) ** 2) * (
                                (numpy.cos(numpy.radians(th))) ** 2) * (0.68 ** 2) * ((s1hg ** 2) + (s2hg ** 2)) / (
                                                        (float(
                                                            self.lineEdit_s1_sample_dist.text()) - float(
                                                            self.lineEdit_s2_sample_dist.text())) ** 2) + (
                                                        (float(self.lineEdit_wavel_resol.text()) ** 2) * (Qz ** 2)))
                    else:
                        if FWHM_proj == s2hg:
                            Resolution = numpy.sqrt(
                                ((2 * numpy.pi / float(self.lineEdit_wavelength.text())) ** 2) * (
                                        (numpy.cos(numpy.radians(th))) ** 2) * (0.68 ** 2) * (
                                        (s1hg ** 2) + (s2hg ** 2)) / ((float(
                                    self.lineEdit_s1_sample_dist.text()) - float(
                                    self.lineEdit_s2_sample_dist.text())) ** 2) + (
                                        (float(self.lineEdit_wavel_resol.text()) ** 2) * (Qz ** 2)))
                        else:
                            Resolution = numpy.sqrt(
                                ((2 * numpy.pi / float(self.lineEdit_wavelength.text())) ** 2) * (
                                        (numpy.cos(numpy.radians(th))) ** 2) * (0.68 ** 2) * (
                                        (s1hg ** 2) + (FWHM_proj ** 2)) / (
                                        float(self.lineEdit_s1_sample_dist.text()) ** 2) + (
                                        (float(self.lineEdit_wavel_resol.text()) ** 2) * (Qz ** 2)))

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

                    if self.checkBox_SubtrBKG.isChecked() and Qz > skip_BKG:
                        if Intens_bkg > 0:
                            Intens_err = numpy.sqrt(Intens + Intens_bkg)
                            Intens = Intens - Intens_bkg

                    if self.checkBox_DevideByMon.isChecked():
                        if Intens == 0:  Intens_err = Intens_err / monitor
                        else: Intens_err = (Intens / monitor) * numpy.sqrt((Intens_err / Intens) ** 2 + (1 / monitor))
                        Intens = Intens / monitor

                    if self.checkBox_OverillCorr.isChecked() and overill_corr > 0:
                        Intens_err = Intens_err / overill_corr
                        Intens = Intens / overill_corr

                    if self.checkBox_NormDB.isChecked():
                        DB_intens = float(self.DB_info[self.SFM_DB_file + ";" + str(s1hg) + ";" + str(s2hg)].split(";")[0]) * self.DB_atten_factor
                        DB_err = overill_corr * float(self.DB_info[self.SFM_DB_file + ";" + str(s1hg) + ";" + str(s2hg)].split(";")[1]) * self.DB_atten_factor
                        Intens_err = (Intens / DB_intens) * numpy.sqrt((DB_err / DB_intens) ** 2 + (Intens_err / Intens) ** 2)
                        Intens = Intens / DB_intens

                    try:
                        show_first = int(self.lineEdit_skip_first_points.text())
                        show_last = len(self.th_motor_data) - int(self.lineEdit_skip_last_points.text())
                    except:
                        show_first = 0
                        show_last = len(self.th_motor_data)

                    if not Intens < 0 and index < show_last and index > show_first:
                        # I need this for "Reduce SFM" option. First - store one pol.
                        SFM_export_Qz_one_pol.append(Qz)
                        SFM_export_I_one_pol.append(Intens)
                        SFM_export_dI_one_pol.append(Intens_err)
                        SFM_export_Resolution_one_pol.append(Resolution)

                        if Intens > 0:
                            plot_I.append(numpy.log10(Intens))
                            plot_angle.append(Qz)
                            plot_dI_err_top.append(abs(numpy.log10(Intens + Intens_err) - numpy.log10(Intens)))

                            plot_overillumination.append(overill_corr_plot)

                            if Intens > Intens_err: plot_dI_err_bottom.append(numpy.log10(Intens) - numpy.log10(Intens - Intens_err))
                            else: plot_dI_err_bottom.append(0)

                        if self.comboBox_plot_axis.currentText() in ("Reflectivity (lin) vs Angle (Qz)", "Reflectivity (lin) vs Angle (deg)"):
                            plot_I.pop()
                            plot_I.append(Intens)
                            plot_dI_err_top.pop()
                            plot_dI_err_top.append(Intens_err)
                            plot_dI_err_bottom.pop()
                            plot_dI_err_bottom.append(Intens_err)

                        if self.comboBox_plot_axis.currentText() in ("Reflectivity (lin) vs Angle (deg)", "Reflectivity (log) vs Angle (deg)"):
                            plot_angle.pop()
                            plot_angle.append(th)

                # I need this for "Reduse SFM" option. Second - combine all shown pol in one list variable.
                # polarisations are uu, dd, ud, du
                self.SFM_export_Qz.append(SFM_export_Qz_one_pol)
                self.SFM_export_I.append(SFM_export_I_one_pol)
                self.SFM_export_dI.append(SFM_export_dI_one_pol)
                self.SFM_export_Resolution.append(SFM_export_Resolution_one_pol)

                if self.checkBox_incl_errorbars.isChecked():
                    s1 = pg.ErrorBarItem(x=numpy.array(plot_angle), y=numpy.array(plot_I), top=numpy.array(plot_dI_err_top), bottom=numpy.array(plot_dI_err_bottom), pen=pg.mkPen(color[0], color[1], color[2]), brush=pg.mkBrush(color[0], color[1], color[2]))
                    self.graphicsView_refl_profile.addItem(s1)

                s2 = pg.ScatterPlotItem(x=plot_angle, y=plot_I, symbol="o", size=3, pen=pg.mkPen(color[0], color[1], color[2]), brush=pg.mkBrush(color[0], color[1], color[2]))
                self.graphicsView_refl_profile.addItem(s2)

                if self.checkBox_show_overillumination.isChecked():
                    s3 = pg.PlotCurveItem(x=plot_angle, y=plot_overillumination,
                                            pen=pg.mkPen(color=(255, 0, 0), width=3),
                                            brush=pg.mkBrush(color=(255, 0, 0), width=3) )
                    self.graphicsView_refl_profile.addItem(s3)

    def draw_2D_map(self):
        self.graphicsView_map.clear()
        self.int_detector_image = []
        # change interface if for different views
        if self.comboBox_axis.currentText() in ["Qx vs. Qz", "Theta vs. 2Theta"]:
            # show "graphicsView_map_Qxz_Theta"
            self.graphicsView_map_Qxz_Theta.setGeometry(QtCore.QRect(0, 30, 577, 520))
            self.label_scale.setVisible(True)
            self.comboBox_scale.setVisible(True)
            self.horizontalSlider_scale.setVisible(False)
        else:
            self.graphicsView_map_Qxz_Theta.setGeometry(QtCore.QRect(0, 0, 0, 0))
            self.label_scale.setVisible(False)
            self.comboBox_scale.setVisible(False)
            self.horizontalSlider_scale.setVisible(True)

        if self.SFM_file == "": return

        if self.comboBox_polarisation_2d_map.count() == 1: self.int_detector_image = self.I_uu_sfm
        else:
            if self.comboBox_polarisation_2d_map.currentText() == "uu": self.int_detector_image = self.I_uu_sfm
            elif self.comboBox_polarisation_2d_map.currentText() == "du": self.int_detector_image = self.I_du_sfm
            elif self.comboBox_polarisation_2d_map.currentText() == "ud": self.int_detector_image = self.I_ud_sfm
            elif self.comboBox_polarisation_2d_map.currentText() == "dd": self.int_detector_image = self.I_dd_sfm

        if self.int_detector_image == []: return

        self.graphicsView_map.setImage(numpy.flip(self.int_detector_image, axis=0), axes={'x': 1, 'y': 0}, levels=(0, 0.1), scale=(1, 10))
        self.graphicsView_map.ui.histogram.setHistogramRange(0, self.horizontalSlider_scale.value())
        self.graphicsView_map.ui.histogram.setLevels(0, self.horizontalSlider_scale.value())

        # add ROI rectangular
        spots_ROI = []
        if self.draw_roi_2D_map:
            self.graphicsView_map.removeItem(self.draw_roi_2D_map)

        for i in range(int(self.int_detector_image.shape[0])):
            spots_ROI.append({'y': i*10, 'x': int(self.lineEdit_ROI_x_left.text())})
            spots_ROI.append({'y': i*10, 'x': int(self.lineEdit_ROI_x_right.text())})

        self.draw_roi_2D_map = pg.ScatterPlotItem(spots=spots_ROI, size=1.5, pen=pg.mkPen(255, 255, 255))
        self.graphicsView_map.addItem(self.draw_roi_2D_map)

        # Pixel to Angle conversion. For "Qx vs Qz" and "th vs tth" 2d maps
        if self.comboBox_axis.currentText() in ["Qx vs. Qz", "Theta vs. 2Theta"]:
            self.graphicsView_map_Qxz_Theta.clear()

            spots_Qxz = []
            spots_th_tth = []
            self.int_detector_image_Qxz = []

            # we need to flip the detector (X) for correct calculation
            det_image_arr = numpy.flip(self.int_detector_image, 1)

            roi_middle = round((self.int_detector_image.shape[1] - float(self.lineEdit_ROI_x_left.text()) + self.int_detector_image.shape[1] - float(self.lineEdit_ROI_x_right.text())) / 2)
            mm_per_pix = 300 / det_image_arr.shape[1]

            for theta_i, tth_i, det_image_i in zip(self.th_motor_data, self.tth_motor_data, det_image_arr):
                for pixel_num, value in enumerate(det_image_i):
                    # Reduce number of points to draw (to save RAM)
                    if pixel_num % int(self.comboBox_scale.currentText()) == 0:
                        # theta F in deg
                        theta_f = tth_i - theta_i
                        # calculate delta theta F in deg
                        delta_theta_F_mm = (pixel_num - roi_middle) * mm_per_pix
                        delta_theta_F_deg = numpy.degrees(numpy.arctan(delta_theta_F_mm / float(self.lineEdit_sample_det_dist.text())))
                        # final theta F in deg for the point
                        theta_f += delta_theta_F_deg
                        # convert to Q
                        Qx = (2 * numpy.pi / float(self.lineEdit_wavelength.text())) * (numpy.cos(numpy.radians(theta_f)) - numpy.cos(numpy.radians(theta_i)))
                        Qz = (2 * numpy.pi / float(self.lineEdit_wavelength.text())) * (numpy.sin(numpy.radians(theta_f)) + numpy.sin(numpy.radians(theta_i)))

                        self.int_detector_image_Qxz.append([Qx, Qz, value])

                        # define colors - 1 count+ -> green, 0 - blue
                        if value < 1: color = [0, 0, 255]
                        else: color = [0, 255, 0]

                        spots_Qxz.append({'pos': (-Qx, Qz), 'pen': pg.mkPen(color[0], color[1], color[2])})
                        spots_th_tth.append({'pos': (theta_i, theta_i + theta_f), 'pen': pg.mkPen(color[0], color[1], color[2])})

            if self.comboBox_axis.currentText() == "Qx vs. Qz": s0 = pg.ScatterPlotItem(spots=spots_Qxz, size=1, pen=pg.mkPen(255, 255, 255))
            else: s0 = pg.ScatterPlotItem(spots=spots_th_tth, size=2, pen=pg.mkPen(255, 255, 255))

            self.graphicsView_map_Qxz_Theta.addItem(s0)

    def export_2d_map(self):
        if self.comboBox_axis.currentText() == "Pixel vs. Point":
            with open(self.lineEdit_saveAt.text() + self.SFM_file[self.SFM_file.rfind("/") + 1 : -3] + "_" + self.comboBox_polarisation_2d_map.currentText() + " 2D_map.dat", "w") as new_file_2d_map:
                for line in self.int_detector_image:
                    for row in line:
                        new_file_2d_map.write(str(row) + " ")
                    new_file_2d_map.write("\n")

        elif self.comboBox_axis.currentText() in ["Qx vs. Qz", "Theta vs. 2Theta"]:
            with open(self.lineEdit_saveAt.text() + self.SFM_file[self.SFM_file.rfind("/") + 1 : -3] + "_" + self.comboBox_polarisation_2d_map.currentText() + "_" + self.comboBox_axis.currentText() + ".dat", "w") as new_file_2d_map_Qxz:
                for line in self.int_detector_image_Qxz:
                    new_file_2d_map_Qxz.write(str(line[0]) + " " + str(line[1]) + " " + str(line[2]))
                    new_file_2d_map_Qxz.write("\n")


    def update_slits(self):
        roi_width = int(self.lineEdit_ROI_x_right.text()) - int(self.lineEdit_ROI_x_left.text())
        self.lineEdit_ROI_BKG_x_left.setText(str(int(self.lineEdit_ROI_BKG_x_right.text()) - roi_width))

        self.lineEdit_ROI_BKG_y_bottom.setText(str(int(self.lineEdit_ROI_y_bottom.text())))
        self.lineEdit_ROI_BKG_y_top.setText(str(int(self.lineEdit_ROI_y_top.text())))

        self.draw_det_image()
        self.load_reflectivity_preview()

    def change_pol_or_ang(self):
        if not self.comboBox_polarisation.currentText() == "" and not self.comboBox_point_number.currentText() == "":
            self.draw_det_image()

    def color_det_image(self):
        if self.comboBox_colors_cheme.currentText() == "White / Black":
            self.color_det_image = numpy.array([[0, 0, 0, 255], [255, 255, 255, 255], [255, 255, 255, 255]], dtype=numpy.ubyte)
        elif self.comboBox_colors_cheme.currentText() == "Green / Blue":
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

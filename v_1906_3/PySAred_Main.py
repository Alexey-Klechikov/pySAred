from PyQt5 import QtCore, QtGui, QtWidgets
import h5py, numpy, os
import pyqtgraph as pg
import PySAred_FrontEnd

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

current_dir = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

class GUI(PySAred_FrontEnd.Ui_MainWindow):

    def __init__(self):

        super(GUI, self).__init__()
        self.setupUi(self, current_dir)

        # current file in Single File Mode
        self.SFM_file = ""
        self.SFM_file_already_anilized = ""
        self.scan_intens_sfm = []

        # current th point
        self.current_th = ""

        # write calculated overillumination coefficients into library
        self.overill_coeff_lib = {}

        # Write DB info into library
        self.DB_info = {}
        self.DB_already_analized = []

        # ROI frame
        self.draw_roi = []

        # Actions on clicks
        self.pushButton_importScans.clicked.connect(self.button_ImportScans)
        self.pushButton_DeleteImportScans.clicked.connect(self.button_DeleteScans)
        self.pushButton_ImportDB.clicked.connect(self.button_ImportDB)
        self.pushButton_DeleteImportDB.clicked.connect(self.button_DeleteDB)
        self.toolButton_save_at.clicked.connect(self.button_SaveDir)
        self.pushButton_start.clicked.connect(self.button_Start)

        self.comboBox_point_number.currentIndexChanged.connect(self.change_pol_or_ang)
        self.comboBox_polarisation.currentIndexChanged.connect(self.change_pol_or_ang)

        self.comboBox_scan.currentIndexChanged.connect(self.load_detector_images)
        self.comboBox_scan.currentIndexChanged.connect(self.load_reflectivity_preview)
        self.lineEdit_SampleLength.textChanged.connect(self.load_reflectivity_preview)
        self.checkBox_DevideByMon.stateChanged.connect(self.load_reflectivity_preview)
        self.checkBox_NormDB.stateChanged.connect(self.load_reflectivity_preview)
        self.checkBox_DBatten.stateChanged.connect(self.load_reflectivity_preview)
        self.lineEdit_AttenCorrFactor.textChanged.connect(self.load_reflectivity_preview)
        self.checkBox_OverillCorr.stateChanged.connect(self.load_reflectivity_preview)
        self.lineEdit_SkipSubstrBKG.textChanged.connect(self.load_reflectivity_preview)
        self.checkBox_SubstrBKG.stateChanged.connect(self.load_reflectivity_preview)
        self.checkBox_incl_errorbars.stateChanged.connect(self.load_reflectivity_preview)
        self.checkBox_fast_calc.stateChanged.connect(self.load_reflectivity_preview)
        self.lineEdit_wavelength.textChanged.connect(self.load_reflectivity_preview)
        self.lineEdit_wavel_resol.textChanged.connect(self.load_reflectivity_preview)
        self.lineEdit_s1_sample_dist.textChanged.connect(self.load_reflectivity_preview)
        self.lineEdit_s2_sample_dist.textChanged.connect(self.load_reflectivity_preview)

        self.actionVersion.triggered.connect(self.menu_info)
        self.actionAlgorithm_info.triggered.connect(self.menu_algorithm)

        self.comboBox_colors_cheme.addItem("Green / Blue")
        self.comboBox_colors_cheme.addItem("White / Black")
        self.comboBox_colors_cheme.currentIndexChanged.connect(self.color_det_image)

        self.lineEdit_ROI_x_left.editingFinished.connect(self.update_slits)
        self.lineEdit_ROI_x_right.editingFinished.connect(self.update_slits)

    ##--> Main window buttons
    def button_ImportScans(self):
        import_files = QtWidgets.QFileDialog().getOpenFileNames(None, "FileNames", os.path.dirname(os.path.realpath(__file__)).replace("\\", "/"), ".h5 (*.h5)")
        for file in import_files[0]:
            self.tableWidget_Scans.insertRow(self.tableWidget_Scans.rowCount())
            self.tableWidget_Scans.setRowHeight(self.tableWidget_Scans.rowCount()-1, 10)
            # File name (row 0) and full path (row 2)
            for j in range(0, 3):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget_Scans.setItem(self.tableWidget_Scans.rowCount()-1, j, item)
            self.tableWidget_Scans.item(self.tableWidget_Scans.rowCount() - 1, 0).setText(file[file.rfind("/") + 1:])
            self.tableWidget_Scans.item(self.tableWidget_Scans.rowCount() - 1, 2).setText(file)

            # add file into SFM / Scan ComboBox
            self.comboBox_scan.addItem(str(file[file.rfind("/") + 1:]))

            # ROI
            file = h5py.File(file, 'r')
            scan_data = file[list(file.keys())[0]]
            roi_coord = numpy.array(scan_data.get('instrument').get('scalers').get('roi').get("roi"))
            file.close()
            self.tableWidget_Scans.item(self.tableWidget_Scans.rowCount() - 1, 1).setText(str(roi_coord[2])[:-2] + " : " + str(roi_coord[3])[:-2])

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
            self.comboBox_scan.addItem(self.tableWidget_Scans.item(i, 2).text()[
                        self.tableWidget_Scans.item(i, 2).text().rfind("/") + 1:])

    def button_ImportDB(self):
        import_files = QtWidgets.QFileDialog().getOpenFileNames(None, "FileNames", os.path.dirname(os.path.realpath(__file__)).replace("\\", "/"), ".h5 (*.h5)")
        for file in import_files[0]: self.listWidget_DB.addItem(file)

    def button_DeleteDB(self):
        remove_files = self.listWidget_DB.selectedItems()
        if not remove_files: return
        for file in remove_files:
            self.listWidget_DB.takeItem(self.listWidget_DB.row(file))

    def button_SaveDir(self):
        saveAt = QtWidgets.QFileDialog().getExistingDirectory()
        if not saveAt: return

        self.lineEdit_saveAt.setText(str(saveAt))
        if not str(saveAt)[-1] == "/": self.lineEdit_saveAt.setText(str(saveAt) + "/")

    def button_Start(self):

        self.listWidget_filesToCheck.clear()

        self.analazeDB()

        if self.lineEdit_SkipSubstrBKG.text(): skip_BKG = float(self.lineEdit_SkipSubstrBKG.text())
        else: skip_BKG = 0.085

        save_file_directory = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + '/'
        if self.lineEdit_saveAt.text(): save_file_directory = self.lineEdit_saveAt.text()

        if self.lineEdit_SampleLength.text(): sample_len = self.lineEdit_SampleLength.text()
        else: sample_len = 999

        if self.checkBox_OverillCorr.isChecked() and sample_len == 999:
            self.statusbar.showMessage("Sample length is missing")
            return

        # iterate through table with scans
        for i in range(0, self.tableWidget_Scans.rowCount()):
            file_name = self.tableWidget_Scans.item(i, 2).text()[
                        self.tableWidget_Scans.item(i, 2).text().rfind("/") + 1: -3]
            with h5py.File(self.tableWidget_Scans.item(i, 2).text(), 'r') as file:

                scan_data_ponos = file[list(file.keys())[0]].get("ponos")
                scan_data_instr = file[list(file.keys())[0]].get("instrument")
                motors_data = numpy.array(scan_data_instr.get('motors').get('data')).T
                scalers_data = numpy.array(scan_data_instr.get('scalers').get('data')).T

                for index, motor in enumerate(scan_data_instr.get('motors').get('SPEC_motor_mnemonics')):
                    if "'th'" in str(motor): th_motor_data = motors_data[index]
                    elif "'s1hg'" in str(motor): s1hg_motor_data = motors_data[index]
                    elif "'s2hg'" in str(motor): s2hg_motor_data = motors_data[index]

                for index, scaler in enumerate(scan_data_instr.get('scalers').get('SPEC_counter_mnemonics')):
                    if "'mon0'" in str(scaler): monitor_scalers_data = scalers_data[index]
                    elif "'roi'" in str(scaler): intens_scalers_data = scalers_data[index]
                    elif "'rmm'" in str(scaler): intens_dd_scalers_data = scalers_data[index]
                    elif "'rpp'" in str(scaler): intens_uu_scalers_data = scalers_data[index]
                    elif "'rpm'" in str(scaler): intens_ud_scalers_data = scalers_data[index]
                    elif "'rmp'" in str(scaler): intens_du_scalers_data = scalers_data[index]

                # ROI region
                roi_coord = [int(self.tableWidget_Scans.item(i, 1).text().split()[0]),
                                 int(self.tableWidget_Scans.item(i, 1).text().split()[-1])]

                check_this_file = 0

                # check if we have several polarisations
                for detector in scan_data_instr.get('detectors'):
                    if str(detector) not in ("psd", "psd_du", "psd_uu", "psd_ud", "psd_dd"): continue

                    # we use preintegrated I in roi if roi was not changed, otherwice calculate
                    original_roi_coord_arr = numpy.array(scan_data_instr.get('scalers').get('roi').get("roi"))
                    original_roi_coord = [int(original_roi_coord_arr[2]), int(original_roi_coord_arr[3])]

                    if roi_coord == original_roi_coord and not self.checkBox_SubstrBKG.isChecked() and self.checkBox_fast_calc.isChecked():
                        if str(detector) == "psd": scan_intens = intens_scalers_data
                        if str(detector) == "psd_uu":
                            if sum(intens_uu_scalers_data) > 0: scan_intens = intens_uu_scalers_data
                            else: scan_intens = intens_scalers_data
                        elif str(detector) == "psd_dd":
                            if sum(intens_dd_scalers_data) > 0: scan_intens = intens_dd_scalers_data
                            else: scan_intens = ""
                        elif str(detector) == "psd_ud": scan_intens = intens_ud_scalers_data
                        elif str(detector) == "psd_du": scan_intens = intens_du_scalers_data
                    else: scan_intens = scan_data_instr.get("detectors").get(str(detector)).get('data')[:].sum(axis=1)

                    new_file = open(save_file_directory + file_name + "_" + str(detector) + ".dat", "w")

                    # iterate through th points
                    for index, th in enumerate(th_motor_data):

                        # analize integrated intensity for ROI
                        if len(scan_intens.shape) == 1: Intens = scan_intens[index]
                        elif len(scan_intens.shape) == 2: Intens = sum(scan_intens[index][roi_coord[0]: roi_coord[1]])

                        if Intens == 0: continue

                        Intens_err = numpy.sqrt(Intens)

                        # read motors
                        Qz = (4 * numpy.pi / float(self.lineEdit_wavelength.text())) * numpy.sin(numpy.radians(th))
                        s1hg = s1hg_motor_data[index]
                        s2hg = s2hg_motor_data[index]
                        monitor = monitor_scalers_data[index]

                        # check if we are not in a middle of ROI in Qz approx 0.02)
                        if round(Qz, 2) == 0.02 and check_this_file == 0:
                            if not len(scan_data_ponos.get('data')) == 1:
                                scan_data_0_02 = numpy.array(scan_data_ponos.get('data').get("data_uu"))[index][roi_coord[0]: roi_coord[1]]
                            else: scan_data_0_02 = scan_intens[index][roi_coord[0]: roi_coord[1]]

                            if max(scan_data_0_02) != max(scan_data_0_02[round((len(scan_data_0_02) / 2.5)):-round((len(scan_data_0_02) / 2.5))]):
                                self.listWidget_filesToCheck.addItem(file_name)
                                check_this_file = 1

                        coeff = self.overillumination_correct_coeff(s1hg, s2hg, round(th, 4), sample_len)
                        FWHM_proj = coeff[1]

                        if not self.checkBox_OverillCorr.isChecked(): overill_corr = 1
                        else: overill_corr = coeff[0]

                        # calculate resolution in Sared way or better
                        if self.checkBox_resol_sared.isChecked():
                            Resolution = numpy.sqrt(((2 * numpy.pi / float(self.lineEdit_wavelength.text())) ** 2) * (
                                    (numpy.cos(numpy.radians(th))) ** 2) * (0.68 ** 2) * ((s1hg ** 2) + (s2hg ** 2)) / ((float(
                                self.lineEdit_s1_sample_dist.text()) - float(self.lineEdit_s2_sample_dist.text())) ** 2) + (
                                                               (float(self.lineEdit_wavel_resol.text()) ** 2) * (Qz ** 2)))
                        else:
                            if FWHM_proj == s2hg:
                                Resolution = numpy.sqrt(((2 * numpy.pi / float(self.lineEdit_wavelength.text())) ** 2) * (
                                            (numpy.cos(numpy.radians(th))) ** 2) * (0.68 ** 2) * ((s1hg ** 2) + (s2hg ** 2)) / (( float(self.lineEdit_s1_sample_dist.text()) - float(self.lineEdit_s2_sample_dist.text())) ** 2) + ((float(self.lineEdit_wavel_resol.text()) ** 2) * (Qz ** 2)))
                            else:
                                Resolution = numpy.sqrt(((2 * numpy.pi / float(self.lineEdit_wavelength.text())) ** 2) * (
                                            (numpy.cos(numpy.radians(th))) ** 2) * (0.68 ** 2) * (
                                                                   (s1hg ** 2) + (FWHM_proj ** 2)) / (
                                                                   float(self.lineEdit_s1_sample_dist.text()) ** 2) + (
                                                                   (float(self.lineEdit_wavel_resol.text()) ** 2) * (Qz ** 2)))

                        # I cite Gunnar in here "We are now saving dQ as sigma rather than FWHM for genx"
                        Resolution = Resolution / (2 * numpy.sqrt(2 * numpy.log(2)))

                        # minus background, devide by monitor, overillumination correct + calculate errors
                        if self.checkBox_SubstrBKG.isChecked() and Qz > skip_BKG and Intens > 0:
                            Intens_bkg = sum(scan_intens[index][
                                   roi_coord[0] - (roi_coord[1] - roi_coord[0]) - 1: roi_coord[0] - 1])
                            if Intens_bkg > 0:
                                Intens_err = numpy.sqrt(Intens + Intens_bkg)
                                Intens = Intens - Intens_bkg

                        if self.checkBox_DevideByMon.isChecked() and Intens > 0:
                            Intens_err = (Intens / monitor) * numpy.sqrt((Intens_err / Intens) ** 2 + (1 / monitor))
                            Intens = Intens / monitor

                        if self.checkBox_OverillCorr.isChecked() and Intens > 0:
                            Intens_err = Intens_err / overill_corr
                            Intens = Intens / overill_corr

                        if self.checkBox_NormDB.isChecked() and Intens > 0 and len(self.DB_info) > 0:
                            DB_intens = float(self.DB_info[str(s1hg) + ";" + str(s2hg)].split(";")[0])
                            DB_err = overill_corr * float(self.DB_info[str(s1hg) + ";" + str(s2hg)].split(";")[1])

                            Intens_err = (Intens / DB_intens) * numpy.sqrt((DB_err / DB_intens) ** 2 + (Intens_err / Intens) ** 2)
                            Intens = Intens / DB_intens

                        # skip first point
                        if index > 1 and Intens > 0:
                            new_file.write(str(Qz) + ' ' + str(Intens) + ' ' + str(Intens_err) + ' ')
                            if self.checkBox_add_resolution_column.isChecked(): new_file.write(str(Resolution))
                            new_file.write('\n')

                    # close files
                    new_file.close()

                    # check if file is empty - then delete
                    if os.stat(save_file_directory + file_name + "_" + str(detector) + ".dat").st_size == 0:
                        os.remove(save_file_directory + file_name + "_" + str(detector) + ".dat")

        self.statusbar.showMessage(str(self.tableWidget_Scans.rowCount()) + " files reduced, " + str(
            self.listWidget_filesToCheck.count()) + " files need extra care.")
    ##<--

    ##--> extra functions to shorten the code
    def overillumination_correct_coeff(self, s1hg, s2hg, th, sample_len):

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

        if self.checkBox_NormDB.isChecked() and self.listWidget_DB.count() == 0: self.label_DB_missing.setVisible(True)
        else: self.label_DB_missing.setVisible(False)

        if not self.checkBox_NormDB.isChecked(): self.DB_info = {}
        else:
            # check if we already opened DB file from the list AND this list is the same as before
            DB_in_the_list = []
            for i in range(0, self.listWidget_DB.count()):
                DB_in_the_list.append(self.listWidget_DB.item(i).text())
            if self.checkBox_DBatten.isChecked(): DB_in_the_list.append(self.lineEdit_AttenCorrFactor.text())

            for i in range(0, self.listWidget_DB.count()):
                with h5py.File(self.listWidget_DB.item(i).text(), 'r') as file_db:
                    scan_data_instr = file_db[list(file_db.keys())[0]].get("instrument")
                    motors_data = numpy.array(scan_data_instr.get('motors').get('data')).T
                    scalers_data = numpy.array(scan_data_instr.get('scalers').get('data')).T

                    for index, motor in enumerate(scan_data_instr.get('motors').get('SPEC_motor_mnemonics')):
                        if "'th'" in str(motor): th_motor_data = motors_data[index]
                        elif "'s1hg'" in str(motor): s1hg_motor_data = motors_data[index]
                        elif "'s2hg'" in str(motor): s2hg_motor_data = motors_data[index]

                    for index, scaler in enumerate(scan_data_instr.get('scalers').get('SPEC_counter_mnemonics')):
                        if "'mon0'" in str(scaler): monitor_scalers_data = scalers_data[index]
                        elif "'roi'" in str(scaler): intens_scalers_data = scalers_data[index]

                    for j in range(0, len(th_motor_data)):

                        if self.checkBox_DBatten.isChecked():
                            if self.lineEdit_AttenCorrFactor.text(): db_attenuator = self.lineEdit_AttenCorrFactor.text()
                            else: db_attenuator = 10.4
                        else: db_attenuator = 1

                        DB_intens = float(db_attenuator) * float(intens_scalers_data[j]) / float(monitor_scalers_data[j])
                        DB_err = DB_intens * numpy.sqrt(1 / float(intens_scalers_data[j]) + 1 / float(monitor_scalers_data[j]))

                        slits = str(s1hg_motor_data[j]) + ";" + str(s2hg_motor_data[j])
                        DB_intens_and_err = str(DB_intens) + ";" + str(DB_err)
                        self.DB_info[slits] = DB_intens_and_err

                    self.DB_already_analized.append(self.listWidget_DB.item(i).text())

            if self.checkBox_DBatten.isChecked(): self.DB_already_analized.append(self.lineEdit_AttenCorrFactor.text())
    ##<--

    ##--> menu options
    def menu_info(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowIcon(QtGui.QIcon(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "\icon.png"))
        msgBox.setText( "SuperADAM .h5 rapid data extractor. " + self.actionVersion.text() + "\n\n"
                        "Alexey.Klechikov@gmail.com\n\n"                                                                     
                        "Check for newer version at https://github.com/Alexey-Klechikov/pySAred")
        msgBox.exec_()

    def menu_algorithm(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowIcon(QtGui.QIcon(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "\icon.png"))
        msgBox.setText( "1) X limits for analysis are set automatically using ROI settings in .h5 file. Y limits are ignored, intensity is integrated across all detector height.  \n\n"
                        "2) Area for background estimation is set to the same size as ROI and located at the left of ROI.\n\n"
                        "3) All Direct Beam files are analized in the the same order as they are in the table. Only last value with certain combination of s1hg and s2hg is used for Direct Beam normalization. \n\n"
                        "4) File can appear in \"Recheck following files in Single File Mode\" if peak of its intensity (at Qz 0.02-0.03) is not in the middle of ROI.\n\n"
                        "5) Trapezoid beam form is used for overillumination correction.\n\n"
                        "6) Files are exported as Qz, I, dI, (dQz)\n\n"
                        "7) Checkbox 'Fast refl. calculation' defines either use of preintegrated intensity across all detector's height (ON) or calculation of more precise ROI area (OFF)")

        msgBox.exec_()
    ##<--

    ##--> SFM
    def load_detector_images(self):

        if self.comboBox_scan.currentText() == "": return

        self.comboBox_point_number.clear()
        self.comboBox_polarisation.clear()

        # we need to find full path for the SFM file from the table
        for i in range(0, self.tableWidget_Scans.rowCount()):
            if self.tableWidget_Scans.item(i, 0).text() == self.comboBox_scan.currentText():
                self.SFM_file = self.tableWidget_Scans.item(i, 2).text()

        with h5py.File(self.SFM_file, 'r') as file:
            scan_data = file[list(file.keys())[0]]
            roi_coord = numpy.array(scan_data.get("instrument").get('scalers').get('roi').get("roi"))
            roi_width = int(round(roi_coord[3] / 2)) - int(round(roi_coord[2] / 2))

            self.lineEdit_ROI_x_left.setText(str(roi_coord[2])[:-2])
            self.lineEdit_ROI_x_right.setText(str(roi_coord[3])[:-2])
            self.lineEdit_ROI_BKG_x_left.setText((str(2 * int(round(roi_coord[2] / 2) - roi_width - 1))))
            self.lineEdit_ROI_BKG_x_right.setText(str(2 * int(round(roi_coord[2] / 2)) - 1))

            for index, th in enumerate(scan_data.get("instrument").get('motors').get('th').get("value")):
                if str(th)[0:5] in ("-0.00", "0.00"): continue
                #if sum(numpy.array(scan_data.get("ponos").get('data').get('data_uu'))[index]) == 0: continue

                self.comboBox_point_number.addItem(str(round(th, 3)))

            if len(scan_data.get("ponos").get('data')) == 1: self.comboBox_polarisation.addItem("uu")
            for polarisation in scan_data.get("ponos").get('data'):
                if polarisation not in ("data_du", "data_uu", "data_dd", "data_ud"): continue
                if numpy.any(numpy.array(scan_data.get("ponos").get('data').get(polarisation))):
                    self.comboBox_polarisation.addItem(str(polarisation)[-2:])

            self.comboBox_polarisation.setCurrentIndex(0)

    def draw_det_image(self):

        self.graphicsView_det_images.clear()

        if self.SFM_file == "": return
        with h5py.File(self.SFM_file, 'r') as file:

            self.current_th = self.comboBox_point_number.currentText()

            scan_data_instr = file[list(file.keys())[0]].get("instrument")
            motors_data = numpy.array(scan_data_instr.get('motors').get('data')).T
            scalers_data = numpy.array(scan_data_instr.get('scalers').get('data')).T

            ROI_y_top = scan_data_instr.get('scalers').get('roi').get('roi')[1]
            ROI_y_bottom = scan_data_instr.get('scalers').get('roi').get('roi')[0]

            for index, motor in enumerate(scan_data_instr.get('motors').get('SPEC_motor_mnemonics')):
                if "'th'" in str(motor): th_motor_data = motors_data[index]
                elif "'s1hg'" in str(motor): s1hg_motor_data = motors_data[index]
                elif "'s2hg'" in str(motor): s2hg_motor_data = motors_data[index]

            for index, scaler in enumerate(scan_data_instr.get('scalers').get('SPEC_counter_mnemonics')):
                if "'sec'" in str(scaler):
                    time_scalers_data = scalers_data[index]
                    break

            for i in scan_data_instr.get('detectors'):
                if i not in ("psd", "psd_uu", "psd_dd", "psd_du", "psd_ud"): continue

                if i == "psd": scan_psd = "psd"
                else: scan_psd = "psd_" + self.comboBox_polarisation.currentText()

            detector_image = scan_data_instr.get('detectors').get(scan_psd).get('data')

            for index, th in enumerate(th_motor_data):
                # check th
                if self.current_th == str(round(th, 3)):
                    self.lineEdit_slits_s1hg.setText(str(s1hg_motor_data[index]))
                    self.lineEdit_slits_s2hg.setText(str(s2hg_motor_data[index]))
                    self.lineEdit_time.setText(str(time_scalers_data[index]))

                    self.graphicsView_det_images.setImage(detector_image[index], axes={'x':1, 'y':0}, levels=(0,0.1))

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
                    spots = []
                    if self.draw_roi:
                        self.graphicsView_det_images.removeItem(self.draw_roi)

                    for i in range(int(ROI_y_bottom), int(ROI_y_top)):
                        spots.append({'x': int(self.lineEdit_ROI_x_left.text()), 'y': i})
                        spots.append({'x': int(self.lineEdit_ROI_x_right.text()), 'y': i})

                    for i in range(int(self.lineEdit_ROI_x_left.text()), int(self.lineEdit_ROI_x_right.text())):
                        spots.append({'x': i, 'y': int(ROI_y_top)})
                        spots.append({'x': i, 'y': int(ROI_y_bottom)})

                    self.draw_roi = pg.ScatterPlotItem(spots=spots, size=0.5, pen=pg.mkPen(255, 255, 255))
                    self.graphicsView_det_images.addItem(self.draw_roi)

                    break

    def load_reflectivity_preview(self):
        self.graphicsView_refl_profile.getPlotItem().clear()
        self.label_sample_len_missing.setVisible(False)
        self.label_DB_missing.setVisible(False)

        if self.checkBox_OverillCorr.isChecked() and self.lineEdit_SampleLength.text() == "":
            self.label_sample_len_missing.setVisible(True)
            return

        if self.checkBox_NormDB.isChecked() and self.listWidget_DB.count() == 0:
            self.label_DB_missing.setVisible(True)
            return

        self.analazeDB()

        if self.comboBox_scan.currentText() == "": return

        for i in range(0, self.tableWidget_Scans.rowCount()):
            if self.tableWidget_Scans.item(i, 0).text() == self.comboBox_scan.currentText():
                self.SFM_file = self.tableWidget_Scans.item(i, 2).text()

                # ROI region (1400 numbers)
                try:
                    roi_coord = [round(int(self.tableWidget_Scans.item(i, 1).text().split()[0])),
                                 round(int(self.tableWidget_Scans.item(i, 1).text().split()[-1]))]
                except:
                    return

        with h5py.File(self.SFM_file, 'r') as file:

            scan_data_instr = file[list(file.keys())[0]].get("instrument")
            scan_data_ponos = file[list(file.keys())[0]].get("ponos")
            motors_data = numpy.array(scan_data_instr.get('motors').get('data')).T
            scalers_data = numpy.array(scan_data_instr.get('scalers').get('data')).T

            if len(scan_data_ponos.get('data')) == 1:
                self.checkBox_fast_calc.setChecked(False)
                self.checkBox_fast_calc.setEnabled(False)
            else: self.checkBox_fast_calc.setEnabled(True)

            for index, motor in enumerate(scan_data_instr.get('motors').get('SPEC_motor_mnemonics')):
                if "'th'" in str(motor): th_motor_data = motors_data[index]
                elif "'s1hg'" in str(motor): s1hg_motor_data = motors_data[index]
                elif "'s2hg'" in str(motor): s2hg_motor_data = motors_data[index]

            for index, scaler in enumerate(scan_data_instr.get('scalers').get('SPEC_counter_mnemonics')):
                if "'mon0'" in str(scaler): monitor_scalers_data = scalers_data[index]

            if self.lineEdit_SkipSubstrBKG.text(): skip_BKG = float(self.lineEdit_SkipSubstrBKG.text())
            else: skip_BKG = 0.085

            # iterate through scans and th points

            for scan in scan_data_ponos.get('data'):

                if str(scan) in ("data_du", "data_uu", "data_dd", "data_ud") and self.checkBox_fast_calc.isChecked():
                    self.scan_intens_sfm = numpy.array(scan_data_ponos.get('data').get(scan))
                    if str(scan) == "data_uu": color = [0, 0, 0]
                    elif str(scan) == "data_dd": color = [0, 0, 255]
                    elif str(scan) == "data_ud": color = [0, 255, 0]
                    elif str(scan) == "data_du": color = [255, 0, 0]
                    self.SFM_file_already_anilized = ""

                # old files with no polarisation have no ponos
                elif not self.checkBox_fast_calc.isChecked():
                    if "pnr" in list(file[list(file.keys())[0]]):
                        if str(scan) == "data_du":
                            self.scan_intens_sfm = scan_data_instr.get("detectors").get("psd_du").get('data')[:].sum(
                                axis=1)
                            color = [255, 0, 0]
                        elif str(scan) == "data_uu":
                            self.scan_intens_sfm = scan_data_instr.get("detectors").get("psd_uu").get('data')[:].sum(
                                axis=1)
                            color = [0, 0, 0]
                        elif str(scan) == "data_ud":
                            self.scan_intens_sfm = scan_data_instr.get("detectors").get("psd_ud").get('data')[:].sum(
                                axis=1)
                            color = [0, 255, 0]
                        elif str(scan) == "data_dd":
                            self.scan_intens_sfm = scan_data_instr.get("detectors").get("psd_dd").get('data')[:].sum(
                                axis=1)
                            color = [0, 0, 255]

                    else:
                        # SUM of 1400 rows takes 2.5+ seconds, lets avoid useless reSUM each time
                        if not self.SFM_file == self.SFM_file_already_anilized:
                            self.scan_intens_sfm = scan_data_instr.get("detectors").get("psd").get('data')[:].sum(axis=1)
                            self.SFM_file_already_anilized = self.SFM_file
                        color = [0, 0, 0]

                else: continue

                plot_I = []
                plot_angle = []
                plot_dI_err_bottom = []
                plot_dI_err_top = []

                for index, th in enumerate(th_motor_data):
                    # read motors
                    Qz = (4 * numpy.pi / float(self.lineEdit_wavelength.text())) * numpy.sin(numpy.radians(th))
                    s1hg = s1hg_motor_data[index]
                    s2hg = s2hg_motor_data[index]
                    monitor = monitor_scalers_data[index]

                    if not self.checkBox_OverillCorr.isChecked(): overill_corr = 1
                    else: overill_corr = self.overillumination_correct_coeff(s1hg, s2hg, round(th, 4), float(self.lineEdit_SampleLength.text()))[0]

                    # analize integrated intensity for ROI
                    Intens = sum(self.scan_intens_sfm[index][round(roi_coord[0] / 2): round(roi_coord[1] / 2)])
                    Intens_bkg = sum(self.scan_intens_sfm[index][round(roi_coord[0] - (roi_coord[1] - roi_coord[0]) - 1 / 2) : round(roi_coord[0] - 1 / 2)])
                    if self.scan_intens_sfm.shape[1] == 1400:
                        Intens = sum(self.scan_intens_sfm[index][roi_coord[0]: roi_coord[1]])
                        Intens_bkg = sum(self.scan_intens_sfm[index][roi_coord[0]-(roi_coord[1]-roi_coord[0])-1 : roi_coord[0]-1])

                    # minus background, devide by monitor, overillumination correct + calculate errors
                    if Intens < 0: continue

                    Intens_err = numpy.sqrt(Intens)

                    if self.checkBox_SubstrBKG.isChecked() and Qz > skip_BKG and Intens > 0:
                        if Intens_bkg > 0:
                            Intens_err = numpy.sqrt(Intens + Intens_bkg)
                            Intens = Intens - Intens_bkg

                    if self.checkBox_DevideByMon.isChecked() and Intens > 0:
                        Intens_err = (Intens / monitor) * numpy.sqrt((Intens_err / Intens) ** 2 + (1 / monitor))
                        Intens = Intens / monitor

                    if self.checkBox_OverillCorr.isChecked() and Intens > 0:
                        Intens_err = Intens_err / overill_corr
                        Intens = Intens / overill_corr

                    if self.checkBox_NormDB.isChecked() and Intens > 0 and len(self.DB_info) > 0:
                        DB_intens = float(self.DB_info[str(s1hg) + ";" + str(s2hg)].split(";")[0])
                        DB_err = overill_corr * float(self.DB_info[str(s1hg) + ";" + str(s2hg)].split(";")[1])
                        Intens_err = (Intens / DB_intens) * numpy.sqrt((DB_err / DB_intens) ** 2 + (Intens_err / Intens) ** 2)
                        Intens = Intens / DB_intens

                    if Intens > 0:
                        plot_I.append(numpy.log10(Intens))
                        plot_angle.append(Qz)
                        plot_dI_err_top.append(abs(numpy.log10(Intens + Intens_err) - numpy.log10(Intens)))

                        if Intens > Intens_err: plot_dI_err_bottom.append(numpy.log10(Intens) - numpy.log10(Intens - Intens_err))
                        else: plot_dI_err_bottom.append(0)

                if self.checkBox_incl_errorbars.isChecked():
                    s1 = pg.ErrorBarItem(x=numpy.array(plot_angle), y=numpy.array(plot_I), top=numpy.array(plot_dI_err_top), bottom=numpy.array(plot_dI_err_bottom), pen=pg.mkPen(color[0], color[1], color[2]), brush=pg.mkBrush(color[0], color[1], color[2]))
                    self.graphicsView_refl_profile.addItem(s1)

                s2 = pg.ScatterPlotItem(x=plot_angle, y=plot_I, symbol="o", size=2, pen=pg.mkPen(color[0], color[1], color[2]), brush=pg.mkBrush(color[0], color[1], color[2]))
                self.graphicsView_refl_profile.addItem(s2)

    def update_slits(self):
        for i in range(0, self.tableWidget_Scans.rowCount()):
            if self.tableWidget_Scans.item(i, 0).text() == self.comboBox_scan.currentText():
                self.tableWidget_Scans.item(i, 1).setText(self.lineEdit_ROI_x_left.text() + " : " + self.lineEdit_ROI_x_right.text())

        roi_width = int(self.lineEdit_ROI_x_right.text()) - int(self.lineEdit_ROI_x_left.text())
        self.lineEdit_ROI_BKG_x_left.setText(str(2 * round(int(self.lineEdit_ROI_x_left.text()) / 2) - roi_width - 1))
        self.lineEdit_ROI_BKG_x_right.setText(str(2 * round(int(self.lineEdit_ROI_x_left.text()) / 2) - 1))

        self.draw_det_image()

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

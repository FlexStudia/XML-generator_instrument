# coding: utf-8

"""

This script is the GUI script of the XMLGenerator_instrument program.
Its aim is to create an interface to fill the XML instrument template (for SSHADE.eu database).

This script has 5 parts (=sections):
1. IMPORTS with all imported packages, the core script functions and interface templates that we will need
2. GLOBALS with all global variables used in this script
3. external FUNCTIONS
4. MAIN WINDOW class where the interface and its functionality are created
    4.1 GUI beauties to extend UI template
    4.2 SLOT functions connect to put together the interface and its functionality
    4.3 SLOT functions which cover the app functionality
5. MAIN WINDOW class emulation which calls an instance of the MAIN WINDOW class to run the interface

"""


# 1 IMPORTS
# 1.1 PyQt pack
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QAction, QLineEdit, QApplication
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
import sys
# 1.2 core code
from templates.mw import Ui_MainWindow as Ui_MainWindow
from XMLGenerator_instrument_core import xml_parse_and_fill as xml_parse_and_fill
from XMLGenerator_instrument_core import accent_letters_replace as accent_letters_replace


# 2 GLOBALS
# variables
__version__ = 0.83
__copyright__ = "<a href='https://creativecommons.org/licenses/by/4.0/deed.fr'>CC-BY 4.0</a> (Authors attribution alone required)"
__GitHub_repos__ = "https://github.com/FlexStudia/XML-generator_instrument"
__author_mail__ = "flex.studia.dev@gmail.com"
__bug_support_mail__ = "XML.generator.instrument@gmail.com"
# XML template: laboratory
template = "<?xml version='1.0' encoding='UTF-8'?><!-- Data type : Instrument Specific notes : - General notes : - Most of the tags are optional, you can remove the really unnecessary ones. - Tags marked as 'multiple' can be copied (with its block of sub-tag, up to the ending tag) if needed. - all blocs marked 'OPTION' can be fully removed if not needed (now or in the future) - **ABS MANDATORY / ABS COMPULSORY**: a value need to be absolutely provided, no way to escape! (SSHADE will not function properly if absent). - **MANDATORY / COMPULSORY**: very important values for the search of the data. If the value (txt or numeric) of one tag is not known (or irrelevant in your case), then put 'NULL' and write a comment to keep track of the missing value. Remove comment when value is added. - **MANDATORY / COMPULSORY only for ...**: when a value is optionally MANDATORY the condition is written. - 'LINK to existing UID' (unique identifier): references to another table in SSHADE. You have to reconstruct (easy for some: rule is in comment) or found this existing UID in the database beforehand (use 'Provider/Full Search' menu in SSHADE). - 'UID to CREATE': you need to create this UID using their specific rules of creation that are explained in their attached comment. Use only alphanumeric characters and '_'. - For UID you can use only alpha-numeric characters and the following: '_', '-' - Enumeration type ('Enum' or 'OpenEnum') must contain one single item from the list given in brackets {}. - use a CDATA tag when a value contains at least one special character (ie: &, >, <,...). Example: <![CDATA[AT&T]]> for AT&T - The data format is noted beetween [] and is 'ascii' when not specified. Ex: [Float], [Integer]. For [float] 2 formats are possible: decimal (123.456) or scientific (1.234e-56) - when no numerical format or Enum is specified, it is free text but limited to 256 characters. Only those noted [blob] have no size limitation. - to import data for the first time you have to set <import_mode>='first import'. To correct data you have to change it to 'correction'. - when a <filename> is given, then the file should be ziped with this xml file for import. --><import type='instrument' ssdm_version='0.9.0' xmlns='http://sshade.eu/schema/import' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:schemaLocation='http://sshade.eu/schema/import http://sshade.eu/schema/import-0.9.xsd'><instrument><!-- multiple --><import_mode>first import</import_mode><!-- **ABS MANDATORY** Mode of import of the 'instrument' data. Enum: {first import, ignore, draft, no change, correction} --><uid>INSTRU_</uid> <!-- **ABS MANDATORY to CREATE** Unique identifier code given to the instrument+technique set: It should be in fully in UPPERCASE of the style ‘INSTRU_InstrumentName_Technique_LabAcronym’ where ‘InstrumentName’ is the instrument name, ‘Technique’ is a short but unambiguous version of the technique name, and ‘LabAcronym’ is the acronym of the laboratory where it is situated --><!-- INSTRUMENT LOCATION --><manager_databases> <!-- **ABS MANDATORY at least one** --><database_uid>DB_</database_uid><!-- multiple --> <!-- LINK to the existing UID of the database which manages this instrument information [‘DB_DatabaseAcronym’] --></manager_databases><laboratories> <!-- **ABS MANDATORY at least one** --><laboratory current='true'><!-- multiple --> <!-- FlagEnum {yes, no} or {true, false} --><uid>LAB_</uid> <!-- **ABS MANDATORY** LINK to the UID of the laboratory where the instrument is (or was) located [‘LAB_LabAcronym’] --><comments><![CDATA[]]></comments> <!-- Additional information: years, where it was before ... [Blob] --></laboratory></laboratories><!-- INSTRUMENT DESCRIPTION --><type></type> <!-- **ABS MANDATORY** Type of used instrument. FreeList: {FTIR spectrometer, grating spectrometer, AOTF spectrometer, CRDS spectrometer, laser diode spectrometer, SWIFT spectrometer, µSPOC spectrometer, narrow-band filters spectrometer, grating imaging spectrometer, grating hyperspectral imaging system, ImSPOC imaging spectrometer, narrow-band filters imager, spectro-gonio radiometer, Raman spectrometer, Raman micro-spectrometer, FTIR micro-spectrometer, spectrofluorometer, ellipsometer, X-ray absorption spectrometer, gamma-ray spectrometer, Mossbauer spectrometer, vector network analyzer, radiative transfer simulation, quantum mechanical simulation, …} --><name></name> <!-- **ABS MANDATORY** Specific name and model of the instrument --><technique></technique> <!-- **ABS MANDATORY** Instrumental technique. OpenEnum: {transmission, reflection-absorption, ATReflection, specular reflection, ellipsometry, bidirectional reflection, biconical reflection, confocal reflection, diffuse reflection, directional-hemispheric reflection, hemispheric-directional reflection, scattering, thermal emission, Raman scattering, fluorescence emission, gamma emission, Mossbauer absorption, permittivity, time-domain, dual polarisation interferometry} --><technique_name></technique_name> <!-- **ABS MANDATORY** Name describing the combination of instrument, technique and spectral range used -->	<!-- INSTRUMENT TECHNIQUES DESCRIPTION --><microscopy_imaging></microscopy_imaging> <!-- **MANDATORY** Tell if the instrumental technique use a microscope, a micro-imager, an imager or not. Enum: {macroscopic, microscopy, linear scan, linear micro-scan, imaging, micro-imaging} --><optical_accessory></optical_accessory> <!-- Type of additional optical accessory installed in the instrument. Free list: {Ge ATR crystal, KRS-5 crystal, ZnSe ATR crystal, Si ATR crystal, biconical diffuse reflectance, diffuse reflectance (DRIFTS), multipass cell, integrating sphere, absolute specular reflectance, blue filter, red filter, linear polarizer, Vis confocal microscope in reflection, IR microscope in transmission, IR microscope in reflection, IR microscope in ATR, …} --> <source></source> <!-- **MANDATORY** Light source type of the instrument. Free list: {Tungsten/Halogen lamp, Globar-IR, Hydrogen arc lamp, Deuterium arc lamp, Hg lamp, Xe arc lamp, He-Ne laser, laser diode, Ar+/Kr+ laser, Ar+ laser, frequency-doubled Ar+ laser, Nd:YAG laser, frequency-doubled Nd:YAG laser, pulsed laser, synchrotron - bending magnet, synchrotron - undulator, synchrotron - wiggler, Sun, no, ,…} --><source_wavelength></source_wavelength> <!-- **MANDATORY** General spectral range, precise wavelength (laser), or wavelength range (laser diode) of the source. Free list: {gamma, hard X, soft X, EUV, VUV-UV, Vis-NIR, UV-NIR, MIR, FIR, MIR-FIR, submm, mm, 90GHz, 6050-6900 cm-1, 244 nm, 457.9 nm, 488 nm, 514.5 nm, 532 nm, 632.8 nm, 647.1 nm,…} --><source_power></source_power> <!-- **MANDATORY only for Raman and fluorescence techniques** Power of the source [give the unit: W, W/cm2, ...] --><spectral_analyzers><!-- **MANDATORY at least one** --><spectral_analyzer></spectral_analyzer><!-- multiple --> <!-- **MANDATORY** Type of spectral analyzer of the instrument. Free list: {Quartz beamsplitter, CaF2 beamsplitter, KBr/Ge beamsplitter, Si beamsplitter, Mylar 20µm beamsplitter, diffraction grating 1200 l/mm - 250nm, diffraction grating 600 l/mm - 400nm, diffraction grating 300 l/mm - 1000nm, diffraction grating 150 l/mm - 4000nm, diffraction grating 3600 l/mm, diffraction grating 1800 l/mm, diffraction grating 1200 l/mm - 1200nm, diffraction grating 600 l/mm - 550nm, diffraction grating 150 l/mm, Ge AOTF 1.5-3 µm, 2-crystal monochromator Si[111], 2-crystal monochromator Si[220], 2-crystal monochromator Si[311], crystal analyser Ge [110], crystal analyser Ge [111], crystal analyser Ge [331], crystal analyser Si [111], X-ray polychromator, narrow-band filters, no, …} --></spectral_analyzers><detectors><!-- **MANDATORY at least one** --><detector></detector><!-- multiple --> <!-- **MANDATORY** Detector type of the instrument: Free list: {Si, Si drift, Ge array, InSb (liq. N2 cooled), InSb (cryocooler), InGaAs, PbS, PbSe, MCT (liq. N2 cooled), DTGS-KBr, DTGS-PE, Ge bolometer (He cooled), Si bolometer (He cooled), MCT array (liq. N2 cooled), CCD, CCD (liq. N2 cooled), LSO:Tb scintillator, other, no, …} --></detectors> <comments><![CDATA[]]></comments> <!-- Additional information on the instrument and techniques (special configuration, use of cryogenic/thermal/vacuum cell ...) or simulation model [Blob] --><!-- INSTRUMENT: REFERENCES --><documentations> <!-- **OPTION** --> <!-- Documentations describing the instrument and its associated techniques and performances, i.e. all parameters described in this 'instrument' part --><documentation><!-- multiple --><name><![CDATA[]]></name> <!-- Name of the documentation --><filename><![CDATA[]]></filename> <!-- File name of the documentation (pdf file). This image file should be zipped with the xml file --></documentation></documentations><links> <!-- **OPTION** --><!-- Link(s) to web page(s) describing the instrument, technique and/or the cells used, or the simulation model used --><link><!-- multiple --> <name><![CDATA[]]></name> <!-- Name of the web page(s) --><url><![CDATA[]]></url> <!-- URL address (avoid non-perennial commercial URL) --></link></links><publications> <!-- **OPTION** --> <!-- List of publication(s) describing instrument, technique and/or the cells used, or the simulation model used --><publication_uid></publication_uid><!-- multiple --> <!-- LINK to the existing UID of the publication [‘‘PUBLI_FirstAuthorName_Year(Letter)’] --></publications></instrument>	</import>"
# styles
button_style = 'QPushButton{padding: 5px}'


# 3 external FUNCTIONS
# style function to add colors, borders & padding to fields
def style_color_add(field_type, color):
    if color == 'red':
        border_color = '251,157,111'
        background_color = '255,250,245'
    elif color == 'green':
        border_color = '86,231,200'
        background_color = '249,255,254'
    elif color == 'gray':
        border_color = '190,190,190'
        background_color = '240,240,240'
    else:
        border_color = '240,200,41'
        background_color = '253,253,241'
    return f"{field_type}[border-width: 2px; border-style: solid; border-color: rgb({border_color}); " \
           f"background-color: rgb({background_color}); padding: 5px; font-size: 16px]" \
        .replace("[", "{").replace("]", "}")


# class to make a clickable area for QLabel
class QLineEditClickable(QLineEdit):
    clicked = pyqtSignal(str)
    def __init__(self, parent=None):
        super(QLineEditClickable, self).__init__(parent)
    def mousePressEvent(self, event):
        self.ultimo = "Clic"
    def mouseReleaseEvent(self, event):
        QTimer.singleShot(QApplication.instance().doubleClickInterval()/6,
                          self.performSingleClickAction)
    def performSingleClickAction(self):
        if self.ultimo == "Clic":
            self.clicked.emit(self.ultimo)


# 4 MAIN WINDOW class
class XMLGeneratorMainW(QtWidgets.QMainWindow):
    def __init__(self):
        super(XMLGeneratorMainW, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # 4.1 GUI beauties
        self.setWindowTitle(f'SSHADE Instrument XML template v{__version__}')
        # name
        self.ui.name.setStyleSheet(f'{style_color_add("QLineEdit", "red")}')
        # type select
        self.ui.instrument_type.setStyleSheet(f'{style_color_add("QComboBox", "red")}')
        self.ui.instrument_type.insertItem(0, '-- select a type --')
        self.ui.instrument_type.insertItem(1, 'FTIR spectrometer')
        self.ui.instrument_type.insertItem(2, 'grating spectrometer')
        self.ui.instrument_type.insertItem(3, 'AOTF spectrometer')
        self.ui.instrument_type.insertItem(4, 'CRDS spectrometer')
        self.ui.instrument_type.insertItem(5, 'laser diode spectrometer')
        self.ui.instrument_type.insertItem(6, 'SWIFT spectrometer')
        self.ui.instrument_type.insertItem(7, 'µSPOC spectrometer')
        self.ui.instrument_type.insertItem(8, 'narrow-band filters spectrometer')
        self.ui.instrument_type.insertItem(9, 'grating imaging spectrometer')
        self.ui.instrument_type.insertItem(10, 'grating hyperspectral imaging system')
        self.ui.instrument_type.insertItem(11, 'ImSPOC imaging spectrometer')
        self.ui.instrument_type.insertItem(12, 'narrow-band filters imager')
        self.ui.instrument_type.insertItem(13, 'spectro-gonio radiometer')
        self.ui.instrument_type.insertItem(14, 'Raman spectrometer')
        self.ui.instrument_type.insertItem(15, 'Raman micro-spectrometer')
        self.ui.instrument_type.insertItem(16, 'FTIR micro-spectrometer')
        self.ui.instrument_type.insertItem(17, 'spectrofluorometer')
        self.ui.instrument_type.insertItem(18, 'ellipsometer')
        self.ui.instrument_type.insertItem(19, 'X-ray absorption spectrometer')
        self.ui.instrument_type.insertItem(20, 'gamma-ray spectrometer')
        self.ui.instrument_type.insertItem(21, 'Mossbauer spectrometer')
        self.ui.instrument_type.insertItem(22, 'vector network analyzer')
        self.ui.instrument_type.insertItem(23, 'radiative transfer simulation')
        self.ui.instrument_type.insertItem(24, 'quantum mechanical simulation')
        self.ui.instrument_type.insertItem(25, 'Other...')
        self.ui.instrument_type.setCurrentIndex(0)
        # type other
        self.ui.instrument_type_other = QLineEditClickable(self.ui.tab)
        self.ui.instrument_type_other.setObjectName("instrument_type_other")
        self.ui.gridLayout_13.addWidget(self.ui.instrument_type_other, 0, 1, 1, 1)
        self.ui.instrument_type_other.setStyleSheet(f'{style_color_add("QLineEdit", "gray")}')
        self.ui.instrument_type_other.setPlaceholderText("write your instrument type here if it is not listed on the left")
        # technique
        self.ui.technique.setStyleSheet(f'{style_color_add("QComboBox", "red")}')
        self.ui.technique.insertItem(0, '-- select a technique --')
        self.ui.technique.insertItem(1, 'transmission')
        self.ui.technique.insertItem(2, 'reflection-absorption')
        self.ui.technique.insertItem(3, 'ATReflection')
        self.ui.technique.insertItem(4, 'specular reflection')
        self.ui.technique.insertItem(5, 'ellipsometry')
        self.ui.technique.insertItem(6, 'bidirectional reflection')
        self.ui.technique.insertItem(7, 'biconical reflection')
        self.ui.technique.insertItem(8, 'confocal reflection')
        self.ui.technique.insertItem(9, 'diffuse reflection')
        self.ui.technique.insertItem(10, 'directional-hemispheric reflection')
        self.ui.technique.insertItem(11, 'hemispheric-directional reflection')
        self.ui.technique.insertItem(12, 'scattering')
        self.ui.technique.insertItem(13, 'thermal emission')
        self.ui.technique.insertItem(14, 'Raman scattering')
        self.ui.technique.insertItem(15, 'fluorescence emission')
        self.ui.technique.insertItem(16, 'gamma emission')
        self.ui.technique.insertItem(17, 'Mossbauer absorption')
        self.ui.technique.insertItem(18, 'permittivity')
        self.ui.technique.insertItem(19, 'time-domain')
        self.ui.technique.insertItem(20, 'dual polarisation interferometry')
        self.ui.technique.setCurrentIndex(0)
        # technique_name
        self.ui.technique_name.setStyleSheet(f'{style_color_add("QTextEdit", "red")}')
        # comments
        self.ui.comments.setStyleSheet(f'{style_color_add("QTextEdit", "green")}')
        # current lab
        self.ui.lab_current_acronym.setStyleSheet(f'{style_color_add("QLineEdit", "red")}')
        self.ui.lab_current_comment.setStyleSheet(f'{style_color_add("QTextEdit", "green")}')
        # previous 1 lab
        self.ui.lab_previous_1_acronym.setStyleSheet(f'{style_color_add("QLineEdit", "green")}')
        self.ui.lab_previous_1_comment.setStyleSheet(f'{style_color_add("QTextEdit", "green")}')
        # previous 2 lab
        self.ui.lab_previous_2_acronym.setStyleSheet(f'{style_color_add("QLineEdit", "green")}')
        self.ui.lab_previous_2_comment.setStyleSheet(f'{style_color_add("QTextEdit", "green")}')
        # microscopy_imaging
        self.ui.microscopy_imaging.setStyleSheet(f'{style_color_add("QComboBox", "yellow")}')
        self.ui.microscopy_imaging.insertItem(0, '-- select a microscopy imaging type --')
        self.ui.microscopy_imaging.insertItem(1, 'macroscopic')
        self.ui.microscopy_imaging.insertItem(2, 'microscopy')
        self.ui.microscopy_imaging.insertItem(3, 'linear scan')
        self.ui.microscopy_imaging.insertItem(4, 'linear micro-scan')
        self.ui.microscopy_imaging.insertItem(5, 'imaging')
        self.ui.microscopy_imaging.insertItem(6, 'micro-imaging')
        self.ui.microscopy_imaging.setCurrentIndex(0)
        # optical_accessory
        self.ui.optical_accessory.setStyleSheet(f'{style_color_add("QComboBox", "green")}')
        self.ui.optical_accessory.insertItem(0, '-- select an optical_accessory --')
        self.ui.optical_accessory.insertItem(1, 'Ge ATR crystal')
        self.ui.optical_accessory.insertItem(2, 'KRS-5 crystal')
        self.ui.optical_accessory.insertItem(3, 'ZnSe ATR crystal')
        self.ui.optical_accessory.insertItem(4, 'Si ATR crystal')
        self.ui.optical_accessory.insertItem(5, 'biconical diffuse reflectance')
        self.ui.optical_accessory.insertItem(6, 'diffuse reflectance (DRIFTS)')
        self.ui.optical_accessory.insertItem(7, 'multipass cell')
        self.ui.optical_accessory.insertItem(8, 'integrating sphere')
        self.ui.optical_accessory.insertItem(9, 'absolute specular reflectance')
        self.ui.optical_accessory.insertItem(10, 'blue filter')
        self.ui.optical_accessory.insertItem(11, 'red filter')
        self.ui.optical_accessory.insertItem(12, 'linear polarizer')
        self.ui.optical_accessory.insertItem(13, 'Vis confocal microscope in reflection')
        self.ui.optical_accessory.insertItem(14, 'IR microscope in transmission')
        self.ui.optical_accessory.insertItem(15, 'IR microscope in reflection')
        self.ui.optical_accessory.insertItem(16, 'IR microscope in ATR')
        self.ui.optical_accessory.insertItem(17, 'Other...')
        self.ui.optical_accessory.setCurrentIndex(0)
        # optical_accessory other
        self.ui.optical_accessory_other = QLineEditClickable(self.ui.tab_3)
        self.ui.optical_accessory_other.setObjectName("optical_accessory_other")
        self.ui.gridLayout_14.addWidget(self.ui.optical_accessory_other, 0, 1, 1, 1)
        self.ui.optical_accessory_other.setStyleSheet(f'{style_color_add("QLineEdit", "gray")}')
        self.ui.optical_accessory_other.setPlaceholderText("write your optical accessory here if it is not listed on the left")
        # source
        self.ui.source.setStyleSheet(f'{style_color_add("QComboBox", "yellow")}')
        self.ui.source.insertItem(0, '-- select a source --')
        self.ui.source.insertItem(1, 'Tungsten/Halogen lamp')
        self.ui.source.insertItem(2, 'Globar-IR')
        self.ui.source.insertItem(3, 'Hydrogen arc lamp')
        self.ui.source.insertItem(4, 'Deuterium arc lamp')
        self.ui.source.insertItem(5, 'Hg lamp')
        self.ui.source.insertItem(6, 'Xe arc lamp')
        self.ui.source.insertItem(7, 'He-Ne laser')
        self.ui.source.insertItem(8, 'laser diode')
        self.ui.source.insertItem(9, 'Ar+/Kr+ laser')
        self.ui.source.insertItem(10, 'Ar+ laser')
        self.ui.source.insertItem(11, 'frequency-doubled Ar+ laser')
        self.ui.source.insertItem(12, 'Nd:YAG laser')
        self.ui.source.insertItem(13, 'frequency-doubled Nd:YAG laser')
        self.ui.source.insertItem(14, 'pulsed laser')
        self.ui.source.insertItem(15, 'synchrotron - bending magnet')
        self.ui.source.insertItem(16, 'synchrotron - undulator')
        self.ui.source.insertItem(17, 'synchrotron - wiggler')
        self.ui.source.insertItem(18, 'Sun')
        self.ui.source.insertItem(19, 'no')
        self.ui.source.insertItem(20, 'Other...')
        self.ui.source.setCurrentIndex(0)
        # source other
        self.ui.source_other = QLineEditClickable(self.ui.tab_3)
        self.ui.source_other.setObjectName("source_other")
        self.ui.gridLayout_15.addWidget(self.ui.source_other, 0, 1, 1, 1)
        self.ui.source_other.setStyleSheet(f'{style_color_add("QLineEdit", "gray")}')
        self.ui.source_other.setPlaceholderText("write your source here if it is not listed on the left")
        # source_wavelength
        self.ui.source_wavelength.setStyleSheet(f'{style_color_add("QComboBox", "yellow")}')
        self.ui.source_wavelength.insertItem(0, '-- select the source wavelength --')
        self.ui.source_wavelength.insertItem(1, 'gamma')
        self.ui.source_wavelength.insertItem(2, 'hard X')
        self.ui.source_wavelength.insertItem(3, 'soft X')
        self.ui.source_wavelength.insertItem(4, 'EUV')
        self.ui.source_wavelength.insertItem(5, 'VUV-UV')
        self.ui.source_wavelength.insertItem(6, 'Vis-NIR')
        self.ui.source_wavelength.insertItem(7, 'UV-NIR')
        self.ui.source_wavelength.insertItem(8, 'MIR')
        self.ui.source_wavelength.insertItem(9, 'FIR')
        self.ui.source_wavelength.insertItem(10, 'MIR-FIR')
        self.ui.source_wavelength.insertItem(11, 'submm')
        self.ui.source_wavelength.insertItem(12, 'mm')
        self.ui.source_wavelength.insertItem(13, '90GHz')
        self.ui.source_wavelength.insertItem(14, '6050-6900 cm-1')
        self.ui.source_wavelength.insertItem(15, '244 nm')
        self.ui.source_wavelength.insertItem(16, '457.9 nm')
        self.ui.source_wavelength.insertItem(17, '488 nm')
        self.ui.source_wavelength.insertItem(18, '514.5 nm')
        self.ui.source_wavelength.insertItem(19, '532 nm')
        self.ui.source_wavelength.insertItem(20, '632.8 nm')
        self.ui.source_wavelength.insertItem(21, '647.1 nm')
        self.ui.source_wavelength.insertItem(22, 'Other...')
        self.ui.source_wavelength.setCurrentIndex(0)
        # source_wavelength other
        self.ui.source_wavelength_other = QLineEditClickable(self.ui.tab_3)
        self.ui.source_wavelength_other.setObjectName("source_wavelength_other")
        self.ui.gridLayout_16.addWidget(self.ui.source_wavelength_other, 0, 1, 1, 1)
        self.ui.source_wavelength_other.setStyleSheet(f'{style_color_add("QLineEdit", "gray")}')
        self.ui.source_wavelength_other.setPlaceholderText("write your source wavelength here if it is not listed on the left")
        # source_power
        self.ui.source_power.setStyleSheet(f'{style_color_add("QLineEdit", "green")}')
        # spectral_analyzer_1
        self.ui.spectral_analyzer_1.setStyleSheet(f'{style_color_add("QComboBox", "yellow")}')
        self.ui.spectral_analyzer_1.insertItem(0, '-- select a spectral analyzer --')
        self.ui.spectral_analyzer_1.insertItem(1, 'Quartz beamsplitter')
        self.ui.spectral_analyzer_1.insertItem(2, 'CaF2 beamsplitter')
        self.ui.spectral_analyzer_1.insertItem(3, 'KBr/Ge beamsplitter')
        self.ui.spectral_analyzer_1.insertItem(4, 'Si beamsplitter')
        self.ui.spectral_analyzer_1.insertItem(5, 'Mylar 20µm beamsplitter')
        self.ui.spectral_analyzer_1.insertItem(6, 'diffraction grating 1200 l/mm - 250nm')
        self.ui.spectral_analyzer_1.insertItem(7, 'diffraction grating 600 l/mm - 400nm')
        self.ui.spectral_analyzer_1.insertItem(8, 'diffraction grating 300 l/mm - 1000nm')
        self.ui.spectral_analyzer_1.insertItem(9, 'diffraction grating 150 l/mm - 4000nm')
        self.ui.spectral_analyzer_1.insertItem(10, 'diffraction grating 3600 l/mm')
        self.ui.spectral_analyzer_1.insertItem(11, 'diffraction grating 1800 l/mm')
        self.ui.spectral_analyzer_1.insertItem(12, 'diffraction grating 1200 l/mm - 1200nm')
        self.ui.spectral_analyzer_1.insertItem(13, 'diffraction grating 600 l/mm - 550nm')
        self.ui.spectral_analyzer_1.insertItem(14, 'diffraction grating 150 l/mm')
        self.ui.spectral_analyzer_1.insertItem(15, 'Ge AOTF 1.5-3 µm')
        self.ui.spectral_analyzer_1.insertItem(16, '2-crystal monochromator Si[111]')
        self.ui.spectral_analyzer_1.insertItem(17, '2-crystal monochromator Si[220]')
        self.ui.spectral_analyzer_1.insertItem(18, '2-crystal monochromator Si[311]')
        self.ui.spectral_analyzer_1.insertItem(19, 'crystal analyser Ge [110]')
        self.ui.spectral_analyzer_1.insertItem(20, 'crystal analyser Ge [111]')
        self.ui.spectral_analyzer_1.insertItem(21, 'crystal analyser Ge [331]')
        self.ui.spectral_analyzer_1.insertItem(22, 'crystal analyser Si [111]')
        self.ui.spectral_analyzer_1.insertItem(23, 'X-ray polychromator')
        self.ui.spectral_analyzer_1.insertItem(24, 'narrow-band filters')
        self.ui.spectral_analyzer_1.insertItem(25, 'no')
        self.ui.spectral_analyzer_1.insertItem(26, 'Other...')
        self.ui.spectral_analyzer_1.setCurrentIndex(0)
        # spectral_analyzer_1 other
        self.ui.spectral_analyzer_1_other = QLineEditClickable(self.ui.tab_7)
        self.ui.spectral_analyzer_1_other.setObjectName("spectral_analyzer_1_other")
        self.ui.gridLayout_17.addWidget(self.ui.spectral_analyzer_1_other, 0, 1, 1, 1)
        self.ui.spectral_analyzer_1_other.setStyleSheet(f'{style_color_add("QLineEdit", "gray")}')
        self.ui.spectral_analyzer_1_other.setPlaceholderText(
            "write your spectral analyzer here if it is not listed on the left")
        # spectral_analyzer_2
        self.ui.spectral_analyzer_2.setStyleSheet(f'{style_color_add("QComboBox", "green")}')
        self.ui.spectral_analyzer_2.insertItem(0, '-- select a spectral analyzer --')
        self.ui.spectral_analyzer_2.insertItem(1, 'Quartz beamsplitter')
        self.ui.spectral_analyzer_2.insertItem(2, 'CaF2 beamsplitter')
        self.ui.spectral_analyzer_2.insertItem(3, 'KBr/Ge beamsplitter')
        self.ui.spectral_analyzer_2.insertItem(4, 'Si beamsplitter')
        self.ui.spectral_analyzer_2.insertItem(5, 'Mylar 20µm beamsplitter')
        self.ui.spectral_analyzer_2.insertItem(6, 'diffraction grating 1200 l/mm - 250nm')
        self.ui.spectral_analyzer_2.insertItem(7, 'diffraction grating 600 l/mm - 400nm')
        self.ui.spectral_analyzer_2.insertItem(8, 'diffraction grating 300 l/mm - 1000nm')
        self.ui.spectral_analyzer_2.insertItem(9, 'diffraction grating 150 l/mm - 4000nm')
        self.ui.spectral_analyzer_2.insertItem(10, 'diffraction grating 3600 l/mm')
        self.ui.spectral_analyzer_2.insertItem(11, 'diffraction grating 1800 l/mm')
        self.ui.spectral_analyzer_2.insertItem(12, 'diffraction grating 1200 l/mm - 1200nm')
        self.ui.spectral_analyzer_2.insertItem(13, 'diffraction grating 600 l/mm - 550nm')
        self.ui.spectral_analyzer_2.insertItem(14, 'diffraction grating 150 l/mm')
        self.ui.spectral_analyzer_2.insertItem(15, 'Ge AOTF 1.5-3 µm')
        self.ui.spectral_analyzer_2.insertItem(16, '2-crystal monochromator Si[111]')
        self.ui.spectral_analyzer_2.insertItem(17, '2-crystal monochromator Si[220]')
        self.ui.spectral_analyzer_2.insertItem(18, '2-crystal monochromator Si[311]')
        self.ui.spectral_analyzer_2.insertItem(19, 'crystal analyser Ge [110]')
        self.ui.spectral_analyzer_2.insertItem(20, 'crystal analyser Ge [111]')
        self.ui.spectral_analyzer_2.insertItem(21, 'crystal analyser Ge [331]')
        self.ui.spectral_analyzer_2.insertItem(22, 'crystal analyser Si [111]')
        self.ui.spectral_analyzer_2.insertItem(23, 'X-ray polychromator')
        self.ui.spectral_analyzer_2.insertItem(24, 'narrow-band filters')
        self.ui.spectral_analyzer_2.insertItem(25, 'no')
        self.ui.spectral_analyzer_2.insertItem(26, 'Other...')
        self.ui.spectral_analyzer_2.setCurrentIndex(0)
        # spectral_analyzer_2 other
        self.ui.spectral_analyzer_2_other = QLineEditClickable(self.ui.tab_7)
        self.ui.spectral_analyzer_2_other.setObjectName("spectral_analyzer_2_other")
        self.ui.gridLayout_18.addWidget(self.ui.spectral_analyzer_2_other, 0, 1, 1, 1)
        self.ui.spectral_analyzer_2_other.setStyleSheet(f'{style_color_add("QLineEdit", "gray")}')
        self.ui.spectral_analyzer_2_other.setPlaceholderText(
            "write your spectral analyzer here if it is not listed on the left")
        # spectral_analyzer_3
        self.ui.spectral_analyzer_3.setStyleSheet(f'{style_color_add("QComboBox", "green")}')
        self.ui.spectral_analyzer_3.insertItem(0, '-- select a spectral analyzer --')
        self.ui.spectral_analyzer_3.insertItem(1, 'Quartz beamsplitter')
        self.ui.spectral_analyzer_3.insertItem(2, 'CaF2 beamsplitter')
        self.ui.spectral_analyzer_3.insertItem(3, 'KBr/Ge beamsplitter')
        self.ui.spectral_analyzer_3.insertItem(4, 'Si beamsplitter')
        self.ui.spectral_analyzer_3.insertItem(5, 'Mylar 20µm beamsplitter')
        self.ui.spectral_analyzer_3.insertItem(6, 'diffraction grating 1200 l/mm - 250nm')
        self.ui.spectral_analyzer_3.insertItem(7, 'diffraction grating 600 l/mm - 400nm')
        self.ui.spectral_analyzer_3.insertItem(8, 'diffraction grating 300 l/mm - 1000nm')
        self.ui.spectral_analyzer_3.insertItem(9, 'diffraction grating 150 l/mm - 4000nm')
        self.ui.spectral_analyzer_3.insertItem(10, 'diffraction grating 3600 l/mm')
        self.ui.spectral_analyzer_3.insertItem(11, 'diffraction grating 1800 l/mm')
        self.ui.spectral_analyzer_3.insertItem(12, 'diffraction grating 1200 l/mm - 1200nm')
        self.ui.spectral_analyzer_3.insertItem(13, 'diffraction grating 600 l/mm - 550nm')
        self.ui.spectral_analyzer_3.insertItem(14, 'diffraction grating 150 l/mm')
        self.ui.spectral_analyzer_3.insertItem(15, 'Ge AOTF 1.5-3 µm')
        self.ui.spectral_analyzer_3.insertItem(16, '2-crystal monochromator Si[111]')
        self.ui.spectral_analyzer_3.insertItem(17, '2-crystal monochromator Si[220]')
        self.ui.spectral_analyzer_3.insertItem(18, '2-crystal monochromator Si[311]')
        self.ui.spectral_analyzer_3.insertItem(19, 'crystal analyser Ge [110]')
        self.ui.spectral_analyzer_3.insertItem(20, 'crystal analyser Ge [111]')
        self.ui.spectral_analyzer_3.insertItem(21, 'crystal analyser Ge [331]')
        self.ui.spectral_analyzer_3.insertItem(22, 'crystal analyser Si [111]')
        self.ui.spectral_analyzer_3.insertItem(23, 'X-ray polychromator')
        self.ui.spectral_analyzer_3.insertItem(24, 'narrow-band filters')
        self.ui.spectral_analyzer_3.insertItem(25, 'no')
        self.ui.spectral_analyzer_3.insertItem(26, 'Other...')
        self.ui.spectral_analyzer_3.setCurrentIndex(0)
        # spectral_analyzer_3 other
        self.ui.spectral_analyzer_3_other = QLineEditClickable(self.ui.tab_7)
        self.ui.spectral_analyzer_3_other.setObjectName("spectral_analyzer_3_other")
        self.ui.gridLayout_19.addWidget(self.ui.spectral_analyzer_3_other, 0, 1, 1, 1)
        self.ui.spectral_analyzer_3_other.setStyleSheet(f'{style_color_add("QLineEdit", "gray")}')
        self.ui.spectral_analyzer_3_other.setPlaceholderText(
            "write your spectral analyzer here if it is not listed on the left")
        # spectral_analyzer_4
        self.ui.spectral_analyzer_4.setStyleSheet(f'{style_color_add("QComboBox", "green")}')
        self.ui.spectral_analyzer_4.insertItem(0, '-- select a spectral analyzer --')
        self.ui.spectral_analyzer_4.insertItem(1, 'Quartz beamsplitter')
        self.ui.spectral_analyzer_4.insertItem(2, 'CaF2 beamsplitter')
        self.ui.spectral_analyzer_4.insertItem(3, 'KBr/Ge beamsplitter')
        self.ui.spectral_analyzer_4.insertItem(4, 'Si beamsplitter')
        self.ui.spectral_analyzer_4.insertItem(5, 'Mylar 20µm beamsplitter')
        self.ui.spectral_analyzer_4.insertItem(6, 'diffraction grating 1200 l/mm - 250nm')
        self.ui.spectral_analyzer_4.insertItem(7, 'diffraction grating 600 l/mm - 400nm')
        self.ui.spectral_analyzer_4.insertItem(8, 'diffraction grating 300 l/mm - 1000nm')
        self.ui.spectral_analyzer_4.insertItem(9, 'diffraction grating 150 l/mm - 4000nm')
        self.ui.spectral_analyzer_4.insertItem(10, 'diffraction grating 3600 l/mm')
        self.ui.spectral_analyzer_4.insertItem(11, 'diffraction grating 1800 l/mm')
        self.ui.spectral_analyzer_4.insertItem(12, 'diffraction grating 1200 l/mm - 1200nm')
        self.ui.spectral_analyzer_4.insertItem(13, 'diffraction grating 600 l/mm - 550nm')
        self.ui.spectral_analyzer_4.insertItem(14, 'diffraction grating 150 l/mm')
        self.ui.spectral_analyzer_4.insertItem(15, 'Ge AOTF 1.5-3 µm')
        self.ui.spectral_analyzer_4.insertItem(16, '2-crystal monochromator Si[111]')
        self.ui.spectral_analyzer_4.insertItem(17, '2-crystal monochromator Si[220]')
        self.ui.spectral_analyzer_4.insertItem(18, '2-crystal monochromator Si[311]')
        self.ui.spectral_analyzer_4.insertItem(19, 'crystal analyser Ge [110]')
        self.ui.spectral_analyzer_4.insertItem(20, 'crystal analyser Ge [111]')
        self.ui.spectral_analyzer_4.insertItem(21, 'crystal analyser Ge [331]')
        self.ui.spectral_analyzer_4.insertItem(22, 'crystal analyser Si [111]')
        self.ui.spectral_analyzer_4.insertItem(23, 'X-ray polychromator')
        self.ui.spectral_analyzer_4.insertItem(24, 'narrow-band filters')
        self.ui.spectral_analyzer_4.insertItem(25, 'no')
        self.ui.spectral_analyzer_4.insertItem(26, 'Other...')
        self.ui.spectral_analyzer_4.setCurrentIndex(0)
        # spectral_analyzer_4 other
        self.ui.spectral_analyzer_4_other = QLineEditClickable(self.ui.tab_7)
        self.ui.spectral_analyzer_4_other.setObjectName("spectral_analyzer_4_other")
        self.ui.gridLayout_20.addWidget(self.ui.spectral_analyzer_4_other, 0, 1, 1, 1)
        self.ui.spectral_analyzer_4_other.setStyleSheet(f'{style_color_add("QLineEdit", "gray")}')
        self.ui.spectral_analyzer_4_other.setPlaceholderText(
            "write your spectral analyzer here if it is not listed on the left")
        # detector_1
        self.ui.detector_1.setStyleSheet(f'{style_color_add("QComboBox", "yellow")}')
        self.ui.detector_1.insertItem(0, '-- select a detector --')
        self.ui.detector_1.insertItem(1, 'Si')
        self.ui.detector_1.insertItem(2, 'Si drift')
        self.ui.detector_1.insertItem(3, 'Ge array')
        self.ui.detector_1.insertItem(4, 'InSb (liq. N2 cooled)')
        self.ui.detector_1.insertItem(5, 'InSb (cryocooler)')
        self.ui.detector_1.insertItem(6, 'InGaAs')
        self.ui.detector_1.insertItem(7, 'PbS')
        self.ui.detector_1.insertItem(8, 'PbSe')
        self.ui.detector_1.insertItem(9, 'MCT (liq. N2 cooled)')
        self.ui.detector_1.insertItem(10, 'DTGS-KBr')
        self.ui.detector_1.insertItem(11, 'DTGS-PE')
        self.ui.detector_1.insertItem(12, 'Ge bolometer (He cooled)')
        self.ui.detector_1.insertItem(13, 'Si bolometer (He cooled)')
        self.ui.detector_1.insertItem(14, 'MCT array (liq. N2 cooled)')
        self.ui.detector_1.insertItem(15, 'CCD')
        self.ui.detector_1.insertItem(16, 'CCD (liq. N2 cooled)')
        self.ui.detector_1.insertItem(17, 'LSO:Tb scintillator')
        self.ui.detector_1.insertItem(18, 'no')
        self.ui.detector_1.insertItem(19, 'Other...')
        self.ui.detector_1.setCurrentIndex(0)
        # detector_1 other
        self.ui.detector_1_other = QLineEditClickable(self.ui.tab_8)
        self.ui.detector_1_other.setObjectName("detector_1_other")
        self.ui.gridLayout_21.addWidget(self.ui.detector_1_other, 0, 1, 1, 1)
        self.ui.detector_1_other.setStyleSheet(f'{style_color_add("QLineEdit", "gray")}')
        self.ui.detector_1_other.setPlaceholderText(
            "write your detector here if it is not listed on the left")
        # detector_2
        self.ui.detector_2.setStyleSheet(f'{style_color_add("QComboBox", "green")}')
        self.ui.detector_2.insertItem(0, '-- select a detector --')
        self.ui.detector_2.insertItem(1, 'Si')
        self.ui.detector_2.insertItem(2, 'Si drift')
        self.ui.detector_2.insertItem(3, 'Ge array')
        self.ui.detector_2.insertItem(4, 'InSb (liq. N2 cooled)')
        self.ui.detector_2.insertItem(5, 'InSb (cryocooler)')
        self.ui.detector_2.insertItem(6, 'InGaAs')
        self.ui.detector_2.insertItem(7, 'PbS')
        self.ui.detector_2.insertItem(8, 'PbSe')
        self.ui.detector_2.insertItem(9, 'MCT (liq. N2 cooled)')
        self.ui.detector_2.insertItem(10, 'DTGS-KBr')
        self.ui.detector_2.insertItem(11, 'DTGS-PE')
        self.ui.detector_2.insertItem(12, 'Ge bolometer (He cooled)')
        self.ui.detector_2.insertItem(13, 'Si bolometer (He cooled)')
        self.ui.detector_2.insertItem(14, 'MCT array (liq. N2 cooled)')
        self.ui.detector_2.insertItem(15, 'CCD')
        self.ui.detector_2.insertItem(16, 'CCD (liq. N2 cooled)')
        self.ui.detector_2.insertItem(17, 'LSO:Tb scintillator')
        self.ui.detector_2.insertItem(18, 'no')
        self.ui.detector_2.insertItem(19, 'Other...')
        self.ui.detector_2.setCurrentIndex(0)
        # detector_2 other
        self.ui.detector_2_other = QLineEditClickable(self.ui.tab_8)
        self.ui.detector_2_other.setObjectName("detector_2_other")
        self.ui.gridLayout_22.addWidget(self.ui.detector_2_other, 0, 1, 1, 1)
        self.ui.detector_2_other.setStyleSheet(f'{style_color_add("QLineEdit", "gray")}')
        self.ui.detector_2_other.setPlaceholderText(
            "write your detector here if it is not listed on the left")
        # detector_3
        self.ui.detector_3.setStyleSheet(f'{style_color_add("QComboBox", "green")}')
        self.ui.detector_3.insertItem(0, '-- select a detector --')
        self.ui.detector_3.insertItem(1, 'Si')
        self.ui.detector_3.insertItem(2, 'Si drift')
        self.ui.detector_3.insertItem(3, 'Ge array')
        self.ui.detector_3.insertItem(4, 'InSb (liq. N2 cooled)')
        self.ui.detector_3.insertItem(5, 'InSb (cryocooler)')
        self.ui.detector_3.insertItem(6, 'InGaAs')
        self.ui.detector_3.insertItem(7, 'PbS')
        self.ui.detector_3.insertItem(8, 'PbSe')
        self.ui.detector_3.insertItem(9, 'MCT (liq. N2 cooled)')
        self.ui.detector_3.insertItem(10, 'DTGS-KBr')
        self.ui.detector_3.insertItem(11, 'DTGS-PE')
        self.ui.detector_3.insertItem(12, 'Ge bolometer (He cooled)')
        self.ui.detector_3.insertItem(13, 'Si bolometer (He cooled)')
        self.ui.detector_3.insertItem(14, 'MCT array (liq. N2 cooled)')
        self.ui.detector_3.insertItem(15, 'CCD')
        self.ui.detector_3.insertItem(16, 'CCD (liq. N2 cooled)')
        self.ui.detector_3.insertItem(17, 'LSO:Tb scintillator')
        self.ui.detector_3.insertItem(18, 'no')
        self.ui.detector_3.insertItem(19, 'Other...')
        self.ui.detector_3.setCurrentIndex(0)
        # detector_3 other
        self.ui.detector_3_other = QLineEditClickable(self.ui.tab_8)
        self.ui.detector_3_other.setObjectName("detector_3_other")
        self.ui.gridLayout_23.addWidget(self.ui.detector_3_other, 0, 1, 1, 1)
        self.ui.detector_3_other.setStyleSheet(f'{style_color_add("QLineEdit", "gray")}')
        self.ui.detector_3_other.setPlaceholderText(
            "write your detector here if it is not listed on the left")
        # documentation_1
        self.ui.documentation_name_1.setStyleSheet(f'{style_color_add("QLineEdit", "green")}')
        self.ui.documentation_file_1.setStyleSheet(f'{style_color_add("QLineEdit", "green")}')
        # documentation_2
        self.ui.documentation_name_2.setStyleSheet(f'{style_color_add("QLineEdit", "green")}')
        self.ui.documentation_file_2.setStyleSheet(f'{style_color_add("QLineEdit", "green")}')
        # documentation_3
        self.ui.documentation_name_3.setStyleSheet(f'{style_color_add("QLineEdit", "green")}')
        self.ui.documentation_file_3.setStyleSheet(f'{style_color_add("QLineEdit", "green")}')
        # pulbication_1
        self.ui.pub_name_1.setStyleSheet(f'{style_color_add("QLineEdit", "green")}')
        self.ui.pub_year_1.setStyleSheet(f'{style_color_add("QSpinBox", "green")}')
        # pulbication_2
        self.ui.pub_name_2.setStyleSheet(f'{style_color_add("QLineEdit", "green")}')
        self.ui.pub_year_2.setStyleSheet(f'{style_color_add("QSpinBox", "green")}')
        # pulbication_3
        self.ui.pub_name_3.setStyleSheet(f'{style_color_add("QLineEdit", "green")}')
        self.ui.pub_year_3.setStyleSheet(f'{style_color_add("QSpinBox", "green")}')
        # link_1
        self.ui.link_name_1.setStyleSheet(f'{style_color_add("QLineEdit", "green")}')
        self.ui.link_url_1.setStyleSheet(f'{style_color_add("QLineEdit", "green")}')
        # link_2
        self.ui.link_name_2.setStyleSheet(f'{style_color_add("QLineEdit", "green")}')
        self.ui.link_url_2.setStyleSheet(f'{style_color_add("QLineEdit", "green")}')
        # link_3
        self.ui.link_name_3.setStyleSheet(f'{style_color_add("QLineEdit", "green")}')
        self.ui.link_url_3.setStyleSheet(f'{style_color_add("QLineEdit", "green")}')
        # fill & submit button
        self.ui.fill_btn.setStyleSheet(f'{button_style}')
        # Menu
        extractAction = QAction("&About", self)
        extractAction.setStatusTip('About The App')
        extractAction.triggered.connect(self.show_about)
        self.statusBar()
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&Help')
        fileMenu.addAction(extractAction)
        # 4.2 SLOT functions connect
        # technique & source_power toggle
        self.ui.technique.currentIndexChanged.connect(self.technique_source_power_toggle)
        # instrument_type
        self.ui.instrument_type.currentIndexChanged.connect(self.instrument_type_other_toggle)
        self.ui.instrument_type_other.clicked.connect(self.instrument_type_toggle)
        # optical_accessory
        self.ui.optical_accessory.currentIndexChanged.connect(self.optical_accessory_other_toggle)
        self.ui.optical_accessory_other.clicked.connect(self.optical_accessory_toggle)
        # source
        self.ui.source.currentIndexChanged.connect(self.source_other_toggle)
        self.ui.source_other.clicked.connect(self.source_toggle)
        # source_wavelength
        self.ui.source_wavelength.currentIndexChanged.connect(self.source_wavelength_other_toggle)
        self.ui.source_wavelength_other.clicked.connect(self.source_wavelength_toggle)
        # spectral_analyzer_1
        self.ui.spectral_analyzer_1.currentIndexChanged.connect(self.spectral_analyzer_1_other_toggle)
        self.ui.spectral_analyzer_1_other.clicked.connect(self.spectral_analyzer_1_toggle)
        # spectral_analyzer_2
        self.ui.spectral_analyzer_2.currentIndexChanged.connect(self.spectral_analyzer_2_other_toggle)
        self.ui.spectral_analyzer_2_other.clicked.connect(self.spectral_analyzer_2_toggle)
        # spectral_analyzer_3
        self.ui.spectral_analyzer_3.currentIndexChanged.connect(self.spectral_analyzer_3_other_toggle)
        self.ui.spectral_analyzer_3_other.clicked.connect(self.spectral_analyzer_3_toggle)
        # spectral_analyzer_4
        self.ui.spectral_analyzer_4.currentIndexChanged.connect(self.spectral_analyzer_4_other_toggle)
        self.ui.spectral_analyzer_4_other.clicked.connect(self.spectral_analyzer_4_toggle)
        # detector_1
        self.ui.detector_1.currentIndexChanged.connect(self.detector_1_other_toggle)
        self.ui.detector_1_other.clicked.connect(self.detector_1_toggle)
        # detector_2
        self.ui.detector_2.currentIndexChanged.connect(self.detector_2_other_toggle)
        self.ui.detector_2_other.clicked.connect(self.detector_2_toggle)
        # detector_3
        self.ui.detector_3.currentIndexChanged.connect(self.detector_3_other_toggle)
        self.ui.detector_3_other.clicked.connect(self.detector_3_toggle)
        # fill XML button
        self.ui.fill_btn.clicked.connect(self.fill_xml_function)

    # 4.3 SLOT functions
    # function to toggle Source power between mandatory and recommended
    def technique_source_power_toggle(self):
        if self.ui.technique.currentIndex() in [14, 15]:
            self.ui.source_power.setStyleSheet(f'{style_color_add("QLineEdit", "yellow")}')
            self.ui.label_source_power.setText('Source power *')
        else:
            self.ui.source_power.setStyleSheet(f'{style_color_add("QLineEdit", "green")}')
            self.ui.label_source_power.setText('Source power')

    # main fill XML function
    def fill_xml_function(self):
        # data reading
        instrument_type = ""
        if self.ui.instrument_type.currentIndex() != 25:
            instrument_type = self.ui.instrument_type.currentText()
        else:
            instrument_type = self.ui.instrument_type_other.text()
        microscopy_imaging = ""
        if self.ui.microscopy_imaging.currentIndex() != 0:
            microscopy_imaging = self.ui.microscopy_imaging.currentText()
        optical_accessory = ""
        if self.ui.optical_accessory.currentIndex() != 17:
            if self.ui.optical_accessory.currentIndex() != 0:
                optical_accessory = self.ui.optical_accessory.currentText()
        else:
            optical_accessory = self.ui.optical_accessory_other.text()
        source = ""
        if self.ui.source.currentIndex() != 20:
            if self.ui.source.currentIndex() != 0:
                source = self.ui.source.currentText()
        else:
            source = self.ui.source_other.text()
        source_wavelength = ""
        if self.ui.source_wavelength.currentIndex() != 22:
            if self.ui.source_wavelength.currentIndex() != 0:
                source_wavelength = self.ui.source_wavelength.currentText()
        else:
            source_wavelength = self.ui.source_wavelength_other.text()
        spectral_analyzer_1 = ""
        if self.ui.spectral_analyzer_1.currentIndex() != 26:
            if self.ui.spectral_analyzer_1.currentIndex() != 0:
                spectral_analyzer_1 = self.ui.spectral_analyzer_1.currentText()
        else:
            spectral_analyzer_1 = self.ui.spectral_analyzer_1_other.text()
        spectral_analyzer_2 = ""
        if self.ui.spectral_analyzer_2.currentIndex() != 26:
            if self.ui.spectral_analyzer_2.currentIndex() != 0:
                spectral_analyzer_2 = self.ui.spectral_analyzer_2.currentText()
        else:
            spectral_analyzer_2 = self.ui.spectral_analyzer_2_other.text()
        spectral_analyzer_3 = ""
        if self.ui.spectral_analyzer_3.currentIndex() != 26:
            if self.ui.spectral_analyzer_3.currentIndex() != 0:
                spectral_analyzer_3 = self.ui.spectral_analyzer_3.currentText()
        else:
            spectral_analyzer_3 = self.ui.spectral_analyzer_3_other.text()
        spectral_analyzer_4 = ""
        if self.ui.spectral_analyzer_4.currentIndex() != 26:
            if self.ui.spectral_analyzer_4.currentIndex() != 0:
                spectral_analyzer_4 = self.ui.spectral_analyzer_4.currentText()
        else:
            spectral_analyzer_4 = self.ui.spectral_analyzer_4_other.text()
        detector_1 = ""
        if self.ui.detector_1.currentIndex() != 19:
            if self.ui.detector_1.currentIndex() != 0:
                detector_1 = self.ui.detector_1.currentText()
        else:
            detector_1 = self.ui.detector_1_other.text()
        detector_2 = ""
        if self.ui.detector_2.currentIndex() != 19:
            if self.ui.detector_2.currentIndex() != 0:
                detector_2 = self.ui.detector_2.currentText()
        else:
            detector_2 = self.ui.detector_2_other.text()
        detector_3 = ""
        if self.ui.detector_3.currentIndex() != 19:
            if self.ui.detector_3.currentIndex() != 0:
                detector_3 = self.ui.detector_3.currentText()
        else:
            detector_3 = self.ui.detector_3_other.text()
        # data verification
        verification_Ok = 1
        message = ""
        focus_element = ""
        reply = "Yes"
        # abd_mandatory
        phrase = " is mandatory! Please, fill this field."
        # name
        if self.ui.name.text().strip() == "":
            verification_Ok = 0
            message = 'Instrument name' + phrase
            focus_element = 'name'
        # type
        elif self.ui.instrument_type.currentIndex() == 0 or \
                (self.ui.instrument_type.currentIndex() == 25 and instrument_type == ""):
            verification_Ok = 0
            message = 'Instrument type' + phrase
            focus_element = 'type'
        # technique
        elif self.ui.technique.currentIndex() == 0:
            verification_Ok = 0
            message = 'Instrument technique' + phrase
            focus_element = 'technique'
        # technique_name
        elif self.ui.technique_name.toPlainText() == "":
            verification_Ok = 0
            message = 'Technique name' + phrase
            focus_element = 'technique_name'
        # lab_current_acronym
        elif self.ui.lab_current_acronym.text() == "":
            verification_Ok = 0
            message = 'Current laboratory acronym' + phrase
            focus_element = 'lab_current_acronym'
        # element abs_mandatory together
        # previous labs
        elif self.ui.lab_previous_1_comment.toPlainText() != "" and self.ui.lab_previous_1_acronym.text() == "":
            verification_Ok = 0
            message = 'The previous laboratory acronym is mandatory if its comment is filled in!\n' \
                      'Please, fill in the acronym of the laboratory or empty its comment.'
            focus_element = 'lab_previous_1_acronym'
        elif self.ui.lab_previous_2_comment.toPlainText() != "" and self.ui.lab_previous_2_acronym.text() == "":
            verification_Ok = 0
            message = 'The previous laboratory acronym is mandatory if its comment is filled in!\n' \
                      'Please, fill in the acronym of the laboratory or empty its comment.'
            focus_element = 'lab_previous_2_acronym'
        # documentations
        elif (self.ui.documentation_name_1.text() == "" and self.ui.documentation_file_1.text() != "") or (
                self.ui.documentation_name_1.text() != "" and self.ui.documentation_file_1.text() == ""):
            verification_Ok = 0
            message = 'Documentation name and filename are mandatory together!\n' \
                      'Please, fill in or empty both fields.'
            if self.ui.documentation_name_1.text() == "":
                focus_element = 'documentation_name_1'
            else:
                focus_element = 'documentation_file_1'
        elif (self.ui.documentation_name_2.text() == "" and self.ui.documentation_file_2.text() != "") or (
                self.ui.documentation_name_2.text() != "" and self.ui.documentation_file_2.text() == ""):
            verification_Ok = 0
            message = 'Documentation name and filename are mandatory together!\n' \
                      'Please, fill in or empty both fields.'
            if self.ui.documentation_name_2.text() == "":
                focus_element = 'documentation_name_2'
            else:
                focus_element = 'documentation_file_2'
        elif (self.ui.documentation_name_3.text() == "" and self.ui.documentation_file_3.text() != "") or (
                self.ui.documentation_name_3.text() != "" and self.ui.documentation_file_3.text() == ""):
            verification_Ok = 0
            message = 'Documentation name and filename are mandatory together!\n' \
                      'Please, fill in or empty both fields.'
            if self.ui.documentation_name_3.text() == "":
                focus_element = 'documentation_name_3'
            else:
                focus_element = 'documentation_file_3'
        # links
        elif (self.ui.link_name_1.text() == "" and self.ui.link_url_1.text() != "") or (
                self.ui.link_name_1.text() != "" and self.ui.link_url_1.text() == ""):
            verification_Ok = 0
            message = 'Link name and URL are mandatory together!\n' \
                      'Please, fill in or empty both fields.'
            if self.ui.link_name_1.text() == "":
                focus_element = 'link_name_1'
            else:
                focus_element = 'link_url_1'
        elif (self.ui.link_name_2.text() == "" and self.ui.link_url_2.text() != "") or (
                self.ui.link_name_2.text() != "" and self.ui.link_url_2.text() == ""):
            verification_Ok = 0
            message = 'Link name and URL are mandatory together!\n' \
                      'Please, fill in or empty both fields.'
            if self.ui.link_name_2.text() == "":
                focus_element = 'link_name_2'
            else:
                focus_element = 'link_url_2'
        elif (self.ui.link_name_3.text() == "" and self.ui.link_url_3.text() != "") or (
                self.ui.link_name_3.text() != "" and self.ui.link_url_3.text() == ""):
            verification_Ok = 0
            message = 'Link name and URL are mandatory together!\n' \
                      'Please, fill in or empty both fields.'
            if self.ui.link_name_3.text() == "":
                focus_element = 'link_name_3'
            else:
                focus_element = 'link_url_3'
        # mandatory
        else:
            # microscopy_imaging
            if self.ui.microscopy_imaging.currentIndex() == 0:
                reply = QMessageBox.question(self, 'Message',
                                             "Are you sure to leave microscopy imaging empty?", QMessageBox.Yes |
                                             QMessageBox.No, QMessageBox.Yes)
                if reply == QMessageBox.No:
                    reply = "No"
                    verification_Ok = 0
                    self.ui.tabWidget.setCurrentIndex(2)
                    self.ui.microscopy_imaging.setFocus()
                else:
                    reply = "Yes"
            # source
            if reply == "Yes" and self.ui.source.currentIndex() == 0:
                reply = QMessageBox.question(self, 'Message',
                                             "Are you sure to leave source empty?", QMessageBox.Yes |
                                             QMessageBox.No, QMessageBox.Yes)
                if reply == QMessageBox.No:
                    reply = "No"
                    verification_Ok = 0
                    self.ui.tabWidget.setCurrentIndex(2)
                    self.ui.source.setFocus()
                else:
                    reply = "Yes"
            # source_wavelength
            if reply == "Yes" and self.ui.source_wavelength.currentIndex() == 0:
                reply = QMessageBox.question(self, 'Message',
                                             "Are you sure to leave source wavelength empty?", QMessageBox.Yes |
                                             QMessageBox.No, QMessageBox.Yes)
                if reply == QMessageBox.No:
                    reply = "No"
                    verification_Ok = 0
                    self.ui.tabWidget.setCurrentIndex(2)
                    self.ui.source_wavelength.setFocus()
                else:
                    reply = "Yes"
            # source_power
            if reply == "Yes" and self.ui.technique.currentText() in ['Raman scattering',
                                                                      'fluorescence emission'] and self.ui.source_power.text() == "":
                reply = QMessageBox.question(self, 'Message',
                                             "Are you sure to leave source power empty?", QMessageBox.Yes |
                                             QMessageBox.No, QMessageBox.Yes)
                if reply == QMessageBox.No:
                    reply = "No"
                    verification_Ok = 0
                    self.ui.tabWidget.setCurrentIndex(2)
                    self.ui.source_power.setFocus()
                else:
                    reply = "Yes"
            # spectral_analyzers
            if reply == "Yes" and (
                    self.ui.spectral_analyzer_1.currentIndex() == 0 and self.ui.spectral_analyzer_2.currentIndex() == 0 and self.ui.spectral_analyzer_3.currentIndex() == 0 and self.ui.spectral_analyzer_4.currentIndex() == 0):
                reply = QMessageBox.question(self, 'Message',
                                             "Are you sure to leave no information about spectral analyzers?",
                                             QMessageBox.Yes |
                                             QMessageBox.No, QMessageBox.Yes)
                if reply == QMessageBox.No:
                    reply = "No"
                    verification_Ok = 0
                    self.ui.tabWidget.setCurrentIndex(3)
                    self.ui.spectral_analyzer_1.setFocus()
                else:
                    reply = "Yes"
            # detectors
            if reply == "Yes" and (
                    self.ui.detector_1.currentIndex() == 0 and self.ui.detector_2.currentIndex() == 0 and self.ui.detector_3.currentIndex() == 0):
                reply = QMessageBox.question(self, 'Message',
                                             "Are you sure to leave no information about detectors?",
                                             QMessageBox.Yes |
                                             QMessageBox.No, QMessageBox.Yes)
                if reply == QMessageBox.No:
                    reply = "No"
                    verification_Ok = 0
                    self.ui.tabWidget.setCurrentIndex(4)
                    self.ui.detector_1.setFocus()
                else:
                    reply = "Yes"

        # fill data or error message
        if verification_Ok == 1:
            str_to_upload = xml_parse_and_fill(template,
                                               self.ui.lab_current_acronym.text().strip(),
                                               self.ui.lab_current_comment.toPlainText(),
                                               self.ui.lab_previous_1_acronym.text().strip(),
                                               self.ui.lab_previous_1_comment.toPlainText(),
                                               self.ui.lab_previous_2_acronym.text().strip(),
                                               self.ui.lab_previous_2_comment.toPlainText(),
                                               instrument_type,
                                               self.ui.name.text().strip(),
                                               self.ui.technique.currentText(),
                                               self.ui.technique_name.toPlainText(),
                                               microscopy_imaging,
                                               optical_accessory,
                                               source,
                                               source_wavelength,
                                               self.ui.source_power.text(),
                                               spectral_analyzer_1,
                                               spectral_analyzer_2,
                                               spectral_analyzer_3,
                                               spectral_analyzer_4,
                                               detector_1,
                                               detector_2,
                                               detector_3,
                                               self.ui.documentation_name_1.text(),
                                               self.ui.documentation_file_1.text(),
                                               self.ui.documentation_name_2.text(),
                                               self.ui.documentation_file_2.text(),
                                               self.ui.documentation_name_3.text(),
                                               self.ui.documentation_file_3.text(),
                                               self.ui.link_name_1.text(),
                                               self.ui.link_url_1.text(),
                                               self.ui.link_name_2.text(),
                                               self.ui.link_url_2.text(),
                                               self.ui.link_name_3.text(),
                                               self.ui.link_url_3.text(),
                                               self.ui.pub_name_1.text(),
                                               self.ui.pub_year_1.value(),
                                               self.ui.pub_name_2.text(),
                                               self.ui.pub_year_2.value(),
                                               self.ui.pub_name_3.text(),
                                               self.ui.pub_year_3.value(),
                                               self.ui.comments.toPlainText())
            options = QFileDialog.Options()
            file_name_str = "INSTRU_" + accent_letters_replace(self.ui.name.text().strip()).upper().replace("-",
                                                                                                            "_").replace(
                " ", "_") + "_" + accent_letters_replace(self.ui.technique.currentText().strip()).upper().replace(
                "-", "_").replace(" ", "_") + "_" + accent_letters_replace(
                self.ui.lab_current_acronym.text().strip()).upper().replace("-", "_").replace(" ", "_")
            file_name, _ = QFileDialog.getSaveFileName(self, "Save File", file_name_str,
                                                       "Text Files (*.xml)", options=options)
            if file_name:
                with open(file_name, 'wb') as file_output:
                    file_output.write(str_to_upload)
                self.dialog_ok('The XML was saved!')
        elif message != "":
            if focus_element == 'name':
                self.ui.tabWidget.setCurrentIndex(0)
                self.ui.name.setFocus()
            elif focus_element == 'type':
                self.ui.tabWidget.setCurrentIndex(0)
                self.ui.instrument_type.setFocus()
            elif focus_element == 'technique':
                self.ui.tabWidget.setCurrentIndex(0)
                self.ui.technique.setFocus()
            elif focus_element == 'technique_name':
                self.ui.tabWidget.setCurrentIndex(0)
                self.ui.technique_name.setFocus()
            elif focus_element == 'lab_current_acronym':
                self.ui.tabWidget.setCurrentIndex(1)
                self.ui.lab_current_acronym.setFocus()
            elif focus_element == 'lab_previous_1_acronym':
                self.ui.tabWidget.setCurrentIndex(1)
                self.ui.lab_previous_1_acronym.setFocus()
            elif focus_element == 'lab_previous_2_acronym':
                self.ui.tabWidget.setCurrentIndex(1)
                self.ui.lab_previous_2_acronym.setFocus()
            elif focus_element == 'documentation_name_1':
                self.ui.tabWidget.setCurrentIndex(4)
                self.ui.documentation_name_1.setFocus()
            elif focus_element == 'documentation_file_1':
                self.ui.tabWidget.setCurrentIndex(4)
                self.ui.documentation_file_1.setFocus()
            elif focus_element == 'documentation_name_2':
                self.ui.tabWidget.setCurrentIndex(4)
                self.ui.documentation_name_2.setFocus()
            elif focus_element == 'documentation_file_2':
                self.ui.tabWidget.setCurrentIndex(4)
                self.ui.documentation_file_2.setFocus()
            elif focus_element == 'documentation_name_3':
                self.ui.tabWidget.setCurrentIndex(4)
                self.ui.documentation_name_3.setFocus()
            elif focus_element == 'documentation_file_3':
                self.ui.tabWidget.setCurrentIndex(4)
                self.ui.documentation_file_3.setFocus()
            elif focus_element == 'link_name_1':
                self.ui.tabWidget.setCurrentIndex(6)
                self.ui.link_name_1.setFocus()
            elif focus_element == 'link_url_1':
                self.ui.tabWidget.setCurrentIndex(6)
                self.ui.link_url_1.setFocus()
            elif focus_element == 'link_name_2':
                self.ui.tabWidget.setCurrentIndex(6)
                self.ui.link_name_2.setFocus()
            elif focus_element == 'link_url_2':
                self.ui.tabWidget.setCurrentIndex(6)
                self.ui.link_url_2.setFocus()
            elif focus_element == 'link_name_3':
                self.ui.tabWidget.setCurrentIndex(6)
                self.ui.link_name_3.setFocus()
            elif focus_element == 'link_url_3':
                self.ui.tabWidget.setCurrentIndex(6)
                self.ui.link_url_3.setFocus()
            self.dialog_critical(message)

    # functions for FreeList functionality
    def instrument_type_other_toggle(self):
        if self.ui.instrument_type.currentIndex() == 25:
            self.ui.instrument_type_other.setStyleSheet(f'{style_color_add("QLineEdit", "red")}')
        else:
            self.ui.instrument_type_other.setStyleSheet(f'{style_color_add("QLineEdit", "gray")}')
            self.ui.instrument_type_other.setText("")

    def instrument_type_toggle(self):
        self.ui.instrument_type.setCurrentIndex(25)
        self.ui.instrument_type_other.setFocus()

    def optical_accessory_other_toggle(self):
        if self.ui.optical_accessory.currentIndex() == 17:
            self.ui.optical_accessory_other.setStyleSheet(f'{style_color_add("QLineEdit", "green")}')
        else:
            self.ui.optical_accessory_other.setStyleSheet(f'{style_color_add("QLineEdit", "gray")}')
            self.ui.optical_accessory_other.setText("")

    def optical_accessory_toggle(self):
        self.ui.optical_accessory.setCurrentIndex(17)
        self.ui.optical_accessory_other.setFocus()

    def source_other_toggle(self):
        if self.ui.source.currentIndex() == 20:
            self.ui.source_other.setStyleSheet(f'{style_color_add("QLineEdit", "yellow")}')
        else:
            self.ui.source_other.setStyleSheet(f'{style_color_add("QLineEdit", "gray")}')
            self.ui.source_other.setText("")

    def source_toggle(self):
        self.ui.source.setCurrentIndex(20)
        self.ui.source_other.setFocus()

    def source_wavelength_other_toggle(self):
        if self.ui.source_wavelength.currentIndex() == 22:
            self.ui.source_wavelength_other.setStyleSheet(f'{style_color_add("QLineEdit", "yellow")}')
        else:
            self.ui.source_wavelength_other.setStyleSheet(f'{style_color_add("QLineEdit", "gray")}')
            self.ui.source_wavelength_other.setText("")

    def source_wavelength_toggle(self):
        self.ui.source_wavelength.setCurrentIndex(22)
        self.ui.source_wavelength_other.setFocus()

    def spectral_analyzer_1_other_toggle(self):
        if self.ui.spectral_analyzer_1.currentIndex() == 26:
            self.ui.spectral_analyzer_1_other.setStyleSheet(f'{style_color_add("QLineEdit", "yellow")}')
        else:
            self.ui.spectral_analyzer_1_other.setStyleSheet(f'{style_color_add("QLineEdit", "gray")}')
            self.ui.spectral_analyzer_1_other.setText("")

    def spectral_analyzer_1_toggle(self):
        self.ui.spectral_analyzer_1.setCurrentIndex(26)
        self.ui.spectral_analyzer_1_other.setFocus()

    def spectral_analyzer_2_other_toggle(self):
        if self.ui.spectral_analyzer_2.currentIndex() == 26:
            self.ui.spectral_analyzer_2_other.setStyleSheet(f'{style_color_add("QLineEdit", "green")}')
        else:
            self.ui.spectral_analyzer_2_other.setStyleSheet(f'{style_color_add("QLineEdit", "gray")}')
            self.ui.spectral_analyzer_2_other.setText("")

    def spectral_analyzer_2_toggle(self):
        self.ui.spectral_analyzer_2.setCurrentIndex(26)
        self.ui.spectral_analyzer_2_other.setFocus()

    def spectral_analyzer_3_other_toggle(self):
        if self.ui.spectral_analyzer_3.currentIndex() == 26:
            self.ui.spectral_analyzer_3_other.setStyleSheet(f'{style_color_add("QLineEdit", "green")}')
        else:
            self.ui.spectral_analyzer_3_other.setStyleSheet(f'{style_color_add("QLineEdit", "gray")}')
            self.ui.spectral_analyzer_3_other.setText("")

    def spectral_analyzer_3_toggle(self):
        self.ui.spectral_analyzer_3.setCurrentIndex(26)
        self.ui.spectral_analyzer_3_other.setFocus()

    def spectral_analyzer_4_other_toggle(self):
        if self.ui.spectral_analyzer_4.currentIndex() == 26:
            self.ui.spectral_analyzer_4_other.setStyleSheet(f'{style_color_add("QLineEdit", "green")}')
        else:
            self.ui.spectral_analyzer_4_other.setStyleSheet(f'{style_color_add("QLineEdit", "gray")}')
            self.ui.spectral_analyzer_4_other.setText("")

    def spectral_analyzer_4_toggle(self):
        self.ui.spectral_analyzer_4.setCurrentIndex(26)
        self.ui.spectral_analyzer_4_other.setFocus()

    def detector_1_other_toggle(self):
        if self.ui.detector_1.currentIndex() == 19:
            self.ui.detector_1_other.setStyleSheet(f'{style_color_add("QLineEdit", "yellow")}')
        else:
            self.ui.detector_1_other.setStyleSheet(f'{style_color_add("QLineEdit", "gray")}')
            self.ui.detector_1_other.setText("")

    def detector_1_toggle(self):
        self.ui.detector_1.setCurrentIndex(19)
        self.ui.detector_1_other.setFocus()

    def detector_2_other_toggle(self):
        if self.ui.detector_2.currentIndex() == 19:
            self.ui.detector_2_other.setStyleSheet(f'{style_color_add("QLineEdit", "green")}')
        else:
            self.ui.detector_2_other.setStyleSheet(f'{style_color_add("QLineEdit", "gray")}')
            self.ui.detector_2_other.setText("")

    def detector_2_toggle(self):
        self.ui.detector_2.setCurrentIndex(19)
        self.ui.detector_2_other.setFocus()

    def detector_3_other_toggle(self):
        if self.ui.detector_3.currentIndex() == 19:
            self.ui.detector_3_other.setStyleSheet(f'{style_color_add("QLineEdit", "green")}')
        else:
            self.ui.detector_3_other.setStyleSheet(f'{style_color_add("QLineEdit", "gray")}')
            self.ui.detector_3_other.setText("")

    def detector_3_toggle(self):
        self.ui.detector_3.setCurrentIndex(19)
        self.ui.detector_3_other.setFocus()

    # dialog windows
    def dialog_ok(self, s):
        dlg = QMessageBox(self)
        dlg.setWindowTitle('Info')
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Information)
        dlg.show()

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setWindowTitle('Error!')
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def show_about(self):
        self.dialog_ok(f"<b>XML generator: instrument</b> v{__version__}"
                       f"<p>Copyright: {__copyright__}</p>"
                       f"<p><a href='{__GitHub_repos__}'>GitHub repository</a> (program code and more information)</p>"
                       f"<p>Created by Gorbacheva Maria ({__author_mail__})</p>"
                       "<p>Scientific base by Bernard Schmitt, IPAG (bernard.schmitt@univ-grenoble-alpes.fr)</p>"
                       f"<p>For any questions and bug reports, please, mail at {__bug_support_mail__}</p>"
                       "<p>In case of a bug, please report it and specify your operating system, "
                       "provide a detailed description of the problem with screenshots "
                       "and the files used and produced, if possible. Your contribution matters to make it better!</p>")


# 5 MAIN WINDOW class emulation
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = XMLGeneratorMainW()
    win.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
    win.show()
    sys.exit(app.exec())
# coding: utf-8

"""

This script is the core script of the XMLGenerator_instrument program.
Its aim is to fill the XML instrument template (for SSHADE.eu database) with build-in variables.

To run it in command line one must go to section 6 and
* change INPUT parameters inside 'def demo_function()'
* uncomment the call of 'demo_function()'
This will result in filling of the XML instrument template.
And the result will be safe in an XML file in the same folder (as this scritp).

This script has 6 parts (=sections):
1. IMPORTS with all imported packages that we will need
2. GLOBALS with all global variables used in this script
3. accessories FUNCTIONS which used in further sections
    3.1 replacing special character (used to create UIDs & filenames)
    3.2 functions to work with XML
    3.3 function to verify the input data
4 MAIN FUNCTION which parses XML template and fill it
5 MAIN VERIFICATIONS
6 DEMO test function prefilled with "FULL" data set

"""

# 1 IMPORTS
from lxml import etree


# 2 GLOBALS
# XML instrument template in string (without \n, only one space, and '' instead of "")
template = "<?xml version='1.0' encoding='UTF-8'?><!-- Data type : Instrument Specific notes : - General notes : - Most of the tags are optional, you can remove the really unnecessary ones. - Tags marked as 'multiple' can be copied (with its block of sub-tag, up to the ending tag) if needed. - all blocs marked 'OPTION' can be fully removed if not needed (now or in the future) - **ABS MANDATORY / ABS COMPULSORY**: a value need to be absolutely provided, no way to escape! (SSHADE will not function properly if absent). - **MANDATORY / COMPULSORY**: very important values for the search of the data. If the value (txt or numeric) of one tag is not known (or irrelevant in your case), then put 'NULL' and write a comment to keep track of the missing value. Remove comment when value is added. - **MANDATORY / COMPULSORY only for ...**: when a value is optionally MANDATORY the condition is written. - 'LINK to existing UID' (unique identifier): references to another table in SSHADE. You have to reconstruct (easy for some: rule is in comment) or found this existing UID in the database beforehand (use 'Provider/Full Search' menu in SSHADE). - 'UID to CREATE': you need to create this UID using their specific rules of creation that are explained in their attached comment. Use only alphanumeric characters and '_'. - For UID you can use only alpha-numeric characters and the following: '_', '-' - Enumeration type ('Enum' or 'OpenEnum') must contain one single item from the list given in brackets {}. - use a CDATA tag when a value contains at least one special character (ie: &, >, <,...). Example: <![CDATA[AT&T]]> for AT&T - The data format is noted beetween [] and is 'ascii' when not specified. Ex: [Float], [Integer]. For [float] 2 formats are possible: decimal (123.456) or scientific (1.234e-56) - when no numerical format or Enum is specified, it is free text but limited to 256 characters. Only those noted [blob] have no size limitation. - to import data for the first time you have to set <import_mode>='first import'. To correct data you have to change it to 'correction'. - when a <filename> is given, then the file should be ziped with this xml file for import. --><import type='instrument' ssdm_version='0.9.0' xmlns='http://sshade.eu/schema/import' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:schemaLocation='http://sshade.eu/schema/import http://sshade.eu/schema/import-0.9.xsd'><instrument><!-- multiple --><import_mode>first import</import_mode><!-- **ABS MANDATORY** Mode of import of the 'instrument' data. Enum: {first import, ignore, draft, no change, correction} --><uid>INSTRU_</uid> <!-- **ABS MANDATORY to CREATE** Unique identifier code given to the instrument+technique set: It should be in fully in UPPERCASE of the style ‘INSTRU_InstrumentName_Technique_LabAcronym’ where ‘InstrumentName’ is the instrument name, ‘Technique’ is a short but unambiguous version of the technique name, and ‘LabAcronym’ is the acronym of the laboratory where it is situated --><!-- INSTRUMENT LOCATION --><manager_databases> <!-- **ABS MANDATORY at least one** --><database_uid>DB_</database_uid><!-- multiple --> <!-- LINK to the existing UID of the database which manages this instrument information [‘DB_DatabaseAcronym’] --></manager_databases><laboratories> <!-- **ABS MANDATORY at least one** --><laboratory current='true'><!-- multiple --> <!-- FlagEnum {yes, no} or {true, false} --><uid>LAB_</uid> <!-- **ABS MANDATORY** LINK to the UID of the laboratory where the instrument is (or was) located [‘LAB_LabAcronym’] --><comments><![CDATA[]]></comments> <!-- Additional information: years, where it was before ... [Blob] --></laboratory></laboratories><!-- INSTRUMENT DESCRIPTION --><type></type> <!-- **ABS MANDATORY** Type of used instrument. FreeList: {FTIR spectrometer, grating spectrometer, AOTF spectrometer, CRDS spectrometer, laser diode spectrometer, SWIFT spectrometer, µSPOC spectrometer, narrow-band filters spectrometer, grating imaging spectrometer, grating hyperspectral imaging system, ImSPOC imaging spectrometer, narrow-band filters imager, spectro-gonio radiometer, Raman spectrometer, Raman micro-spectrometer, FTIR micro-spectrometer, spectrofluorometer, ellipsometer, X-ray absorption spectrometer, gamma-ray spectrometer, Mossbauer spectrometer, vector network analyzer, radiative transfer simulation, quantum mechanical simulation, …} --><name></name> <!-- **ABS MANDATORY** Specific name and model of the instrument --><technique></technique> <!-- **ABS MANDATORY** Instrumental technique. OpenEnum: {transmission, reflection-absorption, ATReflection, specular reflection, ellipsometry, bidirectional reflection, biconical reflection, confocal reflection, diffuse reflection, directional-hemispheric reflection, hemispheric-directional reflection, scattering, thermal emission, Raman scattering, fluorescence emission, gamma emission, Mossbauer absorption, permittivity, time-domain, dual polarisation interferometry} --><technique_name></technique_name> <!-- **ABS MANDATORY** Name describing the combination of instrument, technique and spectral range used -->	<!-- INSTRUMENT TECHNIQUES DESCRIPTION --><microscopy_imaging></microscopy_imaging> <!-- **MANDATORY** Tell if the instrumental technique use a microscope, a micro-imager, an imager or not. Enum: {macroscopic, microscopy, linear scan, linear micro-scan, imaging, micro-imaging} --><optical_accessory></optical_accessory> <!-- Type of additional optical accessory installed in the instrument. Free list: {Ge ATR crystal, KRS-5 crystal, ZnSe ATR crystal, Si ATR crystal, biconical diffuse reflectance, diffuse reflectance (DRIFTS), multipass cell, integrating sphere, absolute specular reflectance, blue filter, red filter, linear polarizer, Vis confocal microscope in reflection, IR microscope in transmission, IR microscope in reflection, IR microscope in ATR, …} --> <source></source> <!-- **MANDATORY** Light source type of the instrument. Free list: {Tungsten/Halogen lamp, Globar-IR, Hydrogen arc lamp, Deuterium arc lamp, Hg lamp, Xe arc lamp, He-Ne laser, laser diode, Ar+/Kr+ laser, Ar+ laser, frequency-doubled Ar+ laser, Nd:YAG laser, frequency-doubled Nd:YAG laser, pulsed laser, synchrotron - bending magnet, synchrotron - undulator, synchrotron - wiggler, Sun, no, ,…} --><source_wavelength></source_wavelength> <!-- **MANDATORY** General spectral range, precise wavelength (laser), or wavelength range (laser diode) of the source. Free list: {gamma, hard X, soft X, EUV, VUV-UV, Vis-NIR, UV-NIR, MIR, FIR, MIR-FIR, submm, mm, 90GHz, 6050-6900 cm-1, 244 nm, 457.9 nm, 488 nm, 514.5 nm, 532 nm, 632.8 nm, 647.1 nm,…} --><source_power></source_power> <!-- **MANDATORY only for Raman and fluorescence techniques** Power of the source [give the unit: W, W/cm2, ...] --><spectral_analyzers><!-- **MANDATORY at least one** --><spectral_analyzer></spectral_analyzer><!-- multiple --> <!-- **MANDATORY** Type of spectral analyzer of the instrument. Free list: {Quartz beamsplitter, CaF2 beamsplitter, KBr/Ge beamsplitter, Si beamsplitter, Mylar 20µm beamsplitter, diffraction grating 1200 l/mm - 250nm, diffraction grating 600 l/mm - 400nm, diffraction grating 300 l/mm - 1000nm, diffraction grating 150 l/mm - 4000nm, diffraction grating 3600 l/mm, diffraction grating 1800 l/mm, diffraction grating 1200 l/mm - 1200nm, diffraction grating 600 l/mm - 550nm, diffraction grating 150 l/mm, Ge AOTF 1.5-3 µm, 2-crystal monochromator Si[111], 2-crystal monochromator Si[220], 2-crystal monochromator Si[311], crystal analyser Ge [110], crystal analyser Ge [111], crystal analyser Ge [331], crystal analyser Si [111], X-ray polychromator, narrow-band filters, no, …} --></spectral_analyzers><detectors><!-- **MANDATORY at least one** --><detector></detector><!-- multiple --> <!-- **MANDATORY** Detector type of the instrument: Free list: {Si, Si drift, Ge array, InSb (liq. N2 cooled), InSb (cryocooler), InGaAs, PbS, PbSe, MCT (liq. N2 cooled), DTGS-KBr, DTGS-PE, Ge bolometer (He cooled), Si bolometer (He cooled), MCT array (liq. N2 cooled), CCD, CCD (liq. N2 cooled), LSO:Tb scintillator, other, no, …} --></detectors> <comments><![CDATA[]]></comments> <!-- Additional information on the instrument and techniques (special configuration, use of cryogenic/thermal/vacuum cell ...) or simulation model [Blob] --><!-- INSTRUMENT: REFERENCES --><documentations> <!-- **OPTION** --> <!-- Documentations describing the instrument and its associated techniques and performances, i.e. all parameters described in this 'instrument' part --><documentation><!-- multiple --><name><![CDATA[]]></name> <!-- Name of the documentation --><filename><![CDATA[]]></filename> <!-- File name of the documentation (pdf file). This image file should be zipped with the xml file --></documentation></documentations><links> <!-- **OPTION** --><!-- Link(s) to web page(s) describing the instrument, technique and/or the cells used, or the simulation model used --><link><!-- multiple --> <name><![CDATA[]]></name> <!-- Name of the web page(s) --><url><![CDATA[]]></url> <!-- URL address (avoid non-perennial commercial URL) --></link></links><publications> <!-- **OPTION** --> <!-- List of publication(s) describing instrument, technique and/or the cells used, or the simulation model used --><publication_uid></publication_uid><!-- multiple --> <!-- LINK to the existing UID of the publication [‘‘PUBLI_FirstAuthorName_Year(Letter)’] --></publications></instrument>	</import>"


# 3 accessories FUNCTIONS


# 3.1 replacing special character: non-latin letters & HTML special symbols
def accent_letters_replace(string_var):
    # A
    string_var = string_var.replace("À", "A")
    string_var = string_var.replace("Á", "A")
    string_var = string_var.replace("Â", "A")
    string_var = string_var.replace("Ã", "A")
    string_var = string_var.replace("Ä", "A")
    string_var = string_var.replace("Å", "A")
    string_var = string_var.replace("Æ", "Ae")
    # C
    string_var = string_var.replace("Ç", "C")
    # D
    string_var = string_var.replace("Ð", "D")
    # E
    string_var = string_var.replace("È", "E")
    string_var = string_var.replace("É", "E")
    string_var = string_var.replace("Ê", "E")
    string_var = string_var.replace("Ë", "E")
    # I
    string_var = string_var.replace("Ì", "I")
    string_var = string_var.replace("Í", "I")
    string_var = string_var.replace("Î", "I")
    string_var = string_var.replace("Ï", "I")
    # N
    string_var = string_var.replace("Ñ", "N")
    # O
    string_var = string_var.replace("Ò", "O")
    string_var = string_var.replace("Ó", "O")
    string_var = string_var.replace("Ô", "O")
    string_var = string_var.replace("Õ", "O")
    string_var = string_var.replace("Ö", "O")
    string_var = string_var.replace("Ø", "O")
    # T
    string_var = string_var.replace("Þ", "th")
    # U
    string_var = string_var.replace("Ù", "U")
    string_var = string_var.replace("Ú", "U")
    string_var = string_var.replace("Û", "U")
    string_var = string_var.replace("Ü", "U")
    # Y
    string_var = string_var.replace("Ý", "Y")
    # a
    string_var = string_var.replace("à", "a")
    string_var = string_var.replace("á", "a")
    string_var = string_var.replace("â", "a")
    string_var = string_var.replace("ã", "a")
    string_var = string_var.replace("ä", "a")
    string_var = string_var.replace("å", "a")
    string_var = string_var.replace("æ", "ae")
    # c
    string_var = string_var.replace("ç", "c")
    # d
    string_var = string_var.replace("ð", "d")
    # e
    string_var = string_var.replace("è", "e")
    string_var = string_var.replace("é", "e")
    string_var = string_var.replace("ê", "e")
    string_var = string_var.replace("ë", "e")
    # i
    string_var = string_var.replace("ì", "i")
    string_var = string_var.replace("í", "i")
    string_var = string_var.replace("î", "i")
    string_var = string_var.replace("ï", "i")
    # n
    string_var = string_var.replace("ñ", "n")
    # o
    string_var = string_var.replace("ò", "o")
    string_var = string_var.replace("ó", "o")
    string_var = string_var.replace("ô", "o")
    string_var = string_var.replace("õ", "o")
    string_var = string_var.replace("ö", "o")
    string_var = string_var.replace("ø", "o")
    # t
    string_var = string_var.replace("þ", "th")
    # s
    string_var = string_var.replace("ß", "ss")
    # u
    string_var = string_var.replace("ù", "u")
    string_var = string_var.replace("ú", "u")
    string_var = string_var.replace("û", "u")
    string_var = string_var.replace("û", "u")
    string_var = string_var.replace("ü", "u")
    # y
    string_var = string_var.replace("ý", "y")
    string_var = string_var.replace("ÿ", "y")
    # special chars
    string_var = string_var.replace(">", "")
    string_var = string_var.replace("<", "")
    string_var = string_var.replace("\\", "")
    string_var = string_var.replace("/", "")
    string_var = string_var.replace("'", "")
    string_var = string_var.replace('"', "")
    return string_var


# 3.2 functions to work (fill, create, add elements) with XML
# function to fill a child element with a given value
def fill_child_action(child_element, its_value):
    child_element.clear()
    if accent_letters_replace(its_value) == its_value:
        child_element.text = its_value
    else:
        child_element.text = etree.CDATA(its_value)


# function to add a comment
def add_comment(child_element, comment_text):
    comment_verify = etree.Comment(comment_text)
    child_element.insert(0, comment_verify)


# function to add a previous lab
def add_lab_previous(child, lab_previous_acronym, lab_previous_comment):
    child_element = etree.SubElement(child, "laboratory")
    child_element.set("current", "false")
    sub_child_element = etree.SubElement(child_element, "uid")
    sub_child_element.text = "LAB_" + accent_letters_replace(lab_previous_acronym.strip())
    add_comment(sub_child_element, " %%% TO VERIFY ")
    sub_child_element = etree.SubElement(child_element, "comments")
    if accent_letters_replace(lab_previous_comment) != lab_previous_comment:
        sub_child_element.text = etree.CDATA(lab_previous_comment)
    else:
        sub_child_element.text = lab_previous_comment


# function to add a spectral analyzer
def add_spectral_analyzer(already_one_filled, child, spectral_analyzer):
    if already_one_filled:
        child_element = etree.SubElement(child, "spectral_analyzer")
        if accent_letters_replace(spectral_analyzer) == spectral_analyzer:
            child_element.text = spectral_analyzer
        else:
            child_element.text = etree.CDATA(spectral_analyzer)
    else:
        for item in child:
            if item.tag == "{http://sshade.eu/schema/import}spectral_analyzer":
                fill_child_action(item, spectral_analyzer)
    return 1


# function to add a detector
def add_detector(already_one_filled, child, detector):
    if already_one_filled:
        child_element = etree.SubElement(child, "detector")
        if accent_letters_replace(detector) == detector:
            child_element.text = detector
        else:
            child_element.text = etree.CDATA(detector)
    else:
        for item in child:
            if item.tag == "{http://sshade.eu/schema/import}detector":
                fill_child_action(item, detector)
    return 1


# function to add a documentation
def add_documentation(already_one_filled, child, documentation_name, documentation_file):
    if already_one_filled:
        child_element = etree.SubElement(child, "documentation")
        sub_child_element = etree.SubElement(child_element, "name")
        if accent_letters_replace(documentation_name) == documentation_name:
            sub_child_element.text = documentation_name
        else:
            sub_child_element.text = etree.CDATA(documentation_name)
        sub_child_element = etree.SubElement(child_element, "filename")
        if accent_letters_replace(documentation_file) == documentation_file:
            sub_child_element.text = documentation_file
        else:
            sub_child_element.text = etree.CDATA(documentation_file)
    else:
        for item in child:
            if item.tag == "{http://sshade.eu/schema/import}documentation":
                for sub_item in item:
                    if sub_item.tag == "{http://sshade.eu/schema/import}name":
                        fill_child_action(sub_item, documentation_name)
                    if sub_item.tag == "{http://sshade.eu/schema/import}filename":
                        fill_child_action(sub_item, documentation_file)
    return 1


# function to add a link
def add_link(already_one_filled, child, link_name, link_url):
    if already_one_filled:
        child_element = etree.SubElement(child, "link")
        sub_child_element = etree.SubElement(child_element, "name")
        if accent_letters_replace(link_name) == link_name:
            sub_child_element.text = link_name
        else:
            sub_child_element.text = etree.CDATA(link_name)
        sub_child_element = etree.SubElement(child_element, "url")
        if accent_letters_replace(link_url) == link_url:
            sub_child_element.text = link_url
        else:
            sub_child_element.text = etree.CDATA(link_url)
    else:
        for item in child:
            if item.tag == "{http://sshade.eu/schema/import}link":
                for sub_item in item:
                    if sub_item.tag == "{http://sshade.eu/schema/import}name":
                        fill_child_action(sub_item, link_name)
                    if sub_item.tag == "{http://sshade.eu/schema/import}url":
                        fill_child_action(sub_item, link_url)
    return 1


# function to add a publication
def add_publication(already_one_filled, child, pub_name, pub_year):
    if already_one_filled:
        child_element = etree.SubElement(child, "publication_uid")
        child_element.text = f"PUBLI_{accent_letters_replace(pub_name)}_{pub_year}"
        add_comment(child_element, " %%% TO VERIFY ")
    else:
        for item in child:
            if item.tag == "{http://sshade.eu/schema/import}publication_uid":
                UID_author = accent_letters_replace(pub_name).title().replace("'", "").replace(' ', '-')
                fill_child_action(item, f"PUBLI_{UID_author}_{pub_year}")
                add_comment(item, " %%% TO VERIFY ")
    return 1


# 3.3 accessories function to verify the input data
# abs mandatory verification function
def abs_mandatory(name, instrument_type, technique, technique_name, lab_current_acronym):
    phrase = " is mandatory! Please, fill this field."
    # name
    if name == "":
        return ('Instrument name' + phrase, 'name')
    # type
    if instrument_type == "":
        return ('Instrument type' + phrase, 'type')
    # technique
    if technique == "":
        return ('Instrument technique' + phrase, 'technique')
    # technique_name
    if technique_name == "":
        return ('Technique name' + phrase, 'technique_name')
    # lab_current_acronym
    if lab_current_acronym == "":
        return ('Current laboratory acronym' + phrase, 'lab_current_acronym')
    return ('Ok', '')


# function called in pair_abs_mandatory
# it checks that the two dependent fields are filled or empty together
def pair_verification(element_1_value, element_1_name, element_1_uid, element_2_value, element_2_name, element_2_uid):
    if (element_1_value == "" and element_2_value == "") or (element_1_value != "" and element_2_value != ""):
        return ('Ok', '')
    elif element_1_value == "":
        return (f'{element_1_name.capitalize()} is mandatory if {element_2_name} if filled! '
                f'Please, fill or empty both fields.',
                element_1_uid)
    else:
        return (f'{element_2_name.capitalize()} is mandatory if {element_1_name} if filled! '
                f'Please, fill or empty both fields.',
                element_2_uid)


# function called in pair_abs_mandatory
# it verifies that the dependent field is not filled while the parent field is empty
def second_verification(parent_element_value, parent_element_name, parent_element_uid,
                        child_element_value, child_element_name):
    if parent_element_value == "" and child_element_value != "":
        return (f'{parent_element_name.capitalize()} is mandatory if {child_element_name} if filled! '
                f'Please, fill {parent_element_name} or empty {child_element_name}.',
                parent_element_uid)
    else:
        return ('Ok', '')


# function verifies that all data in pairs are filled or not but together
def pair_abs_mandatory(lab_previous_1_acronym, lab_previous_1_comment, lab_previous_2_acronym, lab_previous_2_comment,
                       documentation_name_1, documentation_file_1, documentation_name_2, documentation_file_2,
                       documentation_name_3, documentation_file_3,
                       link_name_1, link_url_1, link_name_2, link_url_2, link_name_3, link_url_3,
                       pub_name_1, pub_year_1, pub_name_2, pub_year_2, pub_name_3, pub_year_3):
    # lab comments & uid
    result = second_verification(lab_previous_1_acronym, 'previous laboratory 1 abbreviation', 'lab_previous_1_acronym',
                                 lab_previous_1_comment, 'previous laboratory 1 comment')
    if result[0] != 'Ok':
        return result
    result = second_verification(lab_previous_2_acronym, 'previous laboratory 2 abbreviation', 'lab_previous_2_acronym',
                                 lab_previous_2_comment, 'previous laboratory 2 comment')
    if result[0] != 'Ok':
        return result
    # documentations
    result = pair_verification(documentation_name_1, 'documentation 1 name', 'documentation_name_1',
                               documentation_file_1, 'documentation 1 filename', 'documentation_file_1')
    if result[0] != 'Ok':
        return result
    result = pair_verification(documentation_name_2, 'documentation 2 name', 'documentation_name_2',
                               documentation_file_2, 'documentation 2 filename', 'documentation_file_2')
    if result[0] != 'Ok':
        return result
    result = pair_verification(documentation_name_3, 'documentation 3 name', 'documentation_name_3',
                               documentation_file_3, 'documentation 3 filename', 'documentation_file_3')
    if result[0] != 'Ok':
        return result
    # links
    result = pair_verification(link_name_1, 'link 1 name', 'link_name_1',
                               link_url_1, 'link 1 URL', 'link_url_1')
    if result[0] != 'Ok':
        return result
    result = pair_verification(link_name_2, 'link 2 name', 'link_name_2',
                               link_url_2, 'link 2 URL', 'link_url_2')
    if result[0] != 'Ok':
        return result
    result = pair_verification(link_name_3, 'link 3 name', 'link_name_3',
                               link_url_3, 'link 3 URL', 'link_url_3')
    if result[0] != 'Ok':
        return result
    # publications
    result = pair_verification(pub_name_1, 'publication 1 first author name', 'pub_name_1',
                               pub_year_1, 'publication 1 year', 'pub_year_1')
    if result[0] != 'Ok':
        return result
    result = pair_verification(pub_name_2, 'publication 2 first author name', 'pub_name_2',
                               pub_year_2, 'publication 2 year', 'pub_year_2')
    if result[0] != 'Ok':
        return result
    result = pair_verification(pub_name_3, 'publication 3 first author name', 'pub_name_3',
                               pub_year_3, 'publication 3 year', 'pub_year_3')
    if result[0] != 'Ok':
        return result
    return ('Ok', '')


# 4 MAIN FUNCTION which parses XML template and fill it
# function to parse and fill the xml template
def xml_parse_and_fill(template,
                       lab_current_acronym, lab_current_comment,
                       lab_previous_1_acronym, lab_previous_1_comment,
                       lab_previous_2_acronym, lab_previous_2_comment,
                       instrument_type, name, technique, technique_name,
                       microscopy_imaging, optical_accessory, source, source_wavelength, source_power,
                       spectral_analyzer_1, spectral_analyzer_2, spectral_analyzer_3, spectral_analyzer_4,
                       detector_1, detector_2, detector_3,
                       documentation_name_1, documentation_file_1, documentation_name_2, documentation_file_2,
                       documentation_name_3, documentation_file_3,
                       link_name_1, link_url_1, link_name_2, link_url_2, link_name_3, link_url_3,
                       pub_name_1, pub_year_1, pub_name_2, pub_year_2, pub_name_3, pub_year_3,
                       comments):
    # parse & fill
    parser = etree.XMLParser(remove_blank_text=True)
    xml_root = etree.fromstring(template.encode("utf8"), parser)
    for child in xml_root.find("{http://sshade.eu/schema/import}instrument").getchildren():
        # uid
        if child.tag == "{http://sshade.eu/schema/import}uid":
            fill_child_action(child, "INSTRU_" + accent_letters_replace(name.strip()).upper().replace("-", "_").replace(" ", "_") + "_" + accent_letters_replace(technique.strip()).upper().replace("-", "_").replace(" ", "_") + "_" + accent_letters_replace(lab_current_acronym.strip()).upper().replace("-", "_").replace(" ", "_"))
            add_comment(child, " %%% TO VERIFY ")
        # laboratories
        if child.tag == "{http://sshade.eu/schema/import}laboratories":
            # current
            for item in child:
                if item.tag == "{http://sshade.eu/schema/import}laboratory":
                    for inner_item in item:
                        if inner_item.tag == "{http://sshade.eu/schema/import}uid":
                            fill_child_action(inner_item, "LAB_" + accent_letters_replace(lab_current_acronym.strip().upper().replace("-", "_").replace(" ", "_")))
                            add_comment(inner_item, " %%% TO VERIFY ")
                        if inner_item.tag == "{http://sshade.eu/schema/import}comments":
                            fill_child_action(inner_item, lab_current_comment)
            # previous
            for unit in [[lab_previous_1_acronym, lab_previous_1_comment], [lab_previous_2_acronym, lab_previous_2_comment]]:
                if unit[0] != "":
                    add_lab_previous(child, unit[0], unit[1])
        # type
        if child.tag == "{http://sshade.eu/schema/import}type":
            fill_child_action(child, instrument_type)
        # name
        if child.tag == "{http://sshade.eu/schema/import}name":
            fill_child_action(child, name)
        # technique
        if child.tag == "{http://sshade.eu/schema/import}technique":
            fill_child_action(child, technique)
        # technique_name
        if child.tag == "{http://sshade.eu/schema/import}technique_name":
            fill_child_action(child, technique_name)
        # microscopy_imaging
        if child.tag == "{http://sshade.eu/schema/import}microscopy_imaging":
            if microscopy_imaging != "":
                fill_child_action(child, microscopy_imaging)
            else:
                fill_child_action(child, "NULL")
        # optical_accessory
        if child.tag == "{http://sshade.eu/schema/import}optical_accessory":
            fill_child_action(child, optical_accessory)
        # source
        if child.tag == "{http://sshade.eu/schema/import}source":
            if source != "":
                fill_child_action(child, source)
            else:
                fill_child_action(child, "NULL")
        # source_wavelength
        if child.tag == "{http://sshade.eu/schema/import}source_wavelength":
            if source_wavelength != "":
                fill_child_action(child, source_wavelength)
            else:
                fill_child_action(child, "NULL")
        # source_power
        if child.tag == "{http://sshade.eu/schema/import}source_power":
            if technique not in ['Raman scattering', 'fluorescence emission']:
                fill_child_action(child, source_power)
            else:
                if source_power != "":
                    fill_child_action(child, source_power)
                else:
                    fill_child_action(child, "NULL")
        # spectral_analyzers
        if child.tag == "{http://sshade.eu/schema/import}spectral_analyzers":
            already_one_filled = 0
            for unit in [spectral_analyzer_1, spectral_analyzer_2, spectral_analyzer_3, spectral_analyzer_4]:
                if unit != "":
                    already_one_filled = add_spectral_analyzer(already_one_filled, child, unit)
            if already_one_filled == 0:
                for item in child:
                    if item.tag == "{http://sshade.eu/schema/import}spectral_analyzer":
                        fill_child_action(item, "NULL")
        # detectors
        if child.tag == "{http://sshade.eu/schema/import}detectors":
            already_one_filled = 0
            for unit in [detector_1, detector_2, detector_3]:
                if unit != "":
                    already_one_filled = add_detector(already_one_filled, child, unit)
            if already_one_filled == 0:
                for item in child:
                    if item.tag == "{http://sshade.eu/schema/import}detector":
                        fill_child_action(item, "NULL")
        # comments
        if child.tag == "{http://sshade.eu/schema/import}comments":
            fill_child_action(child, comments)
        # documentations
        if child.tag == "{http://sshade.eu/schema/import}documentations":
            already_one_filled = 0
            for unit in [[documentation_name_1, documentation_file_1], [documentation_name_2, documentation_file_2],
                         [documentation_name_3, documentation_file_3]]:
                if unit[0] != "":
                    already_one_filled = add_documentation(already_one_filled, child, unit[0], unit[1])
            if already_one_filled == 0:
                for item in child:
                    if item.tag == "{http://sshade.eu/schema/import}documentation":
                        for sub_item in item:
                            if item.tag == "{http://sshade.eu/schema/import}name":
                                fill_child_action(sub_item, "")
                            if item.tag == "{http://sshade.eu/schema/import}filename":
                                fill_child_action(sub_item, "")
        # links
        if child.tag == "{http://sshade.eu/schema/import}links":
            already_one_filled = 0
            for unit in [[link_name_1, link_url_1], [link_name_2, link_url_2], [link_name_3, link_url_3]]:
                if unit[0] != "":
                    already_one_filled = add_link(already_one_filled, child, unit[0], unit[1])
            if already_one_filled == 0:
                for item in child:
                    if item.tag == "{http://sshade.eu/schema/import}link":
                        for sub_item in item:
                            if item.tag == "{http://sshade.eu/schema/import}name":
                                fill_child_action(sub_item, "")
                            if item.tag == "{http://sshade.eu/schema/import}url":
                                fill_child_action(sub_item, "")
        # publications
        if child.tag == "{http://sshade.eu/schema/import}publications":
            already_one_filled = 0
            for unit in [[pub_name_1, pub_year_1], [pub_name_2, pub_year_2], [pub_name_3, pub_year_3]]:
                if unit[0] != "":
                    already_one_filled = add_publication(already_one_filled, child, unit[0], unit[1])
            if already_one_filled == 0:
                for item in child:
                    if item.tag == "{http://sshade.eu/schema/import}publication_uid":
                        fill_child_action(item, "")
    # from xml to byte
    str_to_upload = etree.tostring(xml_root, pretty_print=True, encoding="utf-8", xml_declaration=True, method="xml")
    return str_to_upload


# 5 MAIN VERIFICATIONS
# functions to verify if input data is correct
# (used only in this script as the interface script has its own verification)
def verification_function(lab_current_acronym, lab_current_comment,
                          lab_previous_1_acronym, lab_previous_1_comment,
                          lab_previous_2_acronym, lab_previous_2_comment,
                          instrument_type, name, technique, technique_name,
                          microscopy_imaging, optical_accessory, source, source_wavelength, source_power,
                          spectral_analyzer_1, spectral_analyzer_2, spectral_analyzer_3, spectral_analyzer_4,
                          detector_1, detector_2, detector_3,
                          documentation_name_1, documentation_file_1, documentation_name_2, documentation_file_2,
                          documentation_name_3, documentation_file_3,
                          link_name_1, link_url_1, link_name_2, link_url_2, link_name_3, link_url_3,
                          pub_name_1, pub_year_1, pub_name_2, pub_year_2, pub_name_3, pub_year_3,
                          comments):
    # abs mandatory
    verif = abs_mandatory(name, instrument_type, technique, technique_name, lab_current_acronym)
    if verif[0] != 'Ok':
        return(0, verif[0], verif[1])
    # pairs
    verif = pair_abs_mandatory(lab_previous_1_acronym, lab_previous_1_comment,
                               lab_previous_2_acronym, lab_previous_2_comment,
                               documentation_name_1, documentation_file_1,
                               documentation_name_2, documentation_file_2,
                               documentation_name_3, documentation_file_3,
                               link_name_1, link_url_1, link_name_2, link_url_2, link_name_3, link_url_3,
                               pub_name_1, pub_year_1, pub_name_2, pub_year_2, pub_name_3, pub_year_3)
    if verif[0] != 'Ok':
        return(0, verif[0], verif[1])
    return (1, '', '')


# 6 DEMO test function with "FULL" data set
# (used to test the work of this script)
def demo_function():
    # INPUTS
    lab_current_acronym = "FULL"
    lab_current_comment = "2011-now"
    lab_previous_1_acronym = "VoID"
    lab_previous_1_comment = "2009-2011"
    lab_previous_2_acronym = ""
    lab_previous_2_comment = ""
    instrument_type = "FTIR spectrometer"
    name = "full Brucker Vertex 70v"
    technique = "transmission"
    technique_name = "Brucker Vertex 70v NIR-MIR transmission"
    microscopy_imaging = "macroscopic"
    optical_accessory = "absolute specular reflectance"
    source = "Tungsten/Halogen lamp"
    source_wavelength = "Vis-NIR"
    source_power = "30 W/cm2"
    spectral_analyzer_1 = "CaF2 Beamsplitter"
    spectral_analyzer_2 = "KBr Beamsplitter"
    spectral_analyzer_3 = ""
    spectral_analyzer_4 = ""
    detector_1 = "InGaAs"
    detector_2 = "DTGS"
    detector_3 = ""
    documentation_name_1 = "1FT-Spectrometer Brucker Vertex 70v"
    documentation_file_1 = "Spectro-FTS-Brucker-Vertex70-characteristics.pdf"
    documentation_name_2 = "2FT-Spectrometer Brucker Vertex 70v"
    documentation_file_2 = "Spectro-FTS-Brucker-Vertex70-characteristics_2.pdf"
    documentation_name_3 = ""
    documentation_file_3 = ""
    link_name_1 = "3FT-Spectrometer Brucker Vertex 70v"
    link_url_1 = "https://wiki.sshade.eu/sshade/databases/ghosst/instruments"
    link_name_2 = "4FT-Spectrometer Brucker Vertex 70v"
    link_url_2 = "https://wiki.sshade.eu/sshade/databases/ghosst/fts_spectrometers_cryogenic_cells"
    link_name_3 = ""
    link_url_3 = ""
    pub_name_1 = "Full"
    pub_year_1 = "2000"
    pub_name_2 = "Void"
    pub_year_2 = "2000"
    pub_name_3 = ""
    pub_year_3 = ""
    comments = "comments instrument"

    # input verification
    verification_Ok = 1
    message = ''
    result = verification_function(lab_current_acronym, lab_current_comment,
                       lab_previous_1_acronym, lab_previous_1_comment,
                       lab_previous_2_acronym, lab_previous_2_comment,
                       instrument_type, name, technique, technique_name,
                       microscopy_imaging, optical_accessory, source, source_wavelength, source_power,
                       spectral_analyzer_1, spectral_analyzer_2, spectral_analyzer_3, spectral_analyzer_4,
                       detector_1, detector_2, detector_3,
                       documentation_name_1, documentation_file_1, documentation_name_2, documentation_file_2,
                       documentation_name_3, documentation_file_3,
                       link_name_1, link_url_1, link_name_2, link_url_2, link_name_3, link_url_3,
                       pub_name_1, pub_year_1, pub_name_2, pub_year_2, pub_name_3, pub_year_3,
                       comments)
    verification_Ok = result[0]
    message = result[1] + f" Focus on {result[2]}"

    # template filling
    if verification_Ok:
        str_to_upload = xml_parse_and_fill(template,
                       lab_current_acronym, lab_current_comment,
                       lab_previous_1_acronym, lab_previous_1_comment,
                       lab_previous_2_acronym, lab_previous_2_comment,
                       instrument_type, name, technique, technique_name,
                       microscopy_imaging, optical_accessory, source, source_wavelength, source_power,
                       spectral_analyzer_1, spectral_analyzer_2, spectral_analyzer_3, spectral_analyzer_4,
                       detector_1, detector_2, detector_3,
                       documentation_name_1, documentation_file_1, documentation_name_2, documentation_file_2,
                       documentation_name_3, documentation_file_3,
                       link_name_1, link_url_1, link_name_2, link_url_2, link_name_3, link_url_3,
                       pub_name_1, pub_year_1, pub_name_2, pub_year_2, pub_name_3, pub_year_3,
                       comments)
        # xml file saving
        file_name = f"instrument_{technique.strip().replace('-', '_').replace(' ', '_')}_{name.strip().replace('-', '_').replace(' ', '_')}.xml"
        if file_name:
            with open(file_name, 'wb') as file_output:
                file_output.write(str_to_upload)
    else:
        print(message)

#demo_function()

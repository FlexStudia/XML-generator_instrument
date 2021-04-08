XMLgenerator Instrument


**Description**  
* it is a desctop program 
* it is coded in Python 3.7.6
* it is created for SSHADE.eu to help fill the "instrument" XML file
* it is powered by the PyQt library to create a "web-form" interface which contains all the main fields of the SSHADE instrument XML file
* it generates an "instrument" SSHADE XML file filled with the data entered in the "web-form" interface


**File structure**  

_Support files:_  
* readme.txt (this readme text)  
* requirements.txt (list of all necessay packages)  

_Py code files:_  
* XMLGenerator_instrument_core.py (core code with all functions (can be used on its own as a python skript))  
* XMLGenerator_instrument_GUI.py (program interface powered by PyQt and connected to main code via imports)  

_GUI templates & icons:_  
* templates\MW.ui (ui template for the main window)  
* templates\mw.py (py file for the ui template for the main window)  
* icon\icon.ico (icon file for Windows)  
* icon\icon.icns (icon file for Mac)  


**Usage**  
in any python 3 environment
1. to be able to run this python file, you must have python 3 installed (www.python.org/downloads)
2. after it is necessary to install all the required packages (listed in requirements.txt provided with the py code file and this readme) for example via a virtual environment:    
`python3 -m venv .venv`  
`source .venv/bin/activate`  
`pip install --upgrade pip setuptools wheel`  
`pip install --upgrade -r requirements.txt`    
3. it is possible to read and run the code in the native python environment or install an IDE, for example "PyCharm"


**How ui to py**  
* ui templates are modifiable in Qt Designer (or Qt Creator)
* it is possible to transform ui into py in the command line with the activated virtual environment with the following commands:  
`cd templates`  
`python.exe -m PyQt5.uic.pyuic mw.ui -o mw.py`  


**Compilation**  
it is possile to create a single executable file with PyInstaller with the following command line:  
_for Linux:_  
`pyinstaller --noconsole --onefile XMLGenerator_instrument_GUI.py`  
_for Mac:_  
`pyinstaller --noconsole --onefile --icon "icon.icns" XMLGenerator_instrument_GUI.py`  
_for Windows:_  
`pyinstaller --noconsole --onefile --icon "icon.ico" XMLGenerator_instrument_GUI.py`  
where "icon.ico"/"icon.icns" is an option to include an icon for the executable (provided)


**Authors and acknowledgment**  
* program code is by [Maria Gorbacheva](flex.studia.dev@gmail.com)
* scientific base is by [Bernard Schmitt](bernard.schmitt@univ-grenoble-alpes.fr)
* authors are grateful to andresnino for the [QLabel_clickable package](https://github.com/andresnino/PyQt5/tree/master/QLabel_clickable)
	
  
**Contributing**  
for any questions, proposals and bug reports, please write to [XML.generator.instrument@gmail.com](XML.generator.instrument@gmail.com)


**License**  
CC-BY 4.0 (Authors attribution alone required)

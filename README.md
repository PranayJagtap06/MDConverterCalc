# MDConverterCalc
Build with Python 🐍 and KivyMD, MDConverterCalc is a one stop solution to find your dc-dc converter specifications. MDConverterCalc takes some input parameters like converter type (buck, boost or buck-boost), input voltage, output voltage, output resistance, frequency, % input ripple current (optional) and % output ripple voltage to calculate the converter specifications. So make sure to finalize these prerequisite parameters before calculating converter specifications.

## Features
 -  Calculates dc-dc converter specs like inductor value and capacitor values.
 -  Plots transient response of the dc-dc converter.
 -  Calculates transfer function of the dc-dc converter.

## Dependencies
 - Python 3.11 (lower verison may also work)
 - Kivy 2.3.0
 - KivyMD 2.0.1dev0 (which is the github master version at time of uploading this app)
 - numpy
 - scipy
 - pyrebase4
 - firebase-admin
 - ConverterPackage
 - tf_response
 - emailverify

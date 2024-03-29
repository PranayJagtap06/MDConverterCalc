# MDConverterCalc
Build with Python 🐍 and KivyMD, MDConverterCalc is a one stop solution to find your dc-dc converter specifications. MDConverterCalc takes some input parameters like converter type (buck, boost or buck-boost), input voltage, output voltage, output resistance, frequency, % input ripple current (optional) and % output ripple voltage to calculate the converter specifications. So make sure to finalize these prerequisite parameters before calculating converter specifications.

## Features
 -  Calculates dc-dc converter specs like inductor value and capacitor values.
 -  Plots transient response of the dc-dc converter.
 -  Calculates transfer function of the dc-dc converter.

## Dependencies
 - Python=3.11 (lower verison may also work)
 - Kivy=2.3.0
 - KivyMD=2.0.1dev0 (which is the github master version at time of uploading this app)
 - numpy
 - scipy
 - pyrebase4
 - firebase-admin
 - ConverterPackage
 - tf_response.py
 - emailverify.py

MDConverterCalc requires ConverterPackage package for calculating converter specifications, it has modules for each converter type. tf_response.py is needed for generating transfer function and transient response. Finally, eamilverify.py is required for verifying email id is valid or not. emailverify.py is module provided by [EmailListVerify](https://www.emaillistverify.com/), which is an email verification service provider. More about it later. firebase-admin is required for authenticating users, more about it later.

## EmailListVerify
To be able to verify emails using emailverify.py you will need an api key to access the EmailListVerify API. To get your api key:
 1. Go to https://www.emaillistverify.com/ and create an account.
 2. Go to API section and click on "New API".
 3. A pop will open asking you to enter API name. Enter your preferred name and click "create".
 4. A new API dashboard will open. Scroll down in API section to copy your API key.
 5. In the same section select python language to open a brief guid on how to use the API key.

EmailListVerify Docs: [Docs](https://www.emaillistverify.com/docs/#tag/Email-Validation-API/operation/verifyEmail)

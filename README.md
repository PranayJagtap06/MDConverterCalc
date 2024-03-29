# MDConverterCalc
Build with Python 🐍 and KivyMD, MDConverterCalc is a one stop solution to find your dc-dc converter specifications. MDConverterCalc takes some input parameters like converter type (buck, boost or buck-boost), input voltage, output voltage, output resistance, frequency, % input ripple current (optional) and % output ripple voltage to calculate the converter specifications. So make sure to finalize these prerequisite parameters before calculating converter specifications.

>[!NOTE]
>## Features
> -  Calculates dc-dc converter specs like inductor value and capacitor values.
> -  Plots transient response of the dc-dc converter.
> -  Calculates transfer function of the dc-dc converter.

>[!IMPORTANT]
>## Dependencies
> - Python=3.11 (lower verison may also work)
> - Kivy=2.3.0
> - KivyMD=2.0.1dev0 (which is the github master version at time of uploading this app)
> - numpy
> - scipy
> - pyrebase4
> - firebase-admin
> - ConverterPackage
> - tf_response.py
> - emailverify.py
>
>MDConverterCalc requires ConverterPackage package for calculating converter specifications, it has modules for each converter type. tf_response.py is needed for generating transfer function and transient response. Finally, eamilverify.py is required for verifying email id is valid or not. emailverify.py is module provided by [EmailListVerify](https://www.emaillistverify.com/), which is an email verification service provider. More about it later. firebase-admin is required for authenticating users, more about it later.

>[!TIP]
>## EmailListVerify
>To be able to verify emails using emailverify.py you will need an api key to access the EmailListVerify API. To get your api key:
> 1. Go to https://www.emaillistverify.com/ and create an account.
> 2. Go to API section and click on `New API`.
> 3. A pop will open asking you to enter API name. Enter your preferred name and click `create`.
> 4. A new API dashboard will open. Scroll down in API section to copy your API key.
> 5. In the same section select python language to open a brief guid on how to use the API key.
>
>EmailListVerify Docs: [Docs](https://www.emaillistverify.com/docs/#tag/Email-Validation-API/operation/verifyEmail)
>
>## Firebase Admin
>To be able to use the app you will need to make a firebase account and create a project. After creating a project copy the firebaseConfig content for a `web` app section and paste it the `firebase_config` variable in the main.py file. Here's how you can get your firebaseConfig content:
> 1. Click the settings or gear icon besides `Project Overview` on the left hand panel.
> 2. From the resulting pop up select `Project settings`.
> 3. In `Project settings` go to the `General` tab.
> 4. Scroll down to `Your apps` section in `General` tab, and select the `Config` radio button.
> 5. From the text window below the `Config` radio button copy on the `firebaseConfig` variable content and not the whole syntax. Upcoming section will tell you how to edit and use the content.
>
>You will also need the firebase json key (firebaseConfig also) to initialize the app. To get the firebase json key:
> 1. Click the settings or gear icon besides `Project Overview` on the left hand panel.
> 2. From the resulting pop up select `Project settings`.
> 3. In the `Project settings` go to the `Service accounts` tab.
> 4. Scroll down in `Service accounts` and click on `Generate new private key`.
> 5. Save this key 🔑 in the same folder 📂 as of main.py.

Here's how you should use you firebaseConfig and firebase json key:

    firebase_config = {
      "apiKey": "************"
      "authDomain": "***************"
      "databaseURL": "https://***********"
      "projectId": "***********"
      "storageBucket": "**********"
      "messagingSenderId": "***********"
      "appId": "**************"
      "measurementId": "***********"
    }
    cred = credentials.Certificate('firebase_key.json')  # add your firebase json key (keep your firebase json key and main.py file in same directory)
    firebase_admin.initialize_app(cred, firebase_config)

>[!WARNING]
>The firebase_config variable stores a dictionary containing the keys and identifiers for your app, since it is a dictionary the keys needs to be in double qoutes.


https://github.com/PranayJagtap06/MDConverterCalc/assets/66717457/974174bd-35c4-4d16-868a-ca5f34f98ecd

![1BuckResponseVin12D0 417](https://github.com/PranayJagtap06/MDConverterCalc/assets/66717457/f94b99d2-53db-4be2-a0d2-0af9061fb0f7)


![1BoostResponseVin12D0 75](https://github.com/PranayJagtap06/MDConverterCalc/assets/66717457/71829ead-3f12-4343-a66f-6158cedd1326)

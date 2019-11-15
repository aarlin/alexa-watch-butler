Tinder Voice
=========================================

![](./images/108.png) ![](./images/plus-108.png) ![](./images/108-alexa.png)

Setup
-----

Download Amazon Alexa from Apple Store or Google Play.

[![iOS](./images/appstore.png)](https://apps.apple.com/us/app/amazon-alexa/id944011620)
[![Android](./images/playstore.png)](https://play.google.com/store/apps/details?id=com.amazon.dee.app&hl=en_US)

To run this example skill you need to do two things. The first is to
deploy the example code in lambda, and the second is to configure the
Alexa skill to use Lambda.

[![Get Started](https://camo.githubusercontent.com/db9b9ce26327ad3bac57ec4daf0961a382d75790/68747470733a2f2f6d2e6d656469612d616d617a6f6e2e636f6d2f696d616765732f472f30312f6d6f62696c652d617070732f6465782f616c6578612f616c6578612d736b696c6c732d6b69742f7475746f7269616c732f67656e6572616c2f627574746f6e732f627574746f6e5f6765745f737461727465642e5f5454485f2e706e67)](./instructions/1-voice-user-interface.md)

Skills can be built either by implementing ``AbstractRequestHandler`` classes
or by using skill builder's ``request_handler`` decorator. More information
on this can be checked in the [documentation](https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/REQUEST_PROCESSING.html#request-handlers).

This sample skill shows how to use skill builder's ``request_handler`` decorator. 
The code for this implementation is under [lambda/py](lambda/py) folder.

For the sample skill using the ``AbstractRequestHandler`` classes approach, check 
[skill-sample-python-helloworld-classes](https://github.com/alexa/skill-sample-python-helloworld-classes).

Additional Resources
--------------------

### Documentation

-  [Official Alexa Skills Kit Python SDK](https://pypi.org/project/ask-sdk/)
-  [Official Alexa Skills Kit Python SDK Docs](https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/)
-  [Official Alexa Skills Kit Docs](https://developer.amazon.com/docs/ask-overviews/build-skills-with-the-alexa-skills-kit.html)


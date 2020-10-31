# Build an Alexa-Hosted Skill in Alexa Developer Console

## Setting up Your Alexa Skill in the Developer Console

1.  **Go to the [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask).  In the top-right corner of the screen, click the "Sign In" button.**
(If you don't already have an account, you will be able to create a new one for free.)

1.  From the **Alexa Developer Console** select the **Create Skill** button near the top-right of the list of your Alexa Skills.

1. Give your new skill a **Name**, for example, 'Tinder Voice'. This is the name that will be shown in the Alexa Skills Store, and the name your users will refer to.

1. Select the Default Language.  This tutorial will presume you have selected 'English (US)'.

1. Select the **Custom** model under the *'Choose a model to add to your skill'* section. Select the **Alexa-Hosted (Python)** method under the *'Choose a method to host your skill's backend resources'*. Click the **Create Skill** button at the top right.

1. **Build the Interaction Model for your skill**
	1. On the left hand navigation panel, select the **JSON Editor** tab under **Interaction Model**. In the textfield provided, replace any existing code with the code provided in the [Interaction Model](../models/en-US.json).  Click **Save Model**.
    2. If you want to change the skill invocation name, select the **Invocation** tab. Enter a **Skill Invocation Name**. This is the name that your users will need to say to start your skill.  In this case, it's preconfigured to be 'tinder voice'.
    3. Click "Build Model".

7. **Enable Alexa Presentation Language for your skill**
	1. On the left hand navigation panel, select the **Interface** tab. Enable **Display Interface**
    2. Click "Build Model".

8. **Enable Permissions for your skill**
    1. On the left hand navigation panel, select the **Permissions** tab. Enable **Customer Phone Number**

9. If your interaction model builds successfully, proceed to the next step. If not, you should see an error. Try to resolve the errors. In our next step of this guide, we will be creating our Lambda function.

[![Next](https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/general/buttons/button_next_lambda_function._TTH_.png)](./2-lambda-function.md)

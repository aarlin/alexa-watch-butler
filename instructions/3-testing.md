# Build an Alexa-Hosted Skill in Alexa Developer Console

## Testing Your Alexa Skill

So far, we have [created a Voice User Interface](./1-voice-user-interface.md) and [a Lambda function](./2-lambda-function.md), and [connected the two together](./3-connect-vui-to-code.md).  Your skill is now ready to test.

1.  **Go back to the [Amazon Developer Portal](https://developer.amazon.com/edw/home.html#/skills/list) and select your skill from the list.** You may still have a browser tab open if you started at the beginning of this tutorial.

2. Open the **Test** Pane, by selecting the **Test** link from the top navigation menu.

3. Enable Testing by activating the **Test is enabled for this skill** slider. It should be underneath the top navigation menu.

4. To validate that your skill is working as expected, invoke your skill from the **Alexa Simulator**. You can either type or click and hold the mic from the input box to use your voice.
	1. **Type** "Open" followed by the invocation name you gave your skill in [Step 1](./1-voice-user-interface.md). For example, "Open tinder voice".
	2. **Use your voice** by clicking and holding the mic on the side panel and saying "Open" followed by the invocation name you gave your skill.
	3. **If you've forgotten the invocation name** for your skill, revisit the **Build** panel on the top navigation menu and select Invocation from the sidebar to review it.

5. Ensure your skill works the way that you designed it to.
	* After you interact with the Alexa Simulator, you should see the Skill I/O **JSON Input** and **JSON Output** boxes get populated with JSON data. You can also view the **Device Log** to trace your steps.
	* If it's not working as expected, you can dig into the JSON to see exactly what Alexa is sending and receiving from the endpoint. If something is broken, AWS Lambda offers an additional testing tool to help you troubleshoot your skill.

6.  **Configure a test event in AWS Lambda.** Now that you are familiar with the **request** and **response** boxes in the Service Simulator, it's important for you to know that you can use your **requests** to directly test your Lambda function every time you update it.  To do this:
    1.  Enter an utterance in the service simulator, and copy the generated Lambda Request for the next step.

    2.  **Open your Lambda function in AWS, open the Actions menu, and select "Configure test events."**

        <img src="https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/general/4-5-2-configure-test-event._TTH_.png" />

8.  **If your sample skill is working properly, you can now customize your skill.**

<a href="./5-next-steps.md"><img src="https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/general/buttons/button_next_customization._TTH_.png" />

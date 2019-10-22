Input Event Format
------------------

The following shows the general format of an Amazon Lex event that is passed to a Lambda function. Use this information when you are writing your Lambda function.

Note

The input format may change without a corresponding change in the `messageVersion`. Your code should not throw an error if new fields are present.

```json
{
  "currentIntent": {
    "name": "_`intent-name`_",
    "slots": {
      "_`slot name`_": "_`value`_",
      "_`slot name`_": "_`value`_"
    },
    "slotDetails": {
      "_`slot name`_": {
        "resolutions" : [
          { "value": "_`resolved value`_" },
          { "value": "_`resolved value`_" }
        ],
        "originalValue": "_`original text`_"
      },
      "_`slot name`_": {
        "resolutions" : [
          { "value": "_`resolved value`_" },
          { "value": "_`resolved value`_" }
        ],
        "originalValue": "_`original text`_"
      }
    },
    "confirmationStatus": "_`None, Confirmed, or Denied (intent confirmation, if configured)`_"
  },
  "bot": {
    "name": "_`bot name`_",
    "alias": "_`bot alias`_",
    "version": "_`bot version`_"
  },
  "userId": "_`User ID specified in the POST request to Amazon Lex.`_",
  "inputTranscript": "_`Text used to process the request`_",
  "invocationSource": "_`FulfillmentCodeHook or DialogCodeHook`_",
  "outputDialogMode": "_`Text or Voice, based on ContentType request header in runtime API request`_",
  "messageVersion": "1.0",
  "sessionAttributes": { 
     "_`key`_": "_`value`_",
     "_`key`_": "_`value`_"
  },
  "requestAttributes": { 
     "_`key`_": "_`value`_",
     "_`key`_": "_`value`_"
  },
  "recentIntentSummaryView": [
    {
        "intentName": "_`Name`_",
        "checkpointLabel": _`Label`_,
        "slots": {
          "_`slot name`_": "_`value`_",
          "_`slot name`_": "_`value`_"
        },
        "confirmationStatus": "_`None, Confirmed, or Denied (intent confirmation, if configured)`_",
        "dialogActionType": "_`ElicitIntent, ElicitSlot, ConfirmIntent, Delegate, or Close`_",
        "fulfillmentState": "_`Fulfilled or Failed`_",
        "slotToElicit": "_`Next slot to elicit`_
    }
  ]
}
```

Note the following additional information about the event fields:

*   **currentIntent** – Provides the intent `name`, `slots`, `slotDetails` and `confirmationStatus` fields.
    
    `slots` is a map of slot names, configured for the intent, to slot values that Amazon Lex has recognized in the user conversation. A slot value remains null until the user provides a value.
    
    The slot value in the input event may not match one of the values configured for the slot. For example, if the user responds to the prompt "What color car would you like?" with "pizza," Amazon Lex will return "pizza" as the slot value. Your function should validate the values to make sure that they make sense in context.
    
    `slotDetails` provides additional information about a slot value. The `resolutions` array contains a list of additional values recognized for the slot. Each slot can have a maximum of five values.
    
    The `originalValue` field contains the value that was entered by the user for the slot. When the slot type is configured to return the top resolution value as the slot value, the `originalValue` may be different from the value in the `slots` field.
    
    `confirmationStatus` provides the user response to a confirmation prompt, if there is one. For example, if Amazon Lex asks "Do you want to order a large cheese pizza?," depending on the user response, the value of this field can be `Confirmed` or `Denied`. Otherwise, this value of this field is `None`.
    
    If the user confirms the intent, Amazon Lex sets this field to `Confirmed`. If the user denies the intent, Amazon Lex sets this value to `Denied`.
    
    In the confirmation response, a user utterance might provide slot updates. For example, the user might say "yes, change size to medium." In this case, the subsequent Lambda event has the updated slot value, `PizzaSize` set to `medium`. Amazon Lex sets the `confirmationStatus` to `None`, because the user modified some slot data, requiring the Lambda function to perform user data validation.
    
*   **bot** – Information about the bot that processed the request.
    
    *   `name` – The name of the bot that processed the request.
        
    *   `alias` – The alias of the bot version that processed the request.
        
    *   `version` – The version of the bot that processed the request.
        
    
*   **userId** – This value is provided by the client application. Amazon Lex passes it to the Lambda function.
    
*   **inputTranscript** – The text used to process the request.
    
    If the input was text, the `inputTranscript` field contains the text that was input by the user.
    
    If the input was an audio stream, the `inputTranscript` field contains the text extracted from the audio stream. This is the text that is actually processed to recognize intents and slot values.
    
*   **invocationSource** – To indicate why Amazon Lex is invoking the Lambda function, it sets this to one of the following values:
    
    *   `DialogCodeHook` – Amazon Lex sets this value to direct the Lambda function to initialize the function and to validate the user's data input.
        
        When the intent is configured to invoke a Lambda function as an initialization and validation code hook, Amazon Lex invokes the specified Lambda function on each user input (utterance) after Amazon Lex understands the intent.
        
        Note
        
        If the intent is not clear, Amazon Lex can't invoke the Lambda function.
        
    *   `FulfillmentCodeHook` – Amazon Lex sets this value to direct the Lambda function to fulfill an intent.
        
        If the intent is configured to invoke a Lambda function as a fulfillment code hook, Amazon Lex sets the `invocationSource` to this value only after it has all the slot data to fulfill the intent.
        
    
    In your intent configuration, you can have two separate Lambda functions to initialize and validate user data and to fulfill the intent. You can also use one Lambda function to do both. In that case, your Lambda function can use the `invocationSource` value to follow the correct code path.
    
*   **outputDialogMode** – For each user input, the client sends the request to Amazon Lex using one of the runtime API operations, [PostContent](API_runtime_PostContent.html) or [PostText](API_runtime_PostText.html). Amazon Lex use the request parameters, Amazon Lex to determine whether the response to the client is text or voice, and sets this field accordingly.
    
    The Lambda function can use this information to generate an appropriate message. For example, if the client expects a voice response, your Lambda function could return Speech Synthesis Markup Language (SSML) instead of text.
    
*   **messageVersion** – The version of the message that identifies the format of the event data going into the Lambda function and the expected format of the response from a Lambda function.
    
    Note
    
    You configure this value when you define an intent. In the current implementation, only message version 1.0 is supported. Therefore, the console assumes the default value of 1.0 and doesn't show the message version.
    
*   **sessionAttributes** – Application-specific session attributes that the client sends in the request. If you want Amazon Lex to include them in the response to the client, your Lambda function should send these back to Amazon Lex in the response. For more information, see [Setting Session Attributes](context-mgmt.html#context-mgmt-session-attribs)
    
*   **requestAttributes** – Request-specific attributes that the client sends in the request. Use request attributes to pass information that doesn't need to persist for the entire session. If there are no request attributes, the value will be null. For more information, see [Setting Request Attributes](context-mgmt.html#context-mgmt-request-attribs)
    
*   **recentIntentSummaryView** – Information about the state of an intent. You can see information about the last three intents used. You can use this information to set values in the intent or to return to a previous intent. For more information, see [Managing Sessions With the Amazon Lex API](how-session-api.html).
    

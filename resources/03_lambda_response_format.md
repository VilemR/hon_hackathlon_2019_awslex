Response Format
---------------

Amazon Lex expects a response from a Lambda function in the following format:

```json
{
    "sessionAttributes": {
    "key1": "value1",
    "key2": "value2"
  },
  "recentIntentSummaryView": [
    {
       "intentName": "_`Name`_",
       "checkpointLabel": "_`Label`_",
       "slots": {
         "_`slot name`_": "_`value`_",
         "_`slot name`_": "_`value`_"
        },
       "confirmationStatus": "_`None, Confirmed, or Denied (intent confirmation, if configured)`_",
        "dialogActionType": "_`ElicitIntent, ElicitSlot, ConfirmIntent, Delegate, or Close`_",
        "fulfillmentState": "_`Fulfilled or Failed`_",
        "slotToElicit": "_`Next slot to elicit`_"
    }
  ],
  "dialogAction": {
    "type": "_`ElicitIntent, ElicitSlot, ConfirmIntent, Delegate, or Close`_",
    "_`Full structure based on the type field. See below for details.`_"
  }
}
```

The response consists of three fields. The `sessionAttributes` and `recentIntentSummaryView` fields are optional, the `dialogAction` field is required. The contents of the `dialogAction` field depends on the value of the `type` field. For details, see [dialogAction](lambda-input-response-format.html#lambda-response-dialogAction).

### sessionAttributes

Optional. If you include the `sessionAttributes` field it can be empty. If your Lambda function doesn't return session attributes, the last known `sessionAttributes` passed via the API or Lambda function remain. For more information, see the [PostContent](API_runtime_PostContent.html) and [PostText](API_runtime_PostText.html) operations.

 ```json
 "sessionAttributes": { 
     "key1": "_`value1`_",
     "key2": "_`value2`_"
  }
```

### recentIntentSummaryView

Optional. If included, sets values for one or more recent intents. You can include information for up to three intents. For example, you can set values for previous intents based on information gathered by the current intent. The information in the summary must be valid for the intent. For example, the intent name must be an intent in the bot. If you include a slot value in the summary view, the slot must exist in the intent. If you don't include the `recentIntentSummaryView` in your response, all of the values for the recent intents remain unchanged. For more information, see the [PutSession](API_runtime_PutSession.html) operation or the [IntentSummary](API_runtime_IntentSummary.html) data type.

```json
"recentIntentSummaryView": [
    {
       "intentName": "_`Name`_",
       "checkpointLabel": "_`Label`_",
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
``` 

### dialogAction

Required. The `dialogAction` field directs Amazon Lex to the next course of action, and describes what to expect from the user after Amazon Lex returns a response to the client.

The `type` field indicates the next course of action. It also determines the other fields that the Lambda function needs to provide as part of the `dialogAction` value.

*   `Close` — Informs Amazon Lex not to expect a response from the user. For example, "Your pizza order has been placed" does not require a response.
    
    The `fulfillmentState` field is required. Amazon Lex uses this value to set the `dialogState` field in the [PostContent](API_runtime_PostContent.html) or [PostText](API_runtime_PostText.html) response to the client application. The `message` and `responseCard` fields are optional. If you don't specify a message, Amazon Lex uses the goodbye message or the follow-up message configured for the intent.
    
    ```json
    "dialogAction": {
        "type": "Close",
        "fulfillmentState": "_`Fulfilled or Failed`_",
        "message": {
          "contentType": "_`PlainText or SSML or CustomPayload`_",
          "content": "_`Message to convey to the user. For example, Thanks, your pizza has been ordered.`_"
        },
       "responseCard": {
          "version": _`integer-value`_,
          "contentType": "application/vnd.amazonaws.card.generic",
          "genericAttachments": [
              {
                 "title":"_`card-title`_",
                 "subTitle":"_`card-sub-title`_",
                 "imageUrl":"_`URL of the image to be shown`_",
                 "attachmentLinkUrl":"_`URL of the attachment to be associated with the card`_",
                 "buttons":[ 
                     {
                        "text":"_`button-text`_",
                        "value":"_`Value sent to server on button click`_"
                     }
                  ]
               } 
           ] 
         }
      }
    ```
    
*   `ConfirmIntent` — Informs Amazon Lex that the user is expected to give a yes or no answer to confirm or deny the current intent.
    
    You must include the `intentName` and `slots` fields. The `slots` field must contain an entry for each of the filled slots for the specified intent. You don't need to include a entry in the `slots` field for slots that aren't filled. You must include the `message` field if the intent's `confirmationPrompt` field is null. The contents of the `message` field returned by the Lambda function take precedence over the `confirmationPrompt` specified in the intent. The `responseCard` field is optional.
    
    ```json
    "dialogAction": {
        "type": "ConfirmIntent",
        "message": {
          "contentType": "_`PlainText or SSML or CustomPayload`_",
          "content": "_`Message to convey to the user. For example, Are you sure you want a large pizza?`_"
        },
       "intentName": "_`intent-name`_",
       "slots": {
          "slot-name": "_`value`_",
          "slot-name": "_`value`_",
          "slot-name": "_`value`_"  
       },
       "responseCard": {
          "version": _`integer-value`_,
          "contentType": "application/vnd.amazonaws.card.generic",
          "genericAttachments": [
              {
                 "title":"_`card-title`_",
                 "subTitle":"_`card-sub-title`_",
                 "imageUrl":"_`URL of the image to be shown`_",
                 "attachmentLinkUrl":"_`URL of the attachment to be associated with the card`_",
                 "buttons":[ 
                     {
                        "text":"_`button-text`_",
                        "value":"_`Value sent to server on button click`_"
                     }
                  ]
               } 
           ] 
         }
      }
    ```
    
*   `Delegate` — Directs Amazon Lex to choose the next course of action based on the bot configuration. If the response does not include any session attributes Amazon Lex retains the existing attributes. If you want a slot value to be null, you don't need to include the slot field in the request. You will get a `DependencyFailedException` exception if your fulfilment function returns the `Delegate` dialog action without removing any slots.
    ```json
     dialogAction": {
       "type": "Delegate",
       "slots": {
          "slot-name": "_`value`_",
          "slot-name": "_`value`_",
          "slot-name": "_`value`_"  
       }
      }
    ```
    
*   `ElicitIntent` — Informs Amazon Lex that the user is expected to respond with an utterance that includes an intent. For example, "I want a large pizza," which indicates the `OrderPizzaIntent`. The utterance "large," on the other hand, is not sufficient for Amazon Lex to infer the user's intent.
    
    The `message` and `responseCard` fields are optional. If you don't provide a message, Amazon Lex uses one of the bot's clarification prompts. If there is no clarification prompt defined, Amazon Lex returns a 400 Bad Request exception.
    
    ```json
    {
      "dialogAction": {
        "type": "ElicitIntent",
        "message": {
          "contentType": "_`PlainText or SSML or CustomPayload`_",
          "content": "_`Message to convey to the user. For example, What can I help you with?`_"
        },
        "responseCard": {
          "version": _`integer-value`_,
          "contentType": "application/vnd.amazonaws.card.generic",
          "genericAttachments": [
              {
                 "title":"_`card-title`_",
                 "subTitle":"_`card-sub-title`_",
                 "imageUrl":"_`URL of the image to be shown`_",
                 "attachmentLinkUrl":"_`URL of the attachment to be associated with the card`_",
                 "buttons":[ 
                     {
                        "text":"_`button-text`_",
                        "value":"_`Value sent to server on button click`_"
                     }
                  ]
               } 
           ] 
        }
     }
    ``` 
    
*   `ElicitSlot` — Informs Amazon Lex that the user is expected to provide a slot value in the response.
    
    The `intentName`, `slotToElicit`, and `slots` fields are required. The `message` and `responseCard` fields are optional. If you don't specify a message, Amazon Lex uses one of the slot elicitation prompts configured for the slot.
    
    ```json
     "dialogAction": {
        "type": "ElicitSlot",
        "message": {
          "contentType": "_`PlainText or SSML or CustomPayload`_",
          "content": "_`Message to convey to the user. For example, What size pizza would you like?`_"
        },
       "intentName": "_`intent-name`_",
       "slots": {
          "slot-name": "_`value`_",
          "slot-name": "_`value`_",
          "slot-name": "_`value`_"  
       },
       "slotToElicit" : "_`slot-name`_",
       "responseCard": {
          "version": _`integer-value`_,
          "contentType": "application/vnd.amazonaws.card.generic",
          "genericAttachments": [
              {
                 "title":"_`card-title`_",
                 "subTitle":"_`card-sub-title`_",
                 "imageUrl":"_`URL of the image to be shown`_",
                 "attachmentLinkUrl":"_`URL of the attachment to be associated with the card`_",
                 "buttons":[ 
                     {
                        "text":"_`button-text`_",
                        "value":"_`Value sent to server on button click`_"
                     }
                  ]
               } 
           ] 
         }
      }
    ```
    

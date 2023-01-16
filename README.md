# GMail

|           |                                                                   |
| --------- | ----------------------------------------------------------------- |
| Name      | GMail                                                             |
| Version   | v1.0.0                                                            |
| DockerHub | [weevenetwork/gmail](https://hub.docker.com/r/weevenetwork/gmail) |
| Authors   | Jakub Grzelak                                                     |

- [GMail](#gmail)
  - [Description](#description)
  - [Environment Variables](#environment-variables)
    - [Module Specific](#module-specific)
    - [Set by the weeve Agent on the edge-node](#set-by-the-weeve-agent-on-the-edge-node)
  - [Dependencies](#dependencies)
  - [Input](#input)
  - [Output](#output)

## Description

Send data or files (as attachments) via email from your GMail account. The module accepts standard JSON object (headers: `application/json` or `application/*+json`) or files (we use `bottle` framework so after receiving it has type: `bottle.FileUpload`) as input. You can compose an email main body (content message) using double curly brackets to access labels from your data (i.e. to access data assigned to temperature label use {{temperature}}) or you can hard-type your message. The module can send emails with or without attachments.

## Environment Variables

### Module Specific

The following module configurations can be provided in a data service designer section on weeve platform:

| Name                  | Environment Variables | type   | Description                                                                                                                                                                                 |
| --------------------- | --------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sender Email          | SENDER_EMAIL          | string | GMail of the sender.                                                                                                                                                                        |
| Sender Pass           | SENDER_PASS           | string | Sender GMail pass for logging into Google account with less secure apps. You need to go to your Google account settings, then enable and generate a pass for logging with less secure apps. |
| Recipient Email       | RECIPIENT_EMAIL       | string | Email address of the recipient.                                                                                                                                                             |
| Email Subject         | EMAIL_SUBJECT         | string | Subject of the email.                                                                                                                                                                       |
| Email Body Message    | EMAIL_BODY_MESSAGE    | string | Email content. Use double curly brackets to access labels from your data (i.e. to access data assigned to temperature label use {{temperature}}).                                           |
| Attachment File Label | ATTACHMENT_FILE_LABEL | string | If the module input is a file to be sent as an attachment, then provide a label assigned to the file in the input data. Otherwise leave empty ("").                                         |



### Set by the weeve Agent on the edge-node

Other features required for establishing the inter-container communication between modules in a data service are set by weeve agent.

| Environment Variables | type   | Description                                    |
| --------------------- | ------ | ---------------------------------------------- |
| MODULE_NAME           | string | Name of the module                             |
| MODULE_TYPE           | string | Type of the module (Input, Processing, Output) |
| INGRESS_HOST          | string | Host to which data will be received            |
| INGRESS_PORT          | string | Port to which data will be received            |

## Dependencies

```txt
bottle
```

## Input

Input to this module is:

* a single JSON body object, example:

```json
{
    "label-1": 12,
    "label-2": "speed"
}
```

* or an attachment file

## Output

Output of this module is an email send with GMail services.

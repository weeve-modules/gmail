"""
This file implements module's main logic.
Data outputting should happen here.

Edit this file to implement your module.
"""

import re
import werkzeug
import smtplib
from logging import getLogger
from .params import PARAMS
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

log = getLogger("module")

# login to the GMail server
SERVER = smtplib.SMTP('smtp.gmail.com', 587)
SERVER.starttls()
SERVER.login(PARAMS["SENDER_EMAIL"], PARAMS["SENDER_PASS"])

def module_main(received_data: any) -> str:
    """
    Send received data to the next module by implementing module's main logic.
    Function description should not be modified.

    Args:
        received_data (any): Data received by module and validated.

    Returns:
        str: Error message if error occurred, otherwise None.

    """

    log.debug("Outputting ...")

    try:
        # compose email message
        email_message = PARAMS["EMAIL_BODY_MESSAGE"]

        # if received data is json not attachment file then compose the email body from received data
        if type(received_data) == dict:
            for label in [x[2:-2] for x in re.findall("{{.*?}}", PARAMS["EMAIL_BODY_MESSAGE"])]:
                # emplace data into the email message
                email_message = email_message.replace("{{" + label + "}}", str(received_data[label]))

        msg = MIMEMultipart()
        msg['From'] = PARAMS["SENDER_EMAIL"]
        msg['To'] = PARAMS["RECIPIENT_EMAIL"]
        msg['Subject'] = PARAMS["EMAIL_SUBJECT"]
        msg.attach(MIMEText(email_message, 'plain'))

        # check if received data is attachment file and add the attachment to the email
        if type(received_data) == werkzeug.datastructures.FileStorage:
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(received_data.read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', "attachment; filename=attachment-file")

            msg.attach(attachment)

        # send the email
        SERVER.sendmail(PARAMS["SENDER_EMAIL"], PARAMS["RECIPIENT_EMAIL"], msg.as_string())

        return None

    except Exception as e:
        return f"Exception in the module business logic: {e}"

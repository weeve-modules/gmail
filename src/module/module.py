"""
This file implements module's main logic.
Data outputting should happen here.

Edit this file to implement your module.
"""

import re
import smtplib
import bottle
import magic
from logging import getLogger
from .params import PARAMS
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage

log = getLogger("module")

# login to the GMail server
SERVER = smtplib.SMTP('smtp.gmail.com', 587)
SERVER.starttls()
SERVER.login(PARAMS["SENDER_EMAIL"], PARAMS["SENDER_PASS"])

# for checking incoming file type
mime = magic.Magic(mime=True)

# supported MIME classes
mime_classes = {
    "application": MIMEApplication,
    "image": MIMEImage,
    "text": MIMEText
}

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
        body = PARAMS["EMAIL_BODY_MESSAGE"]

        # if received data is json not attachment file then compose the email body from received data
        if type(received_data) == dict:
            for label in [x[2:-2] for x in re.findall("{{.*?}}", PARAMS["EMAIL_BODY_MESSAGE"])]:
                # emplace data into the email message
                body = body.replace("{{" + label + "}}", str(received_data[label]))

        msg = MIMEMultipart()
        msg['From'] = PARAMS["SENDER_EMAIL"]
        msg['To'] = PARAMS["RECIPIENT_EMAIL"]
        msg['Subject'] = PARAMS["EMAIL_SUBJECT"]
        msg.attach(MIMEText(body, 'plain'))

        # check if received data is attachment file and add the attachment to the email
        if type(received_data) == bottle.FileUpload:
            log.debug("Adding attachment to the email.")

            # check received file type and create a corresponding MIME object
            file = received_data.file.read()
            file_type = mime.from_buffer(file)
            log.debug(f"Received file type: {file_type}")
            attachment = mime_classes[file_type.split("/")[0]](file)
            attachment.add_header('Content-Disposition', f"attachment; filename={PARAMS['ATTACHMENT_FILE_LABEL']}")

            msg.attach(attachment)

        # send the email
        SERVER.sendmail(PARAMS["SENDER_EMAIL"], PARAMS["RECIPIENT_EMAIL"], msg.as_string())

        return None

    except Exception as e:
        return f"Exception in the module business logic: {e}"

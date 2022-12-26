"""
Validates whether the incoming data has an acceptable type and structure.

Edit this file to verify data expected by you module.
"""

import re
from logging import getLogger
from os import getenv

log = getLogger("validator")

# make a list of required data labels that will be later replaced in the email content text
required_labels = [x[2:-2] for x in re.findall("{{.*?}}", getenv("EMAIL_BODY_MESSAGE"))]

def data_validation(data: any) -> str:
    """
    Validate incoming data i.e. by checking if it is of type dict or list.
    Function description should not be modified.

    Args:
        data (any): Data to validate.

    Returns:
        str: Error message if error is encountered. Otherwise returns None.

    """

    log.debug("Validating ...")

    try:
        allowed_data_types = [dict]

        if not type(data) in allowed_data_types:
            return f"Detected type: {type(data)} | Supported types: {allowed_data_types} | invalid!"

        # check if all labels required in email message are present in the received data
        missing_labels = set(required_labels) - set(data.keys())
        if missing_labels:
            return f"The following data labels included in Email Body Message were not found in received data: {missing_labels}"

        return None

    except Exception as e:
        return f"Exception when validating module input data: {e}"

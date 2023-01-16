from os import getenv

PARAMS = {
    "SENDER_EMAIL": getenv("SENDER_EMAIL", "james.bond@gmail.com"),
    "SENDER_PASS": getenv("SENDER_PASS", "*****"),
    "RECIPIENT_EMAIL": getenv("RECIPIENT_EMAIL", "mrs.m@gmail.com"),
    "EMAIL_SUBJECT": getenv("EMAIL_SUBJECT", "Daily status report"),
    "EMAIL_BODY_MESSAGE": getenv("EMAIL_BODY_MESSAGE", "See the attachment"),
    "ATTACHMENT_FILE_LABEL": getenv("ATTACHMENT_FILE_LABEL", "")
}

import email
from email import policy
from email.parser import BytesParser

def load_email_from_file(filepath):
    with open(filepath,'rb') as f:
        msg =BytesParser(policy=policy.default).parse(f)
    email_body = msg.get_body(preferencelist=('plain')).get_content()
    return email_body
import imaplib
import email
from email import policy

def fetch_all_unread_email_texts(imap_host, email_user, email_pass, mailbox="INBOX", search='UNSEEN'):
   
    mail = imaplib.IMAP4_SSL(imap_host)
    mail.login(email_user, email_pass)
    mail.select(mailbox)

    result, data = mail.search(None, search)
    email_ids = data[0].split()
    if not email_ids:
        return []

    email_texts = []
    for email_id in email_ids:
        result, msg_data = mail.fetch(email_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email, policy=policy.default)

        try:
            body = msg.get_body(preferencelist=('plain')).get_content()
            email_texts.append(body)
        except:
            continue 

    return email_texts

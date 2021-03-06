import smtplib
from email.mime.text import MIMEText
from collections import defaultdict

def send_mail(subject, message, from_addr, *to_addr,
        host="localhost", port=1025, headers=None):
    email = MIMEText(message)
    email['Subject'] = subject
    email["Frome"] = from_addr
    headers = {} if headers is None else headers
    for header, value in headers.items():
        email[header] = value
    
    sender = smtplib.SMTP(host, port)
    for addr in to_addr:
        del email['To']
        email['To'] = addr
        sender.sendmail(from_addr, addr, email.as_string())
    sender.quit()

class MailingList():
    def __init__(self):
        self.email_map = defaultdict(set)
    
    def add_to_group(self, email, group):
        self.email_map[email].add(group)
    
    def emails_in_groups(self, *groups):
        groups = set(groups)
        emails = set()
        for e, g in self.email_map.items():
            if g & groups:
                emails.add(e)
        return emails
    
    def send_mailing(self, subject, message, from_addr,
            *groups, headers=None):
        emails = self.emails_in_groups(*groups)
        send_mail(subject, message, from_addr,
                *emails, headers=headers)
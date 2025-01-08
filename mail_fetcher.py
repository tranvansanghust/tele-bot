import imaplib
import email
from email.header import decode_header


class MailBox:
    def __init__(self, username, password) -> None:
        # Account credentials
        self.mail = self.connect_to_server(username, password)
        pass

    def connect_to_server(self, u_name, pwd):
        try:
            
            # Connect to the server
            mail = imaplib.IMAP4_SSL("imap.gmail.com")

            # Login to your account
            mail.login(u_name, pwd)

            return mail
        
        except imaplib.IMAP4.error as e:
            print(f"IMAP4 error: {e}")
            return None
    
    def fetch_unseen_mails(self):
        # Select the mailbox you want to check
        self.mail.select("inbox")

        # Search for all unread messages
        status, messages = self.mail.search(None, '(UNSEEN)')

        if status == "OK":
            messages = messages[0].split(b' ')
            print(f"Number of unread emails: {len(messages)}")

            for mail_id in messages:
                # Fetch the email by ID
                status, msg_data = self.mail.fetch(mail_id, "(RFC822)")

                if status == "OK":
                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_bytes(response_part[1])
                            subject, encoding = decode_header(msg["Subject"])[0]
                            if isinstance(subject, bytes):
                                subject = subject.decode(encoding if encoding else 'utf-8')
                            from_ = msg.get("From")
                            print("Subject:", subject)
                            print("From:", from_)
                            # Print body
                            if msg.is_multipart():
                                for part in msg.walk():
                                    content_type = part.get_content_type()
                                    if content_type == "text/plain":
                                        print(part.get_payload(decode=True).decode())
                            else:
                                print(msg.get_payload(decode=True).decode())
                else:
                    print(f"Failed to fetch email with ID {mail_id}")

        else:
            print("Failed to retrieve unread messages.")
    
    def get_newest_mail(self):
        # Select the mailbox you want to check
        self.mail.select("inbox")

        # Search for all unread messages
        status, messages = self.mail.search(None, '(UNSEEN)')

        subject = ""
        sender = ""

        if status == "OK":
            messages = messages[0].split(b' ')

            mail_id = messages[0] # get only one mail
                # Fetch the email by ID
            status, msg_data = self.mail.fetch(mail_id, "(RFC822)")

            if status == "OK":
                
                response_part = msg_data[0]
                print(response_part)
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else 'utf-8')
                    from_ = msg.get("From")
                    print("Get a mail")
                    print("From:", from_)

                    print("Subject:", subject)

                    sender = from_
                    # Print body
                    # if msg.is_multipart():
                    #     for part in msg.walk():
                    #         content_type = part.get_content_type()
                    #         if content_type == "text/plain":
                    #             print(part.get_payload(decode=True).decode())
                    # else:
                    #     print(msg.get_payload(decode=True).decode())
                
            else:
                print(f"Failed to fetch email with ID {mail_id}")



        else:
            print("Failed to retrieve unread messages.")
        
        return sender, subject


    def close_mail(self):
        self.mail.close()
    
    def logout_mail(self):
        # Logout and close connection
        try:
            self.mail.logout()
        except:
            pass
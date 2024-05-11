import firebase_admin
from firebase_admin import credentials, firestore
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Initialize Firebase Admin SDK
cred = credentials.Certificate(r"sample-1-fcb7b-firebase-adminsdk-sqfvi-24fd5ad500.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore yes
db = firestore.client()

# Function to fetch data from Firebase
def fetch_contact_data():
    # Replace 'contact_us' with the actual collection name in Firestore
    contact_us_ref = db.collection('resq_email_notify')
    docs = contact_us_ref.stream()
    contact_data = []

    for doc in docs:
        contact_data.append(doc.to_dict())

    return contact_data
# tgutf
# Function to fetch previously sent data
def fetch_sent_data():
    # Replace 'sent_data' with the name of the collection where you store sent data
    sent_data_ref = db.collection('resq_email_sent_data')
    docs = sent_data_ref.stream()
    sent_data = []

    for doc in docs:
        sent_data.append(doc.to_dict())

    return sent_data

# Function to send email
def send_email(contact_data, sent_data):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'aiprostacksolutions@gmail.com'  # Gmail sender email
    smtp_password = 'klpwsrgwyibhwqpw'  # Replace with your Gmail password

    # Create a MIMEText object
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = 'aiprostacksolutions@gmail.com'
    msg['Subject'] = 'New Contact Request from ResQ-Notify Website'

    # Create the email body
    body = "New Contact Requests:\n\n"
    
    # Filter out already sent data
    unsent_data = [data for data in contact_data if data not in sent_data]

    if not unsent_data:
        print("No new data to send.")
        return
    
    for data in unsent_data:
        body += f"Name: {data['name']}\n"
        body += f"Email: {data['email']}\n"
        body += f"Contact Number: {data['contact']}\n\n"

    msg.attach(MIMEText(body, 'plain'))

    # Send the email using Gmail's SMTP server
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, 'aiprostacksolutions@gmail.com', msg.as_string())
        server.quit()
        print("Email sent successfully to Resq-notify!")

        # Update the sent data in the 'sent_data' collection
        sent_data_ref = db.collection('resq_email_sent_data')
        for data in unsent_data:
            sent_data_ref.add(data)
    except Exception as e:
        print("Error sending email:", str(e))

if __name__ == "__main__":
    contact_data = fetch_contact_data()
    sent_data = fetch_sent_data()
    if contact_data:
        send_email(contact_data, sent_data)
        
        
        
        
        
        
        
# Function to fetch data from Firebase
def fetch_contact_data():
    # Replace 'contact_us' with the actual collection name in Firestore
    contact_us_ref = db.collection('resq_email_notify')
    docs = contact_us_ref.stream()
    contact_data = []

    for doc in docs:
        contact_data.append(doc.to_dict())

    return contact_data

# Function to fetch previously sent data
def fetch_email_sent_to_user():
    # Replace 'email_sent_to_user' with the name of the collection where you store sent data
    email_sent_to_user_ref = db.collection('resq_email_sent_to_user')
    docs = email_sent_to_user_ref.stream()
    email_sent_to_user = []

    for doc in docs:
        email_sent_to_user.append(doc.to_dict())

    return email_sent_to_user

# Function to send a confirmation email to the user
def send_confirmation_email(email, name):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'aiprostacksolutions@gmail.com'  # Gmail sender email
    smtp_password = 'klpwsrgwyibhwqpw'  # Replace with your Gmail password

    # Load the HTML email template
    with open('resq.html', 'r') as file:
        email_template = file.read()

    # Replace placeholders with user data
    email_template = email_template.replace('{{name}}', name)

    # Create a MIMEText object
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = email
    msg['Subject'] = 'Thank You for Contacting ResQ-Notify'

    # Attach the HTML email body
    msg.attach(MIMEText(email_template, 'html'))

    # Send the confirmation email using Gmail's SMTP server
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, email, msg.as_string())
        server.quit()
        print(f"Confirmation email sent successfully to {email}!")
    except Exception as e:
        print(f"Error sending confirmation email to {email}:", str(e))

if __name__ == "__main__":
    contact_data = fetch_contact_data()
    email_sent_to_user = fetch_email_sent_to_user()
    
    for data in contact_data:
        # Check if the data has already been sent
        if data not in email_sent_to_user:
            send_confirmation_email(data['email'], data['name'])
            # Add the data to the 'email_sent_to_user' collection in Firestore
            email_sent_to_user_ref = db.collection('resq_email_sent_to_user')
            email_sent_to_user_ref.add(data)
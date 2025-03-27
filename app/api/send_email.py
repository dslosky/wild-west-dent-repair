import boto3
client = boto3.client('ses', region_name='us-east-1')

def send_new_contact_email(name, email, phone, message):
    
    response = client.send_email(
    Destination={
        'ToAddresses': ['info@wildwestdentrepair.com']
    },
    Message={
        'Body': {
            'Text': {
                'Charset': 'UTF-8',
                'Data': f""""
New contact from: {name}
Email: {email}
Phone Number: {phone}

Message:
{message}
                """,
            }
        },
        'Subject': {
            'Charset': 'UTF-8',
            'Data': f'new contact - {name}',
        },
    },
    Source='contact@wildwestdentrepair.com'
    )
    
    print(response)

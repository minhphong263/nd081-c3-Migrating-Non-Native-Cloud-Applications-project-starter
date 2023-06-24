import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

    # TODO: Get connection to database
    host = 'phongvm.postgres.database.azure.com'
    database = 'techconfdb'
    user = 'phongvm'
    password = '1qaZ2wsX'
    sslmode = "require"

    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, database, password, sslmode)
    conn = psycopg2.connect(conn_string)
    
    try:
        # TODO: Get notification message and subject from database using the notification_id
        cur = conn.cursor()

        query = "SELECT message, subject FROM notification WHERE id = %s"
        cur.execute(query, (notification_id,))
        notification = cur.fetchone()

        notificaitonMessage = notification[0]
        notificaitonSubject = notification[1]

        query = "SELECT email, first_name FROM attendee"
        cur.execute(query)
        attendees = cur.fetchall()
        # TODO: Get attendees email and name

        # TODO: Loop through each attendee and send an email with a personalized subject
        for attendee in attendees:
            email = attendee[0]
            first_name = attendee[1]
            subject = '{}: {}'.format(first_name, notificaitonSubject)
            send_email(email, subject, notificaitonMessage)

        total_attendees_notified = "Notified " + str(len(attendees)) + " attendees"

        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        query = "UPDATE notification SET completed_date = CURRENT_DATE, status = %s WHERE id = %s"
        cur.execute(query, (total_attendees_notified, notification_id))
        
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        conn.close()

def send_email(email, subject, body):
    message = Mail(
            from_email="phongvm@outlook.com",
            to_emails=email,
            subject=subject,
            plain_text_content=body)

    sg = SendGridAPIClient("")
    sg.send(message)
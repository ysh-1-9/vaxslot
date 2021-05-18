import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from vaxslot import sender_email, server


def notify(districtID, sessions, users, centers):
    # go through the users in the (districtID,age)->list of users for every districtID and age
    #  for each districtID,age come up with 3 things - a> email in general likhna hai?, b> updates kya kya dene hai and c> newadditions kya kya batane hai
    # then for each districtID send (or don't) the respective email to all users from that category
    additions = []
    updates = []
    for x in sessions:
        if x.prevCap == 0:  # can get rid of createEmail and do what it does here only for better speed
            additions.append(x)
        elif x.prevCap!= x.currCap:
            updates.append(x)
    if len(updates) + len(additions) == 0:
        return

    s = createEmail(updates, additions, centers)

    bcc = users.keys()
    recipients = ', '.join(bcc)
    if len(bcc) !=0:
        print('Changes to slots for district ', districtID)
        print('Updates: ', updates)
        print('Additions: ', additions)
        print('Email: ', s)
        message = MIMEMultipart("alternative")
        message["Subject"] = "Vaccine Slots Available"
        message["From"] = sender_email
        message["To"] = 'yash@vaxslot.in'
        message['Bcc'] = recipients
        message.attach(MIMEText(s,'html'))
        server.send_message(message)


def createEmail(updates, additions, centerdeets):
    s = ""
    for x in updates:
        if x.centerID in centerdeets:
            s += "<tr>" + "<td>" + str(x.currCap) + "</td>" + "<td>" + x.date + "</td>" + "<td>" + str(x.age) + "</td>" + """<td width = "15%">""" + \
                 centerdeets[x.centerID].name + "</td>" + """<td width = "45%">""" + centerdeets[
                     x.centerID].address + "</td>" + "</tr>"
        else:
            print(x.centerID, 'Not in centerdict')

    for x in additions:
        if x.centerID in centerdeets:
            s += "<tr>" + "<td>" + str(x.currCap) +'  ' "</td>" + "<td>" + x.date + "</td>" + "<td>" + str(x.age) + "</td>" + """<td width = "15%">""" + \
                 centerdeets[x.centerID].name + "</td>" + """<td width = "45%">""" + centerdeets[
                     x.centerID].address + "</td>" + "</tr>"+'\n'
        else:
            print(x.centerID, 'Not in centerdict')

    return s


def send_test():
    s = 'Test Message 3'
    bcc = ['evilyash02@gmail.com','yash.dps@outlook.com','yash@vaxslot.in']
    recipients = ', '.join(bcc)

    message = MIMEMultipart("alternative")
    message["Subject"] = "Vaccine Slots Available"
    message["From"] = sender_email
    message["To"] = 'yash@vaxslot.in'
    message['Bcc'] = recipients
    message.attach(MIMEText(s, 'plain'))
    server.send_message(message)

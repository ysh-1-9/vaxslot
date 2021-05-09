def notify(districtID, sessions, users, centers):
    # go through the users in the (districtID,age)->list of users for every districtID and age
    #  for each districtID,age come up with 3 things - a> email in general likhna hai?, b> updates kya kya dene hai and c> newadditions kya kya batane hai
    # then for each districtID send (or don't) the respective email to all users from that category
    additions = []
    updates = []
    for x in sessions:
        if x.prevCap == 0:  # can get rid of createEmail and do what it does here only for better speed
            additions.append(x)
        else:
            updates.append(x)
    s = createEmail(updates, additions, centers)
    # send s

    pass


def createEmail(updates, additions, centerdeets):
    s = ""
    for x in updates:
        if x.centerID in centerdeets:
            s += "<tr>" + "<td>" + x.currCap + "</td>" + "<td>" + x.date + "</td>" + "<td>" + x.age + "</td>" + """<td width = "15%">""" + \
                 centerdeets[x.centerID].name + "</td>" + """<td width = "45%">""" + centerdeets[
                     x.centerID].address + "</td>" + "</tr>"

    for x in additions:
        if x.centerID in centerdeets:
            s += "<tr>" + "<td>" + x.currCap + "</td>" + "<td>" + x.date + "</td>" + "<td>" + x.age + "</td>" + """<td width = "15%">""" + \
                 centerdeets[x.centerID].name + "</td>" + """<td width = "45%">""" + centerdeets[
                     x.centerID].address + "</td>" + "</tr>"

    return s


def send():
    import smtplib, ssl

    port = 465  # For SSL
    password = 'toHmip-myvgoq-tyhka2'

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("vaxslottest@gmail.com", password)
        # TODO: Send email here
        sender_email = "vaxslottest@gmail.com"
        receiver_email = "yash@vaxslot.in"
        message = """\
        Subject: Hi there

        This message is sent from Python."""
        server.sendmail(sender_email, receiver_email, message)



send()
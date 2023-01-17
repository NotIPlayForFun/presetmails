import smtplib
import ssl
import my_error as mye
import config as cfg

def sendmail_simple(FROM, TO, SUBJECT, TEXT, USERNAME, PASSWORD, SMTP_SERVER, PORT = cfg.DEFAULT_PORT):
    MESSAGE = f'''From: {FROM}\nTo: {', '.join(TO)}\nSubject: {SUBJECT}\n\n{TEXT}'''.encode() #apparently cant just encode manually once
                                                                                            #you also wanna send html or other data or w/e
                                                                                            #so if you ever want to send more than just text,
                                                                                            #need to use email lib or EmailMessage API
                                                                                            #here to generate text (me thinks)

    #if not SMTP_SERVER:
    #    sys.stderr.write("Please enter valid SMTP_SERVER host")
    #    exit(1)

    #establish first connection (unsecure)
    try:
        server = smtplib.SMTP()                                 #changed to manual connect
        server._host = SMTP_SERVER
        resp = server.connect(host = SMTP_SERVER, port = PORT)
        print(f"SERVER: {server}")
        print(f'RESP: {resp}')
    except Exception as e:
        mye.eprint(e, 'Could not connect to server using this input:', [['SMTP_HOST (mailserver)', SMTP_SERVER], ['PORT', PORT]])
        raise  

    #secure connection with tls
    context = ssl.create_default_context()
    try:
        server.starttls(context = context)
    except Exception as e:
        mye.eprint(e, 'Could not secure connection to server using this input:', ('SMTP_HOST (mailserver)', SMTP_SERVER), ('PORT', PORT), ('context:', context))
        raise e
    #log into server
    try:
        server.login(USERNAME, PASSWORD)
    except Exception as e:
        mye.eprint(e, 'Login to mailserver failed')
        raise e

    server.set_debuglevel(1)

    #send mail
    try:
        print(FROM)
        print(TO)
        print(MESSAGE)
        SendErrs = server.sendmail(FROM, TO, MESSAGE)
    except Exception as e:
        print("Error sending mail")
        mye.eprint(e, "Error sending mail, probably incorrect message format/encoding/..."
        , [["FROM", FROM], ["TO", TO], ["MESSAGE", MESSAGE]])
        raise e
    #close connection
    server.quit()

    #return dictionary of rejected messages: { "receiver" : ( ERRORCODE ,"REASON" ) }
    return SendErrs
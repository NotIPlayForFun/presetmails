import smtplib
import ssl
import my_error as mye
import config as cfg

def sendmail_simple(FROM, TO, SUBJECT, TEXT, USERNAME, PASSWORD, SMTP_SERVER, PORT = cfg.DEFAULT_PORT):
    MESSAGE = f'''From: {FROM}\nTo: {TO}\nSubject: {SUBJECT}\n\n{TEXT}'''

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
        mye.eprint(e, 'Could not connect to server using this input:', ['SMTP_HOST (mailserver)', SMTP_SERVER], ['PORT', PORT])
        exit(1)        

    #secure connection with tls
    context = ssl.create_default_context()
    try:
        server.starttls(context = context)
    except Exception as e:
        mye.eprint(e, 'Could not secure connection to server using this input:', ('SMTP_HOST (mailserver)', SMTP_SERVER), ('PORT', PORT), ('context:', context))
        exit(1)
    #log into server
    server.login(USERNAME, PASSWORD)

    server.set_debuglevel(1)

    #send mail
    SendErrs = server.sendmail(FROM, TO, MESSAGE)

    #close connection
    server.quit()

    #return dictionary of rejected messages: { "receiver" : ( ERRORCODE ,"REASON" ) }
    return SendErrs
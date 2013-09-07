from flask import Flask, request, redirect
import twilio.twiml

import re, httplib

app = Flask(__name__)
 
CONFIRM_TYPE = 'confirm'
AUTOREPLY_TYPE = 'yes'
OTHER_TYPE = 'other'

@app.route("/", methods=['GET', 'POST'])
def respond():
    """Respond to incoming calls with a simple text message."""

    # Prepare response
    resp = twilio.twiml.Response()

    # Get sender's number and the body of their text
    from_number = request.values.get('From', None)
    body = request.values.get('Body', None)
    
    # See if they are replying to confirm their number
    if regex(CONFIRM_TYPE, body):
        resp.sms("Confirmed!")
        connectToScriptDb(from_number, CONFIRM_TYPE)
    elif regex(AUTOREPLY_TYPE, body):
        resp.sms("Autoreply sent!")
        connectToScriptDb(from_number, AUTOREPLY_TYPE)
    elif regex(OTHER_TYPE, body):
        resp.sms("Custom autoreply sent!")
        connectToScriptDb(from_number, OTHER_TYPE, body)
    else:
        resp.sms(body)
    
    return str(resp)

def regex(phrase, body):
    """Check if a given phrase is contained in a body of text (case insensitive)"""
    regex = re.compile(phrase, re.IGNORECASE)
    found = regex.findall(body)
    return len(found) > 0

def connectToScriptDb(number, msg_type, msg = None):
    # Connect to server
    httpServ = \
    httplib.HTTPConnection("script.google.com", 80)
    httpServ.connect()

    # Send Get html request
    httpServ.request('GET',
        '/macros/s/AKfycbxvQ_b8bf6gr_6vvIsO5w9B30LJoAm_5G5JrZWykoFw0fCdHBw/exec&type=' + msg_type + '&number=' + number)
    
    # Wait for response
    response = httpServ.getresponse()
    if response.status == httplib.OK:
        print "Output from GET request"
        print "========================="
        print response.read()

    httpServe.close()

if __name__ == "__main__":
    app.run(debug=True)
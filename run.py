from flask import Flask, request, redirect
import twilio.twiml

import re

app = Flask(__name__)
 
@app.route("/", methods=['GET', 'POST'])
def respond():
    """Respond to incoming calls with a simple text message."""

    # Prepare response
    resp = twilio.twiml.Response()

    # Get sender's number and the body of their text
    from_number = request.values.get('From', None)
    body = request.values.get('Body', None)
    
    # See if they are replying to confirm their number
    regex = re.compile("confirm", re.IGNORECASE)
    found = regex.findall(body)
    if len(found) > 0:
        resp.sms("Confirmed!")
    else:
        resp.sms(body)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
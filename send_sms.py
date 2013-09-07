# Download the Python helper library from twilio.com/docs/python/install
from twilio.rest import TwilioRestClient
 
# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "AC0073eed6d4f0255009df0abe8479072f"
auth_token  = "49a1207bd03e354adeb466835233e6db"
client = TwilioRestClient(account_sid, auth_token)
 
message = client.sms.messages.create(body="Hello!",
    to="+14013741842",
    from_="+17324973872")
print message.sid

sagefrom flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
app = Flask(__name__)
@app.route("/incoming", methods=['POST'])
def incoming():
    body=request.values.get("Body","").lower()
    resp=MessagingResponse()
    if body =="hi":
    	resp.message("Hi! I'm here to help you.Please make a choice :\n1. New voter\n2.Existing voter")
    elif body=="1":
    	resp.message("you chose New voter.Redirecting you to the New Voter registration website.")
    	resp.message("https://voters.eci.gov.in")
    elif body =="2":
    	resp.message("yoi chose  existing voter.Redirecting you to Existing voter login website.")
    	resp.message("https://electorlsearch.eci.gov.in")
    else:
    	resp.message("invalid choice.Please enter  for new voter or  for existing voter.")
  
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

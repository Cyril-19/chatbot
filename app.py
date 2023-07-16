from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "chatbot"

@app.route("/", methods=["POST"])
def incoming():
    body = request.values.get("Body", "").lower()
    resp = MessagingResponse()

    if body == "hi":
        session.clear()
        resp.message("Hi! I'm here to help you. Please make a choice by typing the option or first letter:\nNew Voter - Type 'N'\nExisting Voter - Type 'E'")
    elif body.lower() == "n" or body.lower() == "new voter":
        session["choice"] = "new_voter"
        resp.message("You chose New Voter. Please select an option:\nA) Am I eligible?\nB) Registration\nC) Already registered")
    elif body.lower() == "e" or body.lower() == "existing voter":
        session["choice"] = "existing_voter"
        resp.message("You chose Existing Voter. Please make a choice by typing the option or first letter\nInformation - Type 'I'\nServices - Type 'S'")
    elif session.get("choice") == "new_voter":
        resp = handle_new_voter(body)
    elif session.get("choice") == "existing_voter":
        resp = handle_existing_voter(body)
    else:
        resp.message("Invalid choice. Please enter 'hi' to start a new chat or 'end' to exit.")

    return str(resp)


def handle_new_voter(body):
    resp = MessagingResponse()

    if body.lower() == "a" or body.lower() == "am i eligible?":
        resp.message("Please enter your date of birth (format: DD/MM/YYYY):")
        session["step"] = "verify_age"
    elif session.get("step") == "verify_age" and "/" in body:
        dob = body
        age = calculate_age(dob)
        if age is not None:
            if age >= 18:
                resp.message("You are eligible to vote.")
                resp.message("Redirecting you to the registration website.\n'https://voters.eci.gov.in'")
            else:
                resp.message("You are not eligible to vote. You must be at least 18 years old.")
            resp.message("Please enter 'hi' to start a new chat or 'end' to exit.")
        else:
            resp.message("Invalid date of birth format. Please try again. Please enter 'hi' to start a new chat")
        session.clear() 
    elif body.lower() == "b" or body.lower() == "registration":
        resp.message("Redirecting you to the registration website.\n'https://voters.eci.gov.in'")
        resp.message("Please enter 'hi' to start a new chat or 'end' to exit.")
    elif body.lower() == "c" or body.lower() == "already registered-track your application":
        resp.message("Redirecting you to the already registered website.\n'https://voters.eci.gov.in'")
        resp.message("Please enter 'hi' to start a new chat or 'end' to exit.")
    else:
        resp.message("Invalid choice. Please enter 'hi' to start a new chat or 'end' to exit.")

    return resp



def handle_existing_voter(body):
    resp = MessagingResponse()

    if body.lower() == "information" or body.lower() == "i":
        resp.message("You selected 'Information'. Enter the corresponding number or type your choice. Please choose an option:\n1.1) Voter List\n1.2) Download EPIC\n1.3) PwD (Saksham App)\n1.4) Know Your Candidate\n1.5) Know Your Electoral Ecosystem (BLO, ERO, DEO, Polling Station)\n1.6) Complaints")
        session["step"] = "existing_info"
    elif session.get("step") == "existing_info":
        if body.lower() == "1.1" or body.lower() == "voter list":
            resp.message("Redirecting you to the Voter List website.\n'https://electoralsearch.eci.gov.in/'")
            session.clear()
        elif body.lower() == "1.2" or body.lower() == "download epic":
            resp.message("Redirecting you to the Download EPIC website.\n'https://voters.eci.gov.in'")
            session.clear()
        elif body.lower() == "1.3" or body.lower() == "pwd (saksham app)":
            resp.message("Redirecting to the PwD (Saksham App) website.")
            resp.message("Android: 'https://play.google.com/store/apps/details?id=pwd.eci.com.pwdapp&hl=en&gl=US'")
            resp.message("iOS: 'https://apps.apple.com/in/app/saksham-eci/id1497864568'")
            session.clear()
        elif body.lower() == "1.4" or body.lower() == "know your candidate":
            resp.message("Redirecting you to the Know Your Candidate website.\n'https://eci.gov.in/it-applications/mobile-applications/%E2%80%98know-your-candidate%E2%80%99-mobile-application-r62/")
            session.clear()
        elif body.lower() == "1.5" or body.lower() == "know your electoral ecosystem (blo, ero, deo, polling station)":
            resp.message("Redirecting you to the Know Your Electoral Ecosystem website.\n'https://example.com/electoral_ecosystem'")
            session.clear()
        elif body.lower() == "1.6" or body.lower() == "complaints":
            resp.message("You selected 'Complaints'. Please choose an option:\n1.7) Voter Portal\n1.8) Grievance Portal\n1.9) Toll-Free Number\n1.10) C-Vigil App")
            session["step"] = "complaints"
        else:
            resp.message("Invalid choice. Please enter 'hi' to start a new chat or 'end' to exit.")
            session.clear()
    elif session.get("step") == "complaints":
        if body.lower() == "1.7" or body.lower() == "voter portal":
            resp.message("Redirecting you to the Voter Portal website.\n'https://voterportal.eci.gov.in/'")
            session.clear()
        elif body.lower() == "1.8" or body.lower() == "grievance portal":
            resp.message("Redirecting you to the Grievance Portal website.\n'https://eci-citizenservices.eci.nic.in/'")
            session.clear()
        elif body.lower() == "1.9" or body.lower() == "toll-free number":
            resp.message("Call: 1950\nSend SMS: 1950 (Format: <ECI> <EPIC NO>)")
            resp.message("Please enter 'hi' to start a new chat or 'end' to exit.")
            session.clear()
        elif body.lower() == "1.10" or body.lower() == "c-vigil app":
            resp.message("Redirecting you to the C-Vigil App (for Android and iOS).")
            resp.message("Android:'https://play.google.com/store/apps/details?id=in.nic.eci.cvigil&hl=en&gl=US'")
            resp.message("iOS:'https://apps.apple.com/in/app/cvigil/id1455719541'")
            session.clear()
        else:
            resp.message("Invalid choice. Please enter 'hi' to start a new chat or 'end' to exit.")
            session.clear()
    elif body.lower() == "services" or body.lower() == "s":
        resp.message("You selected 'Services'. Enter the corresponding number or type your choice. Please choose an option:\n2.1) Entry Correction (Form 8)\n2.2) Shift of Residence (Migration Form 8)\n2.3) Duplicate EPIC\n2.4) Marking of PwD (Form 8)\n2.5) Voter List Name Deletion (Form 7)\n2.6) Aadhar Linking with EPIC or Voter Card Number (Form 6)")
        session["step"] = "existing_services"
    elif session.get("step") == "existing_services":
        if body.lower() == "2.1" or body.lower() == "entry correction (form 8)":
            resp.message("Redirecting you to the Entry Correction (Form 8) website.\'https://voters.eci.gov.in'")
            resp.message("Please enter 'hi' to start a new chat or 'end' to exit.")
            session.clear()
        elif body.lower() == "2.2" or body.lower() == "shift of residence (migration form 8)":
            resp.message("Redirecting you to the Shift of Residence (Migration Form 8) website.\n<'https://voters.eci.gov.in'")
            resp.message("Please enter 'hi' to start a new chat or 'end' to exit.")
            session.clear()
        elif body.lower() == "2.3" or body.lower() == "duplicate epic":
            resp.message("Redirecting you to the Duplicate EPIC website.\n'https://voters.eci.gov.in'")
            resp.message("Please enter 'hi' to start a new chat or 'end' to exit.")
            session.clear()
        elif body.lower() == "2.4" or body.lower() == "marking of pwd (form 8)":
            resp.message("Redirecting you to the Marking of PwD (Form 8) website.\n'https://voters.eci.gov.in'")
            resp.message("Please enter 'hi' to start a new chat or 'end' to exit.")
            session.clear()
        elif body.lower() == "2.5" or body.lower() == "voter list name deletion (form 7)":
            resp.message("Redirecting you to the Voter List Name Deletion (Form 7) website.\n<'voters.eci.gov.in'")
            resp.message("Please enter 'hi' to start a new chat or 'end' to exit.")
            session.clear()
        elif body.lower() == "2.6" or body.lower() == "aadhar linking with epic or voter card number (form 68)":
            resp.message("Redirecting you to the Aadhar Linking with EPIC or Voter Card Number (Form 6) website.\n'voters.eci.gov.in'")
            resp.message("Please enter 'hi' to start a new chat or 'end' to exit.")
            session.clear()
        else:
            resp.message("Invalid choice. Please enter 'hi' to start a new chat or 'end' to exit.")
            session.clear()

    return resp




def calculate_age(dob):
    try:
        birth_date = datetime.strptime(dob, "%d/%m/%Y")
        today = datetime.today()
        age = today.year - birth_date.year

        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1

        return age
    except ValueError:
        return None

if __name__ == "__main__":
    app.run(debug=True, port=5001)


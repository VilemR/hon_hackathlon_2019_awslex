import time
import os
import logging
from datetime import datetime, timedelta

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def build_response(message):
    return {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": message
            }
        }
    }


def build_response_wifi_summary(message):
    return {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": "The WiFi permissions temporarily granted. In order to set up WiFi connection use parameters below.  This infrmation has been sent by email to your inbox for further reference."
                # message
            }
            ,
            'responseCard': {
                'version': 1,
                'contentType': 'application/vnd.amazonaws.card.generic',
                'genericAttachments': [
                    {
                        'title': "WIFI NETWORK ACCESS DETAIL",
                        'subTitle': message,
                        'imageUrl': "https://www.brandsfortheworld.com/upload/images/modules/bftw/brands/original/60397-honeywell-logo-30x9.png"
                    }
                ]
            }
        }
    }


def build_response_taxi_summary(message):
    return {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": "The trip is about to be arranged for you. See detail below. Please confirm to book taxi."
            }
            ,
            'responseCard': {
                'version': 1,
                'contentType': 'application/vnd.amazonaws.card.generic',
                'genericAttachments': [
                    {
                        'title': "HONEYWEL TAXI ONLINE BOOKING",
                        'subTitle': message,
                        'imageUrl': "https://dcassetcdn.com/design_img/248800/25902/25902_2456375_248800_image.jpg",
                        "buttons": [
                            {
                                "text": "Book",
                                "value": "taxi_booked"
                            }
                        ]

                    }
                ]
            }
        }
    }


def build_response_place_summary(message):
    return {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": message
            }
            ,
            'responseCard': {
                'version': 1,
                'contentType': 'application/vnd.amazonaws.card.generic',
                'genericAttachments': [
                    {
                        'title': "HONEYWELL CONTACT DETAIL",
                        'subTitle': 'Scan to save contact into your phone.',
                        'imageUrl': "https://uqr.me/wp-content/uploads/2014/04/free_qr_code_generator.businesscards-770x770.jpg",
                        "buttons": [
                            {
                                "text": "Navigate",
                                "value": "start_navigation"
                            }
                        ]

                    }
                ]
            }
        }
    }


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


def confirm_intent(session_attributes, intent_name, slots, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ConfirmIntent',
            'intentName': intent_name,
            'slots': slots,
            'message': {
                'contentType': 'PlainText',
                'content': message
            }
        }
    }


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': {
                'contentType': 'PlainText',
                'content': message
            }
        }

    }


def elicit_slot_card(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': {
                'contentType': 'PlainText',
                'content': message
            }
            ,
            'responseCard': {
                'version': 1,
                'contentType': 'application/vnd.amazonaws.card.generic',
                'genericAttachments': [
                    {
                        'title': "WIFI NETWORK ACCESS MANAGER",
                        'subTitle': 'Please provide your HID/EID',
                        'imageUrl': "https://www.brandsfortheworld.com/upload/images/modules/bftw/brands/original/60397-honeywell-logo-30x9.png",
                    }
                ]
            }
        }
    }


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def isvalid_hid_honeywell(hid_input):
    hid_input = "" + hid_input.upper()
    if not ((hid_input[0] == "H") or (hid_input[0] == "E")):
        print("Shit " + hid_input[0])
        return False
    if not (len(hid_input) == 7):
        return False
    if not (represents_int(hid_input[1:])):
        return False
    return True


def isvalid_hid_num(hid_input):
    hid_input = "" + hid_input.upper()
    if not (len(hid_input) == 6):
        return False
    if not (represents_int(hid_input)):
        return False
    return True


def handle_wifi_intent(intent_request):
    logger.debug(
        'handle_main_intent userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']))
    source = intent_request['invocationSource']
    output_session_attributes = intent_request['sessionAttributes'] if intent_request[
                                                                           'sessionAttributes'] is not None else {}
    slots = intent_request['currentIntent']['slots']
    HID = slots['userIdValue']
    logger.debug(
        'handle_wifi_intent >>>  userId={}, intentName={}, userIdValue={}'.format(intent_request['userId'],
                                                                                  intent_request['currentIntent'][
                                                                                      'name'], HID))
    output_session_attributes['procedure'] = 'handle_wifi_intent'
    if HID != None:
        output_session_attributes['hid-valid'] = 'HID!=None (OK)'
        if not isvalid_hid_num(HID):
            output_session_attributes['hid-valid'] = 'HID-INVALID (Error)'
            return elicit_slot(output_session_attributes, 'getWiFiAccess', slots, 'userIdValue',
                               "HID " + HID + " je nespravne. Prosim zadejte spravne HID ve formatu NNNNNN (example(546578)")
        else:
            output_session_attributes['hid-valid'] = 'HID-VALID (OK)'
    else:
        output_session_attributes['hid-valid'] = 'HID == None (Error)'
    if source == 'DialogCodeHook':
        output_session_attributes['sub-step'] = 'DialogCodeHook'
        return delegate(output_session_attributes, slots)
    if source == 'FulfillmentCodeHook':
        output_session_attributes['sub-step'] = 'FulfillmentCodeHook'
        tomorrow = datetime.now() + timedelta(hours=24)
        return build_response_wifi_summary(
            'Username:' + HID + ', passw ****, SSID GUEST.Expiration:' + tomorrow.strftime("%d-%b-%Y (%H:%M)"))


def handle_main_intent(intent_request):
    source = intent_request['invocationSource']
    output_session_attributes = intent_request['sessionAttributes'] if intent_request[
                                                                           'sessionAttributes'] is not None else {}
    slots = intent_request['currentIntent']['slots']
    output_session_attributes['procedure'] = 'handle_main_intent'
    if source == 'DialogCodeHook':
        output_session_attributes['sub-step'] = 'DialogCodeHook (M)'
        return delegate(output_session_attributes, slots)
    if source == 'FulfillmentCodeHook':
        output_session_attributes['sub-step'] = 'FulfillmentCodeHook (M)'
        direction = "" + slots['navWelcomeHelpSubject']
        if direction.upper() == "wifi".upper():
            msg = "In order to grant you access please provide valid HID number."
            return elicit_slot(output_session_attributes, 'getWiFiAccess', None, 'userIdValue', msg)
        elif direction.upper() == "taxi".upper():
            msg = "In order to arrange booking please provide required details."
            return elicit_slot(output_session_attributes, 'orderTaxi', None, 'userIdValue', msg)
        elif direction.upper() == "place".upper():
            msg = "In order to find employee please provide enter Name or Surname."
            return elicit_slot(output_session_attributes, 'findPlace', None, 'employeeName', msg)
        # return elicit_slot_card(output_session_attributes, 'getWiFiAccess', None, 'userIdValue', msg)
        return elicit_slot(output_session_attributes, 'mainIntent', None, 'navWelcomeHelpSubject',
                           "Ups,...what a terrible failure (WTF). Let's go back to trees!")


def handle_taxi_intent(intent_request):
    logger.debug(
        'handle_main_intent userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']))
    source = intent_request['invocationSource']
    output_session_attributes = intent_request['sessionAttributes'] if intent_request[
                                                                           'sessionAttributes'] is not None else {}
    slots = intent_request['currentIntent']['slots']
    HID = slots['userIdValue']
    logger.debug(
        'handle_wifi_intent >>>  userId={}, intentName={}, userIdValue={}'.format(intent_request['userId'],
                                                                                  intent_request['currentIntent'][
                                                                                      'name'], HID))
    output_session_attributes['procedure'] = 'handle_taxi_intent'
    if HID != None:
        output_session_attributes['hid-valid'] = 'HID!=None (OK)'
        if not isvalid_hid_num(HID):
            output_session_attributes['hid-valid'] = 'HID-INVALID (Error)'
            return elicit_slot(output_session_attributes, 'getWiFiAccess', slots, 'userIdValue',
                               "HID " + HID + " je nespravne. Prosim zadejte spravne HID ve formatu NNNNNN (example(546578)")
        else:
            output_session_attributes['hid-valid'] = 'HID-VALID (OK)'
    else:
        output_session_attributes['hid-valid'] = 'HID == None (Error)'
    if source == 'DialogCodeHook':
        output_session_attributes['sub-step'] = 'DialogCodeHook'
        return delegate(output_session_attributes, slots)
    if source == 'FulfillmentCodeHook':
        fromPlace = slots['fromWhere']
        toPlace = slots['toWhere']
        timePickup = slots['whatTime']
        output_session_attributes['sub-step'] = 'FulfillmentCodeHook'
        return build_response_taxi_summary(
            'Pickup time:' + timePickup + ', ' + fromPlace + '->' + toPlace + ',fare 3500Kc.')


def handle_place_intent(intent_request):
    logger.debug(
        'handle_main_intent userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']))
    source = intent_request['invocationSource']
    output_session_attributes = intent_request['sessionAttributes'] if intent_request[
                                                                           'sessionAttributes'] is not None else {}
    slots = intent_request['currentIntent']['slots']
    HID = slots['employeeName']
    output_session_attributes['procedure'] = 'handle_place_intent'
    if HID != None:
        output_session_attributes['hid-valid'] = 'HID!=None (OK)'
        person = get_employee_detail(HID)
    else:
        output_session_attributes['hid-valid'] = 'employeeName == None (Error)'

    if source == 'DialogCodeHook':
        output_session_attributes['sub-step'] = 'DialogCodeHook'
        return delegate(output_session_attributes, slots)
    if source == 'FulfillmentCodeHook':
        output_session_attributes['sub-step'] = 'FulfillmentCodeHook'
        return build_response_place_summary(
            "Contact " + person['Name'] + ' ' + person['Surname'] + ', location ' + person['Location'])


def dispatch(intent_request):
    intent_name = intent_request['currentIntent']['name']
    if intent_name == 'mainIntent':
        response = handle_main_intent(intent_request)
    elif intent_name == 'findPlace':
        response = handle_place_intent(intent_request)
    elif intent_name == 'getWiFiAccess':
        response = handle_wifi_intent(intent_request)
    elif intent_name == 'orderTaxi':
        response = handle_taxi_intent(intent_request)
    else:
        raise Exception('Intent with name ' + intent_name + ' not supported')
    return response


def lambda_handler(event, context):
    logger.debug(
        '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    logger.debug(
        'lambda_handler event={}'.format(event))
    logger.debug(
        '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    response = dispatch(event)
    logger.debug(
        'lambda_handler response={}'.format(response))
    logger.debug(
        '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    return response


hid_db = [
    {'hid': ' 000000',
     'user': 'John Doe'},
    {'hid': ' 000001',
     'user': 'Johny Malcome'},
    {'hid': ' Alice Mahony',
     'user': 'Julia Bloom'},
    {'hid': ' 000003',
     'user': 'Alex Rot'},
    {'hid': ' 306101',
     'user': 'Willem Rezn'},
]


def get_user_name(hid):
    for user in hid_db:
        if user['hid'] == hid:
            return user['user']
    return 'unknown_user'


def get_employee_detail(search):
    employees = db_employees
    for employee in employees:
        if search.upper() in employee['Surname'].upper() or search.upper() in employee['Name'].upper():
            return employee
    return None


db_employees = [
    {
        "Surname": "Stuart",
        "Name": "John",
        "Phone": "(01) 2223 5891",
        "Email": "Donec.at.arcu@aptenttacitisociosqu.co.uk",
        "Location": "B-3.0081",
        "Building": "B",
        "Floor": 3,
        "Seat": 81
    },
    {
        "Surname": "Pollard",
        "Name": "Aidan",
        "Phone": "(01) 4297 6430",
        "Email": "dictum.eleifend.nunc@et.co.uk",
        "Location": "D-1.0056",
        "Building": "D",
        "Floor": 1,
        "Seat": 56
    },
    {
        "Surname": "Sandymall",
        "Name": "Sarah",
        "Phone": "(09) 1265 5845",
        "Email": "mollis.vitae@rutrumeuultrices.com",
        "Location": "A-2.0033",
        "Building": "A",
        "Floor": 2,
        "Seat": 33
    },
    {
        "Surname": "Sanders",
        "Name": "Alden",
        "Phone": "(02) 5593 4048",
        "Email": "Maecenas.libero.est@ataugueid.edu",
        "Location": "B-4.0082",
        "Building": "B",
        "Floor": 4,
        "Seat": 82
    },
    {
        "Surname": "Gardner",
        "Name": "Alexandra",
        "Phone": "(05) 9404 0614",
        "Email": "per.inceptos.hymenaeos@Nunc.com",
        "Location": "C-3.0008",
        "Building": "C",
        "Floor": 3,
        "Seat": 8
    },
    {
        "Surname": "Jackson",
        "Name": "Alexandra",
        "Phone": "(03) 9206 5515",
        "Email": "mi.lorem@enimEtiam.com",
        "Location": "A-3.0098",
        "Building": "A",
        "Floor": 3,
        "Seat": 98
    },
    {
        "Surname": "Graham",
        "Name": "Amanda",
        "Phone": "(09) 3045 5949",
        "Email": "elit@sempereratin.co.uk",
        "Location": "D-4.0011",
        "Building": "D",
        "Floor": 4,
        "Seat": 11
    },
    {
        "Surname": "Rivers",
        "Name": "Amery",
        "Phone": "(01) 2284 1019",
        "Email": "dolor@elit.net",
        "Location": "A-4.0037",
        "Building": "A",
        "Floor": 4,
        "Seat": 37
    },
    {
        "Surname": "Gillespie",
        "Name": "Angela",
        "Phone": "(02) 0379 1384",
        "Email": "sapien@mollisnoncursus.org",
        "Location": "C-3.0031",
        "Building": "C",
        "Floor": 3,
        "Seat": 31
    },
    {
        "Surname": "Solis",
        "Name": "Arden",
        "Phone": "(07) 5795 6802",
        "Email": "varius.ultrices@elitAliquam.edu",
        "Location": "B-4.0015",
        "Building": "B",
        "Floor": 4,
        "Seat": 15
    },
    {
        "Surname": "Carrillo",
        "Name": "Arthur",
        "Phone": "(09) 9974 7385",
        "Email": "adipiscing.lacus@urna.org",
        "Location": "C-1.0078",
        "Building": "C",
        "Floor": 1,
        "Seat": 78
    },
    {
        "Surname": "Burns",
        "Name": "Barclay",
        "Phone": "(06) 7291 4607",
        "Email": "molestie.tortor@enimSuspendissealiquet.ca",
        "Location": "A-3.0041",
        "Building": "A",
        "Floor": 3,
        "Seat": 41
    },
    {
        "Surname": "Mcbride",
        "Name": "Barry",
        "Phone": "(08) 9456 6564",
        "Email": "arcu@pharetraNamac.com",
        "Location": "B-3.0069",
        "Building": "B",
        "Floor": 3,
        "Seat": 69
    }
]

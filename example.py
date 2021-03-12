import logging
import sys

import smpplib.client
import smpplib.consts
import smpplib.gsm

HOST = 'abcd.com'
PORT = 2260
SYSTEM_ID = 'login'
PASSWORD = 'password'
FROM_PHONE_NUM = '9898989898989'
TO_PHONE_NUM = '5446545645645456'

# if you want to know what's happening
logging.basicConfig(level='DEBUG')

# Two parts, UCS2, SMS with UDH
parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(u'Привет мир!\n'*10)

client = smpplib.client.Client(
    host=HOST,
    port=PORT
)

# Print when obtain message_id
client.set_message_sent_handler(
    lambda pdu: sys.stdout.write('sent {} {}\n'.format(pdu.sequence, pdu.message_id)))
client.set_message_received_handler(
    lambda pdu: sys.stdout.write('delivered {}\n'.format(pdu.receipted_message_id)))

client.connect()
client.bind_transceiver(system_id=SYSTEM_ID, password=PASSWORD)

for part in parts:
    pdu = client.send_message(
        source_addr_ton=smpplib.consts.SMPP_TON_INTL,
        #source_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
        # Make sure it is a byte string, not unicode:
        source_addr=bytes(FROM_PHONE_NUM, 'utf-8'),

        dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
        #dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
        # Make sure thease two params are byte strings, not unicode:
        destination_addr=bytes(TO_PHONE_NUM, 'utf-8'),
        short_message=part,

        data_coding=encoding_flag,
        esm_class=msg_type_flag,
        registered_delivery=True,
    )
    print(pdu.sequence)
    
# Enters a loop, waiting for incoming PDUs
client.listen()

# You also may want to listen in a thread:

# from threading import Thread

# t = Thread(target=client.listen)
# t.start()

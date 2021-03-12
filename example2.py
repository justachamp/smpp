import os

import smpplib
from smpplib import consts, gsm

HOST = '192.196.264.5'
PORT = 2266
SYSTEM_ID = 'login'
PASSWORD = 'password'
SOURCE_ADDRESS = 998979998899
client = smpplib.client.Client(HOST, PORT)


def check():
    client.connect()
    client.bind_transceiver(system_id=SYSTEM_ID, password=PASSWORD)
    client.disconnect()


def send(phone_number, message):
    client.connect()
    client.bind_transceiver(system_id=SYSTEM_ID, password=PASSWORD)
    parts, encoding_flag, msg_type_flag = gsm.make_parts(message)
    for part in parts:
        client.send_message(
            source_addr_ton=smpplib.consts.SMPP_TON_ALNUM,
            source_addr_npi=smpplib.consts.SMPP_NPI_UNK,
            source_addr=SOURCE_ADDRESS,

            dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
            dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
            destination_addr=phone_number,
            short_message=part,

            data_coding=encoding_flag,
            esm_class=msg_type_flag,
            registered_delivery=True,
        )

    client.disconnect()

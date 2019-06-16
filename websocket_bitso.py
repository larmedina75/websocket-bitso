# websocket_bitso.py
# An example to use the Bitso's websocket API to get the transactions of several books (pairs)
#
# Autor : Luis Armando Medina Avitia @larmedina
# E-mail: lamedina@gmail.com
# Date  : 2019-06-16 
#

import os, sys
import websocket
import _thread as thread
import time
import json

def on_message(ws, message):
    data_message = json.loads(message)
    if data_message['type'] == 'ka':
        pass
    elif 'action' in data_message.keys():
        print(data_message)
    elif data_message['type'] == 'trades':
        book = data_message['book'].split("_")
        print('[{}] {} {} @ {} {} = {} {}'.format(
            data_message['payload'][0]['i'],
            data_message['payload'][0]['a'],
            book[0].upper(),
            data_message['payload'][0]['r'],
            book[1].upper(),
            data_message['payload'][0]['v'],
            book[1].upper(),
            ))
        # Here, you can add the current rate value (r) to any table, control or monitor of a book (pair)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    # you can setup as many books (pairs) like you need
    book=[]
    book.append({ "action": "subscribe", "book": "btc_mxn", "type": "trades" })
    book.append({ "action": "subscribe", "book": "xrp_mxn", "type": "trades" })
    book.append({ "action": "subscribe", "book": "bat_mxn", "type": "trades" })
    # set suscrptions
    ws.send(json.dumps(book[0]))
    ws.send(json.dumps(book[1]))
    ws.send(json.dumps(book[2]))
    time.sleep(1)

def runf(*args):
    websocket.enableTrace(True)
    # set the socket URI to connect
    ws = websocket.WebSocketApp("wss://ws.bitso.com",
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

def start_transactions():
    # starting websocket thread
    thread.start_new_thread(runf, ())
    print('Press "q" to exit ... ')
    # start control loop
    while True:
        # you can use this loop for miselaneus operations
        pass
        

if __name__ == '__main__':
    start_transactions()

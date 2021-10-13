from pubsub import pub

def listener(message):
    print("Function listener received:")
    print(arg1)

while True:
    pub.subscribe(listener, 'log.sent')
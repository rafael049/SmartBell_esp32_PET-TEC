import socket
import sys
from machine import Pin

# class for representing a button
class Button():
    def __init__(self, pin_number):
        self.p = Pin(pin_number, Pin.IN)
        self.last_state = self.p.value()
        
    def is_being_pressed(self):
        last_state = self.last_state
        cur_state = self.p.value()
        self.last_state = cur_state
        
        if last_state == 0 and cur_state == 1:
            return True
        else:
            return False
    
    def is_pressed(self):
        if self.p.value() == 1:
            return True
        
    def is_being_released(self):
        last_state = self.last_state
        cur_state = self.p.value()
        self.last_state = cur_state
        
        if last_state == 1 and cur_state == 0:
            return True
        else:
            return False 

def connect_wifi(ssid, senha):
    import network

    wlan = network.WLAN(network.STA_IF)
    
    if not wlan.active():
        wlan.active(True)
        wlan.connect(ssid, senha)


def main():
    ssid = "Nome Wifi"
    passwd = "Senha Wifi"
    # pino do botao
    pin = 4  # D4
    # Server port
    porta = 2525
    # Message to send to the app
    msg = "DINGDONG"
    
    # connect to wifi
    connect_wifi(ssid, passwd)

    # create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # create server
        sock.bind(('0.0.0.0', porta))
       
        sock.listen(100000)

        print("Servidor na porta ", porta)
        
        # TODO make more than one clinet connect at the same time
        
        # wait for connection
        print("Aguardando coneccao")
        (connection, address) = sock.accept()
        print("Accepted a connection from %s:%s" % (address[0],address[1]))
        
        button = Button(pin)
        
        while True:
            # if button is pressed send message to client
            if button.is_being_pressed():
                print("button pressed!")
                connection.sendall(msg.encode())
                
    except KeyboardInterrupt:
        sock.close()
    else:
        sock.close()
    
main()

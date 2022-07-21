# Universidad de Costa Rica  |  Equipo Layer 8
# Clase ReceptionSocket para comunicarse con multiples clientes

import sys
import threading

from Classes.tcp_server import TCPServer

class ReceptionSocket(TCPServer):
    ''' A simple TCP Server for handling multiple clients '''

    def __init__(self, host, port):
        ''' Constructor '''
        TCPServer.__init__(self, host, port)
        
    def save_operations(self, operation):
        ''' Save operations en local storage '''

        if self.disk.pages[0].pos is None:
            saved_operation = str(operation)
        elif self.disk.pages[0].pos < 0:
            saved_operation = str(operation) + self.disk.pages[0].temp
        elif self.disk.pages[0].pos >= 0:
            saved_operation = self.disk.pages[0].temp + str(operation)
            
        with open('storage.txt', 'a') as File:  
            File.write(saved_operation+'\n')
        

    def wait_for_client(self):
        ''' Wait for clients to connect '''

        try:
            self.printwt('Listening for incoming connection')
            self.sock.listen(10) # 10 clients before server refuses connections

            while True:
                data = self.sock.accept()
                self.printwt(f'Accepted connection from {data[1]}')
                c_thread = threading.Thread(target = self.handle_client,
                                        args = data)
                c_thread.daemon = True
                c_thread.start()

        except KeyboardInterrupt:
            self.shutdown_server()
            
    def calculate_system(self):
        ''' Use memory and disk memory to calculate operations '''
        try:
            while True:
                if len(self.disk.pages) > 0: # if the disk have pages
                    if not self.memory.find_and_update(self.disk.pages[0].buffer):    
                        self.memory.replace_and_update(self.disk.pages[0].buffer)     
                        '''print("Fault")'''
                    else:
                        '''print("Hit")'''
                    
                    if sys.getsizeof(self.disk.pages[0].buffer) <= 88:
                        try:
                            operation = eval(self.disk.pages[0].buffer[0])
                        except:
                            operation = self.disk.pages[0].buffer[0]
                        self.save_operations(operation)
                    else:
                        self.printwt('ENOMEN: not enough memory')
                    self.disk.remove_page(0)
        except KeyboardInterrupt:
            pass
            
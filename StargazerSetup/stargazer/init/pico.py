import serial

class PicoSetup():

    def __init__(self):
        # serial0 tx is pin 8, rx is pin 10
        self.uart = serial.Serial(port="/dev/serial0", baudrate=115200, timeout=3)

    # 
    def send_data(self, data):
        print('[init-status] sending latitude to pico')
        while True:
            try:
                self.uart.write(bytes(f"curr_latitude;{data}\n", 'utf-8'))
                # TODO: Wait for response, maybe parse it to make sure correct?
                uart_ret = self.uart.readline().decode('utf-8')
                if uart_ret == "OK\n":
                    break
                print('[init-status] retrying sending pico latitude')
            except UnicodeDecodeError:
                print('[init-status] error reading/writing, retrying')
            except Exception as e:
                print('[init-status] other error encountered')
                break
        print('[init-status] pico setup complete')
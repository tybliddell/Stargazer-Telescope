from queue import Queue
import time
import serial
from typing import Tuple

class UARTQueue:
    uart_queue = Queue()
    next_seqnum = 0
    # serial0 tx is pin 8, rx is pin 10
    uart = serial.Serial(port="/dev/serial0", baudrate=115200, timeout=3)

    def __init__(self):
        self.seqnum = self.get_seqnum()
        return
    
    def safe_send_request(self, uart_string: str) -> Tuple[str, int]:
        UARTQueue.uart_queue.put((uart_string, self.seqnum))
        while True:
            # Check if your item is at front of queue
            if UARTQueue.uart_queue.queue[0][1] == self.seqnum:
                UARTQueue.uart.write(bytes(f'{UARTQueue.uart_queue.queue[0][0]};{UARTQueue.uart_queue.queue[0][1]}\n', 'utf-8'))
                try:
                    uart_ret = UARTQueue.uart.readline().decode('utf-8')
                except:
                    pass
                if not uart_ret or uart_ret[-1] != '\n':
                    UARTQueue.uart.write(bytes(f'{UARTQueue.uart_queue.queue[0][0]};{UARTQueue.uart_queue.queue[0][1]}\n', 'utf-8'))
                    try:
                        uart_ret = UARTQueue.uart.readline().decode('utf-8')
                    except:
                        pass
                if not uart_ret or uart_ret[-1] != '\n':
                    UARTQueue.uart_queue.get()
                    return 'Not Connected', 0x407
                response, seqnum, status = uart_ret.strip().split(';')
                if int(seqnum) == self.seqnum:
                    UARTQueue.uart_queue.get()
                    return response, int(status)
                UARTQueue.uart_queue.get()
                return 'Not Connected', 0x407
            time.sleep(1)
    
    def get_seqnum(self):
        seqnum = UARTQueue.next_seqnum
        UARTQueue.next_seqnum += 1
        UARTQueue.next_seqnum = UARTQueue.next_seqnum % 64
        return seqnum

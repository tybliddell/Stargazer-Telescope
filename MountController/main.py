import _thread
from machine import UART, Pin, I2C
from config import I2C_ADDRESSES, PINS
from core_1 import run
from hwlib.ssd1306 import SSD1306_I2C
from mount_controller import MountController
from telescope import Telescope
from config import DEBUG

# Set up stuff to pass between threads
lock = _thread.allocate_lock()
oled_i2c = I2C(1, scl=Pin(PINS["oled_i2c_scl"], mode=Pin.OUT, pull=Pin.PULL_UP),
               sda=Pin(PINS["oled_i2c_sda"], mode=Pin.OUT, pull=Pin.PULL_UP), freq=400000)
oled = SSD1306_I2C(128, 32, oled_i2c, lock, addr=I2C_ADDRESSES["screen"])
oled.set_text_and_show('hello from c0', 0)
mount_controller = MountController(oled)
telescope = Telescope(mount_controller)

_thread.start_new_thread(run, (telescope,))

ascom_uart = UART(0, 115200, rx=Pin(PINS["ascom_uart_rx"]), tx=Pin(PINS["ascom_uart_tx"]), parity=0)
ascom_bytes = b""

while True:
    # Append uart communication
    if ascom_uart.any() > 0:
        ascom_bytes += ascom_uart.read(1)
        if ascom_bytes.endswith(b'\n'):
            try:
                func, temp = ascom_bytes.decode("utf-8").split(';')
            except Exception as e:
                oled.set_text_and_show(f'error: {e}', 0)
                ascom_bytes = b""
                continue
            oled.set_text_and_show(f'{func}', 0)
            # must strip any null characters
            func = func.strip('\x00')
            if not telescope.mount_controller.latitude:
                if temp and func == "curr_latitude":
                    telescope.set_latitude(temp)
                    oled.set_text_and_show('waiting for homing', 0)
                    ascom_uart.write(f'OK\n')
                    oled.set_text_and_show('OKing', 0)
                    ascom_bytes = b""
                continue
            try:
                seq_num = int(temp)
            except:
                continue
            if telescope.current_seq is -1:
                # set current_seq to be 1 less than seq_num, wrapping around
                telescope.current_seq = (seq_num + 63) % 64
            if telescope.current_seq != seq_num:
                try:
                    oled.set_text_and_show(f'r: {func}', 0)
                    exec(f'telescope.{func}')
                    telescope.current_seq = seq_num
                except:
                    oled.set_text_and_show(f'DNE: {func}', 0)
                    if DEBUG:
                        print(f"requested command does not exist: {func}")
            ascom_bytes = b""
            ascom_uart.write(f'{telescope.last_response};{telescope.current_seq};{telescope.last_status}\n')

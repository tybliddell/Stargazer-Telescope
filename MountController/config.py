# ascom_uart is UART0, motor_uart is UART1
# oled_i2c is I2C1
PINS = {"ascom_uart_tx": 16 , "ascom_uart_rx": 17, "oled_i2c_sda": 18, "oled_i2c_scl": 19, 
        'motor_uart_rx': 5, 'motor_uart_tx': 4, "sensor_i2c_scl": 1, "sensor_i2c_sda": 0,
        'switch':15, "dec_motor_enable": 14, "ra_motor_enable": 13, "holo": 2, 
        "ra_motor_step": 11, "ra_motor_step_dir": 10}

I2C_ADDRESSES = {"screen": 0x3C, "sensor": 0x28}

DEBUG = True
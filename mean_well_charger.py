"""Module for interfacing Mean Well NPB chargers"""

import time

import can


class MeanWellCharger:
    """Mean Well NPB charger"""

    def __init__(self):
        self._bus = can.Bus(interface="socketcan", channel="can0", bitrate=250000)
        self._id = 0xC0103

    def bus_ok(self):
        """Check if charger replies on bus"""
        msg = can.Message(
            arbitration_id=self._id, data=[0x00, 0x00], is_extended_id=True
        )
        try:
            self._bus.send(msg)
            resp = self._bus.recv(1)
            if int(resp.data[0]) == 0 or int(resp.data[0]) == 1:
                return True
        except can.CanError:
            return False
        return False

    def set_off(self):
        """Turn off charger output"""
        self._set(0x00, [0x00])

    def set_on(self):
        """Turn on charger output"""
        self._set(0x00, [0x01])

    def print_values(self):
        """Print common charger values/settings"""
        settings = [
            [0xB0, "CURVE_CC", 0.01],
            [0xB1, "CURVE_CV", 0.01],
            [0xB2, "CURVE_FV", 0.01],
            [0xB3, "CURVE_TC", 0.01],
            [0xB5, "CURVE_CC_TIMEOUT", 0.01],
            [0xB6, "CURVE_CV_TIMEOUT", 0.01],
            [0xB7, "CURVE_FV_TIMEOUT", 0.01],
            [0xB9, "CHG_RST_VBAT", 0.01],
            [0x60, "READ_VOUT", 0.01],
            [0x61, "READ_IOUT", 0.01],
            [0x62, "Ambient temp", 0.1],
        ]

        for setting in settings:
            value = self._get_two_bytes(setting[0])
            if value is not None:
                print(f"{setting[1]}\t{value * setting[2]}")
                print(f"{setting[1] + ':':<18}{value * setting[2]}")

    def print_charge_status(self):
        """Print charger status data"""
        value = self._get_two_bytes(0xB8)
        if value is not None:
            low = int(value) % 256
            high = int(value) // 256

            print("Charge status")
            print(f"  Temp comp status: {high & 0x4 > 0}")
            print(f"  Bat detect: {high & 0x8 > 0}")
            print(f"  Timeout const current: {high & 0x20 > 0}")
            print(f"  Timeout const voltage: {high & 0x40 > 0}")
            print(f"  Timeout float: {high & 0x80 > 0}")
            print(f"  Fully charged: {low & 0x01 > 0}")
            print(f"  Constant current: {low & 0x02 > 0}")
            print(f"  Constant voltage: {low & 0x04 > 0}")
            print(f"  Float mode: {low & 0x08 > 0}")
            print(f"  Wakeup finished: {low & 0x04 > 0}")

    def set_voltage(self, in_value):
        """Set charger absorbtion voltage"""
        if in_value > 56:
            print("Won't set charging voltage to higher than 56 V")
            value = 5600
        else:
            value = int(in_value * 100)

        self.set_off()

        self._set_two_bytes(0xB1, value)

        time.sleep(0.05)
        self.set_on()

    def set_float_voltage(self, in_value):
        """Set charger float voltage"""
        if in_value > 56:
            print("Won't set charging voltage to higher than 56 V")
            value = 5600
        else:
            value = int(in_value * 100)

        self.set_off()

        self._set_two_bytes(0xB2, value)

        time.sleep(0.05)
        self.set_on()
        
    def set_taper_current(self, in_value):
        """Set taper current"""
        if in_value > 7.5 and in_value < 0.5:
            print("Won't set taper voltage to higher than 7.5A or lower than 0.5A. No change!")
            return
        else:
            value = int(in_value * 100)

        self.set_off()

        self._set_two_bytes(0xB3, value)

        time.sleep(0.05)
        self.set_on()    

    def set_restart_voltage(self, in_value):
        """Set and enable charger restart voltage"""
        if in_value > 56:
            print("Won't set charging voltage to higher than 56 V")
            value = 5600
        else:
            value = int(in_value * 100)

        # Enable restart
        self._set_two_bytes(0xB4, 0x0884)

        time.sleep(0.05)

        self.set_off()

        self._set_two_bytes(0xB9, value)

        time.sleep(0.05)
        self.set_on()

    def shutdown(self):
        """Release CAN bus after usage"""
        self._bus.shutdown()

    def _get_two_bytes(self, code):
        value = None
        msg = can.Message(
            arbitration_id=self._id,
            data=[code & 0xFF, (0x00 << 8) & 0xFF],
            is_extended_id=True,
        )
        try:
            self._bus.send(msg)
            resp = self._bus.recv(1)
            value = float(resp.data[2]) + float(resp.data[3]) * 256.0
        except can.CanError:
            print("CAN error")

        return value

    def _set_two_bytes(self, code, value):
        high = value // 256
        low = value % 256
        self._set(code, [low, high])

    def _set(self, code, data):
        msg = can.Message(
            arbitration_id=self._id,
            data=([code & 0xFF, (0x00 << 8) & 0xFF] + data),
            is_extended_id=True,
        )
        try:
            self._bus.send(msg)
        except can.CanError:
            print("CAN error")

#!/usr/bin/env python3

from mean_well_charger import MeanWellCharger

if __name__ == "__main__":
    mw = MeanWellCharger()
    mw.print_values()
    mw.print_charge_status()

    # mw.set_voltage(3.50 * 16)
    # mw.set_float_voltage(3.375 * 16)
    # mw.set_taper_current(4)
    # mw.set_charge_current(12)
    # mw.set_restart_voltage(3.1 * 16)


    mw.shutdown()

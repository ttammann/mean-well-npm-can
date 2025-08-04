# Mean Well NPB Charger CAN Configuration

Simple module/script to read and configure a Mean Well NPB charger. Mainly used to verify configuration and to set absorbtion and float voltages for LiFePO4 batteries.

Some inspiration from [MeanWell-NPB-canbus-python](https://github.com/mark-joe/MeanWell-NPB-canbus-python.git).

To bring up a socketcan interface, type:

```
ip link set can0 up type can bitrate 250000
```

# Mean Well NPB Charger CAN Configuration

Simple module/script to read and configure a Mean Well NPB charger. Mainly used to verify configuration and to set absorbtion and float voltages for LiFePO4 batteries.

Some inspiration from [MeanWell-NPB-canbus-python](https://github.com/mark-joe/MeanWell-NPB-canbus-python.git).


To bring up a socketcan interface, type:

```
ip link set can0 up type can bitrate 250000
```


If you use a  PC, 

This CANable adapter works great
```
https://www.alibaba.com/product-detail/CANable-2-0-USB-to-CAN_1601451293394.html?spm=a2756.trade-list-buyer.0.0.45a476e9ieSOHo
```
To find the USB device, type:
```
ls /dev/ttyUSB* /dev/ttyACM* 2>/dev/null
```

To initialize the adapter, type:
```
sudo slcand -o -s5 -S115200 /dev/ttyACM0 can0
```

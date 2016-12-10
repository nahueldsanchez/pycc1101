# README #

PYCC1101 a simple Python wrapper for the [CC1101](http://www.ti.com/product/CC1101) RF Transceiver. I've been using it with a [CC1101 Arduino module](https://www.amazon.com/Solu-Wireless-Transceiver-Antenna-Arduino/dp/B00XDL9838/ref=pd_sbs_147_6?_encoding=UTF8&psc=1&refRID=51K5G4WS9ZPJVE7HC2MW) connected trough SPI to a Raspberry Pi.
The code is based on [PanStamp Arduino library ](https://github.com/panStamp/arduino_avr). It uses the Python [SPIDEV module v3.3](https://pypi.python.org/pypi/spidev).

I developed this module for learning purposes and included two simple examples for rx and tx. The idea is to continue improving the module to perform more complex task, for example implementing [Sammy's OpenSesame attack](http://samy.pl/opensesame/). AFAIK there isn't any Python module public available to play with CC1101 SPI devices.

### Steps to make it work ###

1. Clone this repository
2. virutalenv pycc1101
3. Activate the virtualenv
4. pip install spidev
5. python tx.py
6. Perform steps 1-4 in other machine with the module connected.
7. python rx.py
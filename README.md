# README #

PYCC1101 is a simple Python wrapper for the [CC1101](http://www.ti.com/product/CC1101) RF Transceiver.

 I've been using PYCC1101 with a [CC1101 Arduino module](https://www.amazon.com/Solu-Wireless-Transceiver-Antenna-Arduino/dp/B00XDL9838/ref=pd_sbs_147_6?_encoding=UTF8&psc=1&refRID=51K5G4WS9ZPJVE7HC2MW) connected trough SPI to a Raspberry Pi.
The code, based on [PanStamp Arduino library ](https://github.com/panStamp/arduino_avr), uses Python [SPIDEV module v3.3](https://pypi.python.org/pypi/spidev).

I developed this module for learning purposes and included two examples for rx and tx. The idea is to continue improving the module to perform more complex tasks such as implementing [Sammy's OpenSesame attack](http://samy.pl/opensesame/). AFAIK, there isn't any public Python module  available to play with CC1101 SPI devices.

### Steps to make it work: ###

1. Clone this repository
2. Create a virtual environment by running `virtualenv pycc1101` 
3. Activate the virtualenv
4. Install spidev package: `pip install spidev`
5. Run `python tx.py`
6. Repeat steps 1-4 in another machine with the module connected.
7. Run `python rx.py`

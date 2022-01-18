# lorawan-rpigeneui

Raspberry Pi script to generate an EUI for LoRaWAN Networks from the Serial Number and Revision of the Raspberry.

The Script check for Raspberry Pi Serial Number and Revision, and return a valid LoRaWAN EUI specifying it as a local administred EUI to reduce the probability of using an EUI that could exists by other device. The generated EUI will be "02RRRRRRNNNNNNNN", where "R" are the Revision bytes and "N" the Serial Number bytes of the Raspberry.

This Script is useful in Raspberry Pi Zero devices, where there is no Ethernet interface with a MAC Address that could be used for an EUI.

## Install

You can get and setup the current script on a Raspberry device following the next commands:

```bash
sudo apt-get update
sudo apt-get install git

sudo git clone https://github.com/J-Rios/lorawan-rpigeneui.git /opt/lorawan-rpigeneui
sudo ln -s /opt/lorawan-rpigeneui/rpigeneui.py /usr/local/bin/rpi-gen-eui
sudo chmod +x /usr/local/bin/rpi-gen-eui
```

## Usage

To get the EUI, just run the script:

```bash
rpi-gen-eui
```

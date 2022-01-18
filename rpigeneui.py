#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script:
    rpigeneui.git.py
Description:
    Check for Raspberry Pi Serial Number and Revision, and return a valid
    LoRaWAN EUI specifying it as a local administred EUI to reduce the
    probability of using an EUI that could exists by other device.
    The generated EUI will be "02RRRRRRNNNNNNNN", where "R" are the Revision
    bytes and "N" the Serial Number bytes of the Raspberry.
Author:
    Jose Miguel Rios Rubio
Date:
    18/01/2022
Version:
    1.0.0
'''

###############################################################################
### Imported modules

from sys import argv as sys_argv
from sys import exit as sys_exit

###############################################################################
### Constants

# Raspberry Pi Model Information File
F_RPI_INFO = "/proc/cpuinfo"

# Raspberry Serial and Revision String pattern
# To be searched from F_RPI_INFO file
RPI_SERIAL_PATTERN = "Serial"
RPI_REVISION_PATTERN = "Revision"

# EUI First Octect for Local Administred EUIs
EUI_FIRST_OCTECT_LOCAL_ADMINISTRED = "02"

# Invalid EUI to be returned if something fails
INVALID_EUI = "FFFFFFFFFFFFFFFF"

# Expected EUI-64 length in chars (64 bits == 8 Bytes == 16 characters)
EUI_CHARS_LENGTH = 16

# Raspberry Company OUI
# Get the current OUI from:
# http://standards-oui.ieee.org/oui/oui.txt
# Currently not used
#RASPBERRY_OUI = "DCA632"

###############################################################################
### Auxiliar Classes

# Program return codes
class RC():
    OK = 0
    FAIL = -1
    FAIL_BAD_CFG = -2

###############################################################################
### Functions

def file_read_text(file_path):
    '''Read all text file content and return it in a string.'''
    read = ""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            read = f.read()
    except Exception:
        return ""
    return read


def get_rpi_serial_number(rpi_info):
    '''
    Get Raspberry Pi Serial Number from information data.
    Split read file data into lines, check for Serial number line and get it.
    The line is something like: "Serial          : 0000000000NNNNNN"
    '''
    serial_num = ""
    rpi_info_lines = rpi_info.splitlines()
    for line in rpi_info_lines:
        if RPI_SERIAL_PATTERN in line:
            serial_num = line.split(": ", 1)[1]
    return serial_num


def get_rpi_revision(rpi_info):
    '''
    Get Raspberry Pi Revision from information data.
    Split read file data into lines, check for Revision line and get it.
    The line is something like: "Revision           : RRRRRR"
    '''
    rev = ""
    rpi_info_lines = rpi_info.splitlines()
    for line in rpi_info_lines:
        if RPI_REVISION_PATTERN in line:
            rev = line.split(": ", 1)[1]
    return rev


def generate_eui(rpi_info):
    '''
    Create valid LoRaWAN EUI from Raspberry Serial Number and Revision, and
    also specify it as a local administred EUI by setting the bits 0 and 1 of
    first EUI octect as '10'. Using this bits values in the first octect, the
    expected EUIs to generate could be one of the following:
      X2XXXXXXXXXXXXXX, X6XXXXXXXXXXXXXX, XAXXXXXXXXXXXXXX, XEXXXXXXXXXXXXXX
    The generated EUI will be "02RRRRRRNNNNNNNN", where "R" are the Revision
    bytes and "N" the Serial Number bytes of the Raspberry.
    '''
    # Get Raspberry Pi Serial Number and Revision from information data
    rpi_serial_number = get_rpi_serial_number(rpi_info)
    rpi_revision = get_rpi_revision(rpi_info)
    # Make sure it has the expected length
    if (len(rpi_serial_number) != 16) and (len(rpi_serial_number) != 8):
        return INVALID_EUI
    if len(rpi_revision) != 6:
        return INVALID_EUI
    # Remove leading zeros from Serial Number
    if (len(rpi_serial_number) == 16):
        rpi_serial_number = rpi_serial_number[8:]
    # Create the EUI
    eui = "{}{}{}".format(EUI_FIRST_OCTECT_LOCAL_ADMINISTRED,
            rpi_revision, rpi_serial_number)
    if len(eui) != EUI_CHARS_LENGTH:
        return INVALID_EUI
    # Make sure to return it in Upper cases
    return eui.upper()

###############################################################################
### Main Function

def main(argc, argv):
    '''Main Function.'''
    # Read Raspberry Model Information File
    rpi_info = file_read_text(F_RPI_INFO)
    if rpi_info == "":
        print(INVALID_EUI)
        program_exit(RC.FAIL)
    # Create EUI from Raspberry Pi Model information
    eui = generate_eui(rpi_info)
    if eui == INVALID_EUI:
        print(INVALID_EUI)
        program_exit(RC.FAIL)
    print(eui)
    program_exit(RC.OK)

###############################################################################
### Exit Function

def program_exit(return_code):
    '''Program Exit Function.'''
    sys_exit(return_code)

###############################################################################
### Main Script execution Check

if __name__ == "__main__":
    try:
        main(len(sys_argv[1:]), sys_argv[1:])
    except KeyboardInterrupt:
        program_exit(RC.OK)

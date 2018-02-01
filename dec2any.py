#!/usr/bin/env python 3
"""Converting decimal values to any other number system
(binary, hexadecimal itp."""

import traceback


def convert_dec(decimalValue, numberSystem):
    """converts decimal value to a number system with a given number.
    Returns string.
    Arguments:
           decimalValue - value to be converted, e.g. 10; integer
           numberSystem - base of number system, e.g. 2, 6; integer"""
    try:
        if type(decimalValue) != int:
            raise ValueError("Decimal value should be integer")
        if type(numberSystem) != int:
            raise ValueError("Number system base should be integer")
    except ValueError:
        traceback.print_exc()
        raise SystemExit(0)

    codingString = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    finalNumber = ""
    x = decimalValue
    while True:
        finalNumber = codingString[x % numberSystem] + finalNumber
        if x < numberSystem:
            return finalNumber
        else:
            x = x // numberSystem    

MIT License

Copyright (c) 2022 Lawrence Byng

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



SAAM_MAIL v1.0 Beta release de WH6GGO

Designed and developed by Lawrence Byng

SAAM_MAIL is designed to provide group form transfer / email capabilities over Ham Radio using the SAAMFRAM protocol

A quick overview of some of the main features:

    • Email like interface with inbox, outbox, relay box and sent box
    • Fragmentation of messages to allow active session based transfer or passive sessionless transfer
    • CRC checksums to verify accurate message delivery
    • Use of 'stub' messages to notify the group of any messages waiting to be sent.
    • support for a wide variety of underlying modulations including JS8, PSK, QPSK, BPSK, DominoEX, 8PSK and Olivia
    • Form designer capability with many pre-built ICS form templates included.
    • Data efficient protocol for increased performance and resilience to adverse band conditions.
    • Capable of Peer to Peer, Peer to Group, Group to Peer and Group to Group mode communications.
    • Data compression using a variety of techniques such as dictionary compression and run length encoding.
    • Separation of form content from form template information allowing transfer of only the data content portion. 
    • Support for JS8Call and FLDIGI applications


Quick start guide
=================

STEP 1 configure for JS8Call or FLdigi
======================================
Perform step 1a or 1b as appropriate as desribed below...

STEP 1a JS8call configuration:
==============================
make sure JS8Call is configured as follows

1) Mode menu/Enable Auto Reply - checked
This setting is required for the text transfers between js8call and saam_mail to function correctly

2) File/Settings/Reporting tab
    • under the API section:
    • TCP Server Hostname: 127.0.0.1   Enable TCP Server API - checked
    • TCP Server Port:     2442        Accept TCP Requests   - checked
    • TCP Max Connections: 1 or 2

3) When you are ready to transmit, adjust the mode speed in JS8 as required (slow, normal, fast, turbo) and make sure
 the TX button at the top right is enabled.


STEP 1b FLDIGI configuration:
=============================
1) Make sure Fldigi XML-RPC external api is enabled and the ip and port set to 127.0.0.1 and 7362 respectively



STEP 2 running from .py files
=============================

    • download the saam-mail python files into your chosen directory

    • make sure python 3 is installed along with the following modules...

PySimpleGUI, sys, threading, json, random, getopt, datetime, socket, time, select, calendar, gps, crc

this can be done using the pip3 command for any missing modules. for example...

#pip3 install pysimplegui


please note saam_mail is available for python 3 only.

    • now run the application: python3 ./samm_mail.py --opmode=fldigi

    • or: python3 ./samm_mail.py --opmode=js8call


if everything is installed correctly, samm_mail will connect to fldigi or js8call and display the main window.

Now go to the settings tab and fill out your information.
At a minimum, this must include your call sign and chosen group name.
Also make sure one of the template files is loaded into the application on the settings tab

Now you can go to the compose tab and compose a message and send to the group.



For more information please refer to the ssamfram protocol document PROTOCOL.pdf



enjoy :)

73 de WH6GGO

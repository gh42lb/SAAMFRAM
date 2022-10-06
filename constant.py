
"""
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
"""


# Declare constants

RCV = 0
TX  = 1


HEARD   = "<HEARD>"
STANDBY = "<STANDBY>"
NEXT    = "<NEXT>"
TALKING = "<TALKING>"
SKIP    = "<SKIP>"
DONE    = "<DONE>"
QRT     = "<QRT>"
SWL     = "<SWL>"
IGNORE  = "<IGNORE>"
NONE    = "<NONE>"
CHECKIN = "<CHECKIN>"
NCS     = "<NCS>"

SAVED   = 0
EDIT    = 1

NETCONTROL  = 0
PARTICIPANT = 1
ALL         = 2

""" debug level constants """
DEBUG_INFO    = 1
DEBUG_WARNING = 2
DEBUG_ERROR   = 3
DEBUG_OFF     = 4

""" used to determine which preview window to display messages """
PREVIEW_MAIN  = 1
PREVIEW_SIDE  = 2


FLDIGI   = 1
JS8CALL  = 2
JSDIGI   = 3

FORMAT_TEMPLATE = 'FORM'
FORMAT_CONTENT  = 'DATA'
FORMAT_MULTIPAGECONTENT  = 'DATAM'
FORMAT_REPLY    = 'RPLY'
FORMAT_EMAIL    = 'MAIL'
FORMAT_INTERNET = 'WEB'

RENDER_TEXT_ONLY   = 1
RENDER_TEXT_TABLE  = 2
RENDER_ACTUAL      = 3
 
COMM_ACK_MSG       = ' ACK '
COMM_NACK_MSG      = ' KCAN '
COMM_QRYACK_MSG    = ' ACK? '
COMM_QRYSAAM_MSG   = ' SAAM? '
COMM_SAAM_MSG      = ' SAAM '
COMM_REQM_MSG      = ' REQM '
COMM_SAAMQRT_MSG   = ' SAAM QRT '
COMM_CONF_MSG      = ' CONF '
COMM_QRYRDY_MSG    = ' RDY? '
COMM_RR_MSG        = ' RR '
COMM_NR_MSG        = ' NR '
COMM_CCL_MSG       = ' CCL '

COMM_NONE          = 0
COMM_LISTEN        = 1
COMM_RECEIVING     = 2
COMM_QUEUED_TXMSG  = 3
COMM_SENDING       = 4
COMM_AWAIT_REPLY   = 5
COMM_AWAIT_ACKNACK = 6
COMM_AWAIT_RESEND  = 7

SEND_JS8CALL      = 1
SEND_FLDIGI       = 2

JS8CALL_SPEED_SLOW   = '4'
JS8CALL_SPEED_NORMAL = '0'
JS8CALL_SPEED_FAST   = '1'
JS8CALL_SPEED_TURBO  = '2'

EOM_JS8    = '/E'
EOM_FLDIGI = 'EOM'

ESCAPE_CHAR    = '/'
DELIMETER_CHAR = '~'

BASE32_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUV"

COMMAND_NONE      = 0
COMMAND_SAAM      = 1
COMMAND_QRY_SAAM  = 2
COMMAND_QRY_RELAY = 3
COMMAND_RELAY     = 4
COMMAND_CONF      = 5
COMMAND_RDY       = 6
COMMAND_QRY_RDY   = 7
COMMAND_SMT       = 8
COMMAND_EMT       = 9
COMMAND_CHKSUM    = 10
COMMAND_REQM      = 11

SAAM_CAPABLE      = 'YES'
SAAM_NOT_CAPABLE  = 'NO'

FORMAT_NONE                 = 0
FORMAT_TEMPLATE_ONLY        = 1
FORMAT_CONTENT_ONLY         = 2
FORMAT_TEMPLATE_AND_CONTENT = 3

REPEAT_NONE       = 0
REPEAT_FRAGMENTS  = 1
REPEAT_MESSAGE    = 2

SENDTO_NONE       = 0
SENDTO_GROUP      = 1
SENDTO_INDIVIDUAL = 2

WHAT_WHERE_NONE     = 0
FRAGMENTS_TO_GROUP  = 1
FRAGMENTS_TO_ME     = 2
QRYACKNACK_TO_ME    = 3


NO_BOX       = 0
UNKNOWN_BOX  = 0
IN_BOX       = 1
OUT_BOX      = 2
SENT_BOX     = 3
RELAY_BOX    = 4


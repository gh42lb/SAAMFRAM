#!/usr/bin/env python

import PySimpleGUI as sg

import sys
import JS8_Client
import debug as db
import threading
import json
import constant as cn
import random
import getopt

from datetime import datetime, timedelta
from datetime import time

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



class SaamParser(object):

  def __init__(self, debug, group_arq, form_dictionary, rig1, rig2, js8client_rig1, js8client_rig2, fldigiclient_rig1, fldigiclient_rig2, form_gui, saamfram):
    self.group_arq = group_arq
    self.form_dictionary = form_dictionary
    self.js8client = js8client_rig1
    self.fldigiclient = fldigiclient_rig1
    self.debug = debug
    self.form_gui = form_gui
    self.saamfram = saamfram


  def compareStrings(self, text1, text2, modetype):
    if(modetype == cn.JS8CALL):
      return self.js8client.isTextInMessage(text1, text2)
    elif(modetype == cn.FLDIGI):
      if(text1 in text2):
        return True

    return False
   
  def getFromToAddresses(self, text, command):
    remainder      = text.replace('  ', ' ')
    split_string   = remainder.split(command, 1)
    before_text    = split_string[0][-15:]
    after_text     = split_string[1][:15]
    pre_split      = before_text.split(' ')
    post_split     = after_text.split(' ')
    from_call_pre  = pre_split[len(pre_split)-2][:-1]
    toname         = pre_split[len(pre_split)-1]
    from_call_post = post_split[0]

    self.debug.info_message("from_call_pre : " + from_call_pre )
    self.debug.info_message("from_call_post : " + from_call_post )
    self.debug.info_message("to name : " + toname )

    if(from_call_pre == from_call_post):
      remainder = text.split(command,1)[1]
      return True, remainder, from_call_pre, toname
    else:
      return False, text, '', ''

  def testAndDecodeCommands(self, text, modetype):
 
    remainder = text

    try:
      if( self.compareStrings(cn.COMM_SAAM_MSG, text, modetype) ):

        #success, remainder, from_call, to_call = self.getFromToAddresses(text, cn.COMM_SAAM_MSG)
        #if (success):
        #  return cn.COMMAND_SAAM, remainder, from_call, to_call
        #else
        #  return cn.COMMAND_NONE, text, '', ''

        remainder = text.replace('  ', ' ')
        split_string = remainder.split(cn.COMM_SAAM_MSG, 1)
        before_text = split_string[0][-15:]
        after_text = split_string[1][:15]
        pre_split = before_text.split(' ')
        post_split = after_text.split(' ')
        from_call_pre = pre_split[len(pre_split)-2][:-1]
        groupname = pre_split[len(pre_split)-1]
        from_call_post = post_split[0]
        self.debug.info_message("from_call_pre : " + from_call_pre )
        self.debug.info_message("from_call_post : " + from_call_post )
        self.debug.info_message("groupname : " + groupname )

        if(from_call_pre == from_call_post):
          remainder = text.split(cn.COMM_SAAM_MSG,1)[1]
          return cn.COMMAND_SAAM, remainder, from_call_pre, groupname
        else:
          return cn.COMMAND_NONE, text, '', ''

      elif( self.compareStrings(cn.COMM_REQM_MSG, text, modetype) ):
        remainder = text.replace('  ', ' ')
        split_string = remainder.split(cn.COMM_REQM_MSG, 1)
        before_text = split_string[0][-15:]
        after_text = split_string[1]
        pre_split = before_text.split(' ')
        post_split = after_text.split(' ')
        from_call_pre = pre_split[len(pre_split)-2][:-1]
        msgid = post_split[0]
        from_call_post = post_split[1]
        self.debug.info_message("from_call_pre : " + from_call_pre )
        self.debug.info_message("from_call_post : " + from_call_post )

        if(from_call_pre == from_call_post):
          remainder = text.split(cn.COMM_REQM_MSG,1)[1]
          return cn.COMMAND_REQM, remainder, from_call_pre, msgid
        else:
          return cn.COMMAND_NONE, text, '', ''

      elif( self.compareStrings(cn.COMM_QRYSAAM_MSG, text, modetype) ):
        remainder = text.replace('  ', ' ')
        split_string = remainder.split(cn.COMM_QRYSAAM_MSG, 1)
        before_text = split_string[0][-15:]
        after_text = split_string[1][:15]
        pre_split = before_text.split(' ')
        post_split = after_text.split(' ')
        from_call_pre = pre_split[len(pre_split)-2][:-1]
        groupname = pre_split[len(pre_split)-1]
        from_call_post = post_split[0]
        self.debug.info_message("from_call_pre : " + from_call_pre )
        self.debug.info_message("from_call_post : " + from_call_post )
        self.debug.info_message("groupname : " + groupname )

        if(from_call_pre == from_call_post):
          remainder = text.split(cn.COMM_QRYSAAM_MSG,1)[1]
          return cn.COMMAND_QRY_SAAM, remainder, from_call_pre, groupname
        else:
          return cn.COMMAND_NONE, text, '', ''

      elif( self.compareStrings(' QRY RELAY ', text, modetype) ):
        split_string = text.split(' QRY RELAY ', 1)
        contents = split_string[1].split(' ')
        msgid     = contents[0]        
        fragments = contents[1]        
        remainder = text.split(' QRY RELAY '+ msgid + ' ' + fragments,1)[1]
        return cn.COMMAND_QRY_RELAY, remainder, msgid, fragments
      elif( self.compareStrings(' RELAY ', text, modetype) ):
        split_string = text.split(' RELAY ', 1)
        contents = split_string[1].split(' ')
        stationid = contents[0]        
        msgid     = contents[1]        
        fragments = contents[2]        
        remainder = text.split(' RELAY '+ stationid + ' ' + msgid + ' ' + fragments,1)[1]
        return cn.COMMAND_RELAY, remainder, stationid, msgid, fragments
      elif( self.compareStrings(' CONF ', text, modetype) ):
        split_string = text.split(' CONF ', 1)
        contents = split_string[1].split(' ')
        msgid     = contents[0]        
        fragments = contents[1]        
        remainder = text.split(' CONF '+ msgid + ' ' + fragments,1)[1]
        return cn.COMMAND_CONF, remainder, msgid, fragments
      elif( self.compareStrings(' RDY ', text, modetype) ):
        remainder = text.split(' RDY ',1)[1]
        return cn.COMMAND_RDY, remainder
      elif( self.compareStrings(' RDY? ', text, modetype) ):
        split_string = text.split(' RDY? ', 1)
        contents = split_string[1].split(' ')
        msgid     = contents[0]        
        calllist  = contents[1]        
        remainder = text.split(' RDY? '+ msgid + ' ' + calllist,1)[1]
        return cn.COMMAND_QRY_RDY, remainder, msgid, calllist
      elif( self.compareStrings(' SMT ', text, modetype) ):
        remainder = text.split(' SMT ',1)[1]
        return cn.COMMAND_SMT, remainder
      elif( self.compareStrings(' EMT ', text, modetype) ):
        remainder = text.split(' EMT ',1)[1]
        return cn.COMMAND_EMT, remainder
        self.debug.info_message("completed decode roster")
      elif( self.compareStrings(' REQCHK ', text, modetype) ):
        chksum_type = contents[0]        
        remainder = text.split(' REQCHK ',1)[1]
        return cn.COMMAND_CHKSUM, remainder, chksum_type
        self.debug.info_message("completed decode roster")
    except:
      self.debug.error_message("method: decodeCommands. " + str(sys.exc_info()[0]) + str(sys.exc_info()[1] ))

    return cn.COMMAND_NONE, text, '', ''


  def testPreMsgStartEnd(self, text, start, modetype):
    if( self.compareStrings(start, text, modetype) ):
      if( self.compareStrings('),', text, modetype) ):
        return '),'
      elif( self.compareStrings(')[', text, modetype) ):
        return ')'

    return ''

  def validateChecksum(self, message, checksum):
    if(self.saamfram.getChecksum(message) == checksum):
      return True
    else:
      return False

  def decodePreMsgPostNOTUSED(self, text, end_of_premsg):
      
    split_string = text.split(' POST( ', 1)
    split2 = split_string.split(end_of_premsg, 1)
    remainder = split2[1]
    content = split2[0]

    """ look for a two digit cheksum preceeded by a comma"""
    comma    = content[-3]
    checksum = content[-2:]
    if(comma == ',' and checksum[0] in cn.BASE32_CHARS and checksum[1] in cn.BASE32_CHARS):
      post_message = content.split(',' + checksum, 1)[0]
      if(self.validateChecksum(post_message, checksum)):
        return True, remainder, post_message

    self.debug.info_message("completed decode roster")
    """ dont assume anything return the original message intact """
    return False, text, ''

  def decodePreMsgCommon(self, text, end_of_premsg, findstr):
    split_string = text.split(findstr, 1)
    split2 = split_string.split(end_of_premsg, 1)
    remainder = split2[1]
    content = split2[0]

    """ look for a two digit cheksum preceeded by a comma"""
    comma    = content[-3]
    checksum = content[-2:]
    if(comma == ',' and checksum[0] in cn.BASE32_CHARS and checksum[1] in cn.BASE32_CHARS):
      content_2 = content.split(',' + checksum, 1)[0]
      if(self.validateChecksum(content_2, checksum)):
        split3  = content_2.split(',')
        msgid   = split3[0]
        rcvlist = split3[1]
        return True, remainder, msgid, rcvlist

    self.debug.info_message("completed decode roster")
    """ dont assume anything return the original message intact """
    return False, text, '', ''

  def decodePreMsgCommonN(self, text, end_of_premsg, findstr, numparams):
    split_string = text.split(findstr, 1)
    split2 = split_string[1].split(end_of_premsg, 1)
    remainder = split2[1]
    content = split2[0]

    self.debug.info_message("content is: " + str(content) )
    self.debug.info_message("remainder is: " + str(remainder) )

    """ look for a two digit cheksum preceeded by a comma"""

    try:
      self.debug.info_message("LOC 1")
      test_split = content.split(',')
      checksum = test_split[len(test_split)-1]

      self.debug.info_message("testing checksum")

      content_2 = content.split(',' + checksum, 1)[0]

      self.debug.info_message("content2 is: " + str(content_2) )

      if(self.validateChecksum(content_2, checksum)):
        self.debug.info_message("pre msg checksum validated OK!")
        split3  = content_2.split(',')
        if(numparams == 1):
          param1  = split3[0]
          return True, remainder, param1
        elif(numparams == 2):
          param1  = split3[0]
          param2  = split3[1]
          return True, remainder, param1, param2
        elif(numparams == 3):
          param1  = split3[0]
          param2  = split3[1]
          param3  = split3[2]
          return True, remainder, param1, param2, param3
        elif(numparams == 6):
          param1  = split3[0]
          param2  = split3[1]
          param3  = split3[2]
          param4  = split3[3]
          param5  = split3[4]
          param6  = split3[5]
          return True, remainder, param1, param2, param3, param4, param5, param6
    except:
      self.debug.info_message("exception decoding pre message"  + str(sys.exc_info()[0]) + str(sys.exc_info()[1]) )

    self.debug.info_message("completed decode pre message part FAIL")
    """ dont assume anything return the original message intact """
    return False, text, '', ''


  def decodePreMsgPost(self, text, end_of_premsg):
    return self.decodePreMsgCommonN(text, end_of_premsg, ' POST(', 1)

  def decodePreMsgRelay(self, text, end_of_premsg):
    return self.decodePreMsgCommonN(text, end_of_premsg, ' RELAY(', 2)

  def decodePreMsgPend(self, text, end_of_premsg):
    self.debug.info_message("DECODING PRE MSG PEND(")
    succeeded, remainder, msgid, rcv_list = self.decodePreMsgCommonN(text, end_of_premsg, ' PEND(', 2)

    #self.debug.info_message("DECODING PRE MSG PEND LOC 2")

    test_split = rcv_list.split(';')
    add_to_inbox = False
    #self.debug.info_message("DECODING PRE MSG PEND LOC 3")
    for x in range (0, len(test_split)):
      if(test_split[x] == self.saamfram.getMyCall()):
        add_to_inbox = True
    #self.debug.info_message("DECODING PRE MSG PEND LOC 4")
    timestamp = datetime.utcnow().strftime('%y%m%d%H%M%S')
    if(add_to_inbox == True):
      #self.debug.info_message("DECODING PRE MSG PEND LOC 5")
      self.form_dictionary.createInboxDictionaryItem(msgid, rcv_list, '', '-', '-', timestamp, '-', {} )
      self.group_arq.addMessageToInbox('', rcv_list, '-', timestamp, '-', '-', 'Partial', msgid)
      self.form_gui.window['table_inbox_messages'].update(values=self.group_arq.getMessageInbox() )
      self.form_gui.window['table_inbox_messages'].update(row_colors=self.group_arq.getMessageInboxColors())
    else:
      #self.debug.info_message("DECODING PRE MSG PEND LOC 6")
      self.form_dictionary.createRelayboxDictionaryItem(msgid, rcv_list, '', '-', '-', timestamp, '-', {}, '', '')
      self.group_arq.addMessageToRelaybox('', rcv_list, '-', timestamp, '-', '-', msgid, 'Partial', '')
      self.form_gui.window['table_relay_messages'].update(values=self.group_arq.getMessageRelaybox() )
      self.form_gui.window['table_relay_messages'].update(row_colors=self.group_arq.getMessageRelayboxColors())

    #self.debug.info_message("DECODING PRE MSG PEND LOC 7")

    return succeeded, remainder

  def decodePreMsgQmsg(self, text, end_of_premsg):
    return self.decodePreMsgCommonN(text, end_of_premsg, ' QMSG(', 6)

  def decodePreMsgQinfo(self, text, end_of_premsg):
    return self.decodePreMsgCommonN(text, end_of_premsg, ' QINFO(', 1)

  def decodePreMsgCalls(self, text, end_of_premsg):
    return self.decodePreMsgCommonN(text, end_of_premsg, ' CALLS(', 1)

  def decodePreMsgEndm(self, text, end_of_premsg):
    return self.decodePreMsgCommonN(text, end_of_premsg, ' ENDM(', 3)

  def decodePreMsgInfo(self, text, end_of_premsg):
    return self.decodePreMsgCommonN(text, end_of_premsg, ' INFO(', 2)


  def testAndDecodePreMessage(self, text, modetype):

    """ pre message parts must always follow a set predefined order. This applies to send and receive"""
    try:
      end_of_premsg = self.testPreMsgStartEnd(text, ' POST(', modetype)
      if( end_of_premsg != ''):
        self.debug.info_message("decode POST")
        succeeded, remainder = self.decodePreMsgPost(text, end_of_premsg)

      end_of_premsg = self.testPreMsgStartEnd(text, ' RELAY(', modetype)
      if( end_of_premsg != ''):
        self.debug.info_message("decode RELAY")
        succeeded, remainder = self.decodePreMsgRelay(text, end_of_premsg)

      end_of_premsg = self.testPreMsgStartEnd(text, ' PEND(', modetype)
      if( end_of_premsg != ''):
        self.debug.info_message("decode PEND")
        succeeded, remainder = self.decodePreMsgPend(text, end_of_premsg)
        return succeeded, remainder

      end_of_premsg = self.testPreMsgStartEnd(text, ' QMSG(', modetype)
      if( end_of_premsg != ''):
        self.debug.info_message("decode QMSG")
        succeeded, remainder = self.decodePreMsgQmsg(text, end_of_premsg)

      end_of_premsg = self.testPreMsgStartEnd(text, ' QINFO(', modetype)
      if( end_of_premsg != ''):
        self.debug.info_message("decode QINFO")
        succeeded, remainder = self.decodePreMsgQinfo(text, end_of_premsg)

      end_of_premsg = self.testPreMsgStartEnd(text, ' CALLS(', modetype)
      if( end_of_premsg != ''):
        self.debug.info_message("decode CALLS")
        succeeded, remainder = self.decodePreMsgCalls(text, end_of_premsg)

      end_of_premsg = self.testPreMsgStartEnd(text, ' ENDM(', modetype)
      if( end_of_premsg != ''):
        self.debug.info_message("decode ENDM")
        succeeded, remainder = self.decodePreMsgEndm(text, end_of_premsg)

      end_of_premsg = self.testPreMsgStartEnd(text, ' INFO(', modetype)
      if( end_of_premsg != ''):
        self.debug.info_message("decode INFO")
        succeeded, remainder = self.decodePreMsgInfo(text, end_of_premsg)

    except:
      self.debug.error_message("method: decodeCommands. " + str(sys.exc_info()[0]) + str(sys.exc_info()[1] ))

    return False, text






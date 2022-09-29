#!/usr/bin/env python
import sys
import constant as cn
import string
import struct

try:
  import PySimpleGUI as sg
except:
  import PySimpleGUI27 as sg

import json
import threading
import os
import platform
import calendar
import xmlrpc.client

import saam_mail
import js8_form_gui
import js8_form_events

from datetime import datetime, timedelta
from datetime import time

from uuid import uuid4

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

class FormDictionary(object):

  """
  debug level 0=off, 1=info, 2=warning, 3=error
  """
  def __init__(self, debug):  

    self.template_file_dictionary_data = {}
    self.inbox_file_dictionary_data = {}
    self.outbox_file_dictionary_data = {}
    self.relaybox_file_dictionary_data = {}
    self.sentbox_file_dictionary_data = {}
    self.form_events = None
    self.group_arq = None
    self.debug = debug
    return

  def setFormEvents(self, form_events):
    self.form_events = form_events
    return

  def setGroupArq(self, group_arq):
    self.group_arq = group_arq
    return

  """
  Template dictionary section
  """
  def setDataInDictionary(self, formname, category, filename, data):

    js = self.template_file_dictionary_data[filename]
    self.debug.info_message("dictionary data is: " + str(self.template_file_dictionary_data[filename]) )

    description = ''
    version = 0

    data_dictionary = js.get(category)		  

    for key in data_dictionary:
      self.debug.info_message("form name: " + key )
      if(key == formname):
        data_dictionary[key] = data
        self.debug.info_message("data is: " + str(data) )
        break

    self.debug.info_message("returning : " + str(data) )

    return (js)

  def getDataFromDictionary(self, field1, field2, field3, field4):

    data = None
    
    filename = field4

    js = self.template_file_dictionary_data[filename]

    self.debug.info_message("dictionary data is: " + str(self.template_file_dictionary_data[filename]) )

    description = ''
    version = 0
    category = self.form_events.current_edit_category

    data_dictionary = js.get(category)		  

    for key in data_dictionary:
      self.debug.info_message("form name: " + key )
      if(key == field1):
        data = data_dictionary.get(key)		  
        self.debug.info_message("data is: " + str(data) )
        break

    self.debug.info_message("returning : " + str(data) )

    return (data)

  def getFileDescriptionFromTemplateDictionary(self, filename):
    js = self.template_file_dictionary_data[filename]
    description = js.get('description')		  
    return description

  def getFileVersionFromTemplateDictionary(self, filename):
    js = self.template_file_dictionary_data[filename]
    version = js.get('version')		  
    return version

  def getTemplatesFromCategory(self, category):

    self.group_arq.clearTemplates()

    for file_key in self.template_file_dictionary_data:
      js = self.template_file_dictionary_data.get(file_key)
     
      self.debug.info_message("dictionary data is: " + str(js) )

      description = ''
      version = 0

      data_dictionary = js.get(category)		  

      for key in data_dictionary:
        self.debug.info_message("form name: " + key )
        data = data_dictionary.get(key)		  

        self.debug.info_message("data: " + str(data) )

        version = data[0]		  
        self.debug.info_message("version: " + str(version) )
        description = data[1]
        self.debug.info_message("description: " + description )

        self.group_arq.addTemplate(key, description, str(version), file_key)

    return

    """
    details = { 'STD FORMS'   : {'General Message'    : ['v1.0','my description','T1,I1','T2,I2,T5,I3','T3,I2,T6,I3','T4,I2','T7','I4'],
                              'OTHER FORM'         : ['v1.0','my description','T8,I1','T2,I5,T9,I5','T3,I5,T9,I5','T4,I1','T7,T5,I3,T6,I3','I4', 'T10,I5,T9,I5']},
                'ICS FORMS'   : {'ICS Message'        : ['v1.0','my description','T1,I1','T2,I2,T5,I3','T3,I2,T6,I3','T4,I2','T7','I4'],
                              'ICS-213'            : ['v1.0','my description','T8,I1','T2,I5,T9,I5','T3,I5,T9,I5','T4,I1','T7,T5,I3,T6,I3','I4', 'T10,I5,T9,I5']},                              
                'ABC FORMS'   : {'ABC Message'        : ['v1.0','my description','T1,I1','T2,I2,T5,I3','T3,I2,T6,I3','T4,I2','T7','I4'],
                              'ABC other'          : ['v1.0','my description','T8,I1','T2,I5,T9,I5','T3,I5,T9,I5','T4,I1','T7,T5,I3,T6,I3','I4', 'T10,I5,T9,I5']},                              
                'GHI FORMS'   : {'ABC Message'        : ['v1.0','my description','T1,I1','T2,I2,T5,I3','T3,I2,T6,I3','T4,I2','T7','I4'],
                              'ABC other'          : ['v1.0','my description','T8,I1','T2,I5,T9,I5','T3,I5,T9,I5','T4,I1','T7,T5,I3,T6,I3','I4', 'T10,I5,T9,I5']},
                'version'     : 1.3,
                'description' : 'my test forms' }
    """

  def createNewTemplateInDictionary(self, filename, category, formname, version, description, data):

    self.debug.info_message("createNewTemplateInDictionary 1 \n")

    dictionary = self.template_file_dictionary_data[filename]
    self.debug.info_message("dictionary data is: " + str(self.template_file_dictionary_data[filename]) )

    data_dictionary = {}

    self.debug.info_message("createNewTemplateInDictionary 2 \n")
    
    if(category in dictionary):
      self.debug.info_message("createNewTemplateInDictionary 3 \n")
      data_dictionary = dictionary.get(category)		  
      data_dictionary[formname] = data
    else:
      self.debug.info_message("createNewTemplateInDictionary 4 \n")
      data_dictionary[formname] = data
      dictionary[category] = data_dictionary
      
    self.debug.info_message("createNewTemplateInDictionary 5 \n")

    self.debug.info_message("new dictionary is: " + str(data_dictionary) )
      
    return (data_dictionary)


  def getTemplateFromTemplateDictionary(self, formname, category, filename):

    details = self.template_file_dictionary_data[filename]

    for key in details:
      if(key == 'description'):
        description = details.get("description")		  
        self.debug.info_message("description: " + description )
      elif(key == 'version'):
        version = details.get("version")		  
        self.debug.info_message("version: " + str(version) )
      else:
        if(key == category):
          template_dictionary = details.get(category)		  
          for template_key in template_dictionary:
            if(template_key == formname):
              template = template_dictionary.get(formname)
              return template			  
    return (None)

  def removeTemplatesFileFromTemplateDictionary(self, filename):
    self.debug.info_message("REMOVEING FILE: " + filename )
    self.template_file_dictionary_data.pop(filename, None)
    self.debug.info_message("REMOVED FILE\n")
    return (None)

  def removeTemplateFromTemplateDictionary(self, filename, category, formname):

    details = self.template_file_dictionary_data[filename]
    template_dictionary = details.get(category)		  
    template_dictionary.pop(formname, None)
    return (None)

  def removeCategoryFromTemplateDictionary(self, filename, category):
    details = self.template_file_dictionary_data[filename]
    details.pop(category, None)		  
    return (None)


  def getTemplateByFormFromTemplateDictionary(self, formname):

    for file_key in self.template_file_dictionary_data:
      category_dictionary = self.template_file_dictionary_data.get(file_key)		  

      for category_key in category_dictionary:
        if(category_key == 'description'):
          description = category_dictionary.get("description")		  
          self.debug.info_message("description: " + description )
        elif(category_key == 'version'):
          version = category_dictionary.get("version")		  
          self.debug.info_message("version: " + str(version) )
        else:
          template_dictionary = category_dictionary.get(category_key)		  
          for template_key in template_dictionary:
            if(template_key == formname):
              template = template_dictionary.get(formname)
              return template			  
    return (None)


  def getCategoryAndFilenameFromFormname(self, formname):

    for file_key in self.template_file_dictionary_data:
      category_dictionary = self.template_file_dictionary_data.get(file_key)		  

      for category_key in category_dictionary:
        if(category_key == 'description'):
          description = category_dictionary.get("description")		  
          self.debug.info_message("description: " + description )
        elif(category_key == 'version'):
          version = category_dictionary.get("version")		  
          self.debug.info_message("version: " + str(version) )
        else:
          template_dictionary = category_dictionary.get(category_key)		  
          for template_key in template_dictionary:
            if(template_key == formname):
              return category_key, file_key			  
    
    return None, None


  def writeTemplateDictToFile(self, filename):
 
    """ individual fields first """	  
    """
    details = { 'STD FORMS'   : {'General Message'    : ['v1.0','my description','T1,I1','T2,I2,T5,I3','T3,I2,T6,I3','T4,I2','T7','I4'],
                              'OTHER FORM'         : ['v1.0','my description','T8,I1','T2,I5,T9,I5','T3,I5,T9,I5','T4,I1','T7,T5,I3,T6,I3','I4', 'T10,I5,T9,I5']},
                'ICS FORMS'   : {'ICS Message'        : ['v1.0','my description','T1,I1','T2,I2,T5,I3','T3,I2,T6,I3','T4,I2','T7','I4'],
                              'ICS-213'            : ['v1.0','my description','T8,I1','T2,I5,T9,I5','T3,I5,T9,I5','T4,I1','T7,T5,I3,T6,I3','I4', 'T10,I5,T9,I5']},                              
                'ABC FORMS'   : {'ABC Message'        : ['v1.0','my description','T1,I1','T2,I2,T5,I3','T3,I2,T6,I3','T4,I2','T7','I4'],
                              'ABC other'          : ['v1.0','my description','T8,I1','T2,I5,T9,I5','T3,I5,T9,I5','T4,I1','T7,T5,I3,T6,I3','I4', 'T10,I5,T9,I5']},                              
                'GHI FORMS'   : {'ABC Message'        : ['v1.0','my description','T1,I1','T2,I2,T5,I3','T3,I2,T6,I3','T4,I2','T7','I4'],
                              'ABC other'          : ['v1.0','my description','T8,I1','T2,I5,T9,I5','T3,I5,T9,I5','T4,I1','T7,T5,I3,T6,I3','I4', 'T10,I5,T9,I5']},
                'version'     : 1.3,
                'description' : 'my test forms' }
    """
    
    details = self.template_file_dictionary_data[filename]

    self.debug.info_message("WRITING TO FILE DICTIONARY: " + str(details) )
 
    try:
      with open(filename, 'w') as convert_file:
                convert_file.write(json.dumps(details))
    except:
      self.debug.error_message("Exception in writeTemplateDictToFile: " + str(sys.exc_info()[0]) + str(sys.exc_info()[1] ))
              
    return()


  def readTemplateDictFromFile(self, filename):
    with open(filename) as f:
      data = f.read()
  
    """  
    reconstructing the data as a dictionary
    """
    js = json.loads(data)

    """ now add the edited data object """	  
    self.template_file_dictionary_data[filename] = js

    self.debug.info_message("dictionary data is: " + str(self.template_file_dictionary_data[filename]) )

    description = ''
    version = 0
    for key in js:
      if(key == 'description'):
        description = js.get("description")		  
        self.debug.info_message("description: " + description )
      elif(key == 'version'):
        version = js.get("version")		  
        self.debug.info_message("version: " + str(version) )
      else:
        self.group_arq.addCategory(key)
        self.debug.info_message("category: " + key )

    """ add the loaded template to the list """
    self.group_arq.addLoadedTemplateFile(filename, description, version)
   
    return(js)

    """
    This is the format of data in the oubox dictionary
    
    details = { 'ID_GGO_123654'   : {'content'            : ['fred','smith','100 great nothing road','everwhere','the moon','M34-345','Good afternnon I hope all is well 73 Fred'],
                                     'to'                 : ['WH6ABC','WH6DEF','WH6GHI'],
                                     'from'               : ['WH6GGO'],
                                     'subject'            : ['Hi there hope all is well'],
                                     'timestamp'          : ['WH6ABC'],
                                     'ID'                 : ['WH6ABC'],
                                     'priority'           : ['WH6ABC'],
                                     'formname'           : ['WH6ABC']},
                'ID_FGH_123654'   : {'content'            : ['fred','smith','100 great nothing road','everwhere','the moon','M34-345','Good afternnon I hope all is well 73 Fred'],
                                     'to'                 : ['WH6ABC','WH6DEF','WH6GHI'],
                                     'from'               : ['WH6GGO'],
                                     'subject'            : ['Hi there hope all is well'],
                                     'timestamp'          : ['WH6ABC'],
                                     'ID'                 : ['WH6ABC'],
                                     'priority'           : ['WH6ABC'],
                                     'formname'           : ['WH6ABC']},
              }
    """

  """
  Relaybox dictionary section
  """

  def getRelayboxDictionaryItem(self, msgid):
    dictionary = self.relaybox_file_dictionary_data[msgid]
    dictionary2 = dictionary.get('0')
    return dictionary2

  def getContentFromRelayboxDictionary(self, msgid):
    dictionary = self.relaybox_file_dictionary_data[msgid]
    dictionary2 = dictionary.get('0')
    content = dictionary2.get('content')		  
    return content

  def getFormnameFromRelayboxDictionary(self, msgid):
    dictionary = self.relaybox_file_dictionary_data[msgid]
    dictionary2 = dictionary.get('0')
    formname = dictionary2.get('formname')		  
    return formname

  def getVerifiedFromRelayboxDictionary(self, msgid):
    dictionary = self.relaybox_file_dictionary_data[msgid]
    dictionary2 = dictionary.get('0')
    verified = dictionary2.get('verified')		  
    return verified


  def writeRelayboxDictToFile(self, filename):
   
    filename = 'relaybox.msg'
 
    with open(filename, 'w') as convert_file:
              convert_file.write(json.dumps(self.relaybox_file_dictionary_data))
    return()

  def readRelayboxDictFromFile(self, filename):

    with open(filename) as f:
      data = f.read()
  
    self.relaybox_file_dictionary_data = json.loads(data)

    self.group_arq.clearRelaybox()

    for key in self.relaybox_file_dictionary_data:
      ID = key
      pages = self.relaybox_file_dictionary_data.get(ID)
      message = pages.get('0')

      msgto     = message.get('to')
      msgfrom   = message.get('from')
      subject   = message.get('subject')
      timestamp = message.get('timestamp')
      priority  = message.get('priority')
      formname  = message.get('formname')
      verified  = message.get('verified')
      confrcvd  = message.get('confrcvd')
      fragsize  = message.get('fragsize')

      self.group_arq.addMessageToRelaybox(msgfrom, msgto, subject, timestamp, priority, formname, ID, confrcvd, fragsize)
   
    return 

  def doesRelayboxDictionaryItemExist(self, msgid):

    if msgid in self.relaybox_file_dictionary_data:
      return True
    else:
      return False
    return


  def createRelayboxDictionaryItem(self, ID, msgto, msgfrom, subject, priority, timestamp, formname, confrcvd, fragsize, content):

    verified = 'yes'

    self.relaybox_file_dictionary_data[ID] = { '0' : {'content'            : content,
                                                      'to'                 : msgto,
                                                      'from'               : msgfrom,
                                                      'subject'            : subject,
                                                      'timestamp'          : timestamp,
                                                      'priority'           : priority,
                                                      'verified'           : verified,
                                                      'confrcvd'           : confrcvd,
                                                      'fragsize'           : fragsize,
                                                      'formname'           : formname} }

    return (self.relaybox_file_dictionary_data)


  def getContentByIdFromRelayboxDictionary(self, ID):

    message_dictionary = self.relaybox_file_dictionary_data.get(ID)		  
    message_dictionary2 = message_dictionary.get('0')

    for message_key in message_dictionary2:
      if(message_key == 'description'):
        description = message_dictionary2.get("description")		  
        self.debug.info_message("description: " + description )
      elif(message_key == 'version'):
        version = message_dictionary2.get("version")		  
        self.debug.info_message("version: " + str(version) )
      else:
        content = message_dictionary2.get('content')
        return content
    return (None)



  """
  Outbox dictionary section
  """
  def writeOutboxDictToFile(self, filename):
   
    filename = 'outbox.msg'
 
    with open(filename, 'w') as convert_file:
              convert_file.write(json.dumps(self.outbox_file_dictionary_data))
    return()

  def readOutboxDictFromFile(self, filename):

    with open(filename) as f:
      data = f.read()
  
    self.outbox_file_dictionary_data = json.loads(data)

    self.group_arq.clearOutbox()

    for key in self.outbox_file_dictionary_data:
      ID = key
      message = self.outbox_file_dictionary_data.get(key)
      msgto     = message.get('to')
      msgfrom   = message.get('from')
      subject   = message.get('subject')
      timestamp = message.get('timestamp')
      priority  = message.get('priority')
      formname  = message.get('formname')

      self.group_arq.addMessageToOutbox(msgfrom, msgto, subject, timestamp, priority, formname, ID)
   
    return 

  def createOutboxDictionaryItem(self, ID, msgto, msgfrom, subject, priority, timestamp, formname, content):

    self.outbox_file_dictionary_data[ID] = {'content'            : content,
                                            'to'                 : msgto,
                                            'from'               : msgfrom,
                                            'subject'            : subject,
                                            'timestamp'          : timestamp,
                                            'priority'           : priority,
                                            'formname'           : formname}

    return (self.outbox_file_dictionary_data)

  def getContentFromOutboxDictionary(self, msgid):
    dictionary = self.outbox_file_dictionary_data[msgid]
    content = dictionary.get('content')		  
    return content

  def getContentByIdFromOutboxDictionary(self, ID):

    message_dictionary = self.outbox_file_dictionary_data.get(ID)		  
    for message_key in message_dictionary:
      if(message_key == 'description'):
        description = message_dictionary.get("description")		  
        self.debug.info_message("description: " + description )
      elif(message_key == 'version'):
        version = message_dictionary.get("version")		  
        self.debug.info_message("version: " + str(version) )
      else:
        content = message_dictionary.get('content')
        return content
    return (None)

  def doesOutboxDictionaryItemExist(self, msgid):

    if msgid in self.outbox_file_dictionary_data:
      return True
    else:
      return False
    return

  """ currently used for testing purposes only"""
  def getVerifiedFromOutboxDictionary(self, msgid):
    dictionary = self.outbox_file_dictionary_data[msgid]
    verified = 'yes'
    return verified

  def getOutboxDictionaryItem(self, msgid):
    dictionary = self.outbox_file_dictionary_data[msgid]
    return dictionary

  """
  Inbox dictionary section
  """

  def getInboxDictionaryItem(self, msgid):
    dictionary = self.inbox_file_dictionary_data[msgid]
    dictionary2 = dictionary.get('0')
    return dictionary2


  def getContentFromInboxDictionary(self, msgid):
    dictionary = self.inbox_file_dictionary_data[msgid]
    dictionary2 = dictionary.get('0')
    content = dictionary2.get('content')		  
    return content

  def getFormnameFromInboxDictionary(self, msgid):
    dictionary = self.inbox_file_dictionary_data[msgid]
    dictionary2 = dictionary.get('0')
    formname = dictionary2.get('formname')		  
    return formname

  def getVerifiedFromInboxDictionary(self, msgid):
    dictionary = self.inbox_file_dictionary_data[msgid]
    dictionary2 = dictionary.get('0')
    verified = dictionary2.get('verified')		  
    return verified


  def resetInboxDictionary(self):
    self.inbox_file_dictionary_data = {}
    return

  def writeInboxDictToFile(self, filename):

    self.debug.info_message("Writing inbox to file\n")
   
    try:
      filename = 'inbox.msg'
 
      with open(filename, 'w') as convert_file:
                convert_file.write(json.dumps(self.inbox_file_dictionary_data))
    except:
      self.debug.error_message("Exception in writeInboxDictToFile: " + str(sys.exc_info()[0]) + str(sys.exc_info()[1] ))

    return()

  def readInboxDictFromFile(self, filename):

    with open(filename) as f:
      data = f.read()
  
    self.inbox_file_dictionary_data = json.loads(data)

    self.group_arq.clearInbox()

    for key in self.inbox_file_dictionary_data:
      ID = key
      pages = self.inbox_file_dictionary_data.get(ID)
      message = pages.get('0')
      msgto     = message.get('to')
      msgfrom   = message.get('from')
      subject   = message.get('subject')
      timestamp = message.get('timestamp')
      priority  = message.get('priority')
      formname  = message.get('formname')
      verified  = message.get('verified')
      missing_frames = message.get('missingframes')
      self.group_arq.addMessageToInbox(msgfrom, msgto, subject, timestamp, priority, formname, verified, ID)
   
    return 

  def doesInboxDictionaryItemExist(self, msgid):

    if msgid in self.inbox_file_dictionary_data:
      return True
    else:
      return False
    return

  def createInboxDictionaryItem(self, ID, msgto, msgfrom, subject, priority, timestamp, formname, content):

    missing_frames = 'F1,F2,F3'

    verified = 'Yes'

    #self.debug.info_message("in createInboxDictionaryItem LOC 1\n")

    self.inbox_file_dictionary_data[ID] = { '0'  :  {'content'            : content,
                                                     'to'                 : msgto,
                                                     'from'               : msgfrom,
                                                     'subject'            : subject,
                                                     'timestamp'          : timestamp,
                                                     'priority'           : priority,
                                                     'formname'           : formname,
                                                     'verified'           : verified,
                                                     'missingframes'      : missing_frames} }

    return (self.inbox_file_dictionary_data)


  def addInboxDictionaryReply(self, mainID, replyID, msgto, msgfrom, subject, priority, timestamp, formname, content):
    missing_frames = ''

    verified = 'yes'

    #self.debug.info_message("in addInboxDictionaryReply LOC 1\n")

    parent_keyval = self.inbox_file_dictionary_data[mainID]

    page_num = len(parent_keyval)

    parent_keyval[page_num] = {'content'            : content,
                               'to'                 : msgto,
                               'from'               : msgfrom,
                               'subject'            : subject,
                               'timestamp'          : timestamp,
                               'priority'           : priority,
                               'formname'           : formname,
                               'verified'           : verified,
                               'missingframes'      : missing_frames,
                               'replyid'            : replyID} 

    self.inbox_file_dictionary_data[mainID] = parent_keyval

    self.debug.info_message("added page to inbox dictionary: " + str(self.inbox_file_dictionary_data)  )

    return (self.inbox_file_dictionary_data)

  def getPagesKeyvalFromInboxDictionary(self, mainID):
    self.debug.info_message("get pages keval from dictionary\n")
    parent_keyval = self.inbox_file_dictionary_data.get(mainID)
    self.debug.info_message("completed get pages keval from dictionary\n")

    return parent_keyval


  """
  Sendbox dictionary section
  """
  def getContentFromSentboxDictionary(self, msgid):
    dictionary = self.sentbox_file_dictionary_data[msgid]
    content = dictionary.get('content')		  
    return content

  def getFormnameFromSentboxDictionary(self, msgid):
    dictionary = self.sentbox_file_dictionary_data[msgid]
    formname = dictionary.get('formname')		  
    return formname

  def writeSentDictToFile(self, filename):
   
    with open(filename, 'w') as convert_file:
              convert_file.write(json.dumps(self.sentbox_file_dictionary_data))
    return()

  def readSentDictFromFile(self, filename):

    with open(filename) as f:
      data = f.read()
  
    self.sentbox_file_dictionary_data = json.loads(data)

    self.group_arq.clearSentbox()

    for key in self.sentbox_file_dictionary_data:
      ID = key
      message = self.sentbox_file_dictionary_data.get(key)
      msgto     = message.get('to')
      msgfrom   = message.get('from')
      subject   = message.get('subject')
      timestamp = message.get('timestamp')
      priority  = message.get('priority')
      formname  = message.get('formname')

      self.group_arq.addMessageToSentbox(msgfrom, msgto, subject, timestamp, priority, formname, ID)
   
    return 

  def createSentboxDictionaryItem(self, ID, msgto, msgfrom, subject, priority, timestamp, formname, content):

    #self.debug.info_message("in createSentboxDictionaryItem LOC 1\n")

    self.sentbox_file_dictionary_data[ID] = {'content'            : content,
                                             'to'                 : msgto,
                                             'from'               : msgfrom,
                                             'subject'            : subject,
                                             'timestamp'          : timestamp,
                                             'priority'           : priority,
                                             'formname'           : formname}

    return (self.sentbox_file_dictionary_data)




  """
  Multiple dictioary categories section
  """
  def transferOutboxMsgToSentbox(self, ID):

    """ locate the message """
    message = self.outbox_file_dictionary_data.get(ID)
    msgto     = message.get('to')
    msgfrom   = message.get('from')
    subject   = message.get('subject')
    timestamp = message.get('timestamp')
    priority  = message.get('priority')
    formname  = message.get('formname')
    content   = message.get('content')

    """ copy the message over """
    self.createSentboxDictionaryItem(ID, msgto, msgfrom, subject, priority, timestamp, formname, content)
    self.group_arq.addMessageToSentbox(msgfrom, msgto, subject, timestamp, priority, formname, ID)

    return

  """
  Multiple dictioary categories section
  """
  def transferOutboxMsgToRelaybox(self, ID):

    try:
      """ locate the message """
      message = self.outbox_file_dictionary_data.get(ID)
      msgto     = message.get('to')
      msgfrom   = message.get('from')
      subject   = message.get('subject')
      timestamp = message.get('timestamp')
      priority  = message.get('priority')
      formname  = message.get('formname')
      content   = message.get('content')

      confirmed_received = 'yes'
      frag_size = 20

      """ copy the message over """
      self.createRelayboxDictionaryItem(ID, msgto, msgfrom, subject, priority, timestamp, formname, confirmed_received, frag_size, content)
      self.group_arq.addMessageToRelaybox(msgfrom, msgto, subject, timestamp, priority, formname, ID, confirmed_received, frag_size)

    except:
      self.debug.error_message("Exception in transferOutboxMsgToRelaybox: " + str(sys.exc_info()[0]) + str(sys.exc_info()[1] ))

    return


  """
  Main application settings dictionary
  """
  def readMainDictionaryFromFile(self, filename):


    try:
      with open(filename) as f:
        data = f.read()
 
      js = json.loads(data)
    except:
      self.debug.error_message("Exception in readMainDictionaryFromFile: " + str(sys.exc_info()[0]) + str(sys.exc_info()[1] ))

      js = { 'params': {'Templates'         : ['standard_templates.tpl'],
                      'AutoLoadTemplate'  : True,
                      'FirstName'         : '',
                      'LastName'          : '',
                      'Position'          : '',
                      'GPSLat'            : '',
                      'GPSLong'           : '',
                      'CallSign'          : '',
                      'GridSquare'        : '',
                      'Location'          : ''} }

    auto_load_templates = js.get("params").get('AutoLoadTemplate')
    if(auto_load_templates):
      self.group_arq.clearCategories()
      templates = js.get("params").get('Templates')
      for x in range (len(templates)):
        self.readTemplateDictFromFile(templates[x])
        self.debug.info_message("LOADING TEMPLATE: " + templates[x] )

    return(js)


  """ writes the messages to the messages file """
  def writeMainDictionaryToFile(self, filename, values):

    """ individual fields first """	  
    details = { 'params': {
                           'Templates'         : ['standard_templates.tpl'],
                           'UseAttachedGps'      : 'Rig1',
                           'AutoReceive'         : values['cb_mainwindow_autoacceptps'],
                           'AutoLoadTemplate'    : values['cb_settings_autoload'],

                           #'TemplateAutoLoad'    : 'Rig1',
                           'TrustOrigSenderOnly' : values['cb_settings_trustorigsndronly'],
                           'TrustedRelays'       : values['in_settings_trustedrelays'],  
                           'Rig1Vox'             : values['cb_settings_vox1'],
                           'Rig1Js8callIp'       : values['input_settings_js8callip1'],
                           'Rig1Js8callPort'     : values['input_settings_js8callport1'],
                           'Rig1Js8callMode'     : 'Turbo',  #values[''],
                           'Rig1FldigiIp'        : values['input_settings_fldigiip1'],
                           'Rig1FldigiPort'      : values['input_settings_fldigiport1'],
                           'Rig1FldigiMode'      : values['combo_settings_fldigimoode1'],
                           'Rig2Vox'             : values['cb_settings_vox2'],
                           'Rig2Js8callIp'       : values['input_settings_js8callip2'],
                           'Rig2Js8callPort'     : values['input_settings_js8callport2'],
                           'Rig2Js8callMode'     : 'Turbo',  #values[''],
                           'Rig2FldigiIp'        : values['input_settings_fldigiip2'],
                           'Rig2FldigiPort'      : values['input_settings_fldigiport2'],
                           'Rig2FldigiMode'      : values['combo_settings_fldigimoode2'],

                           'ComposeTabClr'      : values['option_colors_compose_tab'],
                           'InboxTabClr'        : values['option_colors_inbox_tab'],
                           'OutboxTabClr'       : values['option_colors_outbox_tab'],
                           'SentboxTabClr'      : values['option_colors_sentbox_tab'],
                           'RelayboxTabClr'     : values['option_colors_relay_tab'],
                           'InfoTabClr'         : values['option_colors_info_tab'],
                           'ColorsTabClr'       : values['option_colors_colors_tab'],
                           'SettingsTabClr'     : values['option_colors_settings_tab'],

                           'FldigChannelClr'    : 'Red',  #values[''],
                           'Js8CallChannelClr'  : 'Red',  #values[''],
                           'TxButtonClr'        : values['option_colors_tx_btns'],
                           'MessagesBtnClr'     : values['option_colors_msgmgmt_btns'],
                           'ClipboardBtnClr'    : values['option_colors_clipboard_btns'],
                           'TabClr'             : 'Red',  #values[''],
                           'TxRig'              : 'Red',  #values[''],
                           'Flash1Clr'          : 'Red',  #values[''],
                           'Flash2Clr'          : 'Red',  #values[''],
                           'StubMsgClr'         : 'Red',  #values[''],
                           'PartialMsgClr'      : 'Red',  #values[''],
                           'CompleteMsgClr'     : 'Red',  #values[''], 
                           'AllConfirmedMsgClr'       : 'Red',  #values[''],
                           'NotAllConfirmedMsgClr'    : 'Red',  #values[''],
                           'FormHeadingClr'           : 'Red',  #values[''],
                           'FormSubHeadingClr'        : 'Red',  #values[''],
                           'FormPreviewBackgroundClr' : 'Red',  #values[''],

                           'TxRig'           : 'Red',  #values[''],
                           'TxModeType'      : 'Red',  #values[''],
                           'Rig1Name'        : 'Red',  #values[''],
                           'Rig1Modem'       : 'Red',  #values[''],
                           'Rig1Mode'        : 'Red',  #values[''],
                           'Rig1FragmSize'   : 'Red',  #values[''],
                           'Rig2Name'        : 'Red',  #values[''],
                           'Rig2Modem'       : 'Red',  #values[''],
                           'Rig2Mode'        : 'Red',  #values[''],
                           'Rig2FragmSize'   : 'Red',  #values[''],
                           'CallSign'        : values['input_myinfo_callsign'],
                           'GroupName'       : values['input_myinfo_group_name'],
                           'OperatorName'    : values['input_myinfo_operator_name'],
                           'OperatorTitle'   : values['input_myinfo_operator_title'],
                           'IncidentName'    : values['input_myinfo_incident_name'],
                           'FirstName'       : values['input_myinfo_firstname'],
                           'LastName'        : values['input_myinfo_lastname'],
                           'Title'           : values['input_myinfo_title'],
                           'Position'        : 'Red',  #values[''],
                           'GPSLat'          : values['input_myinfo_gpslat'],
                           'GPSLong'         : values['input_myinfo_gpslong'],
                           'GridSquare'      : values['input_myinfo_gridsquare'],
                           'Location'        : values['input_myinfo_location'],} }
 
    with open(filename, 'w') as convert_file:
              convert_file.write(json.dumps(details))
    return()



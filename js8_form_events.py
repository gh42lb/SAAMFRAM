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
import js8_form_dictionary

from datetime import datetime, timedelta
from datetime import time

from uuid import uuid4

import clipboard as clip

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


class ReceiveControlsProc(object):
  
  
  def __init__(self, group_arq, form_gui, form_dictionary, debug):  
    self.form_gui = form_gui
    self.form_dictionary = form_dictionary
    self.group_arq = group_arq
    self.current_edit_string = []
    self.current_edit_category = ''
    self.background_snr = ''
    self.saamfram = None
    self.debug = debug

    self.refresh_timer = 0

    self.countdown_timer = 0
    self.countdown_timer_delay = 5 
    self.tablerow_templaterow_xref = {}
    self.window_initialized = False

    self.flash_timer_group1 = 0
    self.flash_toggle_group1 = 0
    self.flash_buttons_group1 = {
                                  'btn_compose_saam'     : ['False', 'red,green1', 'green1,red'],
                                  'btn_compose_qrysaam'  : ['False', 'red,green1', 'green1,red'],
                                }
    

  def setSaamfram(self, saamfram):
    self.saamfram = saamfram

  def getSaamfram(self):
    return self.saamfram

  def setCountdownTimer(self, value):
    self.countdown_timer = value
    return

  def getCountdownTimer(self):
    return self.countdown_timer

  def getCountdownTimerDelay(self):
    return self.countdown_timer_delay	  

  def getCountdownTimerDelay(self, delay):
    self.countdown_timer_delay = delay
    return

  def setCommStatus(self, comm_status):
    self.comm_status = comm_status
    return

  def getCommStatus(self):
    return self.comm_status

  def getRetransmitCount(self):
    return self.retransmit_count

  def setRetransmitCount(self, retransmit_count):
    self.retransmit_count = retransmit_count
    return
    
  def getMaxRetransmit(self):
    return self.max_retransmit


    
  def setFormGui(self, form_gui):
    self.form_gui = form_gui
    return


  def setFormDictionary(self, form_dictionary):
    self.form_dictionary = form_dictionary
    return

  def setGroupArq(self, group_arq):
    self.group_arq = group_arq
    return

   
  def event_catchall(self, values):


    if(self.window_initialized == False and self.form_gui.window != None):
      self.window_initialized = True		
      """ select the initial category and form on the compose tab"""
      self.form_gui.window['tbl_compose_categories'].update(select_rows=[0])

      """ update the colors in the inbox"""
      self.form_gui.window['table_inbox_messages'].update(values=self.group_arq.getMessageInbox() )
      self.form_gui.window['table_inbox_messages'].update(row_colors=self.group_arq.getMessageInboxColors())

      self.form_gui.window['table_relay_messages'].update(values=self.group_arq.getMessageRelaybox() )
      self.form_gui.window['table_relay_messages'].update(row_colors=self.group_arq.getMessageRelayboxColors())


      if(self.getSaamfram().tx_mode == 'JS8CALL'):
        #combo_sendto = 'Rig 1 - JS8'.split(',')
        self.form_gui.window['option_outbox_txrig'].update(values=['Rig 1 - JS8'])
        self.form_gui.window['option_outbox_txrig'].update('Rig 1 - JS8')
      elif(self.getSaamfram().tx_mode == 'FLDIGI'):
        #combo_sendto = 'Rig 1 - JS8'.split(',')
        self.form_gui.window['option_outbox_txrig'].update(values=['Rig 1 - FLDIGI'])
        self.form_gui.window['option_outbox_txrig'].update('Rig 1 - FLDIGI')

      #self.form_gui.window['tbl_compose_select_form'].update(select_rows=[0])

      #FIXME THIS IS BROKEN!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      #FIXME THIS IS BROKEN ALSO FOR FORM DEWSIGNER
      #if(saam != None and saam.tx_mode == 'JS8CALL' and self.group_arq.formdesigner_mode == False):
      #  self.group_arq.getSpeed()


    saam = self.getSaamfram()
    #FIXME NEED TO TEST IF USING JS8 OR FLDIGI 
    if(saam != None and saam.tx_mode == 'JS8CALL' and self.window_initialized == True):
      saam.processSendJS8()

      """ need to poll JS8Call to get the speed"""
      #FIXME THIS IS BROKEN ALSO FOR FORM DEWSIGNER
      if(self.refresh_timer <30):
        self.refresh_timer = self.refresh_timer + 1
      elif(self.refresh_timer >=30):
        self.group_arq.getSpeed()
        self.refresh_timer = 0


    if(self.group_arq.formdesigner_mode == False):
      if(self.flash_timer_group1 <6):
        self.flash_timer_group1 = self.flash_timer_group1 + 1
      elif(self.flash_timer_group1 >=6):
        self.flash_timer_group1 = 0

        if(self.window_initialized == True and self.form_gui.window['in_inbox_listentostation'].get().strip() == ''):
          #self.form_gui.window['text_mainarea_connect_to'].update(text_color='Red')
          self.form_gui.window['in_inbox_listentostation'].update(background_color = 'Red')
        else:
          #self.form_gui.window['text_mainarea_connect_to'].update(text_color='White')
          self.form_gui.window['in_inbox_listentostation'].update(background_color = 'White')

        if(self.form_gui.window['in_inbox_listentostation'].get().strip() == ''):
          self.changeFlashButtonState('btn_compose_qrysaam', True)
        else:
          self.changeFlashButtonState('btn_compose_qrysaam', False)

        for key in self.flash_buttons_group1:
          button_colors = self.flash_buttons_group1.get(key)
          flash = button_colors[0]
          if(flash == 'True'):
            if(self.flash_toggle_group1 == 0 and values != None):
              self.flash_toggle_group1 = 1
              button_on = button_colors[1].split(',')
              button_clr1_on = button_on[0]
              button_clr2_on = button_on[1]
              self.form_gui.window[key].Update(button_color=(button_clr1_on, button_clr2_on))
            else:
              self.flash_toggle_group1 = 0
              button_off = button_colors[2].split(',')
              button_clr1_off = button_off[0]
              button_clr2_off = button_off[1]
              self.form_gui.window[key].Update(button_color=(button_clr1_off, button_clr2_off))
	  
    return()

  def changeFlashButtonState(self, button_name, state):
    button_colors = self.flash_buttons_group1.get(button_name)
    button_on  = button_colors[1]
    button_off = button_colors[2]
    if(state == True):
      self.flash_buttons_group1[button_name] = ['True', button_on, button_off]
    elif(state == False):
      self.flash_buttons_group1[button_name] = ['False', button_on, button_off]

  def updateSimulatedPreview(self, mytemplate):

    self.debug.info_message("update simulated preview\n")

    text_equiv = ''
    table_data = []
   
    form_content = ['gfhjgfhj', 'asdf', 'gfhjgfhj', 'sadf']
    content_count = 0
    field_count = 0
    
    row_num = 1
    
    for x in range (2, len(mytemplate)):
      line = mytemplate[x]

      self.debug.info_message("processing line: " + str(x) )

      self.debug.info_message("line is: " + str(line) )

      window_line = ''
      split_string = line.split(',')
      for y in range (len(split_string)):
        field = split_string[y]
        mylist = self.form_gui.field_lookup[field]

        self.debug.info_message("mylist is: " + str(mylist) )

        keyname = 'field_' + str(field_count)
        window_line = window_line + ' ' + (mylist[4](self, keyname, '', mylist[0], mylist[1], mylist[2], 0, None))

        self.debug.info_message("window line: " + str(window_line) )

        if(mylist[4] == True):
          content_count = content_count + 1  
        field_count = field_count + 1
        self.debug.info_message("line : " + str(mylist) )

      split_string = window_line.split('\n')
      for z in range(len(split_string)):
        self.tablerow_templaterow_xref[row_num] = x-1
        table_data.append( [str("{:02d}".format(row_num)) + ':    ' + split_string[z]] )
        row_num = row_num + 1

    self.debug.info_message("tablerow_templaterow_xref: " + str(self.tablerow_templaterow_xref) )
    self.debug.info_message("TABLE DATA IS: " + str(table_data) )

    return (table_data)


  def event_btntmpltpreviewform(self, values):
    self.debug.info_message("BTN NEW TEMPLATE\n")

    form_content = ['', '', '', '']

    #FIXME SHOULD NOT BE HARDCODED
    ID='123'
    msgto = 'WH6ABC;WH6DEF;WH6XYZ'

    category    = values['in_tmpl_category_name']
    formname    = values['in_tmpl_name']
    description = values['in_tmpl_desc']
    version     = values['in_tmpl_ver']
    filename    = values['in_tmpl_file']
    
    subject = ''
    window = self.form_gui.createDynamicPopupWindow(formname, form_content, category, msgto, filename, ID, subject, True)
    dispatcher = PopupControlsProc(self, window)
    self.form_gui.runPopup(self, dispatcher, window)

    return()

  def event_tmplt_template(self, values):
    self.debug.info_message("EVENT TMPLT TEMPLATE\n")
    
    line_index = int(values['tbl_tmplt_templates'][0])
    field_1 = (self.group_arq.getTemplates()[line_index])[0]
    field_2 = (self.group_arq.getTemplates()[line_index])[1]
    field_3 = (self.group_arq.getTemplates()[line_index])[2]
    field_4 = (self.group_arq.getTemplates()[line_index])[3]

    self.form_gui.window['in_tmpl_name'].update(field_1)
    self.form_gui.window['in_tmpl_desc'].update(field_2)
    self.form_gui.window['in_tmpl_ver'].update(field_3)
    self.form_gui.window['in_tmpl_file'].update(field_4)

    edit_list = self.form_dictionary.getDataFromDictionary(field_1, field_2, field_3, field_4)

    self.debug.info_message("edit string: " + str(edit_list) )

    self.debug.info_message("UPDATEING SIMULATED PREVIEW WITH: " + str(edit_list) )
    table_data = self.updateSimulatedPreview(edit_list)

    self.debug.info_message("table data : " + str(table_data) )

    self.form_gui.window['table_templates_preview'].update(values=table_data)

    self.current_edit_string = edit_list

    self.debug.info_message("edit string: " + str(self.current_edit_string) )
    return()

  def event_tmplt_newtemplate(self, values):
    self.debug.info_message("EVENT TMPLT NEW TEMPLATE\n")

    category    = values['in_tmpl_category_name']
    formname    = values['in_tmpl_name']
    description = values['in_tmpl_desc']
    version     = values['in_tmpl_ver']
    filename    = values['in_tmpl_file']

    self.debug.info_message("EVENT TMPLT NEW TEMPLATE 2\n")

    self.group_arq.addTemplate(formname, description, version, filename)

    self.debug.info_message("EVENT TMPLT NEW TEMPLATE 3\n")

    data = [version,description,'T1,I1']

    self.debug.info_message("EVENT TMPLT NEW TEMPLATE 4\n")

    self.form_dictionary.createNewTemplateInDictionary(filename, category, formname, version, description, data)

    table_data = self.updateSimulatedPreview(data)
    self.debug.info_message("table data : " + str(table_data) )
    self.form_gui.window['table_templates_preview'].update(values=table_data)
    self.current_edit_string = data

    self.debug.info_message("EVENT TMPLT NEW TEMPLATE 5\n")

    self.form_gui.window['tbl_tmplt_templates'].update(self.group_arq.getTemplates())
    return

  def event_tmplt_updatetemplate(self, values):
    self.debug.info_message("EVENT TMPLT UPDATE TEMPLATE\n")

    line_index = int(values['tbl_tmplt_templates'][0])

    field_1 = values['in_tmpl_name']
    field_2 = values['in_tmpl_desc']
    field_3 = values['in_tmpl_ver']
    field_4 = values['in_tmpl_file']

    templates = self.group_arq.getTemplates()
    templates[line_index][0] = field_1
    templates[line_index][1] = field_2
    templates[line_index][2] = field_3
    templates[line_index][3] = field_4

    self.form_gui.window['tbl_tmplt_templates'].update(self.group_arq.getTemplates())

    return

  def event_tmplt_deletetemplate(self, values):
    self.debug.info_message("EVENT TMPLT DELETE TEMPLATE\n")

    line_index = int(values['tbl_tmplt_templates'][0])

    self.debug.info_message("line index = " + str(line_index) )
    
    templates = self.group_arq.getTemplates()
    filename = templates[line_index][3]
    formname = templates[line_index][0]
    category = values['in_tmpl_category_name']
    templates.remove(templates[line_index])
    
    self.debug.info_message("FILENAME:  " + str(filename) )
    self.debug.info_message("FORMNAME:  " + str(formname) )
    self.debug.info_message("CATEGORY:  " + str(category) )
    self.form_dictionary.removeTemplateFromTemplateDictionary(filename, category, formname)
   
    self.form_gui.window['tbl_tmplt_templates'].update(self.group_arq.getTemplates())
   
    return
    
  def event_tmplt_savetemplate(self, values):
    self.debug.info_message("EVENT TMPLT SAVE TEMPLATE\n")

    field_1 = values['in_tmpl_name']
    field_2 = values['in_tmpl_desc']
    field_3 = values['in_tmpl_ver']
    field_4 = values['in_tmpl_file']
    
    self.debug.info_message("WRITING FILE: "+ field_4 )
    
    self.form_dictionary.writeTemplateDictToFile(field_4)

    return

  def event_tmplt_loadsel(self, values):
    self.debug.info_message("EVENT TMPLT LOAD SELECTED FILE\n")

    self.form_dictionary.readTemplateDictFromFile("my_test_tmplt.tpl")

    self.form_gui.window['tbl_tmplt_categories'].update(self.group_arq.getCategories())
    self.form_gui.window['tbl_compose_categories'].update(self.group_arq.getCategories())

    return
    

  def event_settings_add(self, values):
    self.debug.info_message("EVENT TMPLT ADD FILE\n")

    line_index = int(values['tbl_layout_all_files'][0])

    templatefiles = self.group_arq.getTemplateFiles()
    filename = templatefiles[line_index][0]

    self.debug.info_message("filename to add is: " + str(filename) )

    self.form_dictionary.readTemplateDictFromFile(filename)
    self.form_gui.window['tbl_tmplt_categories'].update(self.group_arq.getCategories())
    self.form_gui.window['tbl_compose_categories'].update(self.group_arq.getCategories())

    description = self.form_dictionary.getFileDescriptionFromTemplateDictionary(filename)
    version     = self.form_dictionary.getFileVersionFromTemplateDictionary(filename)

    self.group_arq.addLoadedTemplateFile(filename, description, version)
    self.form_gui.window['tbl_tmplt_files'].update(self.group_arq.getLoadedTemplateFiles())
    return

  def event_settings_tmplt_remove(self, values):
    self.debug.info_message("EVENT TMPLT REMOVE SELECTED FILE\n")

    line_index = int(values['tbl_tmplt_files'][0])

    self.debug.info_message("line index = " + str(line_index) )
    
    templatefiles = self.group_arq.getLoadedTemplateFiles()
    filename = templatefiles[line_index][0]
    templatefiles.remove(templatefiles[line_index])

    self.debug.info_message("filename: " + str(filename) )
    self.form_dictionary.removeTemplatesFileFromTemplateDictionary(filename)
    
    self.form_gui.window['tbl_tmplt_files'].update(self.group_arq.getLoadedTemplateFiles())

    return


  def event_tmplt_categories(self, values):
    self.debug.info_message("EVENT TMPLT CATEGORIES\n")
    line_index = int(values['tbl_tmplt_categories'][0])
    category = (self.group_arq.getCategories()[line_index])[0]

    self.debug.info_message("category: " + category )

    self.form_dictionary.getTemplatesFromCategory(category)

    self.current_edit_category = category

    self.form_gui.window['tbl_tmplt_templates'].update(self.group_arq.getTemplates())

    self.form_gui.window['in_tmpl_category_name'].update(category)
    
    return

  def event_tablepreview(self, values):
    self.debug.info_message("EVENT TABLE PREVIEW\n")

    line_index_form = int(values['table_templates_preview'][0])+1
    self.debug.info_message("line index form = " + str(line_index_form) )
    line_index = self.tablerow_templaterow_xref[line_index_form]-1
    self.debug.info_message("line index = " + str(line_index) )

    self.form_gui.window['in_tmpl_line_number'].update(str(line_index+1))

    edit_list = self.current_edit_string

    line_data = str(edit_list[2+line_index]) 		
    self.debug.info_message("data item:" + line_data )

    for x in range (12):
      field_name = 'combo_element' + str(x+1)
      self.form_gui.window[field_name].update('-')


    split_string = line_data.split(',')
    for x in range (len(split_string)):
      self.debug.info_message(" line item:" + split_string[x] )
      field_name = 'combo_element' + str(x+1)
      self.form_gui.window[field_name].update(self.form_gui.field_names[ split_string[x] ])

    clipboard_string = 'JSDIGI_FORMS_CLIPBOARD_DATA={'
    checked = values['cb_tmplt_clipcopyto']
    if(checked):
      self.form_gui.window['in_tmpl_clipcopyto'].update(str(line_index+1))
      self.form_gui.window['cb_tmplt_clipcopyto'].update(False)

      index_from = values['in_tmpl_clipcopyfrom']
      index_to = str(line_index+1)
      if(index_to != '' and index_from != ''):
        for line_index in range(int(index_from)-1, int(index_to)) :
          string_data = str(edit_list[2+line_index]) 		
          self.debug.info_message(" line to copy: " + string_data )
          if(line_index > int(index_from)-1):
            clipboard_string = clipboard_string + ',\'' + string_data + '\''
          else:
            clipboard_string = clipboard_string + '\'' + string_data + '\''

      clipboard_string = clipboard_string + '}'

      self.debug.info_message(" clipboard string: " + clipboard_string )
      clip.copy(clipboard_string)

    checked = values['cb_tmplt_clipcopyfrom']
    if(checked):
      self.form_gui.window['in_tmpl_clipcopyfrom'].update(str(line_index+1))
      self.form_gui.window['cb_tmplt_clipcopyfrom'].update(False)
      self.form_gui.window['cb_tmplt_clipcopyto'].update(True)

    return

  def event_tmpltupdate(self, values):
    self.debug.info_message("EVENT TABLE UPDATE\n")
    self.debug.info_message("line index: " + str(values['in_tmpl_line_number']) )

    line_index = int(values['in_tmpl_line_number'])-1

    self.debug.info_message("line index: " + str(line_index) )

    new_string = ''
    
    try:
      for x in range(12):
        field_name = 'combo_element' + str(x+1)
        if(values[field_name] != '-'):
          if(x > 0):		  
            new_string = new_string + ',' + self.form_gui.reverse_field_names[values[field_name] ]
          else:
            new_string = new_string + self.form_gui.reverse_field_names[values[field_name] ]
    except:
      self.debug.error_message("Exception in event_tmpltupdate: " + str(sys.exc_info()[0]) + str(sys.exc_info()[1] ))

    self.debug.info_message("new string: " + new_string )
					  
    self.current_edit_string[2+line_index]=new_string

    formname = values['in_tmpl_name']
    filename = values['in_tmpl_file']
    category = self.current_edit_category
    self.debug.info_message("formname: " + formname )
    self.debug.info_message("filename: " + filename )
    self.debug.info_message("category: " + category )
    self.debug.info_message("edit string: " + str(self.current_edit_string) )
    js = self.form_dictionary.setDataInDictionary(formname, category, filename, self.current_edit_string)
    self.debug.info_message("js: " + str(js) )
        
    table_data = self.updateSimulatedPreview(self.current_edit_string)
    self.form_gui.window['table_templates_preview'].update(values=table_data)

    return

  def event_tmplt_addrow(self, values):
    self.debug.info_message("EVENT TEMPLATE ADD ROW\n")

    insert_where = values['combo_tmplt_insertwhere']

    self.debug.info_message("combo value = " + str(insert_where) )

    if(insert_where == 'Before'):
      linestr = values['table_templates_preview']
      self.debug.info_message("line str is: " + str(linestr) )
      if(linestr != '[]'):		
        line_index_form = int(values['table_templates_preview'][0])+1
        line_index = self.tablerow_templaterow_xref[line_index_form]-1

        self.debug.info_message("line index is" + str(line_index) )
        new_string = 'T1'		
        self.current_edit_string.insert(line_index+2, new_string)
        self.debug.info_message("edit string: " + str(self.current_edit_string) )
        formname = values['in_tmpl_name']
        filename = values['in_tmpl_file']
        category = self.current_edit_category
        js = self.form_dictionary.setDataInDictionary(formname, category, filename, self.current_edit_string)
        table_data = self.updateSimulatedPreview(self.current_edit_string)
        self.form_gui.window['table_templates_preview'].update(values=table_data)

        self.form_gui.window['table_templates_preview'].update(select_rows=[line_index_form-1])

      self.debug.info_message("insert before\n")
    elif(insert_where == 'After'):
      linestr = values['table_templates_preview']
      self.debug.info_message("line str is: " + str(linestr) )
      if(linestr != '[]'):		
        line_index_form = int(values['table_templates_preview'][0])+1
        line_index = self.tablerow_templaterow_xref[line_index_form]-1

        self.debug.info_message("line index is" + str(line_index) )
        new_string = 'T1'		
        self.current_edit_string.insert(line_index+3, new_string)
        self.debug.info_message("edit string: " + str(self.current_edit_string) )
        formname = values['in_tmpl_name']
        filename = values['in_tmpl_file']
        category = self.current_edit_category
        js = self.form_dictionary.setDataInDictionary(formname, category, filename, self.current_edit_string)
        table_data = self.updateSimulatedPreview(self.current_edit_string)
        self.form_gui.window['table_templates_preview'].update(values=table_data)
        self.form_gui.window['in_tmpl_line_number'].update(str(line_index+2))

        self.form_gui.window['table_templates_preview'].update(select_rows=[line_index_form])

      self.debug.info_message("inser after\n")
    elif(insert_where == 'At'):
      linestr = values['table_templates_preview']
      self.debug.info_message("line str is: " + str(linestr) )
      if(linestr != '[]'):		
        line_index_form = int(values['table_templates_preview'][0])+1
        line_index = self.tablerow_templaterow_xref[line_index_form]-1

        self.debug.info_message("line index is" + str(line_index) )
        new_string = 'T1'		
        self.current_edit_string.insert(line_index+2, new_string)
        self.debug.info_message("edit string: " + str(self.current_edit_string) )
        formname = values['in_tmpl_name']
        filename = values['in_tmpl_file']
        category = self.current_edit_category
        js = self.form_dictionary.setDataInDictionary(formname, category, filename, self.current_edit_string)
        table_data = self.updateSimulatedPreview(self.current_edit_string)
        self.form_gui.window['table_templates_preview'].update(values=table_data)
        self.form_gui.window['in_tmpl_line_number'].update(str(line_index+2))

        self.form_gui.window['table_templates_preview'].update(select_rows=[line_index_form-1])

      self.debug.info_message("inser at\n")
    elif(insert_where == 'End'):
      self.debug.info_message("Insert at End\n")
      new_string = 'T1'		
      self.current_edit_string.append(new_string)
      self.debug.info_message("edit string: " + str(self.current_edit_string) )
      formname = values['in_tmpl_name']
      filename = values['in_tmpl_file']
      category = self.current_edit_category
      js = self.form_dictionary.setDataInDictionary(formname, category, filename, self.current_edit_string)
      table_data = self.updateSimulatedPreview(self.current_edit_string)
      self.form_gui.window['table_templates_preview'].update(values=table_data)

    return

  def event_tmplt_typingsomething(self, values):
    self.debug.info_message("EVENT TYPING SOMETHING\n")

    categoryname = values['in_tmpl_category_name']
    templatename = values['in_tmpl_name']
    description  = values['in_tmpl_desc']
    version      = values['in_tmpl_ver']
    filename     = values['in_tmpl_file']
    return


  def event_composemsg(self, values):
    self.debug.info_message("BTN COMPOSE\n")

    line_index = int(values['tbl_compose_categories'][0])
    category = (self.group_arq.getCategories()[line_index])[0]
    line_index = int(values['tbl_compose_select_form'][0])
    formname = (self.group_arq.getTemplates()[line_index])[0]
    filename = (self.group_arq.getTemplates()[line_index])[3]
    form_content = ['', '', '', '']

    self.debug.info_message("SELECTED CATEGORY IS: "  + category )
    self.debug.info_message("SELECTED FORMNAME IS: "  + formname )

    selected_stations = self.group_arq.getSelectedStations()

    msgto = values['in_compose_selected_callsigns']
   
    callsign = self.saamfram.getMyCall()

    self.debug.info_message("saamfram: " + str(self.saamfram) +  "\n")

    ID = self.saamfram.getEncodeUniqueId(callsign)
   
    self.saamfram.getDecodeTimestampFromUniqueId(ID)

    self.debug.info_message("reverse encoded callsign is: " + self.group_arq.saamfram.getDecodeCallsignFromUniqueId(ID) )

    self.debug.info_message("UNIQUE ID USING UUID IS: " + str(ID) )
    subject = ''
    window = self.form_gui.createDynamicPopupWindow(formname, form_content, category, msgto, filename, ID, subject, True)
    dispatcher = PopupControlsProc(self, window)
    self.form_gui.runPopup(self, dispatcher, window)

    return()

  def event_prevposttooutbox(self, values):
    self.debug.info_message("BTN POST TO OUTBOX\n")

    try:
      """ loop thru the dictionary to populate outbox display """
      fromform_ID = values['preview_message_id']	  
    
      self.debug.info_message("ID IS: " + str(fromform_ID) )

      ID = ''

      self.debug.info_message("POST TO OUTBOX LOC1\n")

      if(self.group_arq.saamfram.isReply(fromform_ID)):
        mainID = self.group_arq.getOriginalSenderID(fromform_ID)
        replyID = self.group_arq.getReplyID(fromform_ID)
        ID = replyID
      else:
        ID = fromform_ID

      timestamp = self.group_arq.saamfram.getDecodeTimestampFromUniqueId(ID)
      msgfrom   = self.group_arq.saamfram.getDecodeCallsignFromUniqueId(ID)

      self.debug.info_message("POST TO OUTBOX LOC2\n")

      msgto = values['preview_message_msgto']
      subject = values['preview_form_subject']
      priority = values['preview_message_priority']
      formname = values['preview_form_type']	  
      content = self.form_gui.extractContentFromForm(values)
  
      self.debug.info_message("POST TO OUTBOX LOC3\n")
  
      dictionary = self.form_dictionary.createOutboxDictionaryItem(ID, msgto, msgfrom, subject, priority, timestamp, formname, content)
      message_dictionary = dictionary.get(ID)		  

      self.debug.info_message("POST TO OUTBOX LOC4\n")
		  
      content   = message_dictionary.get('content')		  
      msgto     = message_dictionary.get('to')		  
      msgfrom   = message_dictionary.get('from')		  
      subject   = message_dictionary.get('subject')		  
      timestamp = message_dictionary.get('timestamp')		  
      priority  = message_dictionary.get('priority')		  
      msgtype   = message_dictionary.get('formname')		  
      self.group_arq.addMessageToOutbox(msgfrom, msgto, subject, timestamp, priority, msgtype, ID)
      self.form_gui.window['table_outbox_messages'].update(values=self.group_arq.getMessageOutbox() )

      self.debug.info_message("POST TO OUTBOX LOC5\n")

      if(self.group_arq.saamfram.isReply(fromform_ID)):
        """ there is no need to refresh the inbox table as the item already exist this is just a sub page"""
        self.form_dictionary.addInboxDictionaryReply(mainID, replyID, msgto, msgfrom, subject, priority, timestamp, formname, content)

      self.debug.info_message("POST TO OUTBOX LOC6\n")

      self.form_dictionary.writeOutboxDictToFile('outbox.msg')
    except:
      self.debug.error_message("Exception in event_prevposttooutbox: " + str(sys.exc_info()[0]) + str(sys.exc_info()[1] ))

    self.debug.info_message("POST TO OUTBOX LOC7\n")

    return()


  def event_tableoutboxmessages(self, values):
    self.debug.info_message("TABLE OUTBOX MESSAGES\n")

    line_index = int(values['table_outbox_messages'][0])
    msgid = (self.group_arq.getMessageOutbox()[line_index])[6]
    formname = (self.group_arq.getMessageOutbox()[line_index])[5]

    self.debug.info_message("MESSAGE ID = " + str(msgid) )

    form_content = self.form_dictionary.getContentFromOutboxDictionary(msgid)

    mytemplate = self.form_dictionary.getTemplateByFormFromTemplateDictionary(formname)
    use_dynamic_content_macro = False
    text_render, table_data, actual_render = self.form_gui.renderPage(mytemplate, use_dynamic_content_macro, form_content)


    self.form_gui.window['table_outbox_preview'].update(values=table_data )
    return

  def event_tableinboxmessages(self, values):
    self.debug.info_message("TABLE INBOX MESSAGES\n")

    line_index = int(values['table_inbox_messages'][0])
    msgid = (self.group_arq.getMessageInbox()[line_index])[7]
    formname = self.form_dictionary.getFormnameFromInboxDictionary(msgid)

    self.debug.info_message("MESSAGE ID AND FORMNAME = " + str(msgid) + "," + formname)

    form_content = self.form_dictionary.getContentFromInboxDictionary(msgid)

    mytemplate = self.form_dictionary.getTemplateByFormFromTemplateDictionary(formname)
    use_dynamic_content_macro = False
    text_render, table_data, actual_render = self.form_gui.renderPage(mytemplate, use_dynamic_content_macro, form_content)
    
    self.form_gui.window['table_inbox_preview'].update(values=table_data )

    return

  def event_outboxeditform(self, values):
    self.debug.info_message("OUTBOX EDIT FORM\n")

    line_index = int(values['table_outbox_messages'][0])
    ID        = (self.group_arq.getMessageOutbox()[line_index])[6]
    formname  = (self.group_arq.getMessageOutbox()[line_index])[5]
    priority  = (self.group_arq.getMessageOutbox()[line_index])[4]
    timestamp = (self.group_arq.getMessageOutbox()[line_index])[3]
    subject   = (self.group_arq.getMessageOutbox()[line_index])[2]
    msgto     = (self.group_arq.getMessageOutbox()[line_index])[1]
    msgfrom   = (self.group_arq.getMessageOutbox()[line_index])[0]
    
    form_content = ['gfhjgfhj', 'asdf', 'gfhjgfhj', 'sadf']

    category, filename = self.form_dictionary.getCategoryAndFilenameFromFormname(formname)

    form_content = self.form_dictionary.getContentFromOutboxDictionary(ID)
   
    window = self.form_gui.createDynamicPopupWindow(formname, form_content, category, msgto, filename, ID, subject, False)
    dispatcher = PopupControlsProc(self, window)
    self.form_gui.runPopup(self, dispatcher, window)
    return

  def event_settingslist(self, values):
    self.debug.info_message("SETTINGS LIST\n")

    try:
      self.debug.info_message("self.form_gui.window: " + str(self.form_gui) )
    except:  
      self.debug.error_message("Exception in event_settingslist: " + str(sys.exc_info()[0]) + str(sys.exc_info()[1] ))

    """ Code to locate all the template files """
    self.group_arq.clearTemplateFiles()
    folder = values['in_settings_templatefolder']
    dir_list = os.listdir(folder)
    for x in dir_list:
      if x.endswith(".tpl"):
        self.debug.info_message("template file located: " + str(x) )
        self.group_arq.addTemplateFile(str(x))
    self.form_gui.window['tbl_layout_all_files'].update(self.group_arq.getTemplateFiles())

    return


  def event_compose_categories(self, values):
    self.debug.info_message("EVENT TMPLT CATEGORIES\n")
    line_index = int(values['tbl_compose_categories'][0])
    category = (self.group_arq.getCategories()[line_index])[0]

    self.debug.info_message("category: " + category )

    self.form_dictionary.getTemplatesFromCategory(category)

    self.current_edit_category = category

    self.form_gui.window['tbl_compose_select_form'].update(self.group_arq.getTemplates())

    return

  def event_outboxsendselected(self, values):
    self.debug.info_message("EVENT OUTBOX SEND SELECTED\n")
    line_index = int(values['table_outbox_messages'][0])
    msgid = (self.group_arq.getMessageOutbox()[line_index])[6]
    formname = (self.group_arq.getMessageOutbox()[line_index])[5]
    priority = (self.group_arq.getMessageOutbox()[line_index])[4]
    subject  = (self.group_arq.getMessageOutbox()[line_index])[2]
    tolist   = (self.group_arq.getMessageOutbox()[line_index])[1]

    self.debug.info_message("EVENT OUTBOX SEND SELECTED 2\n")
    
    frag_size = 20
    frag_string = values['option_framesize'].strip()
    if(frag_string != ''):
      frag_size = int(values['option_framesize'])
      
    include_template = values['cb_outbox_includetmpl']

    self.debug.info_message("EVENT OUTBOX SEND SELECTED 2b\n")

    # this is for testing only!!!!!!
    #FIXME

    sender_callsign = self.group_arq.saamfram.getMyCall()
    tagfile = 'ICS'
    version  = '1.3'
    complete_send_string = ''
    if(include_template):
      self.debug.info_message("EVENT OUTBOX SEND SELECTED 2c\n")

      complete_send_string = self.group_arq.saamfram.getContentAndTemplateSendString(msgid, formname, priority, tolist, subject, frag_size, tagfile, version, sender_callsign)
    else:  
      self.debug.info_message("EVENT OUTBOX SEND SELECTED 2d\n")

      complete_send_string = self.group_arq.saamfram.getContentSendString(msgid, formname, priority, tolist, subject, frag_size, tagfile, version, sender_callsign)

    self.debug.info_message("EVENT OUTBOX SEND SELECTED 3\n")
    self.form_dictionary.transferOutboxMsgToSentbox(msgid)

    self.form_dictionary.transferOutboxMsgToRelaybox(msgid)
    self.form_gui.window['table_relay_messages'].update(values=self.group_arq.getMessageRelaybox() )

    self.form_gui.window['table_sent_messages'].update(values=self.group_arq.getMessageSentbox() )
    self.form_gui.window['table_outbox_messages'].update(values=self.group_arq.getMessageOutbox() )
    self.debug.info_message("EVENT OUTBOX SEND SELECTED 4\n")

    
    self.debug.info_message("EVENT OUTBOX SEND SELECTED 5\n")
    
    sender_callsign = self.group_arq.saamfram.getMyCall()
    fragtagmsg = self.group_arq.saamfram.buildFragTagMsg(complete_send_string, frag_size, self.group_arq.getSendModeRig1(), sender_callsign)

    self.debug.info_message("SEND STRING IS: " + fragtagmsg )
    
    self.debug.info_message("ACTUAL MSG SENT TO FLDIGI: " + str(fragtagmsg) )
    
    self.group_arq.sendFormRig1(fragtagmsg, tolist)

    self.form_gui.window['table_inbox_messages'].update(values=self.group_arq.getMessageInbox() )

    return

  def event_outboxsendall(self, values):
    self.debug.info_message("EVENT OUTBOX SEND ALL\n")

    for line_index in reversed(range(len(self.group_arq.getMessageOutbox()))):
      msgid = (self.group_arq.getMessageOutbox()[line_index])[6]
      formname = (self.group_arq.getMessageOutbox()[line_index])[5]
      priority = (self.group_arq.getMessageOutbox()[line_index])[4]
      subject  = (self.group_arq.getMessageOutbox()[line_index])[2]
      tolist   = (self.group_arq.getMessageOutbox()[line_index])[1]
 
      frag_size = int(values['option_framesize'])
      include_template = values['cb_outbox_includetmpl']


      complete_send_string = ''
      sender_callsign = self.saamfram.getMyCall()
      tagfile = 'ICS'
      version  = '1.3'
      if(include_template):
        complete_send_string = self.group_arq.saamfram.getContentAndTemplateSendString(msgid, formname, priority, tolist, subject, frag_size, tagfile, version, sender_callsign)
      else:  
        complete_send_string = self.group_arq.saamfram.getContentSendString(msgid, formname, priority, tolist, subject, frag_size, tagfile, version, sender_callsign)

      self.form_dictionary.transferOutboxMsgToSentbox(msgid)

    self.form_gui.window['table_sent_messages'].update(values=self.group_arq.getMessageSentbox() )
    self.form_gui.window['table_outbox_messages'].update(values=self.group_arq.getMessageOutbox() )

    return

  def event_outboxdeletemsg(self, values):
    self.debug.info_message("EVENT OUTBOX DELETE SELECTED\n")

    line_index = int(values['table_outbox_messages'][0])
    msgid = (self.group_arq.getMessageOutbox()[line_index])[6]

    self.form_dictionary.outbox_file_dictionary_data.pop(msgid, None)
    self.group_arq.deleteMessageFromOutbox(msgid)
    self.form_gui.window['table_outbox_messages'].update(values=self.group_arq.getMessageOutbox() )
    return


  def event_outboxdeleteallmsg(self, values):
    self.debug.info_message("EVENT OUTBOX DELETE ALL\n")

    self.form_dictionary.outbox_file_dictionary_data = {}
    self.group_arq.clearOutbox()
    self.form_gui.window['table_outbox_messages'].update(values=self.group_arq.getMessageOutbox() )
    return


  def event_sentboxdeletemsg(self, values):
    self.debug.info_message("EVENT SENTBOX DELETE SELECTED\n")

    line_index = int(values['table_sent_messages'][0])
    msgid = (self.group_arq.getMessageSentbox()[line_index])[6]

    self.form_dictionary.sentbox_file_dictionary_data.pop(msgid, None)
    self.group_arq.deleteMessageFromSentbox(msgid)
    self.form_gui.window['table_sent_messages'].update(values=self.group_arq.getMessageSentbox() )
    return

  def event_sentboxdeleteallmsg(self, values):
    self.debug.info_message("EVENT SENTBOX DELETE ALL\n")

    self.form_dictionary.sentbox_file_dictionary_data = {}
    self.group_arq.clearSentbox()
    self.form_gui.window['table_sent_messages'].update(values=self.group_arq.getMessageSentbox() )
    return


  def event_inboxdeleteselected(self, values):
    self.debug.info_message("EVENT INBOX DELETE SELECTED\n")

    line_index = int(values['table_inbox_messages'][0])
    msgid = (self.group_arq.getMessageInbox()[line_index])[7]

    self.form_dictionary.inbox_file_dictionary_data.pop(msgid, None)
    self.group_arq.deleteMessageFromInbox(msgid)
    self.form_gui.window['table_inbox_messages'].update(values=self.group_arq.getMessageInbox() )

    return

  def event_inboxdeleteall(self, values):
    self.debug.info_message("EVENT INBOX DELETE ALL\n")

    for line_index in reversed(range(len(self.group_arq.getMessageInbox()))):
      msgid = (self.group_arq.getMessageInbox()[line_index])[7]
      self.group_arq.deleteMessageFromInbox(msgid)

    self.form_gui.window['table_inbox_messages'].update(values=self.group_arq.getMessageInbox() )

    self.form_dictionary.resetInboxDictionary()

    return


  def event_relayboxdeleteselected(self, values):
    self.debug.info_message("EVENT RELAYBOX DELETE SELECTED\n")

    line_index = int(values['table_relay_messages'][0])
    msgid = (self.group_arq.getMessageRelaybox()[line_index])[6]

    self.form_dictionary.relaybox_file_dictionary_data.pop(msgid, None)
    self.group_arq.deleteMessageFromRelaybox(msgid)
    self.form_gui.window['table_relay_messages'].update(values=self.group_arq.getMessageRelaybox() )

    return

  def event_relayboxdeleteall(self, values):
    self.debug.info_message("EVENT RELAYBOX DELETE ALL\n")

    for line_index in reversed(range(len(self.group_arq.getMessageRelaybox()))):
      msgid = (self.group_arq.getMessageRelaybox()[line_index])[6]
      self.group_arq.deleteMessageFromRelaybox(msgid)

    self.form_gui.window['table_relay_messages'].update(values=self.group_arq.getMessageRelaybox() )

    self.form_dictionary.resetRelayboxDictionary()

    return




  def event_tablesentmessages(self, values):
    self.debug.info_message("EVENT TABLE SENT MESSAGES\n")

    line_index = int(values['table_sent_messages'][0])
    msgid = (self.group_arq.getMessageSentbox()[line_index])[6]
    formname = self.form_dictionary.getFormnameFromSentboxDictionary(msgid)

    self.debug.info_message("MESSAGE ID AND FORMNAME = " + str(msgid) + "," + formname)

    form_content = self.form_dictionary.getContentFromSentboxDictionary(msgid)

    #FIXME
    mytemplate = self.form_dictionary.getTemplateByFormFromTemplateDictionary(formname)
    use_dynamic_content_macro = False
    text_render, table_data, actual_render = self.form_gui.renderPage(mytemplate, use_dynamic_content_macro, form_content)


    self.form_gui.window['table_sent_preview'].update(values=table_data )

    return


  def event_outboxreqconfirm(self, values):
    self.debug.info_message("EVENT RESEND FRAMES OUTBOX REQUEST CONFIRM\n")

    to_callsign = self.saamfram.getSenderCall()
    from_callsign = self.saamfram.getMyCall()
    resend_frames = values['in_outbox_resendframes']
    self.group_arq.resendFrames(resend_frames, from_callsign, to_callsign)

    return

  def event_inboxrcvstatus(self, values):
    self.debug.info_message("EVENT INBOX SEND RCV STATUS\n")

    frames_missing = self.group_arq.saamfram.getFramesMissingReceiver("ABC_FDE", 5)
    self.debug.info_message("FRAMES MISSING: " + frames_missing + " \n")
    
    #FIXME CALL SIGNS SHOULD NOT BE HARDCODED
    self.group_arq.sendFormRig1("WH6ABC 3495865_DFE567 " + frames_missing, '')

    return

  def event_templateseditline(self, values):
    self.form_gui.window['cb_templates_insertdeleteline'].update(False)
    self.form_gui.window['btn_tmplt_update'].update(disabled = False)
    self.form_gui.window['btn_tmplt_add_row'].update(disabled = True)
    self.form_gui.window['btn_delete_row'].update(disabled = True)
    self.form_gui.window['in_tmpl_line_number'].update(disabled = False)
    self.form_gui.window['in_tmpl_insert_linenumber'].update(disabled = True)
    self.form_gui.window['combo_tmplt_insertwhere'].update(disabled = True)
    
    
    return
    
  def event_templatesinsertdeleteline(self, values):
    self.form_gui.window['cb_templates_editline'].update(False)
    self.form_gui.window['btn_tmplt_update'].update(disabled = True)
    self.form_gui.window['btn_tmplt_add_row'].update(disabled = False)
    self.form_gui.window['btn_delete_row'].update(disabled = False)
    self.form_gui.window['in_tmpl_line_number'].update(disabled = True)
    self.form_gui.window['in_tmpl_insert_linenumber'].update(disabled = False)
    self.form_gui.window['combo_tmplt_insertwhere'].update(disabled = False)
    
    return

  def event_tmpltdeletetemplatecategory(self, values):

    self.debug.info_message("EVENT TMPLT DELETE TEMPLATE CATEGORY\n")
    
    filename = values['in_tmpl_file']
    category = values['in_tmpl_category_name']
    
    self.debug.info_message("FILENAME:  " + str(filename) )
    self.debug.info_message("CATEGORY:  " + str(category) )

    self.form_dictionary.removeCategoryFromTemplateDictionary(filename, category)
    self.group_arq.deleteCategory(category)
    self.form_gui.window['tbl_tmplt_categories'].update(self.group_arq.getCategories())
    self.form_gui.window['tbl_tmplt_templates'].update([])

    return

  def event_composeselectform(self, values):

    self.debug.info_message("EVENT COMPOSE SELECT FORM\n")
    
    self.debug.info_message("EVENT TMPLT TEMPLATE\n")
    
    line_index = int(values['tbl_compose_select_form'][0])
    field_1 = (self.group_arq.getTemplates()[line_index])[0]
    field_2 = (self.group_arq.getTemplates()[line_index])[1]
    field_3 = (self.group_arq.getTemplates()[line_index])[2]
    field_4 = (self.group_arq.getTemplates()[line_index])[3]

    """ enable the compose button on compose tab"""
    self.form_gui.window['btn_cmpse_compose'].update(disabled = False)


    edit_list = self.form_dictionary.getDataFromDictionary(field_1, field_2, field_3, field_4)

    self.debug.info_message("edit string: " + str(edit_list) )

    self.debug.info_message("UPDATEING SIMULATED PREVIEW WITH: " + str(edit_list) )
    table_data = self.updateSimulatedPreview(edit_list)

    self.debug.info_message("table data : " + str(table_data) )

    self.form_gui.window['table_compose_preview'].update(values=table_data)

    self.current_edit_string = edit_list

    self.debug.info_message("edit string: " + str(self.current_edit_string) )
    
    return

  def event_outboxfldigimode(self, values):

    self.debug.info_message("EVENT OUTBOX FLDIGI MODE\n")
   
    selected_string = values['option_outbox_fldigimode']
    split_string = selected_string.split(' - ')
    mode = split_string[1]

    self.group_arq.fldigiclient.setMode(mode)

    return

  def event_inboxsendacknack(self, values):

    self.debug.info_message("EVENT SEND ACK NACK\n")

    error_frames = values['in_inbox_errorframes'].strip()
    from_callsign = self.saamfram.getMyCall()
    to_callsign = self.saamfram.getSenderCall()
    if(error_frames == ''):
      self.group_arq.sendAck(from_callsign, to_callsign)
    else:  
      self.group_arq.sendNack(error_frames, from_callsign, to_callsign)

    return


  def event_outboxpleaseconfirm(self, values):

    self.debug.info_message("EVENT PLEASE COONFIRM\n")

    to_callsign = self.saamfram.getSenderCall()
    from_callsign = self.saamfram.getMyCall()
    self.group_arq.requestConfirm(from_callsign, to_callsign)

  def event_inboxcopyclipboard(self, values):

    self.debug.info_message("EVENT COPY TO CLIPBOARD\n")

    a1 = "I am some text to be copied to the clipboard"
    clip.copy(a1)

  def event_outboximportfromclipboard(self, values):

    self.debug.info_message("EVENT OUTBOX IMPORT FROM CLIPBOARD\n")

    text_from_clipboard = clip.paste()
    self.debug.info_message(text_from_clipboard)

  def event_inboxreplytomsg(self, values):

    self.debug.info_message("EVENT REPLY TO INBOX MESSAGE\n")

    line_index = int(values['table_inbox_messages'][0])
    mainID = (self.group_arq.getMessageInbox()[line_index])[7]

    line_index = int(values['tbl_compose_categories'][0])
    category = (self.group_arq.getCategories()[line_index])[0]
    line_index = int(values['tbl_compose_select_form'][0])
    formname = (self.group_arq.getTemplates()[line_index])[0]
    filename = (self.group_arq.getTemplates()[line_index])[3]
   
    form_content = ['', '', '', '']

    self.debug.info_message("SELECTED CATEGORY IS: "  + category )
    self.debug.info_message("SELECTED FORMNAME IS: "  + formname )

    selected_stations = self.group_arq.getSelectedStations()
    msgto = ''
    for x in range(len(selected_stations)):
      if(x>0):		
        msgto = msgto + ';' + str(selected_stations[x])
      else:		
        msgto = msgto + str(selected_stations[x])
    
    callsign = self.saamfram.getMyCall()

    self.debug.info_message("mainID: "  + mainID )

    replyID = mainID + '-' + self.group_arq.saamfram.getEncodeUniqueId(callsign)

    self.debug.info_message("UNIQUE ID USING UUID IS: " + str(replyID) )
    
    subject = ''
    window = self.form_gui.createInboxViewReplyWindow(formname, form_content, category, msgto, filename, replyID, subject, True, True, True)
    dispatcher = PopupControlsProc(self, window)
    self.form_gui.runPopup(self, dispatcher, window)


  def event_inboxviewmsg(self, values):

    self.debug.info_message("EVENT INBOX VIEW MSG\n")

    line_index = int(values['table_inbox_messages'][0])
    ID = (self.group_arq.getMessageInbox()[line_index])[7]
    formname = (self.group_arq.getMessageInbox()[line_index])[5]
    category, filename = self.form_dictionary.getCategoryAndFilenameFromFormname(formname)

    form_content = ['', '', '', '']

    self.debug.info_message("SELECTED CATEGORY IS: "  + category )
    self.debug.info_message("SELECTED FORMNAME IS: "  + formname )

    selected_stations = self.group_arq.getSelectedStations()
    msgto = ''
    for x in range(len(selected_stations)):
      if(x>0):		
        msgto = msgto + ';' + str(selected_stations[x])
      else:		
        msgto = msgto + str(selected_stations[x])
    
    self.group_arq.saamfram.getDecodeTimestampFromUniqueId(ID)

    self.debug.info_message("reverse encoded callsign is: " + self.group_arq.saamfram.getDecodeCallsignFromUniqueId(ID) )
    self.debug.info_message("UNIQUE ID USING UUID IS: " + str(ID) )

    subject = ''
    window = self.form_gui.createInboxViewReplyWindow(formname, form_content, category, msgto, filename, ID, subject, False, False, False)
    dispatcher = PopupControlsProc(self, window)
    self.form_gui.runPopup(self, dispatcher, window)


  def event_fordesignerInsertElement(self, values):
    self.debug.info_message("INSERT ELEMENT\n")

    at_before_after = values['combo_tmplt_insertelementwhere'].strip()
    self.debug.info_message("at_before_after = " + str(at_before_after) + " \n")
    index = int(values['in_tmpl_insertelementnumber'])
    self.debug.info_message("index = " + str(index) + " \n")

    start_index = 0
    end_index = 12
    if(at_before_after == 'At' or at_before_after == 'Before'):
      start_index = index
    elif(at_before_after == 'After'):
      start_index = index +1

    self.debug.info_message("start index = " + str(start_index) + " \n")
    self.debug.info_message("end index = " + str(end_index) + " \n")

    for x in reversed (range (start_index, end_index)):
      field_name_from = 'combo_element' + str(x)
      field_name_to = 'combo_element' + str(x+1)
      contents = values[field_name_from]
      self.form_gui.window[field_name_to].update(contents)

    self.form_gui.window[field_name_from].update('-')

  def event_fordesignerDeleteElement(self, values):

    self.debug.info_message("DELETE ELEMENT\n")

    at_before_after = values['combo_tmplt_insertelementwhere'].strip()
    self.debug.info_message("at_before_after = " + str(at_before_after) + " \n")
    index = int(values['in_tmpl_insertelementnumber'])
    self.debug.info_message("index = " + str(index) + " \n")

    start_index = 0
    end_index = 12
    if(at_before_after == 'At' or at_before_after == 'Before'):
      start_index = index
    elif(at_before_after == 'After'):
      start_index = index +1

    self.debug.info_message("start index = " + str(start_index) + " \n")
    self.debug.info_message("end index = " + str(end_index) + " \n")

    for x in range (start_index, end_index):
      field_name_from = 'combo_element' + str(x+1)
      field_name_to = 'combo_element' + str(x)
      contents = values[field_name_from]
      self.form_gui.window[field_name_to].update(contents)

    self.form_gui.window[field_name_from].update('-')

  def event_tmpltnewcategory(self, values):
    self.debug.info_message("NEW CATEGORY\n")

    category    = values['in_tmpl_category_name']
    formname    = values['in_tmpl_name']
    description = values['in_tmpl_desc']
    version     = values['in_tmpl_ver']
    filename    = values['in_tmpl_file']

    data = [version,description,'T1,I1']
    self.form_dictionary.createNewTemplateInDictionary(filename, category, formname, version, description, data)
    self.group_arq.addCategory(category)
    self.group_arq.addTemplate(formname, description, version, filename)

    table_data = self.updateSimulatedPreview(data)
    self.debug.info_message("table data : " + str(table_data) )
    self.form_gui.window['table_templates_preview'].update(values=table_data)
    self.current_edit_string = data

    self.debug.info_message("EVENT TMPLT NEW TEMPLATE 5\n")

    self.form_gui.window['tbl_tmplt_categories'].update(self.group_arq.getCategories())
    self.form_gui.window['tbl_tmplt_templates'].update(self.group_arq.getTemplates())
    return

  def event_tmpltdeleterow(self, values):
    self.debug.info_message("TEMPLATE DELETE ROW\n")

    insert_where = values['combo_tmplt_insertwhere']

    self.debug.info_message("combo value = " + str(insert_where) )

    #FIXME NEEDS TO REMOVE THE DATA FROM THE DICTIONARY ITEM
    if(insert_where == 'At'):
      linestr = values['table_templates_preview']
      self.debug.info_message("line str is: " + str(linestr) )
      if(linestr != '[]'):		
        line_index_form = int(values['table_templates_preview'][0])+1
        line_index = self.tablerow_templaterow_xref[line_index_form]-1

        self.debug.info_message("line index is" + str(line_index) )

        del self.current_edit_string[line_index+2]
        self.debug.info_message("edit string: " + str(self.current_edit_string) )
        formname = values['in_tmpl_name']
        filename = values['in_tmpl_file']
        category = self.current_edit_category
        js = self.form_dictionary.setDataInDictionary(formname, category, filename, self.current_edit_string)
        table_data = self.updateSimulatedPreview(self.current_edit_string)
        self.form_gui.window['table_templates_preview'].update(values=table_data)
        self.form_gui.window['in_tmpl_line_number'].update(str(line_index+2))

        self.form_gui.window['table_templates_preview'].update(select_rows=[line_index_form-1])

      self.debug.info_message("inser after\n")
    elif(insert_where == 'Before'):
      linestr = values['table_templates_preview']
      self.debug.info_message("line str is: " + str(linestr) )
      if(linestr != '[]'):		
        line_index_form = int(values['table_templates_preview'][0])+1
        line_index = self.tablerow_templaterow_xref[line_index_form]-2

        self.debug.info_message("line index is" + str(line_index) )

        del self.current_edit_string[line_index+2]

        self.debug.info_message("edit string: " + str(self.current_edit_string) )
        formname = values['in_tmpl_name']
        filename = values['in_tmpl_file']
        category = self.current_edit_category
        js = self.form_dictionary.setDataInDictionary(formname, category, filename, self.current_edit_string)
        table_data = self.updateSimulatedPreview(self.current_edit_string)
        self.form_gui.window['table_templates_preview'].update(values=table_data)

        #FIXME NEED TO GO BACK THRU THE XREF TABLE THEN BACK AGAIN
        self.form_gui.window['table_templates_preview'].update(select_rows=[line_index_form-2])

      self.debug.info_message("insert before\n")
    elif(insert_where == 'After'):
      linestr = values['table_templates_preview']
      self.debug.info_message("line str is: " + str(linestr) )
      if(linestr != '[]'):		
        line_index_form = int(values['table_templates_preview'][0])+1
        line_index = self.tablerow_templaterow_xref[line_index_form]-1

        self.debug.info_message("line index is" + str(line_index) )
        del self.current_edit_string[line_index+3]

        self.debug.info_message("edit string: " + str(self.current_edit_string) )
        formname = values['in_tmpl_name']
        filename = values['in_tmpl_file']
        category = self.current_edit_category
        js = self.form_dictionary.setDataInDictionary(formname, category, filename, self.current_edit_string)
        table_data = self.updateSimulatedPreview(self.current_edit_string)
        self.form_gui.window['table_templates_preview'].update(values=table_data)
        self.form_gui.window['in_tmpl_line_number'].update(str(line_index+2))

        self.form_gui.window['table_templates_preview'].update(select_rows=[line_index])

      self.debug.info_message("inser after\n")
    elif(insert_where == 'End'):
      self.debug.info_message("Insert at End\n")
      del self.current_edit_string[len(self.current_edit_string)-1]
      self.debug.info_message("edit string: " + str(self.current_edit_string) )
      formname = values['in_tmpl_name']
      filename = values['in_tmpl_file']
      category = self.current_edit_category
      js = self.form_dictionary.setDataInDictionary(formname, category, filename, self.current_edit_string)
      table_data = self.updateSimulatedPreview(self.current_edit_string)
      self.form_gui.window['table_templates_preview'].update(values=table_data)

      self.form_gui.window['table_templates_preview'].update(select_rows=[len(self.current_edit_string)-2])

    return

  def event_tmpltduplicaterow(self, values):
    self.debug.info_message("TEMPLATE DUPLICATE ROW\n")

    line_index_form = int(values['in_tmpl_line_number'])-1

    self.debug.info_message("line index form: " + str(line_index_form) )
    line_index_form = int(values['table_templates_preview'][0])+1
    line_index = self.tablerow_templaterow_xref[line_index_form]-1
    self.debug.info_message("line index: " + str(line_index) )

    new_string = ''
    
    try:
      for x in range(12):
        field_name = 'combo_element' + str(x+1)
        if(values[field_name] != '-'):
          if(x > 0):		  
            new_string = new_string + ',' + self.form_gui.reverse_field_names[values[field_name] ]
          else:
            new_string = new_string + self.form_gui.reverse_field_names[values[field_name] ]
    except:
      self.debug.error_message("Exception in event_tmpltduplicaterow: " + str(sys.exc_info()[0]) + str(sys.exc_info()[1] ))

    self.debug.info_message("new string: " + new_string )
					  
    formname = values['in_tmpl_name']
    filename = values['in_tmpl_file']
    self.current_edit_string.insert(line_index+2, new_string)
    category = self.current_edit_category
    js = self.form_dictionary.setDataInDictionary(formname, category, filename, self.current_edit_string)
    self.debug.info_message("js: " + str(js) )
        
    table_data = self.updateSimulatedPreview(self.current_edit_string)
    self.form_gui.window['table_templates_preview'].update(values=table_data)

    self.form_gui.window['table_templates_preview'].update(select_rows=[line_index+1])

    return

  def event_outboxtxrig(self, values):
    self.debug.info_message("OUTBOX SELECT TXRIG\n")

    txrig = values['option_outbox_txrig']

    self.debug.info_message("TXRIG: " + str(txrig) )

    saam = self.getSaamfram()
    saam.setTxRig(txrig)

    return



  def event_compose_qrysaam(self, values):
    self.debug.info_message("COMPOSE QUERY SAAM\n")

    saam = self.getSaamfram()
    from_call = self.saamfram.getMyCall()
    group_name = self.saamfram.getMyGroup()
    saam.sendQuerySAAM(from_call, group_name)
    saam.send('SAAM?')

    return

  def event_compose_saam(self, values):
    self.debug.info_message("COMPOSE SAAM\n")

    saam = self.getSaamfram()
    from_call = self.saamfram.getMyCall()
    group_name = self.saamfram.getMyGroup()
    saam.sendSAAM(from_call, group_name)
    self.changeFlashButtonState('btn_compose_saam', False)

    saam.send('SAAM?')

    return


  def event_tmpltcopytoclip(self, values):
    self.debug.info_message("TEMPLATE COPY TO CLIPBOARD\n")
    return

  def event_tmpltpastefromclip(self, values):
    self.debug.info_message("TEMPLATE PASTE FROM CLIPBOARD\n")

    clipboard_string = clip.paste()
    
    clipboard_string = clipboard_string.replace('JSDIGI_FORMS_CLIPBOARD_DATA={\'', '')
    clipboard_string = clipboard_string.replace('\'}', '')

    self.debug.info_message(" clipboard string: " + clipboard_string )
    
    sublist = clipboard_string.split('\',\'')
    for sublist_items in range(len(sublist)):
      self.debug.info_message(" substring : " + str(sublist[sublist_items]) )

    insert_where = values['combo_tmplt_insertwhere']

    self.debug.info_message("combo value = " + str(insert_where) + "---\n")

    linestr = values['table_templates_preview']
    self.debug.info_message("line str is:---" + str(linestr) + "---\n")

    if(insert_where == 'Before' or insert_where == 'After'):
      self.debug.info_message("processing before and after\n")
      line_index_form = int(values['table_templates_preview'][0])+1
      line_index = self.tablerow_templaterow_xref[line_index_form]-1

      self.debug.info_message("line index is" + str(line_index) )

      if(insert_where == 'Before'):
        for sublist_items in reversed(range(len(sublist))):
          self.debug.info_message(" substring : " + str(sublist[sublist_items]) )
          new_string = str(sublist[sublist_items])
          self.current_edit_string.insert(line_index+2, new_string)
        self.debug.info_message("edit string: " + str(self.current_edit_string) )
        formname = values['in_tmpl_name']
        filename = values['in_tmpl_file']
        category = self.current_edit_category
        js = self.form_dictionary.setDataInDictionary(formname, category, filename, self.current_edit_string)
        table_data = self.updateSimulatedPreview(self.current_edit_string)
        self.form_gui.window['table_templates_preview'].update(values=table_data)

        self.form_gui.window['table_templates_preview'].update(select_rows=[len(sublist) + line_index_form-1])

        self.debug.info_message("insert before\n")
      elif(insert_where == 'After'):
        for sublist_items in reversed(range(len(sublist))):
          self.debug.info_message(" substring : " + str(sublist[sublist_items]) )
          new_string = str(sublist[sublist_items])
          self.current_edit_string.insert(line_index+3, new_string)
        self.debug.info_message("edit string: " + str(self.current_edit_string) )
        formname = values['in_tmpl_name']
        filename = values['in_tmpl_file']
        category = self.current_edit_category
        js = self.form_dictionary.setDataInDictionary(formname, category, filename, self.current_edit_string)
        table_data = self.updateSimulatedPreview(self.current_edit_string)
        self.form_gui.window['table_templates_preview'].update(values=table_data)
        self.form_gui.window['in_tmpl_line_number'].update(str(line_index+2))

        self.form_gui.window['table_templates_preview'].update(select_rows=[len(sublist) + line_index_form])

        self.debug.info_message("inser after\n")

    if(insert_where == 'End'):
      self.debug.info_message("Insert at End\n")
      for sublist_items in reversed(range(len(sublist))):
        self.debug.info_message(" substring : " + str(sublist[sublist_items]) )
        new_string = str(sublist[sublist_items])
        self.current_edit_string.append(new_string)
      self.debug.info_message("edit string: " + str(self.current_edit_string) )
      formname = values['in_tmpl_name']
      filename = values['in_tmpl_file']
      category = self.current_edit_category
      js = self.form_dictionary.setDataInDictionary(formname, category, filename, self.current_edit_string)
      table_data = self.updateSimulatedPreview(self.current_edit_string)
      self.form_gui.window['table_templates_preview'].update(values=table_data)

    return


  def event_colorsupdate(self, values):
    self.debug.info_message("COLORS UPDATE\n")
    txbtn_color        = values['option_colors_tx_btns']
    msgmgmt_color      = values['option_colors_msgmgmt_btns']
    clipboard_color    = values['option_colors_clipboard_btns']
    compose_tab_color  = values['option_colors_compose_tab']
    inbox_tab_color    = values['option_colors_inbox_tab']
    outbox_tab_color   = values['option_colors_outbox_tab']
    relaybox_tab_color = values['option_colors_relay_tab']
    sentbox_tab_color  = values['option_colors_sentbox_tab']
    info_tab_color     = values['option_colors_info_tab']
    colors_tab_color   = values['option_colors_colors_tab']
    settings_tab_color = values['option_colors_settings_tab']

    try:
      wording_color = 'black'
      self.form_gui.window['btn_compose_saam'].update(button_color=(wording_color, txbtn_color))
      self.form_gui.window['btn_compose_qrysaam'].update(button_color=(wording_color, txbtn_color))
      self.form_gui.window['btn_inbox_replytomsg'].update(button_color=(wording_color, txbtn_color))
      self.form_gui.window['btn_inbox_sendacknack'].update(button_color=(wording_color, txbtn_color))
      self.form_gui.window['btn_outbox_sendselected'].update(button_color=(wording_color, txbtn_color))

      self.debug.info_message("DONE COLORS UPDATE\n")
    except:
      self.debug.error_message("Exception in event_colorsupdate: " + str(sys.exc_info()[0]) + str(sys.exc_info()[1] ))


  def event_btncomposeabortsend(self, values):
    self.debug.info_message("ABORT BUTTON PRESSED\n")

    self.group_arq.saamfram.sendAbort('','')

    return

  def event_composeselectedstations(self, values):
    self.debug.info_message("SELECT CALLSIGN\n")

    line_index = int(values['tbl_compose_selectedstations'][0])
    selected_callsigns = self.group_arq.toggleSelectedStations(line_index)
    self.form_gui.window['in_compose_selected_callsigns'].update(selected_callsigns)
    self.debug.info_message("selected callsigns: " + selected_callsigns )


    table = self.group_arq.getSelectedStations()
    self.form_gui.window['tbl_compose_selectedstations'].update(values=table )

    self.form_gui.window['tbl_compose_selectedstations'].update(row_colors=self.group_arq.getSelectedStationsColors())

  def event_composestationcapabilities(self, values):
    self.debug.info_message("event_composestationcapabilities\n")

    callsign, channel_name = self.group_arq.saamfram.updateChannelView(values)

    self.form_gui.window['in_inbox_listentostation'].update(callsign )

    if('TX_' in channel_name):
      txchannel = channel_name
      self.form_gui.window['in_mainwindow_activetxchannel'].update(txchannel )
    else:
      rxchannel = channel_name
      self.form_gui.window['in_mainwindow_activerxchannel'].update(rxchannel )


  def event_btnrelaysendreqm(self, values):
    self.debug.info_message("event_btnrelaysendreqm\n")

    line_index = int(values['table_relay_messages'][0])
    selected_msgid = (self.group_arq.getMessageRelaybox()[line_index])[6]

    self.debug.info_message("selected msgid: " + str(selected_msgid) )

    from_call = self.saamfram.getMyCall()
    sender_call = self.saamfram.getSenderCall()
    self.saamfram.sendREQM(from_call, sender_call, selected_msgid)

  def event_btninboxsendreqm(self, values):
    self.debug.info_message("event_btninboxsendreqm\n")

    line_index = int(values['table_inbox_messages'][0])
    selected_msgid = (self.group_arq.getMessageInbox()[line_index])[7]

    self.debug.info_message("selected msgid: " + str(selected_msgid) )

    from_call = self.saamfram.getMyCall()
    sender_call = self.saamfram.getSenderCall()
    self.saamfram.sendREQM(from_call, sender_call, selected_msgid)


  def event_btncomposegoingqrtsaam(self, values):
    self.debug.info_message("event_btncomposegoingqrtsaam\n")
    self.saamfram.sendSaamQrt()

  def event_btncomposeconfirmedhavecopy(self, values):
    self.debug.info_message("event_btncomposeconfirmedhavecopy\n")
    self.saamfram.sendConf()

  def event_btncomposeareyoureadytoreceive(self, values):
    self.debug.info_message("event_btncomposeareyoureadytoreceive\n")
    self.saamfram.sendQryReady()

  def event_btncomposereadytoreceive(self, values):
    self.debug.info_message("event_btncomposereadytoreceive\n")
    self.saamfram.sendReadyToReceive()

  def event_btncomposenotreadytoreceive(self, values):
    self.debug.info_message("event_btncomposenotreadytoreceive\n")
    self.saamfram.sendNotReady()

  def event_btncomposecancelalreadyhavecopy(self, values):
    self.debug.info_message("event_btncomposecancelalreadyhavecopy\n")
    self.saamfram.sendCancelHaveCopy()



  def event_combosettingschannels(self, values):
    self.debug.info_message("event_combosettingschannels\n")
    channel = values['combo_settings_channels'].split(' - ')[1]
    self.debug.info_message("selected channel : " + channel )
    self.debug.info_message("selected channel : " + channel.split('Hz')[0] )

    if(self.saamfram.tx_mode == 'JS8CALL'):
      dial = 7095000
      offset = int(channel.split('Hz')[0])
      self.group_arq.setDialAndOffset(dial, offset)
      self.group_arq.setSpeed(cn.JS8CALL_SPEED_NORMAL)

    else:
      self.group_arq.fldigiclient.setChannel(channel.split('Hz')[0])


  def event_combomainsignalwidth(self, values):
    self.debug.info_message("event_combomainsignalwidth\n")

    selected_width = values['combo_main_signalwidth']
    if(selected_width == 'HF - 500'):
      new_selection_list = 'MODE 5 - QPSK500,MODE 8 - BPSK500,MODE 13 - 8PSK125,MODE 14 - 8PSK250F,MODE 15 - 8PSK250FL,MODE 16 - PSK500R,\
MODE 18 - QPSK250,MODE 19 - BPSK250,MODE 22 - 8PSK125FL,MODE 23 - 8PSK125F,MODE 24 - PSK250R,MODE 25 - PSK63RC4,MODE 26 - DOMX22,\
MODE 28 - DOMX16'.split(',')
      self.form_gui.window['option_outbox_fldigimode'].update(values=new_selection_list )
      self.form_gui.window['option_outbox_fldigimode'].update(new_selection_list[0] )
      self.group_arq.saamfram.fldigiclient.setMode('QPSK500')
    elif(selected_width == 'VHF/UHF - 1000'):
      new_selection_list = 'MODE 5 - QPSK500,MODE 8 - BPSK500,MODE 9 - PSK1000R,MODE 12 - PSK250RC3,MODE 13 - 8PSK125,MODE 14 - 8PSK250F,\
MODE 15 - 8PSK250FL,MODE 16 - PSK500R,MODE 17 - PSK250RC2,MODE 18 - QPSK250,MODE 19 - BPSK250,MODE 20 - PSK125RC4,MODE 22 - 8PSK125FL,\
MODE 23 - 8PSK125F,MODE 24 - PSK250R,MODE 25 - PSK63RC4,MODE 26 - DOMX22,MODE 27 - OLIVIA-4/1K,MODE 28 - DOMX16'.split(',')
      self.form_gui.window['option_outbox_fldigimode'].update(values=new_selection_list )
      self.form_gui.window['option_outbox_fldigimode'].update(new_selection_list[0] )
      self.group_arq.saamfram.fldigiclient.setMode('QPSK500')
    elif(selected_width == 'VHF/UHF - 2000'):
      new_selection_list = 'MODE 3 - PSK800RC2,MODE 4 - PSK250RC6,MODE 5 - QPSK500,MODE 6 - PSK500RC3,MODE 7 - PSK250RC5,MODE 8 - BPSK500,\
MODE 9 - PSK1000R,MODE 10 - PSK500RC2,MODE 11 - DOMX88,MODE 12 - PSK250RC3,MODE 13 - 8PSK125,MODE 14 - 8PSK250F,MODE 15 - 8PSK250FL,\
MODE 16 - PSK500R,MODE 17 - PSK250RC2,MODE 18 - QPSK250,MODE 19 - BPSK250,MODE 20 - PSK125RC4,MODE 21 - DOMX44,MODE 22 - 8PSK125FL,\
MODE 23 - 8PSK125F,MODE 24 - PSK250R,MODE 25 - PSK63RC4,MODE 26 - DOMX22,MODE 27 - OLIVIA-4/1K,MODE 28 - DOMX16'.split(',')
      self.form_gui.window['option_outbox_fldigimode'].update(values=new_selection_list )
      self.form_gui.window['option_outbox_fldigimode'].update(new_selection_list[0] )
      self.group_arq.saamfram.fldigiclient.setMode('PSK800RC2')
    elif(selected_width == 'VHF/UHF - 3000'):
      new_selection_list = 'MODE 1 - PSK1000RC2,MODE 2 - PSK500RC4,MODE 3 - PSK800RC2,MODE 4 - PSK250RC6,MODE 5 - QPSK500,MODE 6 - PSK500RC3,\
MODE 7 - PSK250RC5,MODE 8 - BPSK500,MODE 9 - PSK1000R,MODE 10 - PSK500RC2,MODE 11 - DOMX88,MODE 12 - PSK250RC3,MODE 13 - 8PSK125,MODE 14 - 8PSK250F,\
MODE 15 - 8PSK250FL,MODE 16 - PSK500R,MODE 17 - PSK250RC2,MODE 18 - QPSK250,MODE 19 - BPSK250,MODE 20 - PSK125RC4,MODE 21 - DOMX44,MODE 22 - 8PSK125FL,\
MODE 23 - 8PSK125F,MODE 24 - PSK250R,MODE 25 - PSK63RC4,MODE 26 - DOMX22,MODE 27 - OLIVIA-4/1K,MODE 28 - DOMX16'.split(',')
      self.form_gui.window['option_outbox_fldigimode'].update(values=new_selection_list )
      self.form_gui.window['option_outbox_fldigimode'].update(new_selection_list[0] )
      self.group_arq.saamfram.fldigiclient.setMode('PSK1000RC2')
      #self.group_arq.saamfram.fldigiclient.setChannel('500')


  def event_btnoutboxviewform(self, values):
    self.debug.info_message("event_btnoutboxviewform")

    line_index = int(values['table_outbox_messages'][0])
    ID = (self.group_arq.getMessageOutbox()[line_index])[6]
    formname = (self.group_arq.getMessageOutbox()[line_index])[5]
    category, filename = self.form_dictionary.getCategoryAndFilenameFromFormname(formname)

    form_content = ['', '', '', '']

    self.debug.info_message("SELECTED CATEGORY IS: "  + category )
    self.debug.info_message("SELECTED FORMNAME IS: "  + formname )
    
    msgto = ''
    self.group_arq.saamfram.getDecodeTimestampFromUniqueId(ID)

    self.debug.info_message("reverse encoded callsign is: " + self.group_arq.saamfram.getDecodeCallsignFromUniqueId(ID) )
    self.debug.info_message("UNIQUE ID USING UUID IS: " + str(ID) )

    subject = ''
    window = self.form_gui.createInboxViewReplyWindow(formname, form_content, category, msgto, filename, ID, subject, False, False, False)
    dispatcher = PopupControlsProc(self, window)
    self.form_gui.runPopup(self, dispatcher, window)



  def event_optionoutboxjs8callmode(self, values):
    self.debug.info_message("event_optionoutboxjs8callmode\n")

    speed = values['option_outbox_js8callmode']
    self.debug.info_message("selected speed : " + speed )

    if(self.saamfram.tx_mode == 'JS8CALL'):
      if(speed == 'SLOW'):
        self.group_arq.setSpeed(cn.JS8CALL_SPEED_SLOW)
      if(speed == 'NORMAL'):
        self.group_arq.setSpeed(cn.JS8CALL_SPEED_NORMAL)
      if(speed == 'FAST'):
        self.group_arq.setSpeed(cn.JS8CALL_SPEED_FAST)
      if(speed == 'TURBO'):
        self.group_arq.setSpeed(cn.JS8CALL_SPEED_TURBO)

  def event_comboelement1(self, values):
    self.debug.info_message("COMBO ELEMENT 1\n")
    self.form_gui.window['in_tmpl_insertelementnumber'].update('1')

  def event_comboelement2(self, values):
    self.debug.info_message("COMBO ELEMENT 2\n")
    self.form_gui.window['in_tmpl_insertelementnumber'].update('2')
    
  def event_comboelement3(self, values):
    self.debug.info_message("COMBO ELEMENT 3\n")
    self.form_gui.window['in_tmpl_insertelementnumber'].update('3')

  def event_comboelement4(self, values):
    self.debug.info_message("COMBO ELEMENT 4\n")
    self.form_gui.window['in_tmpl_insertelementnumber'].update('4')

  def event_comboelement5(self, values):
    self.debug.info_message("COMBO ELEMENT 5\n")
    self.form_gui.window['in_tmpl_insertelementnumber'].update('5')

  def event_comboelement6(self, values):
    self.debug.info_message("COMBO ELEMENT 6\n")
    self.form_gui.window['in_tmpl_insertelementnumber'].update('6')

  def event_comboelement7(self, values):
    self.debug.info_message("COMBO ELEMENT 7\n")
    self.form_gui.window['in_tmpl_insertelementnumber'].update('7')

  def event_comboelement8(self, values):
    self.debug.info_message("COMBO ELEMENT 8\n")
    self.form_gui.window['in_tmpl_insertelementnumber'].update('8')

  def event_comboelement9(self, values):
    self.debug.info_message("COMBO ELEMENT 9\n")
    self.form_gui.window['in_tmpl_insertelementnumber'].update('9')

  def event_comboelement10(self, values):
    self.debug.info_message("COMBO ELEMENT 10\n")
    self.form_gui.window['in_tmpl_insertelementnumber'].update('10')

  def event_comboelement11(self, values):
    self.debug.info_message("COMBO ELEMENT 11\n")
    self.form_gui.window['in_tmpl_insertelementnumber'].update('11')

  def event_comboelement12(self, values):
    self.debug.info_message("COMBO ELEMENT 12\n")
    self.form_gui.window['in_tmpl_insertelementnumber'].update('12')


  def event_exit_receive(self, values):

    try:
      self.debug.info_message("WRITING DICTIONARIES TO FILE\n")
      """ write the main dictionary of values to file """
      self.form_dictionary.writeMainDictionaryToFile("saamcom_save_data.txt", values)
      """ write the inbox dictionary to file """
      self.form_dictionary.writeInboxDictToFile('inbox.msg')

      self.form_dictionary.writeOutboxDictToFile('outbox.msg')
      self.form_dictionary.writeSentDictToFile('sentbox.msg')
      self.form_dictionary.writeRelayboxDictToFile('relaybox.msg')


      if(self.group_arq.js8client != None):
        self.group_arq.js8client.stopThreads()
      if(self.group_arq.fldigiclient != None):
        self.group_arq.fldigiclient.stopThreads()

    except:
      self.debug.error_message("Exception in event_exit_receive: " + str(sys.exc_info()[0]) + str(sys.exc_info()[1] ))
      
    return()


  dispatch = {
      'btn_tmplt_preview_form'    : event_btntmpltpreviewform,
      'tbl_tmplt_templates'       : event_tmplt_template,
      'btn_tmplt_new_template'    : event_tmplt_newtemplate,
      'btn_tmplt_update_template' : event_tmplt_updatetemplate,
      'btn_tmplt_delete_template' : event_tmplt_deletetemplate,
      'btn_tmplt_save_template'   : event_tmplt_savetemplate,
      'btn_tmplt_load_sel'        : event_tmplt_loadsel,
      'btn_settings_add'          : event_settings_add,
      'btn_settings_tmplt_remove'          : event_settings_tmplt_remove,
      'tbl_tmplt_categories'      : event_tmplt_categories,
      'table_templates_preview'   : event_tablepreview,
      'btn_tmplt_update'          : event_tmpltupdate,
      'btn_tmplt_add_row'         : event_tmplt_addrow,
      'in_tmpl_category_name'     : event_tmplt_typingsomething,
      'in_tmpl_name'              : event_tmplt_typingsomething,
      'in_tmpl_desc'              : event_tmplt_typingsomething,
      'in_tmpl_ver'               : event_tmplt_typingsomething,
      'in_tmpl_file'              : event_tmplt_typingsomething,
      'btn_cmpse_compose'         : event_composemsg,
      'btn_prev_post_to_outbox'   : event_prevposttooutbox,
      'table_outbox_messages'     : event_tableoutboxmessages,
      'table_inbox_messages'      : event_tableinboxmessages,
      'btn_outbox_editform'       : event_outboxeditform,
      'btn_settings_list'         : event_settingslist,
      'tbl_compose_categories'    : event_compose_categories,
      'btn_outbox_sendselected'   : event_outboxsendselected,
      'btn_outbox_deletemsg'      : event_outboxdeletemsg,
      'btn_outbox_deleteallmsg'   : event_outboxdeleteallmsg,
      'btn_sentbox_deletemsg'      : event_sentboxdeletemsg,
      'btn_sentbox_deleteallmsg'   : event_sentboxdeleteallmsg,
      'btn_outbox_sendall'        : event_outboxsendall,
      'btn_inbox_deleteselected'  : event_inboxdeleteselected,
      'btn_inbox_deleteall'       : event_inboxdeleteall,
      'btn_relaybox_deleteselected'  : event_relayboxdeleteselected,
      'btn_relaybox_deleteall'       : event_relayboxdeleteall,
      'table_sent_messages'       : event_tablesentmessages,
      'btn_outbox_reqconfirm'     : event_outboxreqconfirm,
      'btn_inbox_rcvstatus'       : event_inboxrcvstatus,
      'cb_templates_editline'         : event_templateseditline,
      'cb_templates_insertdeleteline' : event_templatesinsertdeleteline,
      'btn_tmplt_delete_template_category' : event_tmpltdeletetemplatecategory,
      'tbl_compose_select_form'   : event_composeselectform,
      'option_outbox_fldigimode'  : event_outboxfldigimode,
      'btn_inbox_sendacknack'     : event_inboxsendacknack,
      'btn_outbox_pleaseconfirm'  : event_outboxpleaseconfirm,
      'btn_inbox_copyclipboard'   : event_inboxcopyclipboard,
      'btn_outbox_importfromclipboard' :  event_outboximportfromclipboard,
      'btn_inbox_replytomsg'      : event_inboxreplytomsg,
      'btn_inbox_viewmsg'         : event_inboxviewmsg,
      'btn_tmplt_insertelement'   : event_fordesignerInsertElement,
      'btn_tmplt_deleteelement'   : event_fordesignerDeleteElement,
      'btn_tmplt_delete_row'      : event_tmpltdeleterow,
      'btn_tmplt_new_category'    : event_tmpltnewcategory,
      'btn_tmplt_duplicate_row'   : event_tmpltduplicaterow,
      'btn_tmplt_copytoclip'      : event_tmpltcopytoclip,
      'btn_tmplt_pastefromclip'   : event_tmpltpastefromclip,
      'option_outbox_txrig'       : event_outboxtxrig,
      'btn_compose_qrysaam'       : event_compose_qrysaam,
      'btn_compose_saam'          : event_compose_saam,
      'btn_colors_update'         : event_colorsupdate,
      'tbl_compose_selectedstations' : event_composeselectedstations,
      'tbl_compose_stationcapabilities' : event_composestationcapabilities,
      'btn_compose_abortsend'     : event_btncomposeabortsend,
      'btn_relay_sendreqm'        : event_btnrelaysendreqm,
      'btn_inbox_sendreqm'        : event_btninboxsendreqm,
      'combo_settings_channels'   : event_combosettingschannels,
      'option_outbox_js8callmode' : event_optionoutboxjs8callmode,
      'combo_main_signalwidth'    : event_combomainsignalwidth,

      'btn_compose_goingqrtsaam'          : event_btncomposegoingqrtsaam,
      'btn_compose_confirmedhavecopy'     : event_btncomposeconfirmedhavecopy,
      'btn_compose_areyoureadytoreceive'  : event_btncomposeareyoureadytoreceive,
      'btn_compose_readytoreceive'        : event_btncomposereadytoreceive,
      'btn_compose_notreadytoreceive'     : event_btncomposenotreadytoreceive,
      'btn_compose_cancelalreadyhavecopy' : event_btncomposecancelalreadyhavecopy,
      'btn_outbox_viewform'       : event_btnoutboxviewform,
      
      'combo_element1'            : event_comboelement1,
      'combo_element2'            : event_comboelement2,
      'combo_element3'            : event_comboelement3,
      'combo_element4'            : event_comboelement4,
      'combo_element5'            : event_comboelement5,
      'combo_element6'            : event_comboelement6,
      'combo_element7'            : event_comboelement7,
      'combo_element8'            : event_comboelement8,
      'combo_element9'            : event_comboelement9,
      'combo_element10'           : event_comboelement10,
      'combo_element11'           : event_comboelement11,
      'combo_element12'           : event_comboelement12,
  }


class PopupControlsProc(object):
  
  
  def __init__(self, view, window):  
    return
    
  def event_catchall(self, values):
    return()

  def event_exit_receive(self, values):
    return


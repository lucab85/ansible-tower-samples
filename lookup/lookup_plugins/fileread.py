# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
  name: file
  author: Luca Berton <luca@ansiblepilot.com>
  version_added: "0.1"
  short_description: read file contents
  description:
      - This lookup returns the contents from a file on the Ansible controller's file system.
  options:
    _terms:
      description: path(s) of files to read
      required: True
    option1:
      description:
            - Sample option that could modify plugin behaviour.
            - This one can be set directly ``option1='x'`` or in ansible.cfg, but can also use vars or environment.
      type: string
      ini:
        - section: file_lookup
          key: option1
  notes:
    - if read in variable context, the file can be interpreted as YAML if the content is valid to the parser.
    - this lookup does not understand globbing --- use the fileglob lookup instead.
"""
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

display = Display()

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
      self.set_options(var_options=variables, direct=kwargs)
      ret = []
      for term in terms:
          display.debug("File lookup term: %s" % term)
          lookupfile = self.find_file_in_search_path(variables, 'files', term)
          display.vvvv(u"File lookup using %s as file" % lookupfile)
          try:
              if lookupfile:
                  contents, show_data = self._loader._get_file_contents(lookupfile)
                  ret.append(contents.rstrip())
              else:
                  raise AnsibleParserError()
          except AnsibleParserError:
              raise AnsibleError("could not locate file in lookup: %s" % term)
          if self.get_option('option1') == 'do something':
            pass
      return ret

"""Configuration file for Sphinx."""
import sys
import os
from subprocess import check_output

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))

# Fake import to avoid actually loading CFFI and the PortAudio library
import fake__sounddevice
sys.modules['_sounddevice'] = sys.modules['fake__sounddevice']

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',  # support for NumPy-style docstrings
]

autoclass_content = 'init'
autodoc_member_order = 'bysource'

napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = False
napoleon_use_rtype = False

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'numpy': ('https://docs.scipy.org/doc/numpy/', None),
}

master_doc = 'index'

authors = 'Matthias Geier'
project = 'python-sounddevice'
copyright = '2020, ' + authors

try:
    release = check_output(['git', 'describe', '--tags', '--always'])
    release = release.decode().strip()
except Exception:
    release = '<unknown>'

try:
    today = check_output(['git', 'show', '-s', '--format=%ad', '--date=short'])
    today = today.decode().strip()
except Exception:
    today = '<unknown date>'

default_role = 'any'

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'collapse_navigation': False,
}
html_title = project + ', version ' + release
html_domain_indices = False
html_show_sourcelink = True
html_show_copyright = False
htmlhelp_basename = 'python-sounddevice'

latex_elements = {
'papersize': 'a4paper',
#'preamble': '',
'printindex': '',
}
latex_documents = [('index', 'python-sounddevice.tex', project, authors, 'howto')]
latex_show_urls = 'footnote'
latex_domain_indices = False

# -*- coding: utf-8 -*-
#
# ASL documentation build configuration file

# -- General configuration ------------------------------------------------

extensions = ["sphinx_rtd_theme",]
templates_path = ['_templates']

# General information about the project.
project = u'BASIL documentation'
copyright = u'2017, University of Oxford'
author = u'Michael Chappel, Martin Craig'
master_doc = 'index'
version = u''
release = u''
source_suffix = ['.rst',]
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output ----------------------------------------------

try:
    import sphinx_rtd_theme
    html_theme = "sphinx_rtd_theme"
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
except ImportError:
    html_theme = 'alabaster'

# -- Options for LaTeX output ---------------------------------------------

latex_documents = [
    (master_doc, 'basil.tex', project, author, 'manual'),
]

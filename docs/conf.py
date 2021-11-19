# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../rticonnextdds_connector'))


# -- Project information -----------------------------------------------------

project = 'RTI Connector for Python'
copyright = '2021, Real-Time Innovations, Inc'
author = 'Real-Time Innovations, Inc.'

# The full version, including alpha/beta/rc tags
version = '1.1.0'
release = '1.1.0'

master_doc = 'index'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.doctest"
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['static']

def setup(app):
    app.add_stylesheet('theme_overrides.css')


# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    "collapse_navigation" : False
    "canonical_url" : "https://community.rti.com/static/documentation/connector/current/api/python/"
}

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#
html_logo = "static/rti-logo-FINALv2-White-OrangeDot.png"

# The name of an image file (relative to this directory) to use as a favicon of
# the docs.  This file should be a Windows icon file (.ico) being 16x16 or
# 32x32 pixels large.
#
html_favicon = "static/favicon.ico"

# -- Options for LaTeX output -------------------------------------------------------------------------------------------
latex_engine = 'lualatex'
latex_use_xindy = False

# latex config taken from connextdds repo
latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt')
    'pointsize': '11pt',
    'preamble': '''\
\\sphinxsetup{TitleColor={named}{black},InnerLinkColor={named}{black},OuterLinkColor={named}{blue}}
\\usepackage[utf8]{inputenc}
\\usepackage[titles]{tocloft}
\\usepackage{multirow}
\\usepackage{newunicodechar}
\\usepackage{hyperref}
\\usepackage{fontspec}
\\usepackage{graphicx}
\\setkeys{Gin}{width=.85\\textwidth}
\\hypersetup{bookmarksnumbered}
\\setcounter{tocdepth}{3}
\\usepackage{fancyhdr}
\\setlength{\headheight}{14pt}
\\usepackage[draft]{minted}\\fvset{breaklines=true, breakanywhere=true}''',
    'printindex': '\\footnotesize\\raggedright\\printindex',
    'inputenc': '',
    'utf8extra': '',
    'classoptions': ',openany,oneside',
    'releasename': 'Version',
    'fncychap': '',
    'maketitle': '''\
        \\pagenumbering{Roman} %%% to avoid page 1 conflict with actual page 1
        \\begin{titlepage}
            \\centering

            \\vspace{40mm} %%% * is used to give space from top

            \\textbf{\\Huge{''' + project + '''}}
            \\vspace{17mm}

            \\textbf{\\Large{Version ''' + version + '''}}

            \\vspace{100mm}
            \\vspace{0mm}
        \\end{titlepage}
        '''
}

latex_use_modindex = True

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        'rticonnectorforpython.tex',
        'RTI Connector for Python',
        '2021, Real-Time Innovations, Inc.',
        'manual'
    ),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#
html_logo = "static/rti-logo-FINALv2-White-OrangeDot.png"
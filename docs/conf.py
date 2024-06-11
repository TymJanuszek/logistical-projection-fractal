# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

numpy_site_packages = r'\doc_packages'
if numpy_site_packages not in sys.path:
    sys.path.append(numpy_site_packages)

eqhandler_site_packages = r'..\src'
if eqhandler_site_packages not in sys.path:
    sys.path.append(eqhandler_site_packages)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'logistic projection for fractals'
copyright = '2024, Tymoteusz Januszek & Jan Bialy'
author = 'Tymoteusz Januszek & Jan Bialy'
release = 'v.1.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.todo', 'sphinx.ext.viewcode', 'sphinx.ext.autodoc']
todo_include_todos = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'renku'
html_static_path = ['_static']

#-*-coding=utf8-*-
import platform
import os.path
import sys

if platform.system() == 'Windows':
    BASE_DIR            = os.path.split(sys.path[0])[0]
    TOOL_DIR 			= os.path.join(BASE_DIR, 'tools')
    EXTRA_DIR           = os.path.join(BASE_DIR, 'extra')
    PLUGINS_DIR           = os.path.join(BASE_DIR, 'plugins')

ICON_TOOLS = "icon.png"
README_TOOLS = "readme.html"

if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)


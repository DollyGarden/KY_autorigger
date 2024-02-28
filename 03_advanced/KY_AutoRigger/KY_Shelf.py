#  ********************************************************************
#  content = create shelf with an AutoRigger button in Maya
#  version = 0.1.2
#  date = 2022-02-15
#  dependencies = Maya
# 
#  license = MIT
#  author = Kelly Yang <kelly.yang1116@hotmail.com>
#  ********************************************************************


import os
import sys

import maya.cmds as cmds

SHELF_NAME = 'KY_AnimTool'
PATH = os.path.dirname(__file__)
sys.path.append(PATH)


def delete_custom_shelf():
	if cmds.shelfLayout(SHELF_NAME, exists=True):
		cmds.deleteUI(SHELF_NAME)


def custom_shelf():
	delete_custom_shelf()
	cmds.shelfLayout(SHELF_NAME, parent='ShelfLayout')
	cmds.shelfButton(parent=SHELF_NAME,
					 annotation='AutoRigger',
					 image1=PATH+'/shelf_AR.jpg',
					 command='import KY_CreateUI; import importlib; importlib.reload(KY_CreateUI); KY_CreateUI.build_ui()')
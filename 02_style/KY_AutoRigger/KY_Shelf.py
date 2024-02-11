import maya.cmds as cmds
import os
import sys

SHELF_NAME = 'KY_AnimTool'
PATH = os.path.dirname(__file__)
sys.path.append(PATH)

def custom_shelf():
	delete_custom_shelf()

	cmds.shelfLayout(SHELF_NAME, parent='ShelfLayout')
	cmds.shelfButton(parent=SHELF_NAME,
					 annotation='AutoRigger',
					 image1=PATH+'/shelf_AR.jpg',
					 command='import KY_CreateUI; import importlib; importlib.reload(KY_CreateUI); KY_CreateUI.build_ui()')

def delete_custom_shelf():
	if cmds.shelfLayout(SHELF_NAME, exists=True):
		cmds.deleteUI(SHELF_NAME)

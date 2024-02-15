#********************************************************************
# content = create ui functions
# version = 0.1.2
# date = 2022-02-15
# dependencies = Maya
#
# license = MIT
# author = Kelly Yang <kelly.yang1116@hotmail.com>
#********************************************************************


import os
import importlib
import webbrowser

import maya.cmds as cmds

import KY_Locators
import KY_Controller
import KY_Constraints
import KY_CreateIK

importlib.reload(KY_Locators)
importlib.reload(KY_Controller)
importlib.reload(KY_Constraints)
importlib.reload(KY_CreateIK)

global selected

PATH = os.path.dirname(__file__)

def open_readme():
    webbrowser.open(PATH+'/readme.txt')

def do_locators():
    spine_count = cmds.intSliderGrp('spines', query=True, value=True)
    finger_count = cmds.intSliderGrp('fingers', query=True, value=True)
    KY_Locators.create_locators(spine_count, finger_count)
    
def finalize_rig():
    spine_count = cmds.intSliderGrp('spines', query=True, value=True)
    finger_count = cmds.intSliderGrp('fingers', query=True, value=True)
    KY_Controller.create_controller(spine_count, finger_count)
    KY_CreateIK.ik_handles()
    KY_Constraints.create_constrains(finger_count, spine_count)

def build_ui():
    """Create main UI."""
    cmds.currentUnit(linear='meter')
    cmds.grid(size=12, spacing=5, divisions=5)

    ui_title = 'AutoRigger'

    if cmds.window(ui_title, exists=True):
        print('Closed duplicate window.')
        cmds.deleteUI(ui_title)


    cmds.window(ui_title, title="Auto Rigger", width=300)
    cmds.columnLayout(adjustableColumn=True)
    cmds.image(image=PATH + '/KY_AR_image.jpg')
    cmds.separator(style='in')

    cmds.text(label='SETTINGS', width=300, height=30)
    cmds.separator(style='in')
    cmds.rowLayout(numberOfColumns=2)
    cmds.text(label='Prefix', width=70)
    cmds.textField(width=130, text='test', editable=True)
    cmds.setParent('..')

    cmds.intSliderGrp('spines', label="Spine Count", min=1, max=10, value=4, step=1, field=True, 
                      width=300, columnWidth3=(70,50,180), columnAlign=(1,'left'))
    cmds.intSliderGrp('fingers', label="Finger Count", min=1, max=10, value=5, step=1, field=True,
                      width=300, columnWidth3=(70,50,180), columnAlign=(1,'left'))
    cmds.separator(style='in')
    
    cmds.text(label='LOCATORS', width=300, height=30)
    cmds.separator(style='in')
    cmds.button(label="Create Base Locators", width=300, command='KY_CreateUI.do_locators()')
    cmds.separator(style='none')
    cmds.button(label="Create Secondary Locators", width=300, 
                command='import KY_SecondaryLocators; importlib.reload(KY_SecondaryLocators); KY_SecondaryLocators.create_seclocator_windows()')
    cmds.separator(style='none')
    cmds.button(label="Delete ALL Locators", width=300, command='import KY_Locators; importlib.reload(KY_Locators); KY_Locators.delete_locators()')
    cmds.separator(style='none')
    cmds.button(label="Mirror L->R", width=300, command='import KY_Locators; importlib.reload(KY_Locators); KY_Locators.mirror_locators()')
    cmds.separator(style='in')

    cmds.text(label='JOINTS', width=300, height=30)
    cmds.separator(style='in')
    cmds.rowColumnLayout(numberOfColumns=2)
    cmds.button(label='Create Joints', w=150, c='import KY_Joints; importlib.reload(KY_Joints); KY_Joints.create_joints()')
    cmds.button(label='Delete Joints', w=150, c='import KY_Joints; importlib.reload(KY_Joints); KY_Joints.delete_joints()')
    cmds.setParent('..')
    cmds.separator( style='in')

    cmds.text(label='RIG', width=300, height=30)
    cmds.separator(style='in')
    cmds.button(label="Finalize Rig", width=300, command='KY_CreateUI.finalize_rig()')
    cmds.separator(style='none')

    cmds.text(label='HELP', width=300, height=30)
    cmds.separator(style='in')
    cmds.rowColumnLayout(numberOfColumns=2)
    cmds.button(label='Readme', width=150, command='KY_CreateUI.open_readme()')
    cmds.button(label='Guide Video', width=150, command='import webbrowser; webbrowser.open("https://youtu.be/RnRnf7ysa1w")')
    cmds.setParent('..')
    cmds.separator(style='none')

    cmds.showWindow()

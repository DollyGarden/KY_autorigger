# ********************************************************************
#  content = create ui functions
#  version = 0.1.4
#  date = 2022-03-18
#  dependencies = Maya
# 
#  license = MIT
#  author = Kelly Yang <kelly.yang1116@hotmail.com>
# ********************************************************************


import os
import importlib
import webbrowser

import maya.cmds as cmds
from Qt import QtWidgets, QtGui, QtCore, QtCompat

import KY_Locators
import KY_Controller
import KY_Constraints
import KY_CreateIK
import KY_SecondaryLocators
import KY_Joints

importlib.reload(KY_Locators)
importlib.reload(KY_Controller)
importlib.reload(KY_Constraints)
importlib.reload(KY_CreateIK)
importlib.reload(KY_SecondaryLocators)
importlib.reload(KY_Joints)

#********************************************************************
# VARIABLES
TITLE = os.path.splitext(os.path.basename(__file__))[0]
CURRENT_PATH = os.path.dirname(__file__)
IMG_PATH = CURRENT_PATH + "/img/{}.jpg"

#********************************************************************
# Main UI Class
class AutoRiggerUI:
    
    def __init__(self):
        cmds.currentUnit(linear='meter')
        cmds.grid(size=12, spacing=5, divisions=5)

        ar_path_ui = CURRENT_PATH + "/" + TITLE + ".ui"
        self.wgAutoRigger = QtCompat.loadUi(ar_path_ui)

        self.wgAutoRigger.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.wgAutoRigger.setWindowIcon(QtGui.QPixmap(IMG_PATH.format("shelf_AR")))
        self.wgAutoRigger.lblImage.setPixmap(QtGui.QPixmap(IMG_PATH.format("KY_AR_image")))

        # SIGNAL
        self.wgAutoRigger.btnCreateBaseLocators.clicked.connect(self.press_btnCreateBaseLocators)
        self.wgAutoRigger.btnCreateSecondaryLocators.clicked.connect(self.press_btnCreateSecondaryLocators)
        self.wgAutoRigger.btnDeleteAllLocators.clicked.connect(self.press_btnDeleteAllLocators)
        self.wgAutoRigger.btnMirrorLtoR.clicked.connect(self.press_btnMirrorLtoR)
        self.wgAutoRigger.btnCreateJoints.clicked.connect(self.press_btnCreateJoints)
        self.wgAutoRigger.btnDeleteJoints.clicked.connect(self.press_btnDeleteJoints)
        self.wgAutoRigger.btnFinalizeRig.clicked.connect(self.press_btnFinalizeRig)
        self.wgAutoRigger.btnReadme.clicked.connect(self.press_btnReadme)
        self.wgAutoRigger.btnGuideVideo.clicked.connect(self.press_btnGuideVideo)
        self.wgAutoRigger.editSpineCount.setText('4')
        self.wgAutoRigger.editFingerCount.setText('5')

        self.wgAutoRigger.show()

    def spine_count(self):
        spine_count_value = int(self.wgAutoRigger.editSpineCount.text())
        return(spine_count_value)

    def finger_count(self):
        finger_count_value = int(self.wgAutoRigger.editFingerCount.text())
        return(finger_count_value)

    #********************************************************************
    # PRESS
    def press_btnCreateBaseLocators(self):
        KY_Locators.create_locators(self.spine_count(), self.finger_count())

    def press_btnCreateSecondaryLocators(self):
        self.sec_locator_ui = SecLocatorUI()
    
    def press_btnDeleteAllLocators(self):
        KY_Locators.delete_locators()

    def press_btnMirrorLtoR(self):
        KY_Locators.mirror_locators()
        
    def press_btnCreateJoints(self):
        KY_Joints.create_joints()
    
    def press_btnDeleteJoints(self):
        KY_Joints.delete_joints()
    
    def press_btnFinalizeRig(self):
        KY_Controller.create_controller(self.spine_count(), self.finger_count())
        KY_CreateIK.ik_handles()
        KY_Constraints.create_constrains(self.spine_count(), self.finger_count())

    def press_btnReadme(self):
        webbrowser.open(CURRENT_PATH+'/readme.txt')
    
    def press_btnGuideVideo(self):
        webbrowser.open("https://youtu.be/RnRnf7ysa1w")

#********************************************************************
# Secondary Locators UI Class
class SecLocatorUI:
    def __init__(self):

        sl_path_ui = CURRENT_PATH + "/KY_SecondaryLocators.ui"

        self.wgSecLocators = QtCompat.loadUi(sl_path_ui)
        self.wgSecLocators.setWindowIcon(QtGui.QPixmap(IMG_PATH.format("shelf_AR")))

        # SIGNAL
        self.wgSecLocators.btnCreateForearmTwist.clicked.connect(self.press_btnCreateForearmTwist)
        self.wgSecLocators.btnCreateReverseFootroll.clicked.connect(self.press_btnCreateReverseFootroll)
        self.wgSecLocators.btnDeleteSecLocators.clicked.connect(self.press_btnDeleteSecLocators)
        
        self.wgSecLocators.editTwistJointsCount.setText('3')

        self.wgSecLocators.show()

    def twist_joints_count(self):
        twist_joints_count_value = int(self.wgSecLocators.editTwistJointsCount.text())
        return(twist_joints_count_value)

    #********************************************************************
    # PRESS
    def press_btnCreateForearmTwist(self):
        KY_SecondaryLocators.create_forearm_twist(self.twist_joints_count())

    def press_btnCreateReverseFootroll(self):
        KY_SecondaryLocators.create_reverse_footroll()
    
    def press_btnDeleteSecLocators(self):
        KY_SecondaryLocators.delete_secondary_locator()

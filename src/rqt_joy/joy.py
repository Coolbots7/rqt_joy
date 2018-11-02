import os
import rospy
import rospkg

from sensor_msgs.msg import Joy

from qt_gui.plugin import Plugin
from python_qt_binding import loadUi
from python_qt_binding.QtWidgets import QWidget

class JoyVis(Plugin):

    def __init__(self, context):
        super(JoyVis, self).__init__(context)

        self.setObjectName('Joy')

        from argparse import ArgumentParser
        parser = ArgumentParser()

        parser.add_argument("-q", "--quiet", action="store_true",
            dest="quiet",
            help="Put plugin in silent mode")
        args, unknowns = parser.parse_known_args(context.argv())


        self._widget = QWidget()

        ui_file = os.path.join(rospkg.RosPack().get_path('rqt_joy'), 'resource', 'Joy.ui')

        loadUi(ui_file, self._widget)

        self._widget.setObjectName('JoyUi')

        if context.serial_number() > 1:
            self._widget.setWindowTitle(self._widget.windowTitle() + (' (%d)' % context.serial_number()))

        context.add_widget(self._widget)

        self._widget.joy_1_x.setValue(0)
        self._widget.joy_1_y.setValue(0)

        rospy.Subscriber("joy", Joy, self.joyMessageCallback)

    def shutdown_plugin(self):
        pass

    def save_settings(self, plugin_settings, instance_settings):
        pass

    def restore_settings(self, plugin_settings, instance_settings):
        pass

    def joyMessageCallback(self,joy):
        self._widget.joy_1_x.setValue(joy.axes[0]*100)
        self._widget.joy_1_y.setValue(joy.axes[1]*100)

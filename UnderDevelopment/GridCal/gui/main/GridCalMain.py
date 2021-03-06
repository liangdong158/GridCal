# This file is part of GridCal.
#
# GridCal is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# GridCal is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GridCal.  If not, see <http://www.gnu.org/licenses/>.

__author__ = 'Santiago Peñate Vera'

"""
This class is the handler of the main gui of GridCal.
"""

import os.path
import platform
import sys
from collections import OrderedDict
from enum import Enum

from gui.main.gui import *
from matplotlib.colors import LinearSegmentedColormap
from multiprocessing import cpu_count
from gui.GuiFunctions import *
from gui.GridEditor import *




########################################################################################################################
# Main Window
########################################################################################################################


# define the IPython console
print(platform.system())
# if platform.system() == 'Linux':
#     from IPython.qt.console.rich_ipython_widget import RichIPythonWidget
#     from IPython.qt.inprocess import QtInProcessKernelManager
#     from IPython.lib import guisupport
#
#     class QIPythonWidget(RichIPythonWidget):
#         """
#         Convenience class for a live IPython console widget.
#         We can replace the standard banner using the customBanner argument
#         """
#
#         def __init__(self, customBanner=None, *args, **kwargs):
#             if customBanner is not None:
#                 self.banner = customBanner
#             super(QIPythonWidget, self).__init__(*args, **kwargs)
#             self.kernel_manager = kernel_manager = QtInProcessKernelManager()
#             kernel_manager.start_kernel(show_banner=False)
#             kernel_manager.kernel.gui = 'qt4'
#             self.kernel_client = kernel_client = self._kernel_manager.client()
#             kernel_client.start_channels()
#
#             def stop():
#                 kernel_client.stop_channels()
#                 kernel_manager.shutdown_kernel()
#                 guisupport.get_app_qt4().exit()
#
#             self.exit_requested.connect(stop)
#
#         def pushVariables(self, variableDict):
#             """
#             Given a dictionary containing name / value pairs, push those variables
#             to the IPython console widget
#             """
#             self.kernel_manager.kernel.shell.push(variableDict)
#
#         def clearTerminal(self):
#             """
#             Clears the terminal
#             """
#             self._control.clear()
#
#             # self.kernel_manager
#
#         def printText(self, text):
#             """
#             Prints some plain text to the console
#             """
#             self._append_plain_text(text)
#
#         def executeCommand(self, command):
#             """
#             Execute a command in the frame of the console widget
#             """
#             self._execute(command, False)
#
#
# elif platform.system() == 'Windows':
#     from qtconsole.qt import QtGui
#     from qtconsole.rich_jupyter_widget import RichJupyterWidget
#     from qtconsole.inprocess import QtInProcessKernelManager
#
#     class QIPythonWidget(RichJupyterWidget):
#         """
#         Convenience class for a live IPython console widget.
#         We can replace the standard banner using the customBanner argument
#         """
#         def __init__(self, customBanner=None, *args, **kwargs):
#             super(QIPythonWidget, self).__init__(*args, **kwargs)
#
#             if customBanner is not None:
#                 self.banner = customBanner
#
#             self.kernel_manager = kernel_manager = QtInProcessKernelManager()
#             kernel_manager.start_kernel(show_banner=False)
#             kernel_manager.kernel.gui = 'qt4'
#             self.kernel_client = kernel_client = self._kernel_manager.client()
#             kernel_client.start_channels()
#
#             def stop():
#                 kernel_client.stop_channels()
#                 kernel_manager.shutdown_kernel()
#                 guisupport.get_app_qt4().exit()
#             self.exit_requested.connect(stop)
#
#         def pushVariables(self, variableDict):
#             """
#             Given a dictionary containing name / value pairs, push those variables
#             to the IPython console widget
#             """
#             self.kernel_manager.kernel.shell.push(variableDict)
#
#         def clearTerminal(self):
#             """
#             Clears the terminal
#             """
#             self._control.clear()
#
#             # self.kernel_manager
#
#         def printText(self, text):
#             """
#             Prints some plain text to the console
#             """
#             self._append_plain_text(text)
#
#         def executeCommand(self, command):
#             """
#             Execute a command in the frame of the console widget
#             """
#             self._execute(command, False)


class ResultTypes(Enum):
    bus_voltage_per_unit = 1,
    bus_voltage = 2,
    bus_s_v_curve = 3,
    bus_QV_curve = 4,
    bus_active_power = 5,
    bus_reactive_power = 6,
    bus_active_and_reactive_power = 7,
    bus_apparent_power = 8,
    branch_current_per_unit = 9,
    branch_current = 10,
    branch_power_flow_per_unit = 11,
    branch_power_flow = 12,
    branch_losses = 13,
    branches_loading = 14,
    gen_reactive_power_pu = 15,
    gen_reactive_power = 16


class ProfileTypes(Enum):
    Loads = 1,
    Generators = 2


class NewProfilesStructureDialogue(QDialog):
    def __init__(self):
        super(NewProfilesStructureDialogue, self).__init__()
        self.setObjectName("self")
        # self.resize(200, 71)
        # self.setMinimumSize(QtCore.QSize(200, 71))
        # self.setMaximumSize(QtCore.QSize(200, 71))
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap("Icons/Plus-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.setWindowIcon(icon)
        self.layout = QVBoxLayout(self)

        self.calendar = QDateTimeEdit()
        self.calendar.setDateTime(QDateTime(2011, 4, 22, 00, 00, 00))

        self.steps_spinner = QSpinBox()
        self.steps_spinner.setMinimum(1)
        self.steps_spinner.setMaximum(9999999)
        self.steps_spinner.setValue(1)

        self.step_length = QDoubleSpinBox()
        self.step_length.setMinimum(1)
        self.step_length.setMaximum(60)
        self.step_length.setValue(1)

        self.units = QComboBox()
        self.units.setModel(get_list_model(['h', 'm', 's']))

        self.accept_btn = QPushButton()
        self.accept_btn.setText('Accept')
        self.accept_btn.clicked.connect(self.accept_click)

        self.layout.addWidget(self.calendar)
        self.layout.addWidget(self.steps_spinner)
        self.layout.addWidget(self.step_length)
        self.layout.addWidget(self.units)
        self.layout.addWidget(self.accept_btn)

        self.setLayout(self.layout)

        self.setWindowTitle('New profiles structure')

    def accept_click(self):
        self.accept()

    def get_values(self):
        steps = self.steps_spinner.value()

        step_length = self.step_length.value()

        step_unit = self.units.currentText()

        time_base = self.calendar.dateTime()

        # a = QDateTime(2011, 4, 22, 00, 00, 00)
        # a
        return steps, step_length, step_unit, time_base.toPyDateTime()


class MainGUI(QMainWindow):

    def __init__(self, parent=None):
        """

        @param parent:
        """

        # create main window
        QWidget.__init__(self, parent)
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        # Declare circuit
        self.circuit = MultiCircuit()

        self.project_directory = None

        # solvers dictionary
        self.solvers_dict = OrderedDict()
        self.solvers_dict['Newton-Raphson [NR]'] = SolverType.NR
        self.solvers_dict['NR Fast decoupled (BX)'] = SolverType.NRFD_BX
        self.solvers_dict['NR Fast decoupled (XB)'] = SolverType.NRFD_XB
        self.solvers_dict['Newton-Raphson-Iwamoto'] = SolverType.IWAMOTO
        self.solvers_dict['Gauss-Seidel'] = SolverType.GAUSS
        self.solvers_dict['Z-Matrix Gauss-Seidel'] = SolverType.ZBUS
        self.solvers_dict['Holomorphic embedding [HELM]'] = SolverType.HELM
        self.solvers_dict['Z-Matrix HELM'] = SolverType.HELMZ
        self.solvers_dict['Continuation NR'] = SolverType.CONTINUATION_NR
        self.solvers_dict['DC approximation'] = SolverType.DC

        lst = list(self.solvers_dict.keys())
        mdl = get_list_model(lst)
        self.ui.solver_comboBox.setModel(mdl)
        self.ui.retry_solver_comboBox.setModel(mdl)

        self.ui.solver_comboBox.setCurrentIndex(0)
        self.ui.retry_solver_comboBox.setCurrentIndex(3)

        mdl = get_list_model(self.circuit.profile_magnitudes.keys())
        self.ui.profile_device_type_comboBox.setModel(mdl)
        self.profile_device_type_changed()

        ################################################################################################################
        # Declare the schematic editor
        ################################################################################################################

        # Widget layout and child widgets:
        self.horizontalLayout = QHBoxLayout(self)
        splitter = QSplitter(self)
        splitter2 = QSplitter(self)
        self.object_editor_table = QTableView(self)
        self.libraryBrowserView = QListView(self)
        self.libraryModel = LibraryModel(self)
        self.libraryModel.setColumnCount(1)

        # Create an icon with an icon:
        object_factory = ObjectFactory()

        # initialize library of items
        self.libItems = []
        self.libItems.append(QStandardItem(object_factory.get_box(), 'Bus'))
        # self.libItems.append(QtGui.QStandardItem(object_factory.get_circle(), 'Generator'))
        # self.libItems.append( QtGui.QStandardItem(object_factory.get_transformer(), 'Transformer') )
        # self.libItems.append(QtGui.QStandardItem(object_factory.get_box(), 'Line'))
        # self.libItems.append(QtGui.QStandardItem(object_factory.get_box(), 'Battery'))
        # self.libItems.append(QtGui.QStandardItem(object_factory.get_box(), 'External Connection'))
        for i in self.libItems:
            self.libraryModel.appendRow(i)

        # set the objects list
        self.object_types = ['Buses', 'Branches', 'Loads', 'Static Generators',
                             'Controlled Generators', 'Batteries', 'Shunts']
        self.ui.dataStructuresListView.setModel(get_list_model(self.object_types))

        # Actual libraryView object
        self.libraryBrowserView.setModel(self.libraryModel)
        self.libraryBrowserView.setViewMode(self.libraryBrowserView.ListMode)
        self.libraryBrowserView.setDragDropMode(self.libraryBrowserView.DragOnly)

        self.diagramScene = DiagramScene(self, self.circuit)  # scene to add to the QGraphicsView
        self.diagramView = EditorGraphicsView(self.diagramScene, parent=self, editor=self)

        # Add the two objects into a layout
        splitter2.addWidget(self.libraryBrowserView)
        splitter2.addWidget(self.object_editor_table)
        splitter2.setOrientation(Qt.Vertical)
        splitter.addWidget(splitter2)
        splitter.addWidget(self.diagramView)

        self.ui.schematic_layout.addWidget(splitter)
        splitter.setStretchFactor(1, 10)
        self.ui.splitter_8.setStretchFactor(1, 15)

        self.startedConnection = None
        self.branch_editor_count = 1
        self.expand_factor = 1.5

        self.lock_ui = False
        self.ui.progress_frame.setVisible(self.lock_ui)

        self.power_flow = None
        self.monte_carlo = None
        self.time_series = None
        self.voltage_stability = None

        self.available_results_dict = None
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(cpu_count())

        ################################################################################################################
        # Console
        ################################################################################################################

        # self.ipyConsole = QIPythonWidget(customBanner="GridCal console.\n\n"
        #                                               "type gridcalhelp() to see the available specific commands.\n\n"
        #                                               "the following libraries are already loaded:\n"
        #                                               "np: numpy\n"
        #                                               "pd: pandas\n"
        #                                               "plt: matplotlib\n\n")
        # self.ui.console_tab.layout().addWidget(self.ipyConsole)
        # self.ipyConsole.pushVariables({"gridcalhelp": self.print_console_help,
        #                                "np": np, "pd": pd, "plt": plt, "clc": self.clc})

        ################################################################################################################
        # Connections
        ################################################################################################################
        self.ui.actionNew_project.triggered.connect(self.new_project)

        self.ui.actionOpen_file.triggered.connect(self.open_file)

        self.ui.actionSave.triggered.connect(self.save_file)

        self.ui.actionPower_flow.triggered.connect(self.run_power_flow)

        self.ui.actionVoltage_stability.triggered.connect(self.run_voltage_stability)

        self.ui.actionPower_Flow_Time_series.triggered.connect(self.run_time_series)

        self.ui.actionPower_flow_Stochastic.triggered.connect(self.run_stochastic)

        self.ui.actionAbout.triggered.connect(self.about_box)

        # Buttons

        self.ui.cancelButton.clicked.connect(self.set_cancel_state)

        self.ui.new_profiles_structure_pushButton.clicked.connect(self.new_profiles_structure)

        self.ui.delete_profiles_structure_pushButton.clicked.connect(self.delete_profiles_structure)

        self.ui.set_profile_state_button.clicked.connect(self.set_profiles_state_to_grid)

        self.ui.profile_import_pushButton.clicked.connect(self.import_profiles)

        self.ui.profile_display_pushButton.clicked.connect(self.display_profiles)

        # node size
        self.ui.actionBigger_nodes.triggered.connect(self.bigger_nodes)

        self.ui.actionSmaller_nodes.triggered.connect(self.smaller_nodes)

        self.ui.actionCenter_view.triggered.connect(self.center_nodes)

        # list clicks
        self.ui.result_listView.clicked.connect(self.update_available_results_in_the_study)
        self.ui.result_type_listView.clicked.connect(self.result_type_click)

        self.ui.dataStructuresListView.clicked.connect(self.view_objects_data)

        # combobox
        self.ui.profile_device_type_comboBox.currentTextChanged.connect(self.profile_device_type_changed)

        ################################################################################################################
        # Other actions
        ################################################################################################################
        fname = 'IEEE_30BUS_profiles.xls'
        self.circuit.load_file(fname)
        self.create_schematic_from_api(explode_factor=50)

        ################################################################################################################
        # Colormaps
        ################################################################################################################
        vmax = 1.2
        seq = [(0 / vmax, 'black'),
               (0.8 / vmax, 'blue'),
               (1.0 / vmax, 'green'),
               (1.05 / vmax, 'orange'),
               (1.2 / vmax, 'red')]
        self.voltage_cmap = LinearSegmentedColormap.from_list('vcolors', seq)
        seq = [(0.0, 'green'),
               (0.8, 'orange'),
               (1.0, 'red')]
        self.loading_cmap = LinearSegmentedColormap.from_list('lcolors', seq)

    def LOCK(self, val=True):
        """
        Lock the interface to prevent new simulation launches
        :param val:
        :return:
        """
        self.lock_ui = val
        self.ui.progress_frame.setVisible(self.lock_ui)

    def UNLOCK(self):
        """
        Unloack the interface
        @return:
        """
        self.LOCK(False)

    def about_box(self):

        url = 'https://github.com/SanPen/GridCal'

        msg = "GridCal is a research oriented electrical grid calculation software.\n"
        msg += "GridCal has been designed by Santiago Peñate Vera since 2015.\n"
        msg += "The calculation engine has been designed in a fully object oriented fashion. " \
               "The power flow routines have been adapted from MatPower, enhancing them to run fast in " \
               "the object oriented scheme.\n\n"

        msg += "The source of Gridcal can be found at:\n" + url + "\n"

        QMessageBox.about(self, "About GridCal", msg)

    def print_console_help(self):
        """
        print the console help in the console
        @return:
        """
        print('GridCal internal commands.\n')
        print('If a command is unavailable is because the study has not been executed yet.')

        print('\n\nclc():\tclear the console.')

        print('\n\nPower flow commands:')
        print('\tpowerflow.voltage:\t the nodal voltages in per unit')
        print('\tpowerflow.current:\t the branch currents in per unit')
        print('\tpowerflow.loading:\t the branch loading in %')
        print('\tpowerflow.losses:\t the branch losses in per unit')
        print('\tpowerflow.power:\t the nodal power injections in per unit')
        print('\tpowerflow.power_from:\t the branch power injections in per unit at the "from" side')
        print('\tpowerflow.power_to:\t the branch power injections in per unit at the "to" side')

        print('\n\nTime series power flow commands:')
        print('\ttimeseries.time:\t Profiles time index (pandas DateTimeIndex object)')
        print('\ttimeseries.load_profiles:\t Load profiles matrix (row: time, col: node)')
        print('\ttimeseries.gen_profiles:\t Generation profiles matrix (row: time, col: node)')
        print('\ttimeseries.voltages:\t nodal voltages results matrix (row: time, col: node)')
        print('\ttimeseries.currents:\t branches currents results matrix (row: time, col: branch)')
        print('\ttimeseries.loadings:\t branches loadings results matrix (row: time, col: branch)')
        print('\ttimeseries.losses:\t branches losses results matrix (row: time, col: branch)')

        print('\n\nVoltage stability power flow commands:')
        print('\tvoltagestability.continuation_voltage:\t Voltage values for every power multiplication factor.')
        print('\tvoltagestability.continuation_lambda:\t Value of power multiplication factor applied')
        print('\tvoltagestability.continuation_power:\t Power values for every power multiplication factor.')

        print('\n\nMonte Carlo power flow commands:')
        print('\tstochastic.V_avg:\t nodal voltage average result.')
        print('\tstochastic.I_avg:\t branch current average result.')
        print('\tstochastic.Loading_avg:\t branch loading average result.')
        print('\tstochastic.Losses_avg:\t branch losses average result.')

        print('\tstochastic.V_std:\t nodal voltage standard deviation result.')
        print('\tstochastic.I_std:\t branch current standard deviation result.')
        print('\tstochastic.Loading_std:\t branch loading standard deviation result.')
        print('\tstochastic.Losses_std:\t branch losses standard deviation result.')

        print('\tstochastic.V_avg_series:\t nodal voltage average series.')
        print('\tstochastic.V_std_series:\t branch current standard deviation series.')
        print('\tstochastic.error_series:\t Monte Carlo error series (the convergence value).')

    def clc(self):
        """
        Clear the console
        @return:
        """
        self.ipyConsole.clearTerminal()

    def startConnection(self, port):
        """
        Start the branch creation
        @param port:
        @return:
        """
        self.startedConnection = BranchGraphicItem(port, None, self.diagramScene)
        self.startedConnection.bus_from = port.parent
        port.setZValue(0)

    def sceneMouseMoveEvent(self, event):
        """

        @param event:
        @return:
        """
        if self.startedConnection:
            pos = event.scenePos()
            self.startedConnection.setEndPos(pos)

    def sceneMouseReleaseEvent(self, event):
        """
        Finalize the branch creation if its drawing ends in a terminal
        @param event:
        @return:
        """
        # Clear or finnish the started connection:
        if self.startedConnection:
            pos = event.scenePos()
            items = self.diagramScene.items(pos)  # get the item (the terminal) at the mouse position

            for item in items:
                if type(item) is TerminalItem:  # connect only to terminals
                    if item.parent is not self.startedConnection.fromPort.parent:  # forbid connecting to itself

                        # if type(item.parent) is not type(self.startedConnection.fromPort.parent): # forbid same type connections

                        self.startedConnection.setToPort(item)
                        item.hosting_connections.append(self.startedConnection)
                        self.startedConnection.setZValue(1000)
                        self.startedConnection.bus_to = item.parent
                        name = 'Branch ' + str(self.branch_editor_count)
                        obj = Branch(bus_from=self.startedConnection.bus_from.api_object,
                                     bus_to=self.startedConnection.bus_to.api_object,
                                     name=name)
                        obj.graphic_obj = self.startedConnection
                        self.startedConnection.api_object = obj
                        self.circuit.add_branch(obj)

            if self.startedConnection.toPort is None:
                self.startedConnection.remove_()

        self.startedConnection = None

        print('Buses:', len(self.circuit.buses))
        print('Branches:', len(self.circuit.branches))

    def bigger_nodes(self):
        """
        Expand the grid
        @return:
        """
        print('bigger')
        for item in self.diagramScene.items():
            if type(item) is BusGraphicItem:
                x = item.pos().x()
                y = item.pos().y()
                item.setPos(QPointF(x*self.expand_factor, y*self.expand_factor))

    def smaller_nodes(self):
        """
        Contract the grid
        @return:
        """
        print('smaller')
        for item in self.diagramScene.items():
            if type(item) is BusGraphicItem:
                x = item.pos().x()
                y = item.pos().y()
                item.setPos(QPointF(x/self.expand_factor, y/self.expand_factor))

    def center_nodes(self):
        """
        Center the view in the nodes
        @return: Nothing
        """
        self.diagramView.fitInView(self.diagramScene.sceneRect(), Qt.KeepAspectRatio)
        self.diagramView.scale(1.0, 1.0)

    def color_based_of_pf(self, Sbus, Sbranch, Vbus, LoadBranch):
        """
        Color the grid based on the results passed
        @param Vbus: Nodal Voltages array
        @param LoadBranch: Branch loading array
        @return: Nothing
        """
        # color nodes
        vmin = 0
        vmax = 1.2
        vrng = vmax - vmin
        vabs = abs(Vbus)
        vang = np.angle(Vbus, deg=True)
        vnorm = (vabs - vmin) / vrng
        # print(vnorm)
        i = 0
        for bus in self.circuit.buses:
            if bus.is_enabled:
                r, g, b, a = self.voltage_cmap(vnorm[i])
                # print(vnorm[i], '->', r*255, g*255, b*255, a)
                # QColor(r, g, b, alpha)
                bus.graphic_obj.setBrush(QColor(r*255, g*255, b*255, a*255))

                tooltip = bus.name + '\n' \
                          + 'V:' + "{:10.4f}".format(vabs[i]) + " <{:10.4f}".format(vang[i]) + 'º'
                if Sbus is not None:
                    tooltip += '\nS:' + "{:10.4f}".format(Sbus[i])
                bus.graphic_obj.setToolTip(tooltip)
            i += 1

        # color branches
        lnorm = abs(LoadBranch)
        lnorm[lnorm == np.inf] = 0
        # print(lnorm)
        i = 0
        for branch in self.circuit.branches:

            w = branch.graphic_obj.pen_width
            if branch.is_enabled:
                style = Qt.SolidLine
                r, g, b, a = self.loading_cmap(lnorm[i])
                color = QColor(r*255, g*255, b*255, a*255)
            else:
                style = Qt.DashLine
                color = Qt.gray

            tooltip = branch.name
            tooltip += '\nloading=' + "{:10.4f}".format(lnorm[i])
            tooltip += '\nPower=' + "{:10.4f}".format(Sbranch[i])
            branch.graphic_obj.setToolTip(tooltip)
            branch.graphic_obj.setPen(QtGui.QPen(color, w, style))
            i += 1

    def new_project(self):
        """
        Create new grid
        :return:
        """
        if len(self.circuit.buses) > 0:
            quit_msg = "Are you sure you want to quit the current grid and create a new one?"
            reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.circuit = MultiCircuit()
                self.diagramScene.circuit = self.circuit
                self.create_schematic_from_api(explode_factor=500)

            else:
                pass
        else:
            pass

    def open_file(self):
        """
        Open GridCal file
        @return:
        """
        # declare the allowed file types
        files_types = "Excel 97 (*.xls);;Excel (*.xlsx);;DigSILENT (*.dgs);;MATPOWER (*.m)"
        # call dialog to select the file

        filename, type_selected = QFileDialog.getOpenFileName(self, 'Open file', directory=self.project_directory, filter=files_types)

        if len(filename) > 0:
            # store the working directory
            self.project_directory = os.path.dirname(filename)
            print(filename)
            self.circuit = MultiCircuit()
            self.circuit.load_file(filename=filename)
            self.create_schematic_from_api(explode_factor=500)
            self.circuit.compile()

            if self.circuit.time_profile is not None:
                print('Profiles available')
                mdl = get_list_model(self.circuit.time_profile)
            else:
                mdl = QStandardItemModel()
            self.ui.profile_time_selection_comboBox.setModel(mdl)
            self.ui.vs_departure_comboBox.setModel(mdl)
            self.ui.vs_target_comboBox.setModel(mdl)

    def save_file(self):
        """
        Save the circuit case to a file
        """
        # declare the allowed file types
        files_types = "Excel (*.xlsx)"
        # call dialog to select the file
        filename, type_selected = QFileDialog.getSaveFileName(self, 'Save file',  self.project_directory, files_types)

        if filename is not "":
            # if the user did not enter the extension, add it automatically
            name, file_extension = os.path.splitext(filename)

            extension = dict()
            extension['Excel (*.xlsx)'] = '.xlsx'
            # extension['Numpy Case (*.npz)'] = '.npz'

            if file_extension == '':
                filename = name + extension[type_selected]

            # call to save the file in the circuit
            self.circuit.save_file(filename)

    def create_schematic_from_api(self, explode_factor=1):
        """
        This function explores the API values and draws an schematic layout
        @return:
        """
        # clear all
        self.diagramView.scene_.clear()

        # first create the buses
        for bus in self.circuit.buses:
            # print(bus.x, bus.y)
            bus.graphic_obj = self.diagramView.add_bus(bus=bus, explode_factor=explode_factor)
            bus.graphic_obj.create_children_icons()

        for branch in self.circuit.branches:
            terminal_from = branch.bus_from.graphic_obj.lower_terminals[0]
            terminal_to = branch.bus_to.graphic_obj.lower_terminals[0]
            connection = BranchGraphicItem(terminal_from, terminal_to, self.diagramScene, branch=branch)
            terminal_from.hosting_connections.append(connection)
            terminal_to.hosting_connections.append(connection)
            connection.redraw()
            branch.graphic_obj = connection

        # self.diagramView.repaint()
        # self.startedConnection.remove_()

    def view_objects_data(self):
        """

        Returns:

        """
        elm_type = self.ui.dataStructuresListView.selectedIndexes()[0].data()

        # ['Buses', 'Branches', 'Loads', 'Static Generators', 'Controlled Generators', 'Batteries']

        if elm_type == 'Buses':
            elm = Bus()
            mdl = ObjectsModel(self.circuit.buses, elm.edit_headers, elm.edit_types,
                               parent=self.ui.dataStructureTableView, editable=True)

        elif elm_type == 'Branches':
            elm = Branch(None, None)
            mdl = ObjectsModel(self.circuit.branches, elm.edit_headers, elm.edit_types,
                               parent=self.ui.dataStructureTableView, editable=True, non_editable_indices=[1, 2])

        elif elm_type == 'Loads':
            elm = Load()
            mdl = ObjectsModel(self.circuit.get_loads(), elm.edit_headers, elm.edit_types,
                               parent=self.ui.dataStructureTableView, editable=True, non_editable_indices=[1])

        elif elm_type == 'Static Generators':
            elm = StaticGenerator()
            mdl = ObjectsModel(self.circuit.get_static_generators(), elm.edit_headers, elm.edit_types,
                               parent=self.ui.dataStructureTableView, editable=True, non_editable_indices=[1])

        elif elm_type == 'Controlled Generators':
            elm = ControlledGenerator()
            mdl = ObjectsModel(self.circuit.get_controlled_generators(), elm.edit_headers, elm.edit_types,
                               parent=self.ui.dataStructureTableView, editable=True, non_editable_indices=[1])

        elif elm_type == 'Batteries':
            elm = Battery()
            mdl = ObjectsModel(self.circuit.get_batteries(), elm.edit_headers, elm.edit_types,
                               parent=self.ui.dataStructureTableView, editable=True, non_editable_indices=[1])

        elif elm_type == 'Shunts':
            elm = Shunt()
            mdl = ObjectsModel(self.circuit.get_shunts(), elm.edit_headers, elm.edit_types,
                               parent=self.ui.dataStructureTableView, editable=True, non_editable_indices=[1])

        self.ui.dataStructureTableView.setModel(mdl)

    def profile_device_type_changed(self):
        """

        Returns:

        """
        dev_type = self.ui.profile_device_type_comboBox.currentText()

        mdl = get_list_model(self.circuit.profile_magnitudes[dev_type][0])
        self.ui.device_type_magnitude_comboBox.setModel(mdl)

    def new_profiles_structure(self):
        print('new_profiles_structure')

        dlg = NewProfilesStructureDialogue()
        if dlg.exec_():
            steps, step_length, step_unit, time_base = dlg.get_values()
            print(steps, step_length, step_unit, time_base)
            self.circuit.create_profiles(steps, step_length, step_unit, time_base)
            self.circuit.compile()

    def delete_profiles_structure(self):
        print('delete_profiles_structure')

    def set_profiles_state_to_grid(self):
        print('set_profiles_state_to_grid')

    def import_profiles(self):
        print('import_profiles')

    def display_profiles(self):
        """

        Returns:

        """
        print('display_profiles')

        dev_type = self.ui.profile_device_type_comboBox.currentText()

        magnitudes, mag_types = self.circuit.profile_magnitudes[dev_type]

        idx = self.ui.device_type_magnitude_comboBox.currentIndex()
        magnitude = magnitudes[idx]
        mtype = mag_types[idx]

        mdl = ProfilesModel(multi_circuit=self.circuit, device=dev_type, magnitude=magnitude, format=mtype, parent=self.ui.tableView)
        self.ui.tableView.setModel(mdl)

    def get_selected_power_flow_options(self):
        """
        Gather power flow run options
        :return:
        """
        solver_type = self.solvers_dict[self.ui.solver_comboBox.currentText()]

        enforce_Q_limits = self.ui.control_Q_checkBox.isChecked()

        exponent = self.ui.tolerance_spinBox.value()
        tolerance = 1.0 / (10.0**exponent)

        max_iter = self.ui.max_iterations_spinBox.value()

        set_last_solution = self.ui.remember_last_solution_checkBox.isChecked()

        if self.ui.helm_retry_checkBox.isChecked():
            solver_to_retry_with = self.solvers_dict[self.ui.retry_solver_comboBox.currentText()]
        else:
            solver_to_retry_with = None

        dispatch_storage = self.ui.dispatch_storage_checkBox.isChecked()

        ops = PowerFlowOptions(solver_type=solver_type,
                               aux_solver_type=solver_to_retry_with,
                               verbose=False,
                               robust=False,
                               initialize_with_existing_solution=True,
                               dispatch_storage=dispatch_storage,
                               tolerance=tolerance,
                               max_iter=max_iter,
                               control_Q=enforce_Q_limits)

        return ops

    def run_power_flow(self):
        """
        Run a power flow simulation
        :return:
        """

        self.LOCK()
        self.circuit.compile()

        options = self.get_selected_power_flow_options()
        self.power_flow = PowerFlow(self.circuit, options)

        # self.power_flow.progress_signal.connect(self.ui.progressBar.setValue)
        # self.power_flow.done_signal.connect(self.UNLOCK)
        # self.power_flow.done_signal.connect(self.post_power_flow)
        #
        # self.power_flow.start()
        self.threadpool.start(self.power_flow)

        self.threadpool.waitForDone()
        self.post_power_flow()

    def post_power_flow(self):
        """
        Run a power flow simulation in a separated thread from the gui
        Returns:

        """
        # update the results in the circuit structures
        print('Post power flow')
        if self.circuit.power_flow_results is not None:
            print('Vbus:\n', abs(self.circuit.power_flow_results.voltage))
            print('Sbr:\n', abs(self.circuit.power_flow_results.Sbranch))
            print('ld:\n', abs(self.circuit.power_flow_results.loading))
            self.color_based_of_pf(Sbus=self.circuit.power_flow_results.Sbus,
                                   Sbranch=self.circuit.power_flow_results.Sbranch,
                                   Vbus=self.circuit.power_flow_results.voltage,
                                   LoadBranch=self.circuit.power_flow_results.loading)
            self.update_available_results()
        else:
            warn('Something went wrong, There are no power flow results.')
        self.UNLOCK()

    def run_voltage_stability(self):
        print('run_voltage_stability')

    def post_voltage_stability(self):
        self.update_available_results()

    def run_time_series(self):
        """
        Run a time series power flow simulation in a separated thread from the gui
        @return:
        """
        self.LOCK()
        self.circuit.compile()

        if self.circuit.has_time_series:

            options = self.get_selected_power_flow_options()
            self.time_series = TimeSeries(grid=self.circuit, options=options)

            # Set the time series run options
            self.time_series.progress_signal.connect(self.ui.progressBar.setValue)
            self.time_series.done_signal.connect(self.UNLOCK)
            self.time_series.done_signal.connect(self.post_time_series)

            self.time_series.start()

        else:
            msg = 'No time series loaded'
            q = QtGui.QMessageBox(QtGui.QMessageBox.Warning, 'GridCal', msg)
            q.setStandardButtons(QtGui.QMessageBox.Ok)
            i = QtGui.QIcon()
            i.addPixmap(QtGui.QPixmap("..."), QtGui.QIcon.Normal)
            q.setWindowIcon(i)
            q.exec_()

    def post_time_series(self):
        """
        Events to do when the time series simulation has finished
        @return:
        """
        if self.circuit.time_series_results is not None:
            print('\n\nVoltages:\n')
            print(self.circuit.time_series_results.voltage)
            print(self.circuit.time_series_results.converged)
            print(self.circuit.time_series_results.error)

            # plot(grid.master_time_array, abs(grid.time_series_results.loading)*100)
            # show()
            ts_analysis = TimeSeriesResultsAnalysis(self.circuit.circuits[0].time_series_results)
            voltage = self.circuit.time_series_results.voltage.max(axis=1)
            loading = self.circuit.time_series_results.loading.max(axis=1)
            Sbranch = self.circuit.time_series_results.Sbranch.max(axis=1)
            self.color_based_of_pf(Sbus=None, Sbranch=Sbranch, Vbus=voltage, LoadBranch=loading)
            self.update_available_results()
        else:
            print('No results for the time series simulation.')

    def run_stochastic(self):
        """
        Run a Monte Carlo simulation
        @return:
        """
        print('run_stochastic')

        self.LOCK()
        self.circuit.compile()

        options = self.get_selected_power_flow_options()

        self.monte_carlo = MonteCarlo(self.circuit, options)

        self.monte_carlo.progress_signal.connect(self.ui.progressBar.setValue)
        self.monte_carlo.done_signal.connect(self.UNLOCK)
        self.monte_carlo.done_signal.connect(self.post_stochastic)

        self.monte_carlo.start()

    def post_stochastic(self):
        """
        Actions to perform after the Monte Carlo simulation is finished
        @return:
        """
        print('post_stochastic')
        # update the results in the circuit structures
        print('Vbus:\n', abs(self.monte_carlo.results.voltage))
        print('Ibr:\n', abs(self.monte_carlo.results.current))
        print('ld:\n', abs(self.monte_carlo.results.loading))
        self.color_based_of_pf(Vbus=self.monte_carlo.results.voltage,
                               LoadBranch=self.monte_carlo.results.loading,
                               Sbranch=None,
                               Sbus=None)
        self.update_available_results()

    def set_cancel_state(self):
        """
        Cancell whatever's going on
        @return:
        """
        if self.power_flow is not None:
            self.power_flow.cancel()

        if self.monte_carlo is not None:
            self.monte_carlo.cancel()

        if self.time_series is not None:
            self.time_series.cancel()

        if self.voltage_stability is not None:
            self.voltage_stability.cancel()

    def update_available_results(self):
        """

        Returns:

        """
        lst = list()
        self.available_results_dict = dict()
        if self.power_flow is not None:
            lst.append("Power Flow")
            self.available_results_dict["Power Flow"] = self.power_flow.results.available_results

        if self.voltage_stability is not None:
            lst.append("Voltage Stability")
            self.available_results_dict["Power Flow"] = self.voltage_stability.results.available_results

        if self.time_series is not None:
            lst.append("Time Series")
            self.available_results_dict["Time Series"] = self.time_series.results.available_results

        if self.monte_carlo is not None:
            lst.append("Monte Carlo")
            self.available_results_dict["Monte Carlo"] = self.monte_carlo.results.available_results

        mdl = get_list_model(lst)
        self.ui.result_listView.setModel(mdl)

    def update_available_results_in_the_study(self):
        """

        Returns:

        """

        elm = self.ui.result_listView.selectedIndexes()[0].data()
        lst = self.available_results_dict[elm]
        mdl = get_list_model(lst)
        self.ui.result_type_listView.setModel(mdl)

    def result_type_click(self):
        print()
        study = self.ui.result_listView.selectedIndexes()[0].data()
        study_type = self.ui.result_type_listView.selectedIndexes()[0].data()

        if 'Bus' in study_type:
            names = self.circuit.bus_names
        elif 'Branch' in study_type:
            names = self.circuit.branch_names

        mdl = get_list_model(names, checks=True)
        self.ui.result_element_selection_listView.setModel(mdl)

        self.ui.resultsPlot.clear()

        if study == 'Power Flow':
            self.power_flow.results.plot(type=study_type, ax=self.ui.resultsPlot.get_axis(), indices=None, names=names)
        elif study == 'Time Series':
            pass
        elif study == 'Voltage Stability':
            pass
        elif study == 'Monte Carlo':
            pass

        self.ui.resultsPlot.redraw()


def run():
    app = QApplication(sys.argv)
    window = MainGUI()
    window.resize(1.61 * 700, 700)  # golden ratio
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()

from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QModelIndex, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtWidgets import QAction, QFileDialog

from .Inspector import LabelInspector
from .QWidget import QLabelGraphicScene, QLabelGraphicView

FILE = Path(__file__).resolve()
ROOT = str(FILE.parents[0])


class Ui_LabelPoly(object):
    def setupUi(self, LabelPoly):
        LabelPoly.setObjectName("LabelPoly")
        LabelPoly.resize(981, 636)
        LabelPoly.setMinimumSize(QtCore.QSize(1200, 675))
        self.centralwidget = QtWidgets.QWidget(LabelPoly)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        #Main window
        self.label_inspector = LabelInspector([])
        self.graphicsView = QLabelGraphicView(self.centralwidget, self.label_inspector)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout_2.addWidget(self.graphicsView)

        #Lists
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        #Label list
        self.label_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_label.setFont(font)
        self.label_label.setMouseTracking(True)
        self.label_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_label.setLineWidth(1)
        self.label_label.setMidLineWidth(0)
        self.label_label.setScaledContents(False)
        self.label_label.setAlignment(QtCore.Qt.AlignCenter)
        self.label_label.setObjectName("label_2")
        self.label_label.setText("Labels")
        self.verticalLayout.addWidget(self.label_label)
        self.labels_list = QtWidgets.QListView(self.centralwidget)
        self.label_list_model = QStandardItemModel()
        self.labels_list.setModel(self.label_list_model)
        self.labels_list.clicked[QModelIndex].connect(self.changeLabelClass)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labels_list.sizePolicy().hasHeightForWidth())
        self.labels_list.setSizePolicy(sizePolicy)
        self.labels_list.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.labels_list.setObjectName("classesList")
        self.verticalLayout.addWidget(self.labels_list)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_label_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_label_button.setMaximumSize(QtCore.QSize(80, 16777215))
        self.add_label_button.setObjectName("add_label_button")
        self.add_label_button.setText("Add")
        self.add_label_button.clicked.connect(self.addLabelClass)
        self.horizontalLayout.addWidget(self.add_label_button)


        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        #Object list
        self.object_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.object_label.setFont(font)
        self.object_label.setMouseTracking(False)
        self.object_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.object_label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.object_label.setLineWidth(1)
        self.object_label.setMidLineWidth(0)
        self.object_label.setTextFormat(QtCore.Qt.MarkdownText)
        self.object_label.setScaledContents(False)
        self.object_label.setAlignment(QtCore.Qt.AlignCenter)
        self.object_label.setObjectName("label")
        self.object_label.setText("Objects")
        self.verticalLayout.addWidget(self.object_label)
        self.object_list = QtWidgets.QListView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.object_list.sizePolicy().hasHeightForWidth())
        self.object_list.setSizePolicy(sizePolicy)
        self.object_list_model = QStandardItemModel()
        self.object_list.setModel(self.object_list_model)
        self.object_list.clicked[QModelIndex].connect(self.changeLabel)
        self.label_inspector.labels_changed = self.updateLabelList
        self.object_list.setObjectName("objectList")
        self.verticalLayout.addWidget(self.object_list)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.graphicsView.setMouseTracking(True)

        LabelPoly.setCentralWidget(self.centralwidget)
        self.retranslateUi(LabelPoly)
        QtCore.QMetaObject.connectSlotsByName(LabelPoly)

        # Toolbar
        self.toolBar = QtWidgets.QToolBar(LabelPoly)
        self.toolBar.setObjectName("toolBar")
        self.toolBar.setIconSize(QSize(40, 40))
        LabelPoly.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        open_single_action = QAction('Open file', self.toolBar)
        open_single_action.triggered.connect(self.openImage)
        open_single_action.setStatusTip('Open a document')
        open_single_action.setIcon(QIcon(ROOT + "/icons/open_single.png"))
        self.toolBar.addAction(open_single_action)
        open_folder_action = QAction("Open folder", self.toolBar)
        open_folder_action.setStatusTip("Open a folder of documents")
        open_folder_action.setIcon(QIcon(ROOT + "/icons/open_folder.png"))
        self.toolBar.addAction(open_folder_action)
        self.toolBar.addSeparator()
        insert_strategy_action = QAction("Create", self.toolBar)
        insert_strategy_action.setStatusTip("Create label")
        insert_strategy_action.setIcon(QIcon(ROOT + "/icons/insert.png"))
        self.toolBar.addAction(insert_strategy_action)
        select_strategy_action = QAction("Select", self.toolBar)
        select_strategy_action.setStatusTip("Select label")
        select_strategy_action.setIcon(QIcon(ROOT + "/icons/drag.png"))
        self.toolBar.addAction(select_strategy_action)

    def openImage(self):
        filename = QFileDialog.getOpenFileName(self.graphicsView,
                                               "Open Image",
                                               ".",
                                               "Images (*.png *.jpg)")
        scene = self.graphicsView.scene
        if isinstance(scene, QLabelGraphicScene):
            scene.changeImage(filename[0])
        self.label_inspector.clear()

    def addLabelClass(self, event):
        name, done = QtWidgets.QInputDialog.getText(
            self.centralwidget, 'Adding label class', 'Enter label class name:')
        if done and name:
            added = self.label_inspector.add_label_class(name)
            if not added:
                warning_dialog = QtWidgets.QMessageBox()
                warning_dialog.setText("Label with that name already exist")
                warning_dialog.setWindowTitle("Warning")
                warning_dialog.exec()
            self.updateLabelClassList()

    def changeLabelClass(self, index):
        item = self.label_list_model.itemFromIndex(index)
        self.label_inspector.change_label_class(item.text())

    def updateLabelClassList(self):
        self.label_list_model.clear()
        for i in self.label_inspector.label_classes:
            self.label_list_model.appendRow(QStandardItem(i))

    def changeLabel(self, index):
        item: QStandardItem = self.object_list_model.itemFromIndex(index)
        self.label_inspector.set_current(item.data())

    def updateLabelList(self):
        self.object_list_model.clear()
        for i in self.label_inspector.labels:
            item = QStandardItem(self.label_inspector.label_classes[i.class_index])
            item.setData(i)
            self.object_list_model.appendRow(item)

    def retranslateUi(self, LabelPoly):
        _translate = QtCore.QCoreApplication.translate
        LabelPoly.setWindowTitle(_translate("LabelPoly", "MainWindow"))

from PyQt5 import QtCore, QtGui, QtWidgets

from .Inspector import LabelInspector, ImageInspector
from .QWidget import QLabelGraphicScene, QLabelGraphicView, QLabelList, QLabelToolBar, QLabelClassList


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

        # Main window
        self.label_inspector = LabelInspector([])
        self.image_inspector = ImageInspector(self.label_inspector)
        self.graphicsScene = QLabelGraphicScene(self.label_inspector, self.image_inspector)
        self.graphicsView = QLabelGraphicView(self.centralwidget, self.graphicsScene)

        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout_2.addWidget(self.graphicsView)

        # Lists
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        # Label list
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
        self.labels_list = QLabelClassList(self.centralwidget, self.label_inspector)
        self.verticalLayout.addWidget(self.labels_list)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_label_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_label_button.setMaximumSize(QtCore.QSize(80, 16777215))
        self.add_label_button.setObjectName("add_label_button")
        self.add_label_button.setText("Add")
        self.add_label_button.clicked.connect(self.labels_list.addLabelClass)
        self.horizontalLayout.addWidget(self.add_label_button)

        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        # Object list
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
        self.object_list = QLabelList(self.centralwidget, self.label_inspector)
        self.verticalLayout.addWidget(self.object_list)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.graphicsView.setMouseTracking(True)

        LabelPoly.setCentralWidget(self.centralwidget)
        self.retranslateUi(LabelPoly)
        QtCore.QMetaObject.connectSlotsByName(LabelPoly)

        # Toolbar
        self.toolbar = QLabelToolBar(LabelPoly, self.graphicsScene)
        LabelPoly.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)

    def retranslateUi(self, LabelPoly):
        _translate = QtCore.QCoreApplication.translate
        LabelPoly.setWindowTitle(_translate("LabelPoly", "MainWindow"))

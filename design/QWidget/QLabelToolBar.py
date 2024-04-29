import functools
import os
from typing import Optional, List

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolBar, QWidget, QAction, QFileDialog

from .Scene import QLabelGraphicScene
from ..Strategy import InsertStrategy, SelectStrategy, LabelStrategy
from ..Icons import IconsPath


class QLabelToolBar(QToolBar):

    def __init__(self, parent: QWidget, scene: QLabelGraphicScene):
        super().__init__(parent)

        self.setObjectName("toolBar")
        self.setIconSize(QSize(40, 40))
        self.scene = scene
        self.scene.label_inspector.labels_classes_changed.append(self.update_classes_file)

        open_single_action = QAction('Open file', self)
        open_single_action.triggered.connect(functools.partial(self.open_images, True))
        open_single_action.setData({"aboba": 1})
        open_single_action.setStatusTip('Open a document')
        open_single_action.setIcon(QIcon(IconsPath.open_single.value))
        self.addAction(open_single_action)
        open_folder_action = QAction("Open folder", self)
        open_folder_action.triggered.connect(functools.partial(self.open_images))
        open_folder_action.setStatusTip("Open a folder of documents")
        open_folder_action.setIcon(QIcon(IconsPath.open_folder.value))
        # open_folder_action.setDisabled(True)
        self.addAction(open_folder_action)
        self.addSeparator()
        insert_strategy_action = QAction("Create", self)
        insert_strategy_action.setStatusTip("Create label")
        insert_strategy_action.setIcon(QIcon(IconsPath.insert.value))
        insert_strategy_action.setData({"strategy": InsertStrategy(scene)})
        insert_strategy_action.triggered.connect(functools.partial(self.set_strategy, insert_strategy_action))
        insert_strategy_action.setCheckable(True)
        self.addAction(insert_strategy_action)
        select_strategy_action = QAction("Select", self)
        select_strategy_action.setStatusTip("Select label")
        select_strategy_action.setIcon(QIcon(IconsPath.drag.value))
        select_strategy_action.setData({"strategy": SelectStrategy(scene)})
        select_strategy_action.triggered.connect(functools.partial(self.set_strategy, select_strategy_action))
        select_strategy_action.setCheckable(True)
        select_strategy_action.setDisabled(True)
        self.addAction(select_strategy_action)
        self.strategy_actions = [insert_strategy_action, select_strategy_action]
        self.set_strategy(insert_strategy_action)
        self.addSeparator()

        self.classes_filepath: str = None

    def set_strategy(self, action: QAction):
        if action.data() and isinstance(action.data(), dict):
            strategy = action.data().get("strategy", None)
            for another_action in self.strategy_actions:
                another_action.setChecked(False)
            if strategy and isinstance(strategy, LabelStrategy):
                strategy.apply()
                action.setChecked(True)

    def open_classes_file(self, filepath: str) -> Optional[List[str]]:
        if not filepath.endswith("classes.txt"):
            filepath = '/'.join(filepath.strip().split("/")[:-1]) + "/classes.txt"
        self.classes_filepath = filepath
        if os.path.isfile(filepath):
            with open(filepath, encoding='utf-8', mode='r') as class_file:
                classes = [x.strip() for x in class_file.readlines()]
            return classes
        else:
            with open(filepath, encoding='utf-8', mode='a'):
                pass
            return []

    def update_classes_file(self):
        if not self.scene.image.width():
            return
        classes = [x + '\n' for x in self.scene.label_inspector.label_classes]
        open(self.classes_filepath, mode='w').close()
        with open(self.classes_filepath, encoding='utf-8', mode='w') as file:
            file.writelines(classes)

    def open_images(self, single: bool = False):
        if single:
            path, done = QFileDialog.getOpenFileName(self,
                                                     "Open Image",
                                                     ".",
                                                     "Images (*.png *.jpg *.jpeg)")
        else:
            path = QFileDialog.getExistingDirectory(self,
                                                    'Select a folder',
                                                    '.',
                                                    QFileDialog.ShowDirsOnly)
            done = True if path else False

        if done:
            self.scene.image_inspector.get_images(path)
            classes = self.open_classes_file(path)
            self.scene.label_inspector.add_label_classes(classes, inplace=True)

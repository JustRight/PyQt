#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年12月11日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
@email: 892768447@qq.com
@file: HotKey
@description: 
'''
import sys

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QTextBrowser, QPushButton,\
    QMessageBox
import keyboard


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class Window(QWidget):

    dialogShow = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.dialogShow.connect(self.onShowDialog, type=Qt.QueuedConnection)
        self.logView = QTextBrowser(self)
        self.logView.append("点击右上角关闭按钮会隐藏窗口,通过热键Alt+S来显示")
        self.logView.append("等待热键中")
        layout.addWidget(QPushButton(
            "退出整个程序", self, clicked=self.onQuit))
        layout.addWidget(self.logView)

        keyboard.add_hotkey('alt+s', self.onShow, suppress=False)  # 显示界面
        keyboard.add_hotkey('ctrl+s', self.onHide, suppress=False)  # 隐藏界面
        keyboard.add_hotkey('shift+s', self.onQuit, suppress=False)  # 退出程序

        # 拦截系统的快捷键,suppress=True表示拦截,不传递到其它程序
        keyboard.add_hotkey(
            'win+s', lambda: self.logView.append('按下了win+s'), suppress=True)
        keyboard.add_hotkey(
            'win+r', lambda: self.logView.append('按下了win+r'), suppress=True)
        # 这个东西千万不能拦截掉，要出问题滴
        keyboard.add_hotkey(
            'ctrl+alt+del', lambda: self.logView.append('😏😏我知道你按了任务管理器😏😏'))

        # 这个函数类似while True，由于这里有界面GUI的loop事件，可以达到类似的效果
#         keyboard.wait()#Block forever, like `while True`.==

    def onShow(self):
        """显示"""
        self.logView.append('按下alt+s')
        self.show()
        self.showNormal()
        self.dialogShow.emit()

    def onShowDialog(self):
        QMessageBox.information(self, '对话框', '按下alt+s键')

    def onHide(self):
        """隐藏"""
        self.logView.append('按下ctrl+s')
        self.hide()

    def onQuit(self):
        """退出函数"""
        keyboard.unhook_all_hotkeys()  # 取消所有热键
        QApplication.instance().quit()

    def closeEvent(self, event):
        # 忽略关闭窗口,直接隐藏
        self.hide()
        return event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial

This example draws three rectangles in three
different colours.

author: Jan Bodnar
website: zetcode.com
last edited: September 2011
"""

import sys
from PyQt4 import QtGui, QtCore

class Grid(QtGui.QWidget):

   def __init__(self, name, path):
      super(Grid, self).__init__()
      self.path = path
      self.name = name
      self.initUI()

   def initUI(self):

      self.setGeometry(300, 300, 500, 500)
      self.setWindowTitle(self.name)
      self.show()

   def paintEvent(self, e):

      qp = QtGui.QPainter()
      qp.begin(self)
      self.drawGrid(qp)
      self.paintPath(qp, self.path)
      qp.end()

   def drawGrid(self, qp):
      width = self.frameGeometry().width()
      height = self.frameGeometry().height()
      pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
      for i in range(0, height, height//8):
         qp.drawLine(0, i, 10*width//11, i)
      for j in range(0, width, width//11):
         qp.drawLine(j,0, j, 7*height//8)

   def paintPath(self, qp, path):
      width = self.frameGeometry().width()
      height = self.frameGeometry().height()
      color = QtGui.QColor(0, 0, 0)
      qp.setPen(color)


      start = path[0]
      end = path[-1]

      for pos in path:
         if pos == start:
            qp.setBrush(QtGui.QColor(45, 115, 181))
         elif pos == end:
            qp.setBrush(QtGui.QColor(181, 67, 45))
         else:
            qp.setBrush(QtGui.QColor(45, 181, 83))

         start_x = pos[1]*(width//11)
         size_x = (width/11)
         start_y = pos[0]*(height//8)
         size_y = (height/8)

         qp.drawRect(start_x, start_y, size_x, size_y)




def main():

   app = QtGui.QApplication(sys.argv)
   ex = Grid([(0,0),(1,1),(6,2)])
   sys.exit(app.exec_())


if __name__ == '__main__':
   main()
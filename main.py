from PyQt5 import QtSql
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer
from ui_MainWindow import Ui_widget
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog
import cv2
import sys
import datetime


class QmyWidget(QWidget):
   def __init__(self, parent=None):
      super().__init__(parent)    #调用父类构造函数，创建窗体
      self.ui = Ui_widget()         #创建UI对象
      self.ui.setupUi(self)       #构造UI
      self.ui.label_5.setText(' ')
      self.video_path = ''
      self.ui.label_6.setText(str(datetime.datetime.now().date()))
      self.ui.lineEdit.setText(str(datetime.datetime.now().date().weekday()+1))
      self.db_name = 'fitness'
      # 添加一个sqlite数据库连接并打开
      db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
      db.setDatabaseName('{}.sqlite'.format(self.db_name))
      if db.open():
         print('连接数据库成功')
      else:
         print(db.lastError().text())  # 打印操作数据库时出现的错误
      query = QtSql.QSqlQuery("SELECT days FROM persitsDay")
      days = 0
      while query.next():
         days = query.value(0)
      days = str(days)
      self.ui.label_3.setText(days)

   def on_pushButton_clicked(self):
      xinqiji = self.ui.lineEdit.text()
      xinqiji = int(xinqiji)
      if xinqiji == 1:
         self.ui.label_5.setText('今天是练胸日')
      elif xinqiji == 2:
         self.ui.label_5.setText('今天是练肩日')
      elif xinqiji == 3:
         self.ui.label_5.setText('今天是练背日')
      elif xinqiji == 4:
         self.ui.label_5.setText('今天是练手臂日')
      elif xinqiji == 5:
         self.ui.label_5.setText('今天是练腿日')
      elif xinqiji == 6:
         self.ui.label_5.setText('今天是休息日')
      else:
         self.ui.label_5.setText('今天是休息日')

   def on_pushButton2_clicked(self):
      persistdays  = self.ui.label_3.text()
      persistdays = int(persistdays)+1
      persistdays = str(persistdays)
      self.ui.label_3.setText(persistdays)
      query = QtSql.QSqlQuery("SELECT lastID FROM persitsDay")
      lastid = 0
      while query.next():
          lastid = query.value(0)
      id = lastid+1
      data = str(self.ui.label_6.text())
      weekday = int(self.ui.lineEdit.text())
      operation = str(self.ui.label_5.text())
      photo = str(self.video_path)
      query.prepare(
         "insert into record values(?,?,?,?,?)")
      query.bindValue(0, id)
      query.bindValue(1, data)
      query.bindValue(2, weekday)
      query.bindValue(3, operation)
      query.bindValue(4, photo)
      result = query.exec()
      query.prepare('UPDATE persitsDay SET days = ?, lastID = ? WHERE id = 1')
      query.bindValue(0, persistdays)
      query.bindValue(1, id)
      result = query.exec()

   def show_dialog(self):
      file_dialog = QFileDialog()
      # file_dialog.setNameFilter("MP4 文件 (*.mp4)")
      file_dialog.setViewMode(QFileDialog.Detail)
      if file_dialog.exec_():
         self.video_path = file_dialog.selectedFiles()[0]
         self.play_video()

   def play_video(self):
      vedioRead = self.video_path  # 读取视频文件的路径
      capRead = cv2.VideoCapture(vedioRead)  # 实例化 VideoCapture 类
      # 读取视频文件
      frameNum = 0  # 视频帧数初值
      while capRead.isOpened():  # 检查视频捕获是否成功
         ret, frame = capRead.read()  # 读取下一帧视频图像
         if ret is True:
            cv2.imshow(vedioRead, frame)  # 播放视频图像
            if cv2.waitKey(1) & 0xFF == ord('q'):  # 按 'q' 退出
               break
         else:
            print("Can't receive frame at frameNum {}".format(frameNum))
            break

   def update_frame(self):
      ret, frame = self.video_capture.read()
      if ret:
         height, width, channel = frame.shape
         bytes_per_line = 3 * width
         q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
         pixmap = QPixmap.fromImage(q_image)
         self.label.setPixmap(pixmap)
      else:
         self.timer.stop()
         self.video_capture.release()


if  __name__ == "__main__":        ##用于当前窗体测试
   app = QApplication(sys.argv)    #创建GUI应用程序
   form=QmyWidget()                #创建窗体
   form.show()
   sys.exit(app.exec_())
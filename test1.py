import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDateTime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import numpy as np
from pandas import Series, DataFrame

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.Sea_Feature_TempList = ['data/Sea_Feature_Temp_2009_a.csv','data/Sea_Feature_Temp_2009_b.csv','data/Sea_Feature_Temp_2010_a.csv','data/Sea_Feature_Temp_2010_b.csv',
                         'data/Sea_Feature_Temp_2011_a.csv','data/Sea_Feature_Temp_2011_b.csv','data/Sea_Feature_Temp_2012_a.csv','data/Sea_Feature_Temp_2012_b.csv',
                         'data/Sea_Feature_Temp_2013_a.csv','data/Sea_Feature_Temp_2013_b.csv','data/Sea_Feature_Temp_2014_a.csv','data/Sea_Feature_Temp_2014_b.csv',
                         'data/Sea_Feature_Temp_2015_a.csv','data/Sea_Feature_Temp_2015_b.csv','data/Sea_Feature_Temp_2016_a.csv','data/Sea_Feature_Temp_2016_b.csv',
                         'data/Sea_Feature_Temp_2017_a.csv','data/Sea_Feature_Temp_2017_b.csv','data/Sea_Feature_Temp_2018_a.csv','data/Sea_Feature_Temp_2018_b.csv',
                         'data/Sea_Feature_Temp_2019_a.csv','data/Sea_Feature_Temp_2019_b.csv','data/Sea_Feature_Temp_2020_a.csv','data/Sea_Feature_Temp_2020_b.csv',]
        self.Sea_TempList = ['data/Sea_Temp1.csv','data/Sea_Temp2.csv','data/Sea_Temp3.csv','data/Sea_Temp4.csv','data/Sea_Temp5.csv','data/Sea_Temp6.csv',
                             'data/Sea_Temp7.csv','data/Sea_Temp8.csv','data/Sea_Temp9.csv','data/Sea_Temp10.csv','data/Sea_Temp11.csv','data/Sea_Temp12.csv',]
        self.pointCsvList = ['output/955.csv','output/956.csv','output/957.csv','output/958.csv','output/959.csv','output/960.csv','output/961.csv','output/962.csv',
                             'output/963.csv','output/21229.csv','output/22101.csv','output/22102.csv','output/22103.csv','output/22104.csv','output/22105.csv','output/22106.csv',
                             'output/22107.csv','output/22108.csv','output/22183.csv','output/22184.csv','output/22185.csv','output/22186.csv','output/22187.csv','output/22188.csv',
                             'output/22189.csv','output/22190.csv','output/22191.csv','output/22192.csv','output/22193.csv','output/22194.csv','output/22297.csv','output/22298.csv',
                             'output/22441.csv','output/22442.csv','output/22443.csv','output/22444.csv','output/22445.csv','output/22446.csv','output/22447.csv','output/22448.csv',
                             'output/22449.csv','output/22450.csv','output/22451.csv','output/22452.csv','output/22453.csv','output/22454.csv','output/22455.csv','output/22456.csv',
                             'output/22457.csv','output/22458.csv','output/22459.csv','output/22460.csv','output/22461.csv','output/22462.csv','output/22464.csv',
                             'output/22465.csv','output/22466.csv','output/22467.csv','output/22468.csv','output/22469.csv','output/22470.csv','output/22471.csv','output/22472.csv',
                             'output/22473.csv','output/22474.csv','output/22475.csv','output/22476.csv','output/22477.csv','output/22478.csv','output/22479.csv','output/22483.csv',
                             'output/22484.csv','output/22485.csv','output/22486.csv','output/22487.csv','output/22489.csv','output/22490.csv','output/22491.csv','output/22492.csv',
                             'output/22493.csv','output/22494.csv','output/22495.csv','output/22496.csv','output/22497.csv','output/22498.csv','output/22499.csv','output/22500.csv',
                             'output/22501.csv','output/22502.csv','output/22503.csv','output/22504.csv','output/22505.csv','output/22507.csv','output/22509.csv',
                             'output/22601.csv','output/22602.csv',]

        self.setupUI()

    def setupUI(self):
        self.setGeometry(600, 200, 1200, 600) #윈도우의 크기와 출력 위치
        self.nullMarkerSize = 5

        self.drawChartpushButton = QPushButton("차트그리기")
        self.drawChartpushButton.clicked.connect(self.drawChartpushButtonClicked)

        self.selectedData = self.Sea_Feature_TempList[0] #맨 처음 데이터를 기본값으로
        self.df = pd.read_csv(fr'{self.selectedData}', encoding='cp949')
        self.df["일시"] = pd.to_datetime(self.df["일시"]) #일시를 DateTime형으로 바꾸기
        it = self.df["지점"].unique() #지점 종류 뽑아내기

        #지점에 따른 수온 렌더링을 위한 ComboBox
        self.tempByPointComboBox = QComboBox(self)
        self.pointListFortempByPointComboBox = []
        for i in self.pointCsvList:
            subpointCsv = pd.read_csv(fr'{i}', encoding='cp949')
            self.pointListFortempByPointComboBox.append(subpointCsv["지점"][0])
            self.tempByPointComboBox.addItem(str(subpointCsv["지점"][0]))
        self.tempByPointComboBox.move(50, 50)



        #지점에 대한 ComboBox
        self.pointComboBox = QComboBox(self)
        for i in it:
            self.pointComboBox.addItem(str(i))
        self.pointComboBox.move(50, 50)
        self.selectedPoint = self.pointComboBox.currentText() # 현재 지점

        #데이터에 대한 ComboBox
        self.dataComboBox = QComboBox(self)
        for i in self.Sea_Feature_TempList:
            self.dataComboBox.addItem(i)
        for i in self.Sea_TempList:
            self.dataComboBox.addItem(i)
        self.dataComboBox.move(50,50)

        iniPoint = it[0]
        self.dfTmp = self.df[self.df["지점"] == int(self.selectedPoint)]
        self.dfTmp = self.dfTmp["일시"]

        self.selectedFirstDateTime = QDateTimeEdit(self)
        self.selectedFirstDateTime.setDateTime(self.dfTmp.iloc[0])
        self.selectedFirstDateTime.setDisplayFormat('yyyy.MM.dd hh:00')

        self.selectedLastDateTime = QDateTimeEdit(self)
        self.selectedLastDateTime.setDateTime(self.dfTmp.iloc[-1])
        self.selectedLastDateTime.setDisplayFormat('yyyy.MM.dd hh:00')

        self.selectedFirstDateTime.dateTimeChanged.connect(self.changeFirstDateTime)


        ## RadioButton
        self.radioGraphType1 = QRadioButton("Line", self) # type 0
        self.radioGraphType1.move(50, 80)
        self.radioGraphType1.setChecked(True)
        self.radioGraphType1.clicked.connect(self.radioGraphTypeSelected)

        self.radioGraphType2 = QRadioButton("Point", self) # type 1
        self.radioGraphType2.move(50, 100)
        self.radioGraphType2.clicked.connect(self.radioGraphTypeSelected)

        self.selectedGraphType = 0 # 기본은 Line

        self.fig = plt.Figure() #그래프의 크기
        self.canvas = FigureCanvas(self.fig)

        self.labelSelectedData = QLabel('Select Data', self)
        self.labelSelectPoint = QLabel('Select Point', self)
        self.labelSelectGraphType = QLabel('Select Graph Type', self)
        self.labelSelectStartDateTime = QLabel('Start DateTime', self)
        self.labelMinimumDatetime = QLabel("Minimum DateTime : " + str(self.dfTmp.iloc[0]))
        self.labelSelectLastDateTime = QLabel('Last DateTime', self)
        self.labelMaximumDatetime = QLabel("Maximum DateTime : " + str(self.dfTmp.iloc[-1]))
        self.labelTempByPoint = QLabel('Water temperature by year for the point', self)

        self.separatedLine = QLabel('----------------------------------------', self)

        leftLayout = QVBoxLayout() #위젯을 수직방향으로 나열함
        leftLayout.addWidget(self.canvas)

        # Right Layout
        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.labelSelectedData)
        rightLayout.addWidget(self.dataComboBox)
        rightLayout.addWidget(self.labelSelectPoint)
        rightLayout.addWidget(self.pointComboBox)
        rightLayout.addWidget(self.labelSelectGraphType)
        rightLayout.addWidget(self.radioGraphType1)
        rightLayout.addWidget(self.radioGraphType2)

        rightLayout.addWidget(self.labelSelectStartDateTime)
        rightLayout.addWidget(self.labelMinimumDatetime)
        rightLayout.addWidget(self.selectedFirstDateTime)
        rightLayout.addWidget(self.labelSelectLastDateTime)
        rightLayout.addWidget(self.labelMaximumDatetime)
        rightLayout.addWidget(self.selectedLastDateTime)

        rightLayout.addWidget(self.drawChartpushButton)
        rightLayout.addWidget(self.separatedLine)
        rightLayout.addWidget(self.labelTempByPoint)
        rightLayout.addWidget(self.tempByPointComboBox)
        rightLayout.addStretch(1)

        self.pointComboBox.activated[str].connect(self.pointComboBoxSelected)
        self.dataComboBox.activated[str].connect(self.dataComboBoxSelected)
        self.tempByPointComboBox.activated[str].connect(self.tempByPointComboBoxSelected)

        layout = QHBoxLayout()
        layout.addLayout(leftLayout)
        layout.addLayout(rightLayout)
        layout.setStretchFactor(leftLayout, 1)
        layout.setStretchFactor(rightLayout, 0)

        self.setLayout(layout)

    def drawChartpushButtonClicked(self):
        # fileName = QFileDialog.getOpenFileName(self, self.tr("Open Data files"), "./", self.tr(
        #     "Data Files (*.csv);;"))
        self.fig.clf()
        self.df = self.df[(self.df["지점"] == int(self.selectedPoint))]
        self.ax = self.fig.add_subplot(111)
        tmp = self.df[['일시', '수온(°C)']]
        tmp = self.df[tmp.isnull().any(axis=1)]
        tmp = tmp.fillna(0)
        self.ax.set_ylabel('Water temperature')
        self.ax.set_xlabel('time')

        if(self.selectedGraphType == 0):
            self.ax.plot(self.df['일시'], self.df['수온(°C)'])
            self.ax.legend(loc='best')
            self.ax.grid()

            self.canvas.draw()
        elif(self.selectedGraphType == 1):
            # self.ax = self.fig.add_axes([0, 0, 1, 1]) #axes를 추가하는거지만 왠지 모르겠는데 plot 전체에 대한 사이즈가 바뀜 아마 axes의 크기가 기존보다 커져서 plot도 같이 커진게 아닐까
            self.ax.scatter(self.df['일시'], self.df['수온(°C)'], s=1)
            self.ax.scatter(tmp['일시'], tmp['수온(°C)'], s=self.nullMarkerSize)
            self.ax.legend(loc='best')
            self.ax.grid()

            self.canvas.draw()


    def pointComboBoxSelected(self, text):
        # file = 'Sea_Feature_Temp_2009_b.csv'
        # df = pd.read_csv(rf'C:\Users\psh01\PycharmProjects\pythonProject2\{file}', encoding='cp949')
        self.selectedPoint = text
        df = self.df[(self.df["지점"] == int(text))]

        self.dfTmp = self.df[self.df["지점"] == int(self.selectedPoint)]
        self.dfTmp = self.dfTmp["일시"]
        # self.selectedFirstDateTime.setDateTime(self.dfTmp.iloc[0])
        # self.selectedLastDateTime.setDateTime(self.dfTmp.iloc[-1])

        self.fig.clf()

        self.ax = self.fig.add_subplot(111)
        tmp = df[['일시', '수온(°C)']]
        tmp = df[tmp.isnull().any(axis=1)]
        tmp = tmp.fillna(0) #수온만 null인게 아니라 아예 일시 자체가 없어서 null이 되는 경우도 있다
        self.ax.set_ylabel('Water temperature')
        self.ax.set_xlabel('time')

        if (self.selectedGraphType == 0):

            self.ax.plot(df['일시'], df['수온(°C)'])
            self.ax.legend(loc='best')
            self.ax.grid()

            self.canvas.draw()
        elif (self.selectedGraphType == 1):
            # self.ax = self.fig.add_axes([0, 0, 1, 1]) #axes를 추가하는거지만 왠지 모르겠는데 plot 전체에 대한 사이즈가 바뀜 아마 axes의 크기가 기존보다 커져서 plot도 같이 커진게 아닐까
            self.ax.scatter(df['일시'], df['수온(°C)'], s=1)
            self.ax.scatter(tmp['일시'], tmp['수온(°C)'], s=self.nullMarkerSize)
            self.ax.legend(loc='best')
            self.ax.grid()

            self.canvas.draw()

    def dataComboBoxSelected(self,text):
        self.selectedData = text
        self.df = pd.read_csv(fr'{self.selectedData}', encoding='cp949')
        self.df["일시"] = pd.to_datetime(self.df["일시"])
        it = self.df["지점"].unique()

        #지점에 대한 ComboBox 갱신
        self.pointComboBox.clear()
        for i in it:
            self.pointComboBox.addItem(str(i))
        self.selectedPoint = self.pointComboBox.currentText() # 현재 지점

        self.selectedGraphType = 0
        self.radioGraphType1.setChecked(True)

        self.dfTmp = self.df[self.df["지점"] == int(self.selectedPoint)]
        self.dfTmp = self.dfTmp["일시"]
        self.selectedFirstDateTime.setDateTime(self.dfTmp.iloc[0])
        self.selectedLastDateTime.setDateTime(self.dfTmp.iloc[-1])

    def tempByPointComboBoxSelected(self, text):
        self.fig.clf()
        point = self.pointListFortempByPointComboBox.index(int(text))

        df = pd.read_csv(fr'{self.pointCsvList[point]}', encoding='cp949')
        df['일시'] = pd.to_datetime(df['일시'])

        tmp = df[['일시', '수온(°C)']]
        tmp = df[tmp.isnull().any(axis=1)]
        tmp = tmp.fillna(0)

        self.ax = self.fig.add_subplot(111)

        self.ax.set_ylabel('Water temperature')
        self.ax.set_xlabel('time')

        self.ax.scatter(df['일시'], df['수온(°C)'], s=1)
        self.ax.scatter(tmp['일시'], tmp['수온(°C)'], s=self.nullMarkerSize)
        self.ax.legend(loc='best')
        self.ax.grid()

        self.canvas.draw()






    def radioGraphTypeSelected(self):
        df = self.df[(self.df["지점"] == int(self.selectedPoint))]
        self.fig.clf()
        self.ax = self.fig.add_subplot(111)
        tmp = df[['일시', '수온(°C)']]
        tmp = df[tmp.isnull().any(axis=1)]
        tmp = tmp.fillna(0)
        self.ax.set_ylabel('Water temperature')
        self.ax.set_xlabel('time')

        if(self.radioGraphType1.isChecked()):
            self.selectedGraphType = 0

            self.ax.plot(df['일시'], df['수온(°C)'])
            self.ax.legend(loc='best')
            self.ax.grid()


            self.canvas.draw()

        elif(self.radioGraphType2.isChecked()):
            self.selectedGraphType = 1

            # self.ax = self.fig.add_axes([0, 0, 1, 1]) #axes를 추가하는거지만 왠지 모르겠는데 plot 전체에 대한 사이즈가 바뀜 아마 axes의 크기가 기존보다 커져서 plot도 같이 커진게 아닐까
            self.ax.scatter(df['일시'], df['수온(°C)'], s=1)
            self.ax.scatter(tmp['일시'], tmp['수온(°C)'], s=self.nullMarkerSize)
            self.ax.legend(loc='best')
            self.ax.grid()

            self.canvas.draw()

    def generatePointData_dataComboBoxSelected(self,text):
        self.selectedData = text
        self.df = pd.read_csv(fr'{self.selectedData}', encoding='cp949')
        self.df["일시"] = pd.to_datetime(self.df["일시"])
        it = self.df["지점"].unique()

        #지점에 대한 ComboBox 갱신
        self.pointComboBox.clear()
        for i in it:
            self.pointComboBox.addItem(str(i))
            self.dfTmp = self.df[self.df["지점"] == int(i)]
            if(int(i) in self.pointList):
                subDf = pd.read_csv(fr'output\{i}.csv', encoding='cp949')
                subDf = pd.concat([subDf,self.dfTmp])
                subDf.to_csv(fr'output\{i}.csv', index= False, encoding='cp949')
            else:
                self.pointList.append(int(i))
                self.dfTmp.to_csv(fr'output\{i}.csv', index= False, encoding='cp949')

        self.selectedPoint = self.pointComboBox.currentText() # 현재 지점

        self.selectedGraphType = 0
        self.radioGraphType1.setChecked(True)

        self.dfTmp = self.df[self.df["지점"] == int(self.selectedPoint)]
        self.dfTmp = self.dfTmp["일시"]
        self.selectedFirstDateTime.setDateTime(self.dfTmp.iloc[0])
        self.selectedLastDateTime.setDateTime(self.dfTmp.iloc[-1])



    def changeFirstDateTime(self):
        # self.fig.clf()
        #
        # self.dfTmp = self.df[self.df["지점"] == int(self.selectedPoint)]
        # self.df["일시"] = pd.to_datetime(self.df["일시"])
        # print(type(self.df["일시"])) #
        # print(type(self.selectedFirstDateTime.dateTime().toPyDateTime()))
        # print(type(self.selectedFirstDateTime.dateTime()))
        # print(type(self.selectedLastDateTime))
        # tmp1 = np.datetime64(self.selectedFirstDateTime.dateTime().toPyDateTime())
        # tmp2 = np.datetime64(self.selectedLastDateTime.dateTime().toPyDateTime())
        # t = self.df["일시"]
        # print(type(t[0]))
        print(self.dfTmp)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
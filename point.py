import numpy as np
import pylab as pl
from numpy import fft
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from sklearn.metrics import mean_squared_error, mean_absolute_error


def fourierExtrapolation(x, n_predict, h):
    n = x.size
    n_harm = h  # number of harmonics in model
    t = np.arange(0, n)
    p = np.polyfit(t, x, 1)  # find linear trend in x
    x_notrend = x - p[0] * t  # detrended x
    x_freqdom = fft.fft(x_notrend)  # detrended x in frequency domain
    f = fft.fftfreq(n)  # frequencies
    indexes = list(range(n))
    # sort indexes by frequency, lower -> higher
    # indexes.sort(key=lambda i: np.absolute(f[i]))
    indexes.sort(key=lambda i: np.absolute(x_freqdom[i]))
    indexes.reverse()

    t = np.arange(0, n + n_predict)
    restored_sig = np.zeros(t.size)
    for i in indexes[:1 + n_harm * 2]:
        ampli = np.absolute(x_freqdom[i]) / n  # amplitude
        phase = np.angle(x_freqdom[i])  # phase
        restored_sig += ampli * np.cos(2 * np.pi * f[i] * t + phase)
    return restored_sig + p[0] * t


def main():
    Sea_Feature_TempList = ['data/Sea_Feature_Temp_2009_a.csv', 'data/Sea_Feature_Temp_2009_b.csv',
                                 'data/Sea_Feature_Temp_2010_a.csv', 'data/Sea_Feature_Temp_2010_b.csv',
                                 'data/Sea_Feature_Temp_2011_a.csv', 'data/Sea_Feature_Temp_2011_b.csv',
                                 'data/Sea_Feature_Temp_2012_a.csv', 'data/Sea_Feature_Temp_2012_b.csv',
                                 'data/Sea_Feature_Temp_2013_a.csv', 'data/Sea_Feature_Temp_2013_b.csv',
                                 'data/Sea_Feature_Temp_2014_a.csv', 'data/Sea_Feature_Temp_2014_b.csv',
                                 'data/Sea_Feature_Temp_2015_a.csv', 'data/Sea_Feature_Temp_2015_b.csv',
                                 'data/Sea_Feature_Temp_2016_a.csv', 'data/Sea_Feature_Temp_2016_b.csv',
                                 'data/Sea_Feature_Temp_2017_a.csv', 'data/Sea_Feature_Temp_2017_b.csv',
                                 'data/Sea_Feature_Temp_2018_a.csv', 'data/Sea_Feature_Temp_2018_b.csv',
                                 'data/Sea_Feature_Temp_2019_a.csv', 'data/Sea_Feature_Temp_2019_b.csv',
                                 'data/Sea_Feature_Temp_2020_a.csv', 'data/Sea_Feature_Temp_2020_b.csv', ]
    Sea_TempList = ['data/Sea_Temp1.csv', 'data/Sea_Temp2.csv', 'data/Sea_Temp3.csv', 'data/Sea_Temp4.csv',
                         'data/Sea_Temp5.csv', 'data/Sea_Temp6.csv',
                         'data/Sea_Temp7.csv', 'data/Sea_Temp8.csv', 'data/Sea_Temp9.csv', 'data/Sea_Temp10.csv',
                         'data/Sea_Temp11.csv', 'data/Sea_Temp12.csv', ]
    pointCsvList = ['output/955.csv', 'outputput/957.csv', 'output/956.csv', 'out/958.csv', 'output/959.csv',
                         'output/960.csv', 'output/961.csv', 'output/962.csv',
                         'output/963.csv', 'output/21229.csv', 'output/22101.csv', 'output/22102.csv',
                         'output/22103.csv', 'output/22104.csv', 'output/22105.csv', 'output/22106.csv',
                         'output/22107.csv', 'output/22108.csv', 'output/22183.csv', 'output/22184.csv',
                         'output/22185.csv', 'output/22186.csv', 'output/22187.csv', 'output/22188.csv',
                         'output/22189.csv', 'output/22190.csv', 'output/22191.csv', 'output/22192.csv',
                         'output/22193.csv', 'output/22194.csv', 'output/22297.csv', 'output/22298.csv',
                         'output/22441.csv', 'output/22442.csv', 'output/22443.csv', 'output/22444.csv',
                         'output/22445.csv', 'output/22446.csv', 'output/22447.csv', 'output/22448.csv',
                         'output/22449.csv', 'output/22450.csv', 'output/22451.csv', 'output/22452.csv',
                         'output/22453.csv', 'output/22454.csv', 'output/22455.csv', 'output/22456.csv',
                         'output/22457.csv', 'output/22458.csv', 'output/22459.csv', 'output/22460.csv',
                         'output/22461.csv', 'output/22462.csv', 'output/22464.csv',
                         'output/22465.csv', 'output/22466.csv', 'output/22467.csv', 'output/22468.csv',
                         'output/22469.csv', 'output/22470.csv', 'output/22471.csv', 'output/22472.csv',
                         'output/22473.csv', 'output/22474.csv', 'output/22475.csv', 'output/22476.csv',
                         'output/22477.csv', 'output/22478.csv', 'output/22479.csv', 'output/22483.csv',
                         'output/22484.csv', 'output/22485.csv', 'output/22486.csv', 'output/22487.csv',
                         'output/22489.csv', 'output/22490.csv', 'output/22491.csv', 'output/22492.csv',
                         'output/22493.csv', 'output/22494.csv', 'output/22495.csv', 'output/22496.csv',
                         'output/22497.csv', 'output/22498.csv', 'output/22499.csv', 'output/22500.csv',
                         'output/22501.csv', 'output/22502.csv', 'output/22503.csv', 'output/22504.csv',
                         'output/22505.csv', 'output/22507.csv', 'output/22509.csv',
                         'output/22601.csv', 'output/22602.csv', ]

    selectedData = Sea_Feature_TempList[0]  # 맨 처음 데이터를 기본값으로
    df = pd.read_csv(fr'{selectedData}', encoding='cp949')
    # df = df[(df["지점"] == 22101)]
    x = df[["수온(°C)", "기온(°C)"]]
    x = x[np.logical_not(np.isnan(x))]
    df["일시"] = pd.to_datetime(df["일시"])

    df = df[(df["지점"] == 22205)]
    tmp = df[['수온(°C)']]
    tmp = df[tmp.isnull().any(axis=1)]
    tmp = tmp.fillna(0)
    n_predict = 0
    h = 700
    extrapolation = fourierExtrapolation(x, n_predict, h)
    pl.plot(np.arange(0, x.size), x, 'b', label='x', linewidth=1)
    start = 20000
    end = 40000
    # pl.plot(np.arange(0, start), x[:start], 'b',  linewidth=1)
    # pl.plot(np.arange(end, x.size), x[end:], 'b', label='x', linewidth=1)
    # print("mse : "+str(mean_squared_error(x[start:end], extrapolation[start:end])))
    # print("rmse : " + str(np.sqrt(mean_squared_error(x[start:end], extrapolation[start:end]))))
    # print("mae : "+str(mean_absolute_error(x[start:end], extrapolation[start:end])))

    # pl.plot(np.arange(0, extrapolation.size), extrapolation, 'r', label='Prediction', linewidth=1.5)
    print("mse : " + str(mean_squared_error(x, extrapolation)))
    print("rmse : " + str(np.sqrt(mean_squared_error(x, extrapolation))))
    print("mae : " + str(mean_absolute_error(x, extrapolation)))
    pl.legend()
    pl.show()


if __name__ == "__main__":
    main()
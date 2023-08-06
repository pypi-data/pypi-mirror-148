import random
import sys
import time
from datetime import datetime, timedelta

from gregory.dataclass.time_series_data import TimeSeriesData
from gregory.granularity.granularity import WeeklyGranularity, DailyGranularity, MonthlyGranularity, QuarterlyGranularity
from gregory.timeseries.batches import batches, aggregate_on_first_day, pick_a_weekday, pick_a_day
from gregory.timeseries.inference import infer_ts_granularity
from gregory.timeseries.processing import add_trend_seasonality
from gregory.timeseries.time_series import TimeSeries
from dateutil.rrule import DAILY, rrule, MO, TU, WE, TH, FR, SA, SU

from gregory.util.relativedelta import relativedelta

if __name__ == '__main__':

    # un = datetime.today().date() + relativedelta(days=7)
    # day_times = rrule(
    #     freq=DAILY,
    #     dtstart=datetime.today().date(),
    #     until=un,  # + relativedelta(days=int(inclusive)),
    #     byweekday=TU
    # )

    # print([day_time.date() for day_time in day_times])
    # sys.exit()

    # GENERATE INPUT
    start_date = '2020-01-01'
    data = {}
    z = []
    i = 0
    for x in range(365*2):
        i += 1
        if i % 2 > 0:
            data = {'real': random.randint(200, 300), 'pippo': 2}
        else:
            data = {}
        day = TimeSeriesData(day=datetime.strptime(start_date, "%Y-%m-%d").date() + timedelta(days=x), series=data)
        z.append(day)

    tsl = TimeSeries(z)

    # rs = pick_a_day(tsl, granularity=MonthlyGranularity(), day_of_batch=-1)
    # print(rs)

    # rs = pick_a_weekday(tsl, granularity=MonthlyGranularity(), weekday=2, day_of_batch=-1)
    # print(rs)

    # rs = batches(tsl, granularity=MonthlyGranularity(), n_elements=-1)
    # for x in rs:
    #     print(x[-1])

    rs = tsl.resample(
        granularity=QuarterlyGranularity(),
        index_of_granularity=-1
    )
    # print(rs)

    print(infer_ts_granularity(rs))
    sys.exit()
    # print(tsl)
    # tsl.delete(datetime.strptime('1000-01-01', "%Y-%m-%d").date())
    # print(tsl)
    # print(tsl.dates)
    #
    # tsl.append(TimeSeriesData(day=datetime.strptime('2000-01-01', "%Y-%m-%d").date(), series=data))
    # print(tsl)
    # # tsl.resample(granularity=QuarterlyGranularity(), inplace=True)
    # # print(fil[:20])
    # print(tsl.dates)
    # sys.exit()

    # tsl.append(day)

    # x = [v for v in tsl[:3]]
    #
    #
    # min_date = datetime.strptime(start_date, "%Y-%m-%d").date() + timedelta(days=len(fil)-50)
    # max_date = datetime.strptime(start_date, "%Y-%m-%d").date() + timedelta(days=len(fil)-1)
    # print(min_date, max_date)
    # min_date_unix = time.mktime(min_date.timetuple())
    # max_date_unix = time.mktime(max_date.timetuple())
    #
    # t1 = time.time()
    # [x for x in filter(lambda element: max_date >= element.day >= min_date, fil)]
    # tempo1 = time.time() - t1
    #
    # z = fil.__indexes__.keys()
    # t2 = time.time()
    # ooo = next(filter(lambda x: x>=min_date.strftime("%Y-%m-%d"), z))
    # t2_z = time.time()
    # print('primo indice', t2_z - t2)
    # idx_1 = fil.__indexes__[ooo]
    # t2_a = time.time()
    # print('primo indice', t2_a - t2_z)
    # # t2_a = time.time()
    # idx_2 = fil.__indexes__[max_date.strftime("%Y-%m-%d")]
    # # t2_b = time.time()
    # # print('secondo indice', t2_b - t2_a)
    # fil[idx_1:idx_2]
    # # print('selezione', time.time() - t2_b)
    # tempo2 = time.time() - t2
    #
    # print('tempo 1', tempo1)
    # print('tempo 2', tempo2)
    # print(tempo2 > tempo1)

    # fil.__indexes__
    # dates = fil.dates
    #
    # # del fil.dates
    #
    # t1 = time.time()
    # fil.get(min_date)
    # print(time.time() - t1)
    #
    # t2 = time.time()
    # # i = index_of(dates, min_date)
    # # fil[i]
    # fil.get(min_date)
    # print(time.time() - t2)
    # t2 = time.time()
    # # i = index_of(dates, min_date)
    # # fil[i]
    # fil.get(min_date)
    # print(time.time() - t2)
    # t2 = time.time()
    # # i = index_of(dates, min_date)
    # # fil[i]
    # fil.get(min_date)
    # print(time.time() - t2)

    #
    # print('cccccccccccc', len(tsl))
    # t1 = time.time()

    # tsl.cut(min_date, max_date, inplace=True)

    # t2 = time.time()
    # print('v2', t2-t1)
    #
    # v2 = tsl.cut_old(min_date, max_date)
    # t3 = time.time()
    #
    # print('v1', t3-t2)

    # fil.interpolate('real', inplace=True)
    #
    # print(fil[:20])
    #
    # t1 = time.time()
    # x = batches(fil, granularity=MonthlyGranularity(), first_day_of_batch=4, delta=10)
    # print('batches', time.time() - t1)
    # print(x[0])
    # print(x[1])
    # print(x[-1])
    #
    # t1 = time.time()
    # y = aggregate_on_first_day(fil, granularity=MonthlyGranularity())
    # print('aggregate', time.time() - t1)
    # print(y[:10])
    #
    # t1 = time.time()
    # z = first_days(fil, granularity=MonthlyGranularity())
    # print('aggregate', time.time() - t1)
    # print(z[:10])

    # #
    # # splits = tsl.batches(output_granularity=WeeklyGranularity())
    # # print(splits[:10])
    # #
    # # print(tsl.batches_first_days(output_granularity=WeeklyGranularity()))
    #
    # tsx = TimeSeriesData(day=datetime.strptime('2021-01-01', "%Y-%m-%d"), series={'a': 2})
    # tsd = TimeSeriesData(day=datetime.strptime('2020-01-01', "%Y-%m-%d"), series={'a': 2, 'b': 3})
    # xxx = TimeSeriesData(day=datetime.strptime('2019-01-01', "%Y-%m-%d"), series={'a': 2, 'd': 4})
    # xxy = TimeSeriesData(day=datetime.strptime('2018-01-01', "%Y-%m-%d"), series={'c': 2, 'b': 3})
    #
    # tsx = [datetime.strptime('2021-01-01', "%Y-%m-%d"), 4, 'ccccc']
    # tsd = [datetime.strptime('2020-01-01', "%Y-%m-%d"), 4, 'ccccc']
    # xxx = [datetime.strptime('2019-01-01', "%Y-%m-%d"), 4, 'ccccc']
    # xxy = [datetime.strptime('2018-01-01', "%Y-%m-%d"), 4, 'ccccc']
    #
    # lll = [xxx, tsx, xxy, tsd]
    #
    # tsl.update_from_array(lll)

    # for x in tsl:
    #     print(x)


    # x = tsl.as_filtered_array('real')
    # print(x[:10])

    #
    # print(x)
    #
    # x.cut(datetime.strptime('2018-01-01', "%Y-%m-%d"), datetime.strptime('2020-02-03', "%Y-%m-%d"))
    #
    # print(x)
    #
    # print(x.as_array)
    #
    # x.append(TimeSeriesData(day=datetime.strptime('2019-06-01', "%Y-%m-%d"), series={'c': 2, 'b': 999}))
    #
    # print(x.__indexes__)
    #
    # print(x.get(day=datetime.strptime('2019-06-01', "%Y-%m-%d")))
    #
    #
    # y = TimeSeriesList([TimeSeriesData(day=datetime.strptime('2023-01-01', "%Y-%m-%d"), series={'h': 2, 'f': 56}), TimeSeriesData(day=datetime.strptime('2020-01-01', "%Y-%m-%d"), series={'z': 2, 'g': 999})])
    # print(intersection(x, y))
    # print('prima merge')
    # print(union(x, y))
    # print('prima union')
    #
    # y = TimeSeriesList([xxx, tsx, TimeSeriesData(day=datetime.strptime('2023-01-01', "%Y-%m-%d"), series={'a': 2, 'f': 56}), TimeSeriesData(day=datetime.strptime('2020-01-01', "%Y-%m-%d"), series={'a': 2, 'g': 999})])
    # print(union(x, y))
    # print('exc')


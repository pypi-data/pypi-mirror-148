import random
import sys
from datetime import datetime, timedelta

from outatime.dataclass.time_series_data import TimeSeriesData
from outatime.granularity.granularity import QuarterlyGranularity, DailyGranularity, MonthlyGranularity

from gregory.timeseries.batches import aggregate_on_first_day
from gregory.timeseries.time_series import TimeSeries

if __name__ == '__main__':

    # GENERATE INPUT
    start_date = '2020-01-09'
    data = {}
    z = []
    i = 0
    for x in range(30*2):
        i += 1
        if i % 2 > 0:
            data = {'real': random.randint(200, 300), 'pippo': 2}
        else:
            data = {}
        day = TimeSeriesData(day=datetime.strptime(start_date, "%Y-%m-%d").date() + timedelta(days=x), data=data)
        z.append(day)

    tsl = TimeSeries(z)

    print(tsl[0], tsl[-1])
    rs = tsl.resample(
        granularity=QuarterlyGranularity(),
        index_of_granularity=-1,
        default_data={}
    )
    print(rs)

    rs.resample(
        granularity=DailyGranularity(),
        index_of_granularity=-1,
        inplace=True,
        default_data={}
    )
    print(rs)

    rs = tsl.resample(
        granularity=MonthlyGranularity(),
        index_of_granularity=-1,
        default_data={}
    )
    print(rs)

    res = aggregate_on_first_day(
        ts=tsl,
        granularity=MonthlyGranularity(),
    )
    print(res)

    sys.exit()

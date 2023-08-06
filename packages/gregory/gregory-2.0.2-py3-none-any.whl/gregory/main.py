import random
import sys
from datetime import datetime, timedelta

from outatime.dataclass.time_series_data import TimeSeriesData
from outatime.granularity.granularity import QuarterlyGranularity, DailyGranularity, MonthlyGranularity

from gregory.timeseries.batches import aggregate, split
from gregory.timeseries.time_series import TimeSeries
from outatime.timeseries.time_series import TimeSeries as T

if __name__ == '__main__':

    # GENERATE INPUT
    start_date = '2020-01-09'
    data = {}
    z = []
    i = 0
    for x in range(365*1):
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

    res = aggregate(
        ts=tsl,
        granularity=MonthlyGranularity(),
    )
    print(res)

    res = split(
        ts=tsl,
        granularity=MonthlyGranularity(),
    )

    sys.exit()

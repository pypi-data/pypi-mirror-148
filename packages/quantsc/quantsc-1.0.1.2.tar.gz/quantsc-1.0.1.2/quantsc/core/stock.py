import numbers

import pandas as pd
import plotly.express as px
# http://theautomatic.net/yahoo_fin-documentation/
# http://theautomatic.net/yahoo_fin-documentation/#methods
import plotly.graph_objects as go
import yahoo_fin.stock_info as si
import yfinance as yf

import quantsc as qsc
import quantsc.config as config
from quantsc.core.timeseries import TimeSeries


class Stock(TimeSeries):
    def __init__(self, ticker=None,start=None,end=None,interval='1d', data=None,name=None):
        if not isinstance(ticker,str) and ticker is not None:
            data = ticker
            ticker = ''
        if data is not None:
            if name is not None:
                self.name = name
                self.ticker = None
            else:
                self.name = "Custom Stock"
            if isinstance(data,TimeSeries):
                self.data = TimeSeries.data
            else:
                super().load_data(data)
                self.dates = self.data.index
        else:
            if interval is not None:
                self.interval = self.is_valid_interval(interval)
            self.ticker = ticker
            self.name = ticker
            try:
                if None in(start,end):
                    stock_data = yf.download(ticker,interval=interval)
                else:
                    stock_data = yf.download(ticker,start=start,end=end,interval=interval)
            except Exception as e:
                print(str(e))
            series = pd.Series(data=stock_data['Open'],index=stock_data.index)
            super().__init__(series)
            self.open = stock_data['Open']
            self.close = stock_data['Close']
            self.low = stock_data['Low']
            self.high = stock_data['High']
            self.dates = stock_data.index
        self.indicators = dict()
        self.diff_count = 0


    def __add__(self, other):
        if isinstance(other, Stock):
            new_stock = Stock(self.data + other.data,name = f"({self.name}+{other.name})")
            try:
                new_stock.open = self.open + other.open
                new_stock.close = self.close + other.close
                new_stock.high = self.high + other.high
                new_stock.low = self.low + other.low
            finally:
                return new_stock.dropna()
        elif isinstance(other, TimeSeries):
            new_stock = Stock(self.data + other.data,name = f"({self.name}+Series)")
            try:
                new_stock.open = self.open + other.data
                new_stock.close = self.close + other.data
                new_stock.high = self.high + other.data
                new_stock.low = self.low + other.data
            finally:
                return new_stock.dropna()
        elif isinstance(other,numbers.Number):
            new_stock = Stock(self.data + other.data, name = f"{self.name}+{str(other)}")
            try:
                new_stock.high = self.high + other
                new_stock.low = self.low + other
                new_stock.open = self.open + other
                new_stock.close = self.close + other
            finally:
                return new_stock.dropna()

        else:
            raise Exception("Add operation only supported for TimeSeries, Stock, int, and float.")

    def __sub__(self, other):
        if isinstance(other, Stock):
            new_stock = Stock(self.data - other.data, name=f"({self.name}-{other.name})")
            try:
                new_stock.open = self.open - other.open
                new_stock.close = self.close - other.close
                new_stock.high = self.high - other.high
                new_stock.low = self.low - other.low
            finally:
                return new_stock.dropna()
        elif isinstance(other, TimeSeries):
            new_stock = Stock(self.data - other.data, name=f"({self.name}-Series)")
            try:
                new_stock.open = self.open - other.data
                new_stock.close = self.close - other.data
                new_stock.high = self.high - other.data
                new_stock.low = self.low - other.data
            finally:
                return new_stock.dropna()
        elif isinstance(other, numbers.Number):
            new_stock = Stock(self.data - other.data, name=f"{self.name}-{str(other)}")
            try:
                new_stock.high = self.high - other
                new_stock.low = self.low - other
                new_stock.open = self.open - other
                new_stock.close = self.close - other
            finally:
                return new_stock.dropna()

        else:
            raise Exception("Subtraction operation only supported for TimeSeries, Stock, int, and float.")

    def __neg__(self):
        new_stock = Stock(self.data, name=f"-({self.name})")
        new_stock.open = -(self.open)
        new_stock.close = -(self.close)
        new_stock.high = -(self.high)
        new_stock.low = -(self.low)
        return new_stock.dropna()

    def __mul__(self, other):
        if isinstance(other, Stock):
            new_stock = Stock(self.data * other.data,name = f"({self.name}*{other.name})")
            try:
                new_stock.open = self.open * other.open
                new_stock.close = self.close * other.close
                new_stock.high = self.high * other.high
                new_stock.low = self.low * other.low
            finally:
                return new_stock.dropna()
        elif isinstance(other, TimeSeries):
            new_stock = Stock(self.data * other.data,name = f"({self.name}*Series)")
            try:
                new_stock.open = self.open * other.data
                new_stock.close = self.close * other.data
                new_stock.high = self.high * other.data
                new_stock.low = self.low * other.data
            finally:
                return new_stock.dropna()
        elif isinstance(other,numbers.Number):
            new_stock = Stock(self.data * other.data, name = f"{self.name}*{str(other)}")
            try:
                new_stock.high = self.high * other
                new_stock.low = self.low * other
                new_stock.open = self.open * other
                new_stock.close = self.close * other
            finally:
                return new_stock.dropna()

        else:
            raise Exception("Multiplication for Stock only supported for TimeSeries, Stock, int, and float.")

    def __truediv__(self, other):
        if isinstance(other, Stock):
            new_stock = Stock(self.data / other.data,name = f"({self.name}/{other.name})")
            try:
                new_stock.open = self.open / other.open
                new_stock.close = self.close / other.close
                new_stock.high = self.high / other.high
                new_stock.low = self.low / other.low
            finally:
                return new_stock.dropna()
        elif isinstance(other, TimeSeries):
            new_stock = Stock(self.data / other.data,name = f"({self.name}/Series)")
            try:
                new_stock.open = self.open / other.data
                new_stock.close = self.close / other.data
                new_stock.high = self.high / other.data
                new_stock.low = self.low / other.data
            finally:
                return new_stock.dropna()
        elif isinstance(other,numbers.Number):
            new_stock = Stock(self.data / other.data, name = f"{self.name}/{str(other)}")
            try:
                new_stock.high = self.high / other
                new_stock.low = self.low / other
                new_stock.open = self.open / other
                new_stock.close = self.close / other
            finally:
                return new_stock.dropna()

        else:
            raise Exception("Division for Stock only supported for TimeSeries, Stock, int, and float.")

    def __pow__(self, other):
        if isinstance(other, Stock):
            new_stock = Stock(self.data ** other.data,name = f"({self.name}^{other.name})")
            try:
                new_stock.open = self.open ** other.open
                new_stock.close = self.close ** other.close
                new_stock.high = self.high ** other.high
                new_stock.low = self.low ** other.low
            finally:
                return new_stock.dropna()
        elif isinstance(other, TimeSeries):
            new_stock = Stock(self.data ** other.data,name = f"({self.name}^Series)")
            try:
                new_stock.open = self.open ** other.data
                new_stock.close = self.close ** other.data
                new_stock.high = self.high ** other.data
                new_stock.low = self.low ** other.data
            finally:
                return new_stock.dropna()
        elif isinstance(other,numbers.Number):
            new_stock = Stock(self.data ** other.data, name = f"{self.name}^{str(other)}")
            try:
                new_stock.high = self.high ** other
                new_stock.low = self.low ** other
                new_stock.open = self.open ** other
                new_stock.close = self.close ** other
            finally:
                return new_stock.dropna()

        else:
            raise Exception("Division for Stock only supported for TimeSeries, Stock, int, and float.")

    def getIndicators(self):
        return self.indicators

    def is_valid_interval(self, period):
        valid_period = ['1m', '2m', '5m', '15m', '30m', '60m', '90m','1h','1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd','max']
        if period in valid_period:
            return period
        else:
            raise("Interval must be one of '1m','2m','5m','15m','30m','60m','90m','1h','1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd','max'!")
            return None

    def update_data(self, ticker, period = None):
        self.data = yf.download(ticker, period)
        self.indicators = dict()

    def len(self):
        return super().__len__()

    def to_csv(self):
        return self.data.to_csv(self.name+'.csv')

    def earnings(self):  # , earnings_date: datetime):
        earning_data = si.get_earnings_history(self.ticker)
        df_eps = pd.DataFrame.from_dict(earning_data)
        eps_data = pd.DataFrame(df_eps["epsactual"])
        eps_data.index = qsc.round_dates(df_eps["startdatetime"])
        self.indicators["earning"] = eps_data
        return self.indicators["earning"]

    def eps_expected(self):
        earning_data = si.get_earnings_history(self.ticker)
        # print(qsc.round_dates(list(earning_data.index())))
        # earning_data.index = pd.Series(earning_data.index).dt.round('D').values
        df_eps = pd.DataFrame.from_dict(earning_data)
        # df_eps.index = pd.Series(df_eps.index).dt.round('D').values
        eps_data = df_eps["epsestimate"]
        eps_index = qsc.round_dates(df_eps["startdatetime"])
        eps_data.index = eps_index
        self.indicators["epsestimate"] = eps_data
        return self.indicators["epsestimate"]

    def eps(self):
        return self.earnings()

    def eps_suprise(self):
        earning_data = si.get_earnings_history(self.ticker)
        df_eps = pd.DataFrame.from_dict(earning_data)
        eps_data = df_eps["epssurprisepct"]
        eps_data.index = qsc.round_dates(df_eps["startdatetime"])
        self.indicators["epssurprisepct"] = eps_data
        return self.indicators["epssurprisepct"]

    def balance_sheet(self, yearly = True):
        self.indicators["balance_sheet"] = (si.get_balance_sheet(self.ticker, yearly) // 100).T
        return self.indicators["balance_sheet"]

    def cash_flow(self, yearly = True):
        self.indicators["cash_flow"] = (si.get_cash_flow(self.ticker, yearly) // 100).T
        return self.indicators["cash_flow"]

    def income_statement(self, yearly = True):
        self.indicators["income_statement"] = si.get_income_statement(self.ticker, yearly) // 100
        return self.indicators["income_statement"]

    def next_earnings_date(self):
        return si.get_next_earnings_date(self.ticker)

    def dividends(self): # can have specified date for onwards
        return si.get_dividends(self.ticker)


    def plot(self,backend=None, style='candle', figsize=(8,6),ylabel='Price'):
        if backend is None:
            backend = config.config['plot_backend']
        if backend == "matplotlib":
            fig,ax = super().get_fig(figsize = figsize, title=self.name, xlabel='Date',ylabel=ylabel)
            ax.plot(self.data)
            fig.show()
        elif backend == "plotly":
            if style == "candle":
                fig = go.Figure(data=[go.Candlestick(x=self.dates,
                        open=self.open,
                        high=self.high,
                        low=self.low,
                        close=self.close)])
                fig.update_layout(title_text = self.name,xaxis_title = 'Date', yaxis_title=ylabel)
            elif style == "line":
                fig = px.line(self.data)
            else:
                raise("type can only be 'candle' or 'line'")
            fig.show()
        else:
            raise("Backend must be either 'plotly' or 'matplotlib!'")

    # def sort_values(self, column = "Open"):
        #df = pd.DataFrame()
        #self.data

    # ""
    # def pairwise_sort(self):

    # def sort_index(self):
    # """
    # Reminder: Sort all self.data(default to 'open') self.open,self.close,self.high,self.low
    # """

    def diff(self,shift=1,inplace=False):
        if inplace:
            self.data = self.data.diff(shift)
            if None not in (self.high,self.low,self.open,self.close):
                self.high = self.high.diff(shift)
                self.low = self.low.diff(shift)
                self.open = self.open.diff(shift)
                self.close = self.close.diff(shift)
                self.diff_count += shift
                self.name = f"{self.ticker}.diff({str(self.diff_count)})"
            return self
        else:
            new_data = self.data.diff(shift)
            new_stock = Stock(new_data)
            new_stock.high = self.high.diff(shift)
            new_stock.low = self.low.diff(shift)
            new_stock.open = self.open.diff(shift)
            new_stock.close = self.close.diff(shift)
            new_stock.diff_count = self.diff_count + shift
            new_stock.name = f"{self.ticker}.diff({str(new_stock.diff_count)})"
            new_stock.ticker = self.ticker
            return new_stock.dropna()

    def autocov(self,lag=1):
        return super().autocov(lag)

    def autocorr(self, lag=1, method='pearson'):
        return super().autocorr(lag)

    def autocov_plot(self, figsize = (8,6), legend=False, title='', backend=None):
        return super().autocov_plot(figsize=figsize, legend=legend,
                                    title=f"Auto Covariance plot for {self.name}",backend=backend)
    def autocorr_plot(self, figsize = (8,6), legend=False, title='', backend=None,method='pearson'):
        return super().autocorr_plot(figsize=figsize, legend=legend,
                                    title=f"Auto Correlation plot for {self.name}",backend=backend,method=method)
    def var(self):
        return super().variance()

    def dropna(self):
        self.data = self.data.dropna()
        try:
            self.open = self.open.dropna()
            self.close = self.close.dropna()
            self.high = self.high.dropna()
            self.low = self.low.dropna()
        finally:
            return self

    def arima(self, p, d, q, plotResiduals=True, getSummary=True):
        super().arima(p, d, q, plotResiduals=True, getSummary=True)


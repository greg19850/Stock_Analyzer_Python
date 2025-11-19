from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.timeseries import TimeSeries

def safe_float(value: str | None)-> float | None:
    """Convert string to float, return None if invalid."""
    if value is None or value == "" or value == "None":
        return None

    try:
        float_value = float(value)
        return float_value
    except ValueError:
        return None



def fetch_stock_data(symbol: str, api_key: str)-> dict:
    """
    Fetch stock data from Alpha Vantage.

    Returns a dict with: symbol, name, exchange, sector, industry,
                        current_price, market_cap, pe_ratio

    Raises: ValueError if symbol not found or API error
    """
    fd = FundamentalData(key=api_key, output_format='json')
    ts = TimeSeries(key=api_key, output_format='json')

    company_data, _ = fd.get_company_overview(symbol)

    if not company_data:
        raise ValueError(f"stock symbol '{symbol}' not found")

    quote_data, _ = ts.get_quote_endpoint(symbol)

    stock_data = {
        'symbol': company_data.get('Symbol'),
        'name': company_data.get('Name'),
        'exchange': company_data.get('Exchange'),
        'sector': company_data.get('Sector'),
        'industry': company_data.get('Industry'),
        'current_price':  safe_float(quote_data.get('05. price')),
        'market_cap': safe_float(company_data.get('MarketCapitalization')),
        'pe_ratio': safe_float(company_data.get('PERatio'))
    }

    return stock_data

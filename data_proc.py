import pandas as pd
import re

from fake_data import get_data

desc_dict = {
    '0': 'success',
    '22': 'proxy_error',
    '25': 'unknown_error',
    '41': 'exception',
    '24': 'no_data',
    '36': 'incomplete',
    '27': 'parse_error',
    '23': 'blocked',
    '29': 'out_of_stock',
    '38': 'date_out_of_range',
    '99': 'unsupported_route',
}


def proc():
    data = get_data()

    # load data into DataFrame
    df = pd.read_json(data, orient='index')
    df.fillna(0, inplace=True)
    df['total'] = df.sum(axis=1)

    # overall total
    sum_overall = {'src': 'overall', 'data': list(df.sum().values)}

    # infer type by name
    df['type'] = map(lambda x: re.findall(r'((Round)?[A-Z][a-z]*$)', x)[0][0], df.index)

    # subtotal by type
    gb = df.groupby('type').sum()
    gb.sort('total', ascending=False, inplace=True)
    sum_by_type = gb.to_dict(orient='split')
    sum_by_type = map(lambda i, d: {'src': i, 'data': d}, sum_by_type['index'], sum_by_type['data'])

    df.sort('total', ascending=False, inplace=True)
    type_list = df['type']
    df.drop('type', axis=1, inplace=True)
    detail = df.to_dict(orient='split')
    detail = map(lambda i, d, t: {'src': i, 'data': d, 'type': t},
                 detail['index'], detail['data'], type_list)

    return {"sum_overall": sum_overall, "sum_by_type": sum_by_type, "detail": detail,
            "error_desc_dict": desc_dict, "columns": map(str, list(df.columns))}


if __name__ == '__main__':
    print proc()
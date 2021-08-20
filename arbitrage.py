from bs4 import BeautifulSoup
import urllib.request
import pandas as pd

html  = urllib.request.urlopen('https://www.exchange-rates.org/MajorRates.aspx').read()
soup = BeautifulSoup(html, 'html.parser')
table = soup.table

# us_dollar = []
def get_table(html_table):
    matrix =[]
    countries = []
    for x, row in enumerate(html_table.find_all('tr')):
        if x == 0:
            columns = [countrie.get('title') for countrie in row.find_all('a')][::2]
        else:
            r = []
            for y, col in enumerate(row.find_all('td')):
                if y == 0:
                    countries.append(col.get_text())
                else:
                    r.append(float(col.get_text()))
                    # if y == 1:
                    #     us_dollar.append(float(col.get_text()))
            matrix.append(r)
    return pd.DataFrame(matrix, index=countries, columns=columns)

df = get_table(table)
df = df[df.index.isin(df.columns)]
df = df.reindex(sorted(df.columns), axis=1)
print(df)

d = dict(zip(range(8), df.columns))
# table = []
# for numerator in us_dollar:
#     table.append([round(numerator/denominator, 2) for denominator in us_dollar])
# df = pd.DataFrame(table, index=countries)
# print(df)

def get_exchanges(dataframe):
    df = dataframe.values
    options_ = []
    for num_row in range(len(df)):
        for num_col, value in enumerate(df[num_row]):
            for num_x1, x1 in enumerate(df[num_col]):
                for num_x2, x2 in enumerate(df[num_x1]):
                    for num_x3, x3 in enumerate(df[num_x2]):
                        for num_x4, x4 in enumerate(df[num_x3]):
                            options_.append([value*x1*x2*x3*x4*df[num_x4][num_row],  [num_row, num_col, num_x1, num_x2, num_x3, num_x4]])
    return options_

def get_best_option(options_):
    highest = 0
    list_of_best_options = []
    for option in options_:
        if option[0] > highest:
            highest = option[0]
            list_of_best_options = [option]
        elif option[0] == highest:
            list_of_best_options.append(option)
    return list_of_best_options

def print_arbitrage():
    for amount in get_best_option(get_exchanges(df)):
        amount[1].append(amount[1][0])
        print(str(amount[0]) + ": " +  ' \u2192 '.join(d[coin] for coin in amount[1]))

print_arbitrage()

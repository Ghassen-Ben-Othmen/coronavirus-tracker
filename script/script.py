import pandas
import concurrent.futures
import json
import os

CONFIRMED_CSV_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
DEATHS_CSV_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
RECOVERED_CSV_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'

# list of csv urls
URLS = [CONFIRMED_CSV_URL, DEATHS_CSV_URL, RECOVERED_CSV_URL]

# data
result_data = {
    'total': {}
}
data = []

def read_csv_data(url):
    return pandas.read_csv(url)

# populate recovered and deaths data in data array
def populate_data(df, key):
    for index, row in df.iterrows():
        date1 = df.iloc[:,(df.shape[1] - 1)].name
        date2 = df.iloc[:,(df.shape[1] - 2)].name
        date3 = df.iloc[:,(df.shape[1] - 3)].name
        data[index]['data'][date1][key] = row[row.shape[0] - 1]
        data[index]['data'][date2][key] = row[row.shape[0] - 2]
        data[index]['data'][date3][key] = row[row.shape[0] - 3]


with concurrent.futures.ThreadPoolExecutor() as executor:

    results = executor.map(read_csv_data, URLS)

    total_confirmed, total_deaths, total_recovered = 0, 0, 0

    confirmed_data = next(results)

    # get today (date) for total result of today
    today_key = confirmed_data.columns[len(confirmed_data.columns)-1]
    total_confirmed = confirmed_data[today_key].sum()

    for _, row in confirmed_data.iterrows():
        el = {}
        el['Province/State'] = row['Province/State'] if str(row['Province/State']) != "nan" else ''
        el['Country/Region'] = row['Country/Region']
        el['Lat'] = row['Lat']
        el['Long'] = row['Long']
        date1 = confirmed_data.columns[len(confirmed_data.columns)-1]
        date2 = confirmed_data.columns[len(confirmed_data.columns)-2]
        date3 = confirmed_data.columns[len(confirmed_data.columns)-3]

        el['data'] = {
            date1: {'confirmed': row[row.shape[0] - 1]},
            date2: {'confirmed': row[row.shape[0] - 2]},
            date3: {'confirmed': row[row.shape[0] - 3]}
        }

        data.append(el)

    deaths_data = next(results)
    total_deaths = deaths_data[today_key].sum()
    populate_data(deaths_data, 'deaths')

    recovered_data = next(results)
    total_recovered = recovered_data[today_key].sum()
    populate_data(recovered_data, 'recovered')


    
    result_data['total'][today_key] = {
        'confirmed': int(total_confirmed),
        'deaths': int(total_deaths),
        'recoveres': int(total_recovered)
    }

    result_data['stats'] = data

# write data to file
filename = os.path.join(os.getcwd(), 'data', 'data.json')
with open(filename, 'w') as f:
    json.dump(result_data, f, indent=2)








        




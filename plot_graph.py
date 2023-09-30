import pandas as pd
import matplotlib.pyplot as plt
import warnings
import matplotlib
warnings.simplefilter("ignore", UserWarning)
matplotlib.use('agg')
#import time

def plot_graph (results):
    dicio_results = []
    for result in results:
        date = str(result[1])+"-"+str(result[2])
        rpk = result[4]
        dicio_results.append({'date': date,'rpk': rpk})
    
    df_results = pd.DataFrame(dicio_results)
    df_results['date'] = pd.to_datetime(df_results['date'], format='%Y-%m').dt.strftime('%Y-%m')
    results_grouped = df_results.groupby(['date'])
    sum_data = results_grouped['rpk'].sum()
    plt.plot(sum_data.index, sum_data.values)
    plt.title('Gáfico RPK por data para o mercado {}'.format(results[0][3]))
    plt.xlabel('Date')
    plt.ylabel('Sum Value')
    plt.rcParams["savefig.directory"] = "/static/images"
#    file_fig_name = 'rpk_por_data_{}.png'.format(str(int(time.time())))
    plt.savefig('static/images/rpk_por_data.png')



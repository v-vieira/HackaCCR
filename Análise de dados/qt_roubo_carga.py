import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

data = pd.read_excel('Datasets/indi_seg_publ.xlsx')

data_rb_full = data[data['Tipo Crime']=='Roubo de carga'].drop('Tipo Crime',axis=1)
data_rb = data_rb_full.copy()

def dates(df):
    mes_dict = {'janeiro': 1,'fevereiro':2, 'março':3, 'abril':4, 'maio':5, 'junho':6, 'julho':7,'agosto':8, 'setembro' :9, 'outubro':10, 'novembro':11, 'dezembro':12}
    mes_nu = mes_dict[df['Mês']]
    ano = df['Ano']
    return dt.date(ano,mes_nu,1)

data_rb['Data'] = data_rb.apply(dates,axis=1)
data_rb.drop(columns=['Ano','Mês'],inplace=True)

def plot_ano(df = data_rb_full):
    ax = df.groupby('Ano').sum().plot.bar(legend=False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_title('Roubos de carga por ano')
    ax.set_ylabel('Quantidade')
    ax.set_xlabel('Ano')
    labels = df['Ano'].unique().astype(str)
    labels[-1] = '2020*'
    ax.set_xticklabels(labels, rotation=0)
    plt.tick_params(length=0,labelsize=9)
    plt.show()

def plot_10_uf(df = data_rb):
    ax = df.groupby(['UF']).sum().sort_values('Ocorrências',ascending=False).head(10).plot.barh(legend=False,color='red')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_title('Estados com maior quantidade de roubo de carga entre Jan/2015 e Mar/2020')
    ax.set_xlabel('Quantidade')
    plt.tick_params(length=0,labelsize=9)
    ax.invert_yaxis()
    plt.show()
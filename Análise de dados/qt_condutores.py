import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

#Open the datasets
data_frota = pd.read_csv("Datasets/2020-04_frota_de_veiculos.csv",sep=';')
data_condu = pd.read_csv("Datasets/condutores_latin.csv",encoding="latin",sep=",")
 
# Function to passa break the 'one-column-dataframe' into 'multi-columns'
def prepare_one_line(df_input):
    df_input= df_input.iloc[:,0].str.split(',', expand=True)
    df_input.columns = ['regiao','uf','sexo','faixa_etaria','categoria','qt']
    return df_input

# Function to clean the driver license category: a, b, ab etc
def clean_cat(element):
    cat = ''
    for i in element:
        if i !='-':
            cat += i
        else:
            break
    return cat

# Function to clean the values.
def clean(element):
    return element.str.replace("\"","").str.replace(" a ","-").str.replace(" ","_").str.replace('ã','a').str.replace('á','a').str.replace('ó','o').str.replace('.','').str.replace('ç','c').str.replace('õ','o').str.lower().str.strip()

data_condu = prepare_one_line(data_condu).apply(clean,axis=1)
data_condu['categoria'] = data_condu['categoria'].apply(clean_cat)
data_condu['qt'] = data_condu['qt'].astype(int)

# Extract only from the truck categories
condu_cam = data_condu[data_condu.categoria.isin(['ac','ae','c','e','xc','xe'])]

# Create the histogram
def hist_idade(df = condu_cam):
    bins_value = []
    dif = []
    mean  = []
    for i in df['faixa_etaria'].unique():
        low_high = i.split('-')
        bins_value.append(int(low_high[0]))
        dif.append(int(low_high[1])-int(low_high[0]))
        mean.append((int(low_high[1])+int(low_high[0]))/2)
    he = df.groupby('faixa_etaria').sum()['qt'][1:]
    yl = np.arange(150000,1500000,step=1500000/10)
    plt.bar(x = mean[:-1],height = he,align = 'center',width=dif[:-1])
    plt.xticks(mean,labels=df['faixa_etaria'].unique(),rotation=70,size=8)
    plt.xlim((0,100))
    plt.xlabel("Idade")
    plt.yticks(yl,labels=yl/1000,size=8)
    plt.ylim((0,1500000))
    plt.ylabel("Qtd. em milhares")
    plt.title("Quantidade de habilitados por idade")
    plt.show()

def hist_uf(df = condu_cam.groupby('uf').sum()):
    uf = df.index
    bins_value = np.arange(len(uf))+1
    he = df['qt']
    yl = np.arange(150000,1500000,step=150000)
    plt.bar(x = bins_value,height = he,align = 'center')
    plt.xticks(bins_value,labels=uf,rotation=70,size=8)
    plt.xlim((0,bins_value[-1]+1))
    plt.xlabel("Estado")
    plt.yticks(yl,labels=yl/1000,size=8)
    plt.ylim((0,1500000))
    plt.ylabel("Qtd. em milhares")
    plt.title("Quantidade de habilitados por estado")
    plt.show()
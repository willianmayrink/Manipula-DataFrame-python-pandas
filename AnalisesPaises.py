import pandas as pd
import csv
import numpy as np

#importando os dados do PIB.
columns_to_keep=['Country Name','2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015'] #Colunas de interesse.
GDP= pd.read_csv('world_bank.csv', skiprows=4) # lendo o arquivo csv a partir da linha 4, local onde inicia os dados.
GDP= GDP[columns_to_keep] # Atualizando o dataframe apenas com as colunas de interesse.
GDP=GDP.rename(columns={'Country Name':'Country'})
GDP= GDP.set_index('Country')
GDP=GDP.rename(index={"Korea, Rep.":"South Korea","Iran, Islamic Rep.":"Iran","Hong Kong SAR, China":"Hong Kong"})
GDP=GDP.reset_index() //as modicações de nomes visam o futuro merge dos dados, então é sempre bom deixar eles padronizados.

#importando os dados de energia
columns_to_keep = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'] #Atualizando as colunas de interesse para entrar com dados de uma nova tabela.
energy= pd.read_excel (r'Energy Indicators.xls', skiprows=17, skipfooter=38)
energy= energy.rename(columns={'Unnamed: 1':'Country','Petajoules': 'Energy Supply','Gigajoules':'Energy Supply per Capita', '%':'% Renewable'}) #Renomeando as colunas após extracao dos dados.
energy= energy[columns_to_keep]
energy= energy.set_index('Country')
energy= energy.rename(index={"Republic of Korea": "South Korea",'Iran (Islamic Republic of)':'Iran', "United States of America": "United States", "United Kingdom of Great Britain and Northern Ireland": "United Kingdom", "China, Hong Kong Special Administrative Region": "Hong Kong",'Bolivia (Plurinational State of)' : 'Bolivia','Switzerland17':'Switzerland'}) 
energy= energy.reset_index()

#importando os dados de produção cientifica.
ScimEn= pd.read_excel('scimagojr-3.xlsx')
ScimEn= ScimEn[ScimEn['Rank']<16] #Como pedido, extração apenas dos 15 primeiros países do rank.

# Merge das tabelas por alguns parametros.
final= pd.merge(ScimEn, GDP, how= 'inner', left_on='Country', right_on='Country') #Juntando os dados dos 15 paises com maior rank de produção científica com seus respectivos dados de PIB.
final= pd.merge(final, energy, how='inner', left_on='Country', right_on='Country') #Atualizando a tabela anterior, e agregando também os dados de energia dos paises top 15 do rank de produção científica.
final= final.set_index('Country') #Tabela final, indexada pelos países.


#Fazer uma função que devolve a média de GDP dos ultimos 10 anos em ordem descrescente e ignorar valores faltantes:

import numpy as np             
def media(row): #Função media para aplicar em cada linha
    data = row[['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']]
    return pd.Series({'avgGDP': np.average(data)})   

def Media_GDP():
    Top15 = final
    Top15= Top15.reset_index()
    rows= ['Country','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']
    Top15= Top15[rows] #selecionado as colunas de interesse
    Top15= Top15.set_index('Country')
    return Top15.apply(media, axis=1).sort('avgGDP',ascending=False) #Fazendo a media de cada linha de dados, por todas as colunas de interesse.
    
# Em quanto o PIB mudou nos últimos 10 anos para o país com o sexto maior PIB?:

def Dif_GDP_Rank6():
    Top15 = Media_GDP()
    Top15= Top15.reset_index()
    x= Top15.loc[5,'Country'] #selecionado o paises na linha 6, com isso colocamos como indice 5.
    return final.loc[x, '2015']- final.loc[x, '2006']

# Qual é o fornecimento médio de energia per capita dos países top 15?:
Top15= final
Top15['Energy Supply per Capita'] = Top15['Energy Supply per Capita'].astype(float)
energiamedia= "%.2f" % np.average(Top15['Energy Supply per Capita'])

#Qual país tem o máximo de % de renováveis e qual é a porcentagem?

Top15['% Renewable'] = Top15['% Renewable'].astype(float)
x= np.max(Top15.loc[:,['% Renewable']])
Top15= Top15.set_index('% Renewable')
MaxReneCountry= Top15.loc[x,'Country']



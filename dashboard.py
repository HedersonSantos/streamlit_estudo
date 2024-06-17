# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 17:18:36 2024

@author: Hederson
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')
st.title('DASHBOARD DE VENDAS :shopping_trolley:')

def formata_numero_decimal(numero):
    formatted_numero = f"{numero:,.2f}".replace('.', ',')
    formatted_numero= formatted_numero.replace(',', '.', formatted_numero.count(',') - 1)
    return formatted_numero

url="https://labdados.com/produtos"

regioes=['Brasil', 'Centro-Oeste', 'Nordeste', 'Norte', 'Sudeste', 'Sul']
st.sidebar.title('Filtros') #barra lateral
regiao = st.sidebar.selectbox('Região',regioes)
if regiao=='Brasil':
    regiao=''
    
todos_anos = st.sidebar.checkbox('Dados de todo o período', value=True)
if todos_anos:
    ano=''
else:
    ano = st.sidebar.slider('Ano', 2020, 2023)

query_string = {'regiao':regiao.lower(), 'ano':ano}
    
response=requests.get(url, params=query_string)
dados= pd.DataFrame.from_dict(response.json())
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format='%d/%m/%Y')

filtro_vendedores=st.sidebar.multiselect('Vendedores',dados['Vendedor'].unique())
if filtro_vendedores:
    dados=dados[dados['Vendedor'].isin(filtro_vendedores)]


##tabelas
receita_estados=dados.groupby('Local da compra')[['Preço']].sum()
estados = dados.drop_duplicates(subset='Local da compra')[['Local da compra','lat','lon']]
receita_estados = pd.merge(receita_estados, estados, on='Local da compra', how = 'inner', )
receita_estados = receita_estados.sort_values(by='Local da compra')

receita_mensal = dados.set_index('Data da Compra').groupby(pd.Grouper(freq='M'))['Preço'].sum().reset_index()
receita_mensal['Ano']=receita_mensal['Data da Compra'].dt.year
receita_mensal['Mes']=receita_mensal['Data da Compra'].dt.month_name()

receita_categorias = dados.groupby('Categoria do Produto')[['Preço']].sum().sort_values('Preço', ascending=False)

#quantidade de vendas
#como exercicio

#Tabelas vendedores

vendedores = pd.DataFrame(dados.groupby('Vendedor')['Preço'].agg(['sum','count']))

#gráficos
fig_mapa_receita = px.scatter_geo(receita_estados, 
                                  lat = 'lat',
                                  lon = 'lon',
                                  scope = 'south america',
                                  size = 'Preço',
                                  template = 'seaborn',
                                  hover_name = 'Local da compra',
                                  hover_data = {'lat':False, 'lon':False},
                                  title = 'Receita por Estado')


fig_receita_mensal = px.line(receita_mensal,
                             x = 'Mes',
                             y = 'Preço',
                             markers = True,
                             range_y = (0,receita_mensal['Preço'].max()),
                             color = 'Ano',
                             line_dash = 'Ano',
                             title = 'Receita Mensal')
fig_receita_mensal.update_layout(yaxis_title='Receita')

fig_receita_estados=px.bar(receita_estados.head(5),
                            x = 'Local da compra',
                            y = 'Preço',
                            text_auto = True,
                            title = 'Top estados (receita)')
fig_receita_estados.update_layout(yaxis_title='Receita')

fig_receita_categorias = px.bar(receita_categorias,
                            text_auto = True,
                            title = 'Receita por categoria')
fig_receita_categorias.update_layout(yaxis_title='Receita')




## vizualização no streamlit
aba1, aba2, aba3 = st.tabs(['Receita', 'Quantidade de vendas', 'Vendedores'])
with aba1:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita', formata_numero_decimal(dados['Preço'].sum()))
        st.plotly_chart(fig_mapa_receita, user_container_width=True)
        st.plotly_chart(fig_receita_estados, user_container_width=True)
        
    with coluna2:
        st.metric('Quantidade de vendas', f"{dados.shape[0]:,.0f}".replace(',', '.'))
        st.plotly_chart(fig_receita_mensal, user_container_width=True)
        st.plotly_chart(fig_receita_categorias, user_container_width=True)
with aba2:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita', formata_numero_decimal(dados['Preço'].sum()))
        
        
    with coluna2:
        st.metric('Quantidade de vendas', f"{dados.shape[0]:,.0f}".replace(',', '.'))
with aba3:
    qtd_vendedores = st.number_input('Quantidade de vendedores',min_value=2,max_value=10, value=5)
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita', formata_numero_decimal(dados['Preço'].sum()))
        maiores_vendedores = vendedores[['sum']].sort_values('sum', ascending=False).head(qtd_vendedores)
        fig_receita_vendedores = px.bar(maiores_vendedores,
                                        x='sum',
                                        y=maiores_vendedores.index,
                                        text_auto=True,
                                        title = f'Top{qtd_vendedores} vendedores (receita)')
        st.plotly_chart(fig_receita_vendedores)
        
        
    with coluna2:
        st.metric('Quantidade de vendas', f"{dados.shape[0]:,.0f}".replace(',', '.'))   
        maiores_vendas = vendedores[['count']].sort_values('count', ascending=False).head(qtd_vendedores)
        fig_vendas_vendedores = px.bar(maiores_vendas,
                                        x='count',
                                        y=maiores_vendas.index,
                                        text_auto=True,
                                        title = f'Top{qtd_vendedores} vendedores (quantidade de vendas)')
        st.plotly_chart(fig_vendas_vendedores)
#st.dataframe(dados)
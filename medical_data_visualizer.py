# Importação das bibliotecas necessárias para análise de dados e visualização
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1 - Carregar o dataset de exame médico e atribuir à variável df
# Vamos utilizar pandas para ler o arquivo CSV com os dados médicos.
df = pd.read_csv('medical_examination.csv')

# 2 - Criar a coluna 'overweight' com base no IMC (Índice de Massa Corporal)
# O cálculo do IMC é realizado dividindo o peso (kg) pelo quadrado da altura (m). 
# Se o valor for maior que 25, consideramos que a pessoa está acima do peso (1), caso contrário, está com peso normal (0).
df['overweight'] = (df['weight'] / (df['height'] / 100) ** 2).apply(lambda x: 1 if x > 25 else 0)

# 3 - Normalizar os dados das colunas 'cholesterol' e 'gluc'
# Para estas variáveis, queremos que 0 seja bom e 1 seja ruim. Valores iguais a 1 serão mantidos como 0, e valores maiores que 1 serão ajustados para 1.
df['cholesterol'] = df['cholesterol'].apply(lambda x: 0 if x == 1 else 1)
df['gluc'] = df['gluc'].apply(lambda x: 0 if x == 1 else 1)

# 4 - Função para desenhar o gráfico categórico (catplot)
def draw_cat_plot():
    # 5 - Transformar o dataframe em um formato longo (long format) utilizando pd.melt
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    # 6 - Agrupar os dados por 'cardio', 'variable', 'value' e contar os valores
    # A função size() será usada para contar as ocorrências.
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')

    # 7 - Utilizar a função catplot do seaborn para criar o gráfico categórico
    # Aqui criamos o gráfico de barras categorizado por 'cardio'
    fig = sns.catplot(x='variable', y='total', hue='value', col='cardio', data=df_cat, kind='bar')

    # 8 - Salvar o gráfico como 'catplot.png'
    fig.savefig('catplot.png')
    return fig

# 10 - Função para desenhar o mapa de calor (heatmap)
def draw_heat_map():
    # 11 - Limpar os dados, removendo registros incorretos
    # Vamos remover dados onde a pressão diastólica é maior que a sistólica, e também valores fora dos percentis 2.5 e 97.5 para altura e peso.
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) &
                 (df['height'] >= df['height'].quantile(0.025)) &
                 (df['height'] <= df['height'].quantile(0.975)) &
                 (df['weight'] >= df['weight'].quantile(0.025)) &
                 (df['weight'] <= df['weight'].quantile(0.975))]

    # 12 - Calcular a matriz de correlação
    # A matriz de correlação mostra como as variáveis estão relacionadas entre si.
    corr = df_heat.corr()

    # 13 - Gerar uma máscara para a parte superior da matriz de correlação
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 14 - Configurar a figura do matplotlib
    fig, ax = plt.subplots(figsize=(12, 12))

    # 15 - Plotar a matriz de correlação utilizando seaborn heatmap
    sns.heatmap(corr, annot=True, fmt='.1f', mask=mask, square=True, cbar_kws={"shrink": .5}, ax=ax)

    # 16 - Salvar o gráfico de mapa de calor como 'heatmap.png'
    fig.savefig('heatmap.png')
    return fig
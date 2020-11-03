### BIBLIOTECAS ###

from requests import get
import json
import pandas as pd
import pyodbc

### AUTENTICAÇÃO ###

headers = {'x-api-key': 'efdcc367-f198-4703-a5ac-ceffb28a9759'}

urlbreeds = "https://api.thecatapi.com/v1/breeds"

urlhats = "https://api.thecatapi.com/v1/images/search?limit=3&category_ids=1"

urlsunglasses = "https://api.thecatapi.com/v1/images/search?limit=3&category_ids=4"


### FUNÇÕES ###


def get_fotos_gatinhos(url):

    data = get(url, headers=headers)

    data_json = data.json()

    data_lista = []
    search_url_lista = []
    image_url_lista = []

    # Coleta a lista de IDs e gera a lista de URLs de busca por ID
    for item in data_json:
        data_lista.append(item['id'])
        search_url_lista.append(
            'https://api.thecatapi.com/v1/images/search?limit=3&breed_id='+item['id'])

    print('Lista de IDs das raças OK')

    # Coleta as infprmações de cada raça e as URLs de 3 imagens
    for i in search_url_lista:
        data = get(i, headers=headers)
        data_json = data.json()

        for url in data_json:
            image_url_lista.append([url['breeds'][0]['id'], url['breeds'][0]['name'], url['breeds'][0]
                                    ['origin'], url['breeds'][0]['temperament'], url['breeds'][0]['description'], url['url']])

    df = pd.DataFrame(image_url_lista, columns=[
        'ID', 'NOME', 'ORIGEM', 'TEMPERAMENTO', 'DESCRICAO', 'URL'])

    print(df)

    # Input no SQL

    cnxn = pyodbc.connect('Driver={SQL Server};'
                          'Server=LAPTOP-0N9TFGS0\SQLEXPRESS;'
                          'Database=DB001;'
                          'Trusted_Connection=yes;')

    cursor = cnxn.cursor()

    for index, row in df.iterrows():
        cursor.execute("INSERT INTO [dbo].[gatos_descricao] (ID, NOME, ORIGEM, TEMPERAMENTO, DESCRICAO, URL) values(?,?,?,?,?,?)",
                       row.ID, row.NOME, row.ORIGEM, row.TEMPERAMENTO, row.DESCRICAO, row.URL)

    cnxn.commit()
    cursor.close()


def get_fotos_categoria(url, url1):

    data = get(url, headers=headers)

    data_json = data.json()

    data_lista = []

    # Coleta URL das imagens de óculos
    for item in data_json:
        data_lista.append([item['categories'][0]['name'], item['url']])

    data1 = get(url1, headers=headers)

    data1_json = data1.json()

    # Coleta URL das imagens de Chapéu
    for item in data1_json:
        data_lista.append([item['categories'][0]['name'], item['url']])

    df_cat = pd.DataFrame(data_lista, columns=['Categoria', 'URL'])

    print('### URL COM ÓCULOS OU CHAPEU ###')
    print(df_cat)  # 1D

    # Input no SQL

    cnxn = pyodbc.connect('Driver={SQL Server};'
                          'Server=LAPTOP-0N9TFGS0\SQLEXPRESS;'
                          'Database=DB001;'
                          'Trusted_Connection=yes;')

    cursor = cnxn.cursor()

    for index, row in df_cat.iterrows():
        cursor.execute("INSERT INTO [dbo].[fotos_categoria] (Categoria,URL) values(?,?)",
                       row.Categoria, row.URL)

    cnxn.commit()
    cursor.close()


### MAIN ###
get_fotos_gatinhos(urlbreeds)
#get_fotos_categoria(urlsunglasses, urlhats)

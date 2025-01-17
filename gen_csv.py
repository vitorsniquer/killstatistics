import pandas as pd
import requests
import json
from datetime import datetime


try:
    response = requests.get('https://api.tibiadata.com/v4/worlds')
    response.raise_for_status()  # Raise an exception for bad status codes

    data = response.json()

except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")

lista_mundos = []
for w in data['worlds']['regular_worlds']:
  lista_mundos.append(f"https://api.tibiadata.com/v4/killstatistics/{w['name']}")
lista_mundos

df_final = pd.DataFrame()

for mundo in lista_mundos:
  try:
    response = requests.get(mundo)
    response.raise_for_status()  # Raise an exception for bad status codes

    data = response.json()
    mundo_nome = mundo.split("/")[-1] 
    print(mundo_nome)
    entries = data['killstatistics']['entries']
    df_temp = pd.DataFrame(entries)
    df_temp['mundo'] = mundo_nome 
    df_final = pd.concat([df_final, df_temp], ignore_index=True)


  except requests.exceptions.RequestException as e:
      print(f"Error fetching data: {e}")
  except json.JSONDecodeError as e:
      print(f"Error decoding JSON: {e}")


# Obter a data atual no formato dd-mm-aaaa
data_atual = datetime.now().strftime("%d-%m-%Y")

# Definir o nome do arquivo com a data
nome_arquivo = f"killstatistics_{data_atual}.csv"

# Salvar o DataFrame com a data no nome do arquivo
df_final.to_csv(nome_arquivo, index=False)
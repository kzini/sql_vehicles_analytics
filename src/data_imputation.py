import pandas as pd

def imputacao_ano_cidade(df):
    df_imputado = df.copy()

    for (cidade, ano), grupo in df_imputado.groupby(['cidade_revendedor', 'ano_fabricacao']):
        valores_grupo = grupo['quilometragem'].dropna()
        nulos_grupo = grupo['quilometragem'].isna().sum()
        
        if nulos_grupo > 0:
            # Tentativa 1: Utiliza dados da própria cidade e ano
            if len(valores_grupo) >= 5:
                Q1 = valores_grupo.quantile(0.25)
                Q3 = valores_grupo.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 3.0 * IQR
                upper_bound = Q3 + 3.0 * IQR
                
                valores_filtrados = valores_grupo[
                    (valores_grupo >= lower_bound) & 
                    (valores_grupo <= upper_bound)
                ]
                
                mediana = valores_filtrados.median()
                
            else:
                # Tentativa 2: Se não houver dados suficientes na cidade, utiliza toda a região + ano
                dados_ano_estado = df_imputado[
                    (df_imputado['ano_fabricacao'] == ano) & 
                    (df_imputado['quilometragem'].notna())
                ]['quilometragem']
                
                if len(dados_ano_estado) > 10:
                    Q1_estado = dados_ano_estado.quantile(0.25)
                    Q3_estado = dados_ano_estado.quantile(0.75)
                    IQR_estado = Q3_estado - Q1_estado
                    
                    lower_bound_estado = Q1_estado - 3.0 * IQR_estado
                    upper_bound_estado = Q3_estado + 3.0 * IQR_estado
                    
                    valores_filtrados_estado = dados_ano_estado[
                        (dados_ano_estado >= lower_bound_estado) & 
                        (dados_ano_estado <= upper_bound_estado)
                    ]
                    
                    mediana = valores_filtrados_estado.median()

                else:
                    mediana = dados_ano_estado.median()
            
            mascara_nulos = (df_imputado['cidade_revendedor'] == cidade) & \
                           (df_imputado['ano_fabricacao'] == ano) & \
                           (df_imputado['quilometragem'].isna())
            
            df_imputado.loc[mascara_nulos, 'quilometragem'] = mediana
    
    return df_imputado

def imputacao_precos_por_grupo(df):
    df_imputado = df.copy()
    carros_sem_preco = df_imputado[df_imputado['preco_usd'].isna()].index
    
    for idx in carros_sem_preco:
        carro = df_imputado.loc[idx]
        ano = carro['ano_fabricacao']
        versao = carro['versao']
        cidade = carro['cidade_revendedor']
        km = carro['quilometragem']
        
        preco_imputado = None
        
        # Estratégia 1: Mesmo ano + versão + cidade + faixa de KM (±20%)
        if not pd.isna(km):
            km_min = km * 0.8  # 80% da quilometragem original (20% menos)
            km_max = km * 1.2 # 120% da quilometragem original (20% mais)
            grupo1 = df_imputado[
                (df_imputado['ano_fabricacao'] == ano) &
                (df_imputado['versao'] == versao) &
                (df_imputado['cidade_revendedor'] == cidade) &
                (df_imputado['quilometragem'] >= km_min) &
                (df_imputado['quilometragem'] <= km_max) &
                (df_imputado['preco_usd'].notna())
            ]
            if len(grupo1) >= 3:
                preco_imputado = grupo1['preco_usd'].median()
        
        # Estratégia 2: Mesmo ano + versão + cidade
        if preco_imputado is None:
            grupo2 = df_imputado[
                (df_imputado['ano_fabricacao'] == ano) &
                (df_imputado['versao'] == versao) &
                (df_imputado['cidade_revendedor'] == cidade) &
                (df_imputado['preco_usd'].notna())
            ]
            if len(grupo2) >= 3:
                preco_imputado = grupo2['preco_usd'].median()
        
        # Estratégia 3: Mesmo ano + versão
        if preco_imputado is None:
            grupo3 = df_imputado[
                (df_imputado['ano_fabricacao'] == ano) &
                (df_imputado['versao'] == versao) &
                (df_imputado['preco_usd'].notna())
            ]
            if len(grupo3) >= 3:
                preco_imputado = grupo3['preco_usd'].median()
        
        # Estratégia 4: Mesmo ano
        if preco_imputado is None:
            grupo4 = df_imputado[
                (df_imputado['ano_fabricacao'] == ano) &
                (df_imputado['preco_usd'].notna())
            ]
            if len(grupo4) >= 3:
                preco_imputado = grupo4['preco_usd'].median()
        
        # Estratégia 5: Mediana geral
        if preco_imputado is None:
            preco_imputado = df_imputado['preco_usd'].median()
        
        df_imputado.loc[idx, 'preco_usd'] = preco_imputado
        df_imputado.loc[idx, 'preco_original_msrp_usd'] = preco_imputado
    
    return df_imputado


# Análise do mercado de veículos Honda Civic usados no estado da Califórnia

### End-to-End ETL e análise SQL com dados reais 

---

## Introdução

Este projeto implementa uma pipeline de ETL e análise exploratória utilizando dados reais de anúncios de veículos Honda Civic na Califórnia.

---

## Contexto e objetivo

O mercado de veículos usados é sensível a múltiplos fatores como idade, quilometragem e região.
Utilizando dados reais de anúncios de veículos Honda Civic usados, este projeto busca responder a perguntas como:

- Como o preço varia conforme a idade e a quilometragem do veículo?
- Existem cidades com preços sistematicamente mais altos ou mais baixos?
- Quais padrões de depreciação média podem ser identificados entre faixas de quilometragem?
- Como esses fatores interagem entre si (idade × km × preço)?

## Estrutura do projeto

```

├── scripts/
│ ├── get_dataset.py # Coleta inicial via API
│ └── get_dataset_2.py # Coleta complementar por cidades específicas
├── src/
│ ├── visualization.py # Funções customizadas para gráficos e plots
│ ├── data_imputation.py # Funções para imputação de dados faltantes
│ └── color_categorization.py # Funções para categorização de cores dos veículos
├── notebooks/
│ ├── data_cleaning.ipynb # Limpeza, transformação e preparação dos dados
│ └── graficos.ipynb # Análise visual e exploração de insights
├── data/
│ ├── sql_exports/ # Resultados das consultas SQL para visualização
│ ├── processed/ # Dados limpos e estruturados
│ └── raw/ # Dados brutos da API MarketCheck
├── sql/
│ └── consultas_sql.sql # Consultas SQL de exploração
├── requirements.txt 
└── README.md 

```

## 1. Extração

A coleta dos dados foi realizada por meio da Marketcheck API. Sua versão impunha duas restrições:   
- Limite de 500 registros por requisição;   
- Restrição geográfica de área dentro do próprio estado.

Para contornar essas barreiras, foram desenvolvidos dois scripts complementares:

- `get_dataset.py` - Coleta inicial ampla;
- `get_dataset_2.py` - Coleta com seleção manual de cidades para enriquecer o dataset.

---

## 2. Transformação

A etapa de transformação foi realizada em Python. A principais tarefas foram:

- **Seleção de features** — Redução de colunas relevantes para análises;
- **Padronização métrica** — Conversão de milhas para km, MPG para km/L e polegadas para metros;
- **Tradução e categorização** —  Devido à minha familiaridade limitada com a terminologia específica da indústria automotiva, colunas e valores foram padronizados em português para facilitar a análise;
- **Imputação** — Valores nulos foram recuperados através de estratégias hierárquicas;
- **Padronização de valores** — Cores, combustíveis e categorias foram uniformizados.

### Estratégias de imputação

Para preservar o tamanho da amostra sem introduzir distorções relevantes, foi adotada uma estratégia de imputação hierárquica baseada em contexto.

**Imputação de quilometragem**  
A quilometragem foi estimada priorizando a combinação cidade × ano de fabricação, utilizando a mediana dentro de cada grupo.
Para garantir maior robustez estatística, foi aplicada detecção de outliers utilizando o critério 3×IQR, removendo observações estatisticamente discrepantes antes do cálculo das medianas.

Quando não havia dados suficientes dentro da mesma cidade, a imputação utilizou dados agregados do mesmo ano de fabricação em todo o estado da Califórnia.

**Imputação de preço**  
A imputação de preços seguiu uma lógica hierárquica baseada na similaridade entre veículos:
- Mesmo ano + versão + cidade + faixa de quilometragem (±20%);
- Mesmo ano + versão + cidade;
- Mesmo ano + versão;
- Mesmo ano;
- Mediana global do dataset (último recurso).

---

## 3. Carga

Após a transformação, os dados foram carregados em um banco **PostgreSQL** local.

**Fluxo de Carga:**

- **Criação/cerificação do banco** - Conexão com PostgreSQL e criação da database civic_db;
- **Definição do Schema** - Criação das tabelas 'revendedores' e 'veículos' relacionados;
- **Preparação dos Data Frames** - Separação dos dados em estruturas relacionais;
- **Exportação para PostgreSQL** - Carga dos dados tratados nas tabelas;
- **Backup em CSV** - Exportação do dataset processado para arquivo csv.

---

## 4. Análise SQL

Com o banco populado, as análises foram conduzidas diretamente em SQL para investigar padrões de mercado.

A análise seguiu os seguintes objetivos:

- Medir tendências de preço médio por idade do veículo;
- Calcular taxas de depreciação por faixa de quilometragem;
- Identificar outliers (oportunidades de mercado);
- Comparar variações de preço entre cidades;
- Analisar correlação entre quilometragem e preço.

---

## 5. Análise e insights

### Depreciação ao longo do tempo

A idade do veículo mostrou-se o fator estrutural mais relevante para a queda de preço.

Foi observada uma redução substancial do preço médio ao longo do ciclo de vida do veículo, com a queda mais acentuada ocorrendo nos primeiros anos. Sendo que uma das maiores reduções relativas de preço ocorre entre 3 e 4 anos.

---

### Impacto da quilometragem

A quilometragem apresenta correlação negativa moderada a forte com o preço, variando aproximadamente entre **-0.45 e -0.74** dependendo da idade do veículo.

A análise por idade revela que essa relação não é constante ao longo do ciclo de vida do veículo.

Há um padrão de intensificação seguido de saturação do impacto da quilometragem:

- **Carros mais novos (2–4 anos)** apresentam correlação negativa mais moderada, indicando que a quilometragem ainda exerce influência limitada no preço.
- Entre **5 e 10 anos**, a correlação se intensifica progressivamente, atingindo valores próximos de **-0.74**, sugerindo maior sensibilidade do mercado ao desgaste acumulado.
- Em **veículos mais antigos (10+ anos)**, a correlação volta a diminuir em magnitude, indicando que o impacto marginal da quilometragem se reduz.

---

### Faixas de quilometragem e desvalorização

A comparação entre faixas de quilometragem evidencia diferenças claras de preço médio:

| Faixa de quilometragem | Diferença média de preço |
|---|---|
| 1–100k km | referência |
| 100–200k km | 27% mais barato |
| 200–300k km | 48.6% mais barato |
| >300k km | 63.4% mais barato |

---

### Variação regional de preços

Foram observadas diferenças relevantes de preço entre as cidades da Califórnia.

Entre veículos com 1–100k km, algumas cidades apresentam preços médios significativamente mais elevados:

**Mercados com preços médios mais altos**

- Indio (~$25.691)
- Fresno (~$24.215)
- San Jose (~$23.881)

Por outro lado, algumas regiões apresentam preços médios inferiores:

**Mercados com preços relativamente menores**

- El Cajon
- Sacramento
- Riverside

---

## Conclusão

O projeto demonstra a construção de uma pipeline completa de dados utilizando Python, PostgreSQL e SQL para investigar padrões reais de mercado. A análise revelou padrões claros de depreciação ao longo do tempo, impacto não linear da quilometragem e variações regionais de preço entre cidades da Califórnia.

---

## Como reproduzir

1. Clone o repositório:
```bash
git clone https://github.com/kzini/sql_vehicles_analytics.git

cd sql_vehicles_analytics
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute os notebooks na pasta `notebooks/` na ordem:

jupyter notebook notebooks/data_cleaning.ipynb
 
jupyter notebook notebooks/graficos.ipynb

---

## Autor

**Bruno Casini**  
LinkedIn: https://www.linkedin.com/in/kzini

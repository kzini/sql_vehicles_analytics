# Análise de vendas do mercado de veículos usados Honda Civic no estado da Califórnia

### End-to-End ETL e análise SQL com dados reais

---

## Introdução

Este projeto implementa um pipeline completo de **ETL** e **análise exploratória de dados** para investigar o mercado de revenda de veículos Honda Civic no estado da Califórnia (EUA).

Minha motivação com este projeto é simples mas central no meu aprendizado no campo de ciência de dados:

> A capacidade de extrair dados brutos do mundo real, limpá-los, estruturá-los e gerar insights relevantes.

---

## Contexto e objetivo

O mercado de veículos usados é sensível a múltiplos fatores como idade, quilometragem e região.
Com dados reais de anúncios de veículos Honda Civic, este projeto busca responder a perguntas práticas como:

- Como o preço varia conforme a idade e a quilometragem do veículo?
- Existem cidades com preços sistematicamente mais altos ou mais baixos?
- Quais padrões de depreciação média podem ser identificados entre faixas de quilometragem?
- Como esses fatores interagem entre si (idade × km × preço)?

O foco é analítico e explicativo, não preditivo. Com o objetivo de compreender o comportamento de mercado por meio de dados limpos e interpretáveis.

## Estrutura do projeto

---

├── scripts/
│ ├── get_dataset.py # Coleta inicial via API
│ └── get_dataset_2.py # Coleta complementar por cidades específicas
├── src/
│ └── visualization.py # Funções customizadas para gráficos e plots
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

---

## 1. Extração

A coleta dos dados foi realizada por meio da Marketcheck API.   
A versão gratuita da API impunha duas restrições:   
- Limite de 500 registros por requisição;   
- Restrição geográfica de área dentro do próprio estado.

Para contornar essas barreiras, foram desenvolvidos dois scripts complementares:

- `get_dataset.py` - Coleta inicial ampla;
- `get_dataset_2.py` - Coleta com seleção manual de cidades para enriquecer o dataset.

---

## 2. Transformação

A etapa de transformação foi realizada em Python.   
Principais tarefas:

- **Seleção de features** — Redução de colunas relevantes para análises;
- **Padronização métrica** — Conversão de milhas para km, MPG para km/L e polegadas para metros;
- **Tradução e categorização** —  Devido à minha familiaridade limitada com a terminologia específica da indústria automotiva,
colunas e alguns valores foram padronizados em português para facilitar a análise;
- **Imputação** — valores nulos recuperados através de estratégias hierárquicas;
- **Padronização de valores** — cores, combustíveis e categorias uniformizadas.

Essa transformação tornou os dados consistentes, relacionáveis e prontos para análise SQL.

---

## 3. Carga

Após a transformação, os dados foram carregados em um banco **PostgreSQL** local.

**Fluxo de Carga:**

- **Criação/cerificação do banco** - Conexão com PostgreSQL e criação da database civic_db;
- **Definição do Schema** - Criação das tabelas 'revendedores' e 'veículos' relacionados;
- **Preparação dos DataFrames** - Separação dos dados em estruturas relacionais;
- **Exportação para PostgreSQL** - Carga dos dados tratados nas tabelas;
- **Backup em CSV** - Exportação do dataset processado para arquivo csv.

Essa estrutura permite consultas SQL complexas com junções diretas entre veículos e revendedores, habilitando análises regionais e segmentadas por múltiplas dimensões.

---

## 4. Análise SQL

Com o banco populado, as análises foram conduzidas diretamente em SQL para investigar padrões de mercado.

**Objetivos da análise:**

- Medir tendências de preço médio por idade do veículo;
- Calcular taxas de depreciação por faixa de quilometragem;
- Identificar outliers (oportunidades de mercado);
- Comparar variações de preço entre cidades;
- Analisar correlação entre quilometragem e preço.

---

## 5. Análise e insights

**Padrões de desvalorização:**

**Idade como fator primário**   
Veículos sofrem desvalorização de aproximadamente 63% ao longo de 13 anos, com queda mais acentuada entre 3-4 anos (-13.4%).

**Quilometragem como amplificador não linear**   
A relação entre quilometragem e preço não evolui de forma constante, mas apresenta um padrão de intensificação e saturação. A correlação negativa se fortalece progressivamente até cerca dos 10 anos, 
quando a quilometragem exerce seu maior impacto sobre o valor do veículo, e perde força em modelos mais antigos, cujo preço já reflete depreciações acumuladas.

Isso explica por que carros de 10 anos são os mais sensíveis à quilometragem, enquanto carros muito novos ou muito velhos são menos afetados.

**Faixas críticas de desvalorização**   

Análise comparativa mostra que veículos com 100-200k km têm valor 27% inferior ao de veículos equivalentes com 1-100k km. Esta diferença aumenta para 48,6% na faixa de 200-300k km e atinge 63,4% acima de 300k km, 
indicando que a quilometragem é um fator crítico na desvalorização."

**Oportunidades Regionais Identificadas:**   

**Mercados premium**   
Indio ($25.691), Fresno ($24.215) e San Jose ($23.881) lideram os preços mais altos para veículos 1-100k km.

**Mercados de oportunidade**   
El Cajon e São Bernadino oferecem melhores condições de compra.

**Insights Estratégicos para Negócios:**

**Melhor custo-benefício para compra**   
Veículos de 4-5 anos com 100-200k km em mercados como Sacramento e Riverside.

**Oportunidades de arbitragem**   
Compra em Sacramento ($19.675) e venda em Indio ($25.691) pode gerar diferenças de até 30.5%.

**Riscos identificados**   
Veículos de 10+ anos com alta quilometragem sofrem desvalorização acelerada e devem ser evitados em estratégias de curto prazo.

**Mercados estáveis**   
Roseville e Montclair oferecem volume e preços consistentes para operações de média escala.

Estes padrões revelam dinâmicas de precificação distintas entre regiões e segmentos etários, permitindo estratégias segmentadas para maximizar retorno em compra e venda.

---

## Conclusão

Este projeto demonstra o ciclo completo de ciência de dados aplicada — da coleta à interpretação de resultados. Utilizando habilidades fundamentais como:

- **Manipulação de dados brutos** — coleta via API e tratamento de inconsistências;
- **Limpeza e transformação criteriosa** — padronização, imputação e engenharia de features;
- **Modelagem relacional em SQL** — estruturação em banco de dados para análise eficiente;
- **Análise exploratória orientada por hipóteses** — investigação guiada por perguntas de negócio;
- **Comunicação de resultados** — visualizações claras que contam a história dos dados.

Em essência, este é um estudo sobre como o dado se torna conhecimento: um pipeline que conecta realidade empírica (anúncios de carros) à extração de padrões econômicos verificáveis.

---

## Como reproduzir

1. Clone o repositório:
```bash
git clone https://github.com/kzini/sql_vehicles_analytics.git

cd ***
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute os notebooks na pasta `notebooks/` na ordem:

jupyter notebook notebooks/data_cleaning.ipynb
 
jupyter notebook notebooks/graficos.ipynb

---

> Desenvolvido por Bruno Casini  
> Contato: kzini1701@gmail.com  
> LinkedIn: https://www.linkedin.com/in/kzini/

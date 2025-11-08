-- Parte 3 
-- Análise de tendência de preço baseada na idade e quilometragem dos veículos, e cidade do revendedor.

-- 1. Panorama geral
-- 1.1 Quantidade total de veículos
SELECT 
	COUNT(chassi) AS total_veiculos 
FROM veiculos;

-- 1.2 Cria a coluna idade
ALTER TABLE veiculos 
ADD COLUMN IF NOT EXISTS idade INT;

UPDATE veiculos
SET idade = 2025 - ano_fabricacao;

-- 1.3 Distribuição de veículos por idade
SELECT 
    idade,
    COUNT(chassi) AS qtd_veiculos
FROM veiculos
GROUP BY idade
ORDER BY idade DESC;

-- 1.4 Distribuição por cidade
SELECT 
    cidade_revendedor, 
    COUNT(id_revendedor) qtd_revendedores
FROM revendedores
GROUP BY cidade_revendedor
ORDER BY qtd_revendedores DESC;

-- 2. Preço e depreciação
-- 2.1 Tendência de preço médio por idade
SELECT 
    idade, 
    ROUND(AVG(preco_usd),2) AS preco_medio 
FROM veiculos
GROUP BY idade
ORDER BY 1 DESC

-- 2.2 Depreciação percentual por faixa de quilometragem
WITH base AS (
  SELECT
    CASE
        WHEN quilometragem < 100000 THEN '1-100k'
        WHEN quilometragem < 200000 THEN '100-200k'
        WHEN quilometragem < 300000 THEN '200-300k'
        WHEN quilometragem < 400000 THEN '300-400k'
        ELSE '400k+'
    END AS faixa_km,
    AVG(preco_usd) AS preco_medio,
    COUNT(*) AS n
  FROM veiculos
  GROUP BY faixa_km
)
SELECT
    faixa_km,
    CASE 
    WHEN faixa_km = '1-100k' THEN 'Base (referência)'
    ELSE CAST(ROUND(100 * (1 - preco_medio / 
         (SELECT preco_medio FROM base WHERE faixa_km = '1-100k')), 1) AS TEXT)
    END AS pct_desvalorizacao,
    n
FROM base
ORDER BY 
    CASE faixa_km
        WHEN '1-100k' THEN 1
        WHEN '100-200k' THEN 2
        WHEN '200-300k' THEN 3
        WHEN '300-400k' THEN 4
        ELSE 5
    END;

-- 3. Outliers por idade e quilometragem
-- Considera outliers veículos com preço 2 desvios-padrão abaixo da média do grupo (idade + faixa de km)
WITH grupo AS (
    SELECT 
        idade,
        CASE
            WHEN quilometragem < 100000 THEN '1-100k'
            WHEN quilometragem < 200000 THEN '100-200k'
            WHEN quilometragem < 300000 THEN '200-300k'
            WHEN quilometragem < 400000 THEN '300-400k'
            ELSE '400k+'
        END AS faixa_km,
        AVG(preco_usd) AS preco_medio,
        STDDEV(preco_usd) AS desvio
    FROM veiculos
    GROUP BY idade, faixa_km
)
SELECT 
    v.chassi,
    v.idade,
    v.quilometragem,
    v.preco_usd,
    ROUND(g.preco_medio, 2) as preco_medio, 
    ROUND((1 - (v.preco_usd / g.preco_medio)) * 100, 2) AS pct_abaixo_media
FROM veiculos v
JOIN grupo g ON v.idade = g.idade
    AND CASE
       WHEN v.quilometragem < 100000 THEN '1-100k'
       WHEN v.quilometragem < 200000 THEN '100-200k'
       WHEN v.quilometragem < 300000 THEN '200-300k'
       WHEN v.quilometragem < 400000 THEN '300-400k'
       ELSE '400k+'
     END = g.faixa_km
-- Considera outliers veículos com preço 2 desvios-padrão abaixo da média (por idade + faixa de km)
WHERE v.preco_usd < (g.preco_medio - 2 * g.desvio)
ORDER BY pct_abaixo_media DESC;

-- 4. Análise de preço por cidade
SELECT 
    r.cidade_revendedor,
    COUNT(v.chassi) AS total_veiculos,
    ROUND(AVG(v.preco_usd), 2) AS preco_medio
FROM veiculos v
JOIN revendedores r
  ON v.id_revendedor = r.id_revendedor
GROUP BY r.cidade_revendedor
HAVING COUNT(v.chassi) >= 30  -- Exclui amostras pequenas
ORDER BY preco_medio DESC;

-- 5. Outliers de preço por idade, faixa de quilometragem e cidade
-- Junta veículos abaixo da média com revendedores para pegar a cidade
WITH veiculos_outliers AS (
    SELECT 
        v.chassi,
        v.id_revendedor,
        v.preco_usd,
        v.idade,
        v.quilometragem,
        ROUND((1 - (v.preco_usd / g.preco_medio)) * 100, 2) AS pct_abaixo_media
    FROM veiculos v
    JOIN (
        SELECT 
            idade,
            CASE
                WHEN quilometragem < 100000 THEN '1-100k'
                WHEN quilometragem < 200000 THEN '100-200k'
                WHEN quilometragem < 300000 THEN '200-300k'
                WHEN quilometragem < 400000 THEN '300-400k'
                ELSE '400k+'
            END AS faixa_km,
            AVG(preco_usd) AS preco_medio,
            STDDEV(preco_usd) AS desvio
        FROM veiculos
        GROUP BY idade, faixa_km
    ) g
    ON v.idade = g.idade
    AND CASE
        WHEN v.quilometragem < 100000 THEN '1-100k'
        WHEN v.quilometragem < 200000 THEN '100-200k'
        WHEN v.quilometragem < 300000 THEN '200-300k'
        WHEN v.quilometragem < 400000 THEN '300-400k'
        ELSE '400k+'
    END = g.faixa_km
    WHERE v.preco_usd < (g.preco_medio - 2 * g.desvio)
)
-- Calcula percentual por cidade
SELECT 
    r.cidade_revendedor,
    COUNT(o.chassi) AS n_abaixo_media,
    COUNT(v.chassi) AS total_veiculos,
    ROUND(100.0 * COUNT(o.chassi) / NULLIF(COUNT(v.chassi),0), 2) AS pct_abaixo_media
FROM veiculos v
JOIN revendedores r ON v.id_revendedor = r.id_revendedor
LEFT JOIN veiculos_outliers o ON v.chassi = o.chassi
GROUP BY r.cidade_revendedor
HAVING COUNT(v.chassi) >= 10 
ORDER BY pct_abaixo_media DESC;

-- 6. Correlação entre quilometragem e preço
-- 6.1 Correlação global
SELECT 
    ROUND(
        (AVG(quilometragem * preco_usd) - AVG(quilometragem) * AVG(preco_usd)) /
        (STDDEV(quilometragem) * STDDEV(preco_usd)),
    3) AS corr_pearson_global
FROM veiculos;

-- 6.2 Correlação por idade
SELECT 
    idade,
    ROUND(
        (AVG(quilometragem * preco_usd) - AVG(quilometragem) * AVG(preco_usd)) /
        (STDDEV(quilometragem) * STDDEV(preco_usd)),
    3) AS corr_pearson
FROM veiculos
GROUP BY idade
HAVING COUNT(*) >= 20
ORDER BY idade;

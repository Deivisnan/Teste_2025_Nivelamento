SELECT 
    reg_ans AS operadora, 
    trimestre, 
    SUM(vl_saldo_inicial - vl_saldo_final) AS total_despesas 
FROM despesas_operadoras 
WHERE 
    descricao ILIKE '%EVENTOS%SINISTROS%' -- Filtra as categorias relacionadas
    AND trimestre = 4  -- Filtra apenas o último trimestre
GROUP BY operadora, trimestre 
ORDER BY total_despesas DESC 
LIMIT 10;


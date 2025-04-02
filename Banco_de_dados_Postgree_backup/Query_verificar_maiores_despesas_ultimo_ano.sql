SELECT 
    reg_ans AS operadora,
    trimestre,
    SUM(vl_saldo_inicial - vl_saldo_final) AS total_despesas
FROM despesas_operadoras
WHERE descricao ILIKE '%EVENTOS%SINISTROS%'  -- Filtra as categorias relacionadas
GROUP BY operadora, trimestre
ORDER BY total_despesas DESC
LIMIT 10;

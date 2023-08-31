# GooleNewsCount_Strategy2
# the AWS lambda program: Investment_Stratgy_CountTheNews collect the data to DB table patrick_strategy_1
# http://patrickfung.esy.es/Ertyuiop/GoogleNewsCount_Strategy2.php

useful sql
**1. find the symbol, close, checkd ate, first close, first check date, last close, last check date, close change in %, day count**
SELECT 
	x.symbol,
	x.close,
	x.checkdate,
	x.firstClose,
	x.firstCheckdate,
	x.lastClose,
	x.lastCheckdate,
	((x.firstClose - x.lastClose) / x.lastClose * 100) as closeChangeinPercentage,
	x.total_count_days,
	x.avg_news_count_of_each_day,
	x.min_and_max_news_count_diff_of_each_day_in_precentage
FROM(
	SELECT 
		z.symbol,
		z.close,
		z.checkdate,
		(SELECT close from patrick_strategy_1 f where f.symbol = z.symbol and f.checkdate = z.firstCheckdate) as firstClose,
		z.firstCheckdate,
		(SELECT close from patrick_strategy_1 f where f.symbol = z.symbol and f.checkdate = z.lastCheckdate) as lastClose,
		z.lastCheckdate,
		z.total_count_days,
		z.avg_news_count_of_each_day,
		z.min_and_max_news_count_diff_of_each_day_in_precentage
	FROM(
		SELECT 
		c.symbol, 
		c.close, 
		c.checkdate,
		(SELECT min(d.checkdate) from patrick_strategy_1 d where d.symbol=c.symbol) as firstCheckdate,
		(SELECT max(e.checkdate) from patrick_strategy_1 e where e.symbol=c.symbol) as lastCheckdate,
		(SELECT count(e.checkdate) from patrick_strategy_1 e where e.symbol=c.symbol) as total_count_days,
		(SELECT avg(e.resultcount) from patrick_strategy_1 e where e.symbol=c.symbol) as avg_news_count_of_each_day,
		(SELECT (max(e.resultcount) - min(e.resultcount)) / max(e.resultcount) * 100 from patrick_strategy_1 e where e.symbol=c.symbol) as min_and_max_news_count_diff_of_each_day_in_precentage
		from patrick_strategy_1 c
		WHERE c.symbol in 
		( SELECT a.symbol FROM ( SELECT symbol, sum(resultcount) as resultcounrsumup FROM patrick_strategy_1 group by symbol, resultcount order by resultcounrsumup desc limit 10 ) a )
	) z
) x
order by x.checkdate desc








**2. find the median**
SET @count := 0;
SELECT a.id, a.resultcount FROM (
   SELECT (@count:=@count+1) as id, resultcount FROM patrick_strategy_1 WHERE symbol='NLY' ORDER BY resultcount
) a WHERE a.id = (@count/2)





**3. find each symbol first and latest date data**
SELECT * FROM (	
	SELECT g.symbol, e.newsCount, e.newsDaysCount, h.maxClose, h.minClose, e.firstCheckDate, e.firstClose, f.lastCheckDate, f.lastClose, ((f.lastClose - e.firstClose)/e.firstClose*100) AS closeChange FROM 
	(
		SELECT distinct symbol from patrick_strategy_1
	) g
	INNER JOIN
	(
		SELECT a.symbol, a.close as firstClose, b.firstCheckDate, b.newsCount, b.newsDaysCount FROM patrick_strategy_1 a
		INNER JOIN ( 
			SELECT min(checkdate) as firstCheckDate, sum(ResultCount) as newsCount, symbol, count(*) as newsDaysCount FROM patrick_strategy_1 group by symbol 
		) b
		ON a.Symbol = b.symbol and a.CheckDate = b.firstCheckDate
	) e ON g.symbol = e.symbol
	INNER JOIN
	(
		SELECT c.symbol, c.close as lastClose, d.lastCheckDate FROM patrick_strategy_1 c
		INNER JOIN ( 
			SELECT max(checkdate) as lastCheckDate, symbol FROM patrick_strategy_1 group by symbol 
		) d
		ON c.Symbol = d.symbol and c.CheckDate = d.lastCheckDate
	) f ON g.symbol = f.symbol
	INNER JOIN(
		SELECT symbol, max(close) as maxClose, min(close) as minClose from patrick_strategy_1 group by symbol
	) h ON g.symbol = h.symbol
) h
ORDER BY h.closeChange


**4. simple check order by checkdate**
select * from patrick_strategy_1 where symbol='SHOP' order by checkdate



**5. check the accl Resut Count of symbol**
SELECT 
c.symbol, 
d.firstCheckDate, 
c.checkdate, 
(SELECT SUM(ResultCount) FROM patrick_strategy_1 WHERE symbol='SHOP' AND checkdate between d.firstCheckDate and c.checkdate) 
FROM patrick_strategy_1 c
INNER JOIN(
	SELECT a.symbol, b.firstCheckDate, a.checkdate FROM patrick_strategy_1 a
	INNER JOIN (
		SELECT symbol, min(checkdate) as firstCheckDate, checkdate FROM patrick_strategy_1 WHERE symbol='SHOP' group by symbol 
	) b
	ON a.symbol = b.symbol
	ORDER BY a.symbol, a.checkdate
) d
ON c.symbol = d.symbol
WHERE c.checkdate between d.firstCheckDate and d.checkdate
group by c.symbol, c.checkdate


# GooleNewsCount_Strategy2
# the AWS lambda program: Investment_Stratgy_CountTheNews collect the data to DB table patrick_strategy_1

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


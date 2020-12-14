1) Вместо: /api/v1/position и вместо параметра qurrentQty
Ставим: https://www.okex.com/docs/en/#futures-only ("instrument_id":"BTC-USD-201225"), в ответе графа long_qty и short_qty нас интересует.
 
2) long_qty или short_qty != 0
Во всех других ботах, которые ты писал Bitmex, Binance, Bybit там одно значение проверяется, а вот у биржи Okex нужно два значения в ответе проверять long_qty и short_qty, например если хотя бы в одном из long_qty или short_qty появилось число >0 или <0 (то есть появилось число не равное нулю) то ждёт таймер 555 и возврат к первому пункту. А если у обоих long_qty и short_qty стоит по 0 то тогда идём к следующему действию торгового бота.


3) Вместо: /api/v/1/execution и вместо TEXT == Liquidation (данный запрос проверял наша последняя сделка закрылась ли она через Liquidation)
Данный этап не нужен больше, его нужно удалить. На скриншоте зачеркнул, что нужно удалить.


4) Вместо запроса: position?filter= для проверки плеча
Ставим: https://www.okex.com/docs/en/#futures-leverage (Интересует BTC-USD) в ответе поле leverage

5) Вместо: установить плечо на 50 POST position/position_get
Ставим: https://www.okex.com/docs/en/#futures-set_leverage
POST /api/futures/v3/accounts/btc-usd/leverage{"leverage":"50"}

6-7) Вместо: (Слева и справа): сделать запрос api/v1/instrument askPrice а также сделать запрос api/v1/instrument bidPrice. 
Ставим: https://www.okex.com/api/futures/v3/instruments/BTC-USD-201225/ticker (слева в ответе будет графа best_ask число нам нужно, а справа  графа best_bid число нам нужно).

Эти данные вставлялись ещё ниже в формулах
Вместо: 
слева: orderQty = int(askPrise * $Fnum * 47) 
справа: orderQty = int(bidPrice * $Fnum * 48)
Ставим: 
слева: size = int(best_ask * $Fnum * 47)
справа: size = int(best_bid * $Fnum * 48)


8) 
(слева) Вместо: отправляем запрос /api/v1/order orderQty=$ordetQty 
Ставим: https://www.okex.com/docs/en/#futures-orders 
POST /api/futures/v3/order{"order_type":"4","instrument_id":"BTC-USD-201225","type":"1","size":"1111"}

size=$size

(справа) Вместо: отправляем запрос /api/v1/order orderQtu=$ordetQty 
Ставим: https://www.okex.com/docs/en/#futures-orders 
POST /api/futures/v3/order{"order_type":"4","instrument_id":"BTC-USD-201225","type":"2","size":"1111"}

size=$size


9) Вместо: Отправляем запрос /api/v1/position извлекаем avgEntryPrice (слева)
Ставим: https://www.okex.com/docs/en/#futures-only ("instrument_id":"BTC-USD-201225"), в ответе графа long_avg_cost нас интересует.
Извлекаем: long_avg_cost

Вместо: Отправляем запрос /api/v1/position извлекаем avgEntryPrice (справа)
Ставим: https://www.okex.com/docs/en/#futures-only ("instrument_id":"BTC-USD-201225"), в ответе графа short_avg_cost нас интересует.
Извлекаем: short_avg_cost


Правим:
слева price = int(long_avg_cost + (long_avg_cost * 0.045))
справа price = int(short_avg_cost - (short_avg_cost * 0.057))

10) 
Вместо: отправляем запрос /api/v1/order  (слева заменяется на то что ниже написал)
Ставим: https://www.okex.com/docs/en/#futures-orders 
POST /api/futures/v3/order{"order_type":"0","instrument_id":"BTC-USD-201225","type":"3","price":"12500","size":"1111"}

size=$size (данный параметр второй раз не высчитывается, тут число тоже самое что и в первом запросе вставлялось СЛЕВО а точнее этап 8 там вставлялось)
price=$price

Вместо: отправляем запрос /api/v1/order  (справа заменяется на то что ниже написал)
Ставим: https://www.okex.com/docs/en/#futures-orders 
POST /api/futures/v3/order{"order_type":"0","instrument_id":"BTC-USD-201225","type":"4","price":"12500","size":"1111"}

size=$size (данный параметр второй раз не высчитывается, тут число тоже самое что и в первом запросе вставлялось СПРАВО а точнее этап 8 там вставлялось)
price=$price

----------------------

Ключи:
KEY = ''
SECRET = ''
BASE_URL = 'https://www.okex.com' # production base url



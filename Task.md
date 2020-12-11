1) Вместо: /api/v1/position и вместо параметра qurrentQty
Ставим: https://bybit-exchange.github.io/docs/inverse/?python#t-myposition (symbol BTCUSD), в ответе графа size нас интересует.

2) size != 0

3) Вместо: /api/v/1/execution и вместо TEXT == Liquidation (данный запрос проверял наша последняя сделка закрылась ли она через Liquidation)
Данный этап не нужен больше, его нужно удалить. На скриншоте зачеркнул, что нужно удалить.


4) Вместо запроса: position?filter= для проверки плеча
Ставим: https://bybit-exchange.github.io/docs/inverse/?console#t-position (symbol BTCUSD) в ответе поле leverage

5) Вместо: установить плечо на 50 POST position/position_get
Ставим: https://bybit-exchange.github.io/docs/inverse/?python#t-setleverage (symbol BTCUSD)

6-7) Вместо: (Слева и справа): сделать запрос api/v1/instrument askPrice а также сделать запрос api/v1/instrument bidPrice. 
Ставим: https://api.bybit.com/v2/public/orderBook/L2?symbol=BTCUSD&depth=1 (слева, в ответе будет 1: там графа price число нам нужно, а справа данное 0: там графа price число нам нужно).

Эти данные вставлялись ещё ниже в формуле orderQty = int(askPrise * $Fnum * 47) и orderQty = int(bidPrice * $Fnum * 48)
В итоге: 
qty = int(1price * $Fnum * 47)
qty = int(0price * $Fnum * 48)


8) 
(слева) Вместо: отправляем запрос /api/v1/order orderQty=$ordetQty 
Ставим: https://bybit-exchange.github.io/docs/inverse/?python#t-placeactive side="Buy",symbol="BTCUSD",order_type="Market",qty=1111,time_in_force="FillOrKill"

qty=$qty

(справа) Вместо: отправляем запрос /api/v1/order orderQtu=$ordetQty 
Ставим: https://bybit-exchange.github.io/docs/inverse/?python#t-placeactive side="Sell",symbol="BTCUSD",order_type="Market",qty=1111,time_in_force="FillOrKill"

qty=$qty


9) Вместо: Отправляем запрос /api/v1/position извлекаем avgEntryPrice (слева и справа)
Ставим: https://bybit-exchange.github.io/docs/inverse/?python#t-myposition (symbol BTCUSD), в ответе графа entry_price нас интересует.
Извлекаем: entry_price

Правим:
слева price = int(entry_price + (entry_price * 0.045))
справа price = int(entry_price - (entry_price * 0.057))

10) 
Вместо: отправляем запрос /api/v1/order  (слева заменяется на то что ниже написал)
Ставим: https://bybit-exchange.github.io/docs/inverse/?python#t-placeactive side="Sell",symbol="BTCUSD",order_type="Limit",qty=1111,price=12500,time_in_force="GoodTillCancel"

qty=$qty (данный параметр второй раз не высчитывается, тут число тоже самое что и в первом запросе вставлялось СЛЕВО а точнее этап 8 там вставлялось)
price=$price

Вместо: отправляем запрос /api/v1/order  (справа заменяется на то что ниже написал)
Ставим: https://bybit-exchange.github.io/docs/inverse/?python#t-placeactive side="Buy",symbol="BTCUSD",order_type="Limit",qty=1111,price=12500,time_in_force="GoodTillCancel"

qty=$qty (данный параметр второй раз не высчитывается, тут число тоже самое что и в первом запросе вставлялось СПРАВО а точнее этап 8 там вставлялось)
price=$price

----------------------

Ключи:
KEY = 'O0WIAYP8jc4tLZ03dc'
SECRET = 'MsoezA2ruNnEGoaAQNHVXAQxL2GFLcHhLtbl'
BASE_URL = 'https://api.bybit.com' # production base url


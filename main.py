# import words
#
# text = 'реДиска Дом редиСКа ornoesring wkemfoweimf ЖОПА'
#
#
# def censor(x):
#     text_1 = ''
#     if isinstance(x, str):
#         for i in x.split():
#             # i = i.lower()
#             if i.lower() in words.WORDS:
#                 text_1 += i.replace(i, f'  {i[0]}{"*" * (len(i) - 1)}   ')
#             else:
#                 text_1 += '   ' + i + '   '
#         text_1 = ' '.join(text_1.split())
#         return text_1
#
#
# a = censor(text)
# print(a)

#
# import logging
#
# logger = logging.getLogger('dev')
# logger.setLevel(logging.DEBUG)
#
# logging.debug('Это отладочное сообщение')
# logging.info('Это информационное сообщение')
# logging.warning('Это предупреждающее сообщение')
# logging.error('Это сообщение об ошибке')
# logging.critical('Это критическое сообщение')
#
# from apscheduler.schedulers.blocking import BlockingScheduler
# import datetime
# from datetime import date
#
#
# def aps_test(x):
#     print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), x)
#
#
# scheduler = BlockingScheduler()
# scheduler.add_job(func=aps_test, args=['Привет'], trigger='cron', second='*/5')
# scheduler.start()


# print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
# print(date.today())
# print(datetime.datetime.now())
# print(datetime.datetime.now().date())
# print(datetime.datetime.now().time())
# print(datetime.time(20, 5))
# print(datetime.date(2022, 10, 14))
# print(';')
# dt_now = datetime.datetime.utcnow()
# print(dt_now)

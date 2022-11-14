import calendar

from program import program
import time

from requests_to_server.telegram import broadcast_to_telegram

# arbs = []
while True:
    #     # new_arbs = []
    #     # try:
    #     # new_arbs = program(arbs)
    program()
    #     # except Exception as e:
    #     #     broadcast_to_telegram("GRESKA!!!!!!!!!!!!!!!!!!!")
    #     #     broadcast_to_telegram(e)
    #
    #     # arbs = new_arbs[:]
    time.sleep(180)

# time.strftime('%H:%M:%S', time.gmtime(1667435400000))
# print(calendar.timegm(time.strptime('Jul 9, 2022 @ 20:02:00 UTC', '%b %d, %Y @ %H:%M:%S UTC')))
# print(calendar.timegm(time.strptime('Jul 9, 2022 @ 20:07:00 UTC', '%b %d, %Y @ %H:%M:%S UTC')))

# print(calendar.timegm(time.strptime('2022-11-14T01:00:00', '%Y-%m-%dT%H:%M:%S')))

# print(int(time.time()))
#
# # 1667747481        - malo pre
# # 1667747543        - sad
# # 1657396978        -  Jul 9, 2022 @ 20:02:58 UTC
# # 1667435400 000     - trazeno
# # 1668387600

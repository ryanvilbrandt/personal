# from re import search, compile
# from ast import literal_eval
#
# a = """
# INFO in zapy: zapy_post: url=http://zapy-bip.sea-001.zonarsystems.net:8888/hos/get_driver_violation_history, data={'account': 'int6354', 'start_epoch': 1550275200, 'end_epoch': 1550860042, 'driver_ids': 59, 'violation_type': 'DD,WD,DOD,7D,8D,DR,WOD,WS,DFD'}"""
#
# reg = compile("url=http://(.*?), data=(.*?)$")
# m = search(reg, a)
# url = m.group(1)
# data = literal_eval(m.group(2))
#
# print('callz {} "{}"'.format(url, "&".join("{}={}".format(k, v) for k, v in data.items())))

from os import getcwd

print(getcwd())
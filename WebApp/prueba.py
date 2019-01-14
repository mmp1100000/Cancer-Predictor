
# import plotly.offline as py
# import plotly.graph_objs as go
#
# import numpy as np
#
# x = np.random.randn(500)
# data = [go.Histogram(x=x)]
#
# py.iplot(data, filename='basic histogram')
# first_plot_url = py.plot(data, filename='basic_histogram', auto_open=False,)
# print(first_plot_url)
#
import hashlib

password = "1234"
input_password = hashlib.sha256(password.encode("utf8"))
hex_dig = input_password.hexdigest()
print(hex_dig)
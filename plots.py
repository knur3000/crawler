import matplotlib.pyplot as plt
import numpy as np
from crawler_get_data import run

data = run()["Top"]

words = set(data.keys())
y_pos = np.arange(len(words))
count = list(data.values())

plt.bar(y_pos, count, align='center', alpha=0.5)
plt.xticks(y_pos, words)
plt.ylabel('Words')
plt.title('Count')

plt.show()

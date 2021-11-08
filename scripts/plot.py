import pandas as pd
import numpy as np
from ast import literal_eval
import sys
import matplotlib.pyplot as plt

systems = ['EvoLearner', 'CELOE', 'SPaCEL', 'Aleph']
x = [5, 10, 30, 60, 120, 180, 240, 300]
#x = [5, 10, 30]

def parse_means(frames):
    #print(frames)
    means = []
    for frame in frames:
        df = pd.read_csv(frame, na_values=' ').iloc[:,1:]
        df = df.applymap(lambda x: literal_eval(x)[0] if not isinstance(x, float) else 0)
        means.append(float(df.mean(axis=1)))
        #print(means)
    return means

system_means = []
for s in systems:
    #print(s)
    system_means.append(parse_means([arg for arg in sys.argv[1:] if s.lower() in arg]))

for idx, means in enumerate(system_means):
    #print(means)
    plt.plot(x, means, label=systems[idx])

plt.xlabel('seconds')
plt.ylabel('F-measure')
plt.title('F-measure over time')
#plt.legend(loc='upper right', bbox_to_anchor=(1, -0.5))
plt.legend()
#plt.show()
plt.savefig('results/runtime_plot.png')

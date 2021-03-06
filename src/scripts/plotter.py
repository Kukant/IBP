import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as mpatches
import matplotlib as mpl
import os
import glob

mpl.rcParams['figure.dpi'] = 300

csvs_dir = 'csvs/4/*3-conv*5-epochs*blahblah'
files = glob.glob(csvs_dir) + glob.glob('csvs/4/*old*')
load = lambda file: np.genfromtxt(file, delimiter=',', names=['Wall time', 'Step', 'Value'])
data_list = [(load(f), f) for f in files]

fig = plt.figure()

ax = fig.add_subplot(111)

ax.set_xlabel("Epocha")
ax.set_ylabel("Úspěšnost")
ax.grid(True)
ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

i = 0
label = None
color = None
for data, filename in data_list:
    #numbers = [int(s) for s in filename.split("-") if s.isdigit()]
    #label = "{}x{}".format(numbers[0], numbers[1])
    #color = "r" if "300" in filename else "b"
    ax.plot(data["Step"], data["Value"], color=color, label=label, antialiased=True,)


if False:
    legend_dict = {'300x300': 'red', '200x200': 'blue'}
    patchList = []
    for key in legend_dict:
            data_key = mpatches.Patch(color=legend_dict[key], label=key)
            patchList.append(data_key)

    ax.legend(handles=patchList)

#ax.legend()
#plt.show()
plt.savefig("random-old.png")

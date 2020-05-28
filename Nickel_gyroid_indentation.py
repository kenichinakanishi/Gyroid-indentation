# change working directory and collate data for sample
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os

folder = os.getcwd() + r'\Indentation Data\750nm_nickel'
os.chdir(folder)

# import all files from directory
all_files_Ni = [f for f in os.listdir(folder) if f.endswith('.txt')]

df_from_each_fileNi = (pd.read_csv(f, sep="\t", header=1, encoding="ISO-8859-1") for f in all_files_Ni)

nfilesNi = len(all_files_Ni)

# create list of keys - the indentation points
x = 1
Ni_list = ["Point %d" % (x)]
for x in range(2, nfilesNi + 1):
    Ni_list.append("Point %d" % x)

# Create indexed dataframe
concatenated_Ni = pd.concat(df_from_each_fileNi, keys=Ni_list)
concatenated_Ni.index.names = ['Point', 'Pressure']
# trim off unreliable data from shallow indentation depths
concatenated_Ni = concatenated_Ni.drop(concatenated_Ni[(concatenated_Ni['hc(nm)'] < 40)].index, inplace=False)


# Get average data and statistics
Ni_means_pos = concatenated_Ni.loc["Point %d" %0:, :]
Ni_means_pos.index.names = ['Point', 'Pressure']
Ni_means = Ni_means_pos.mean(level=['Pressure'])
Ni_stddev = Ni_means_pos.std(level=['Pressure'])

# Plot Ni Data
ax1 = plt.subplot(211)
for x in range(1, nfilesNi + 1):
    Hx1 = concatenated_Ni.loc["Point %d" % (x), ['hc(nm)']]
    Ey1 = concatenated_Ni.loc["Point %d" % (x), ['Er(GPa)']]
    plt.plot(Hx1, Ey1, label=("Point %d" % (x)))

plt.ylabel('E (GPa)')
plt.title('Ni Modulus Indentation')
plt.xlabel('Indentation Depth (nm)')
plt.xlim(xmin=50)
plt.legend()

axHard = plt.subplot(212, sharex=ax1)
for x in range(1, nfilesNi + 1):
    Hx1 = concatenated_Ni.loc["Point %d" % (x), ['hc(nm)']]
    Ey1 = concatenated_Ni.loc["Point %d" % (x), ['H(GPa)']]
    plt.plot(Hx1, Ey1, label=("Point %d" % (x)))
plt.title('Ni Hardness Indentation')
plt.ylabel('Hardness (GPa)')
plt.xlabel('Indentation Depth (nm)')
plt.xlim(xmin=50)
# plt.legend()
fig = plt.gcf()
fig.set_size_inches(14.5, 10.5)
plt.show()

# Mean and error bar plot
NierrorE = Ni_stddev['Er(GPa)']
NierrorH = Ni_stddev['H(GPa)']

Ni_ax = plt.subplot(211)
Hx_Ni = Ni_means['hc(nm)']
Ey_Ni = Ni_means['Er(GPa)']
plt.plot(Hx_Ni, Ey_Ni, label=("Point %d" % (x)))
plt.fill_between(Hx_Ni, Ey_Ni - NierrorE, Ey_Ni + NierrorE,
                 alpha=0.3, edgecolor='#3F7F4C', facecolor='#089FFF',
                 linewidth=0)
plt.ylabel('E (GPa)')
plt.title('Ni Modulus Indentation')
plt.legend()

Mean_axHard = plt.subplot(212)
Hx_Ni = Ni_means['hc(nm)']
Hy_Ni = Ni_means['H(GPa)']
plt.plot(Hx_Ni, Hy_Ni, label=("Point %d" % (x)))
plt.fill_between(Hx_Ni, Hy_Ni - NierrorH, Hy_Ni + NierrorH,
                 alpha=0.3, edgecolor='#3F7F4C', facecolor='#089FFF',
                 linewidth=0)
plt.ylabel('Hardness (GPa)')
plt.xlabel('Indentation Depth (nm)')
plt.title('Ni Hardness Indentation')
# plt.legend()
fig = plt.gcf()
fig.set_size_inches(14.5, 10.5)
plt.show()

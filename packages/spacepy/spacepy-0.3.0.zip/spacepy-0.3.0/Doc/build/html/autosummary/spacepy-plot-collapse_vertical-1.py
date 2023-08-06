import spacepy.plot.utils
import matplotlib.pyplot as plt
fig = plt.figure()
ax0 = fig.add_subplot(311)
ax1 = fig.add_subplot(312)
ax2 = fig.add_subplot(313)
ax0.plot([1, 2, 3], [1, 2, 1]) #just make some lines
# Expected:
## [<matplotlib.lines.Line2D object at 0x0000000>]
ax1.plot([1, 2, 3], [1, 2, 1])
# Expected:
## [<matplotlib.lines.Line2D object at 0x0000000>]
ax2.plot([1, 2, 3], [1, 2, 1])
# Expected:
## [<matplotlib.lines.Line2D object at 0x0000000>]
spacepy.plot.utils.collapse_vertical([ax0, ax1], [ax2])

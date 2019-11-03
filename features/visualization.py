import numpy as np
import matplotlib.pyplot as plt


def lighten_color(color, amount=0.5):
    """
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])


input = [[0.39188915, 0.6204959], [0.74632937, 0.76435804], [0.9796736, 0.39036557], [0.5621101, 0.9073347], [0.543051, 0.103109054], [0.94108874, 0.19921248], [0.27434537, 0.7890164], [0.96881443, 0.85726005], [0.599985, 0.5510349], [0.6892647, 0.5528635], [0.083855, 0.97440565]]
output = [[0.083855, 0.97440565], [0.6892647, 0.5528635], [0.5621101, 0.9073347], [0.083855, 0.97440565], [0.9796736, 0.39036557], [0.083855, 0.97440565], [0.599985, 0.5510349], [0.083855, 0.97440565], [0.39188915, 0.6204959], [0.083855, 0.97440565], [0.74632937, 0.76435804], [0.083855, 0.97440565], [0.96881443, 0.85726005], [0.083855, 0.97440565], [0.94108874, 0.19921248], [0.083855, 0.97440565], [0.27434537, 0.7890164]]

xs,ys = [],[]
for x,y in input:
    xs.append(x)
    ys.append(y)

c = ['b']*(len(xs)-1) + ['r']
plt.scatter(xs,ys,color = c)

c= 'b'
for i in range(len(output) - 1):
    xs = [output[i][0],output[i+1][0]]
    ys = [output[i][1],output[i+1][1]]
    plt.plot(xs,ys,color=c)
    c = lighten_color(c,0.9)

plt.show()

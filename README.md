![](https://github.com/SanPen/GridCal/blob/master/GridCal_banner.png)


This software aims to be a complete platform for power systems research and simulation. [Watch the video](https://youtu.be/O6lv-d8z39k)

![](https://github.com/SanPen/GridCal/blob/master/GridCal.png)

Since it is pure Python, It works for Windows, Linux and OSX.

It is based on PyPower (MatPower for python) and it is compatible with Matpower files, and many more to come.

Some of the features you'll find already are:

- Power flow:
  - Newton Raphson.
  - Gauss-Seidel.
  - Current iteration (or Zbus)
  - Newton Raphson Iwamoto (robust Newton Raphson)
  - Holomorphic Embedding Power flow.
  - DC approximation.
  - Predictor-corrector Newton-Raphson from the base solution.
  
- The ability to handle island grids in all the simulation modes.

- Time series with load and generation profiles. 
  - It includes a nice profile import window.
  - Continuation power flow from step `t-1` to step `t`

- Bifurcation point with predictor-corrector Newton-Raphson and Holomorphic embedding.

- Monte Carlo simulation based on the input profiles. (Stochastic power flow)

Visit the [Wiki](https://github.com/SanPen/GridCal/wiki) to learn more and get started.

Send feedback and requests to santiago.penate.vera@gmail.com.

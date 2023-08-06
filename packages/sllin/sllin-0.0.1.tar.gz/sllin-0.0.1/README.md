# SLLin

![coverage](https://gitlab.com/Menschel/sllin/badges/master/coverage.svg)

[Documentation](https://menschel.gitlab.io/sllin/)

An alternative python lib for SLCAN based LIN adapters currently only for the [one from UCANDevices](https://ucandevices.github.io/ulc.html).

# original lib is broken by design
[UCAN's original python lib](https://github.com/uCAN-LIN/LinUSBConverter) is a demo at best and surely not safe for work.
- multiple class definitions for LinFrame
  
- unsafe threading methods, e.g. multiple threads try to read from the same serial device at the same time
  
- worker threads or not set to daemon

- sequential use of the LUC is not possible because the serial port dies on you

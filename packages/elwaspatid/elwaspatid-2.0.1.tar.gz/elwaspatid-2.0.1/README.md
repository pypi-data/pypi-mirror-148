# ELastic WAve SPAce-TIme Diagrams

[![Documentation Status](https://readthedocs.org/projects/elwaspatid/badge/?version=latest)](https://elwaspatid.readthedocs.io/en/latest/?badge=latest) 
[![PyPI version](https://badge.fury.io/py/elwaspatid.svg)](https://badge.fury.io/py/elwaspatid)

`elwaspatid` is a Python module for the computation of space-time diagrams for
the propagation of elastic waves in 1D rods. The rods can have impedance variations
along the propagation axis, and it is possible to consider several rods in contact.

Initial conditions can be:

* a prescribed input force at the left end of the left (first) rod;
* a prescribed velocity of the left rod, which impacts the next rod.

Boundary conditions can be:

* free end;
* fixed end;
* contact interface with another rod;
* infinite end (ie. anechoic condition).

This module is the extention of the work of the following reference:

Bacon, C. (1993). Numerical prediction of the propagation of elastic waves in 
longitudinally impacted rods : Applications to Hopkinson testing. 
*International Journal of Impact Engineering*, 13(4), 527‑539. 
https://doi.org/10.1016/0734-743X(93)90084-K

![Example of force space-time diagram: two successive compression pulses traveling down two bars (with identical cross-section) in contact.](docs/auto_examples/images/sphx_glr_plot_1_WP2_001.png)


## Installation

`pip install elwaspatid`

## Documentation

[ReadTheDocs](https://elwaspatid.readthedocs.io)

## Usage

See the examples in the documentation and in the `examples` folder of the github source.

## Testing

To test the installation, run all the examples (manually, or by compiling the docs).

The examples can be retrieved from the [Github repository](https://github.com/dbrizard/elwaspatid) 
or from the section [Examples of diagrams](https://elwaspatid.readthedocs.io/en/latest/auto_examples/index.html).

*Note: there are no automated tests of the module, because the aim of the module is to plot propagation diagrams and the underlying data is made of large matrices. However, running all the examples will test all the functionnalities of the module and one can check that we get the expected results/diagrams (ie. the correct relfection/transmission of waves).*


## Community guidelines
### Contributing
Contributions are welcome, be it improvements or new functionalities. Either 
contact directly the author, or use [Pull Requests](https://github.com/dbrizard/elwaspatid/pulls).

Refering to the example called [Under the hood](https://elwaspatid.readthedocs.io/en/latest/auto_examples/plot_6_underHood.html) 
may be a good idea before diving into the code.

### Reporting issues or problems
Use [issues](https://github.com/dbrizard/elwaspatid/issues). Be sure to fully 
describe your issue or problem. If applicable, provide a minimal working example 
(MWE).

### Support
Do not forget to [read the docs!](https://elwaspatid.readthedocs.io) 
Several examples are provided, showing all the available functionalities. They
should be a good starting point. Check the references (articles and books) 
listed in the examples introduction if you need mechanical background.

Also search for [issues](https://github.com/dbrizard/elwaspatid/issues). 
 

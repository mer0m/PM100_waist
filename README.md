# PM100_waist

Make your waist measurment easy with a Thorlabs PM100D.

## Setup
```
==============================
Prepare the setup
==============================
laser             PM100D
-->------------------] in W
        |
        |
        |

 knife at z and x=0mm

==============================
move the knife and press enter
==============================
laser             PM100D
-->-----|------------] in W
        |
        |

 knife at z and x+=0.05mm

==============================
```

## Acquisition
`pm100d_waist.py` acquire the optical power along transverse section at *z* mm.

Create your measurement folder
`mkdir -p my/best/measurement && cd my/best/measurement`

Run the acquisition program with the `-o` option to set z=123mm as terminaison of the filename.
All the files will be saved in the current folder
`path/to/the/program/location/pm100d_waist.py -o 123`

Press *enter* to get a power value, and move the knife of 0.05 mm, repress enter and again and again and again and again and again and again...
When the section is done, enter the new z value in the prompt, the program will inform you that a new file is created.

At the end, press `CTRL + C` and enter to quit *properly*.

## Post-processing
`fit_waist.py` fit each waist of each section and compute the *w0* and the *z0* of the beam.

`./fit_waist.py`

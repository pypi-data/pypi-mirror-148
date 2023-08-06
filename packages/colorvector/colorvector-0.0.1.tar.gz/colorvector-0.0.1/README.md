# Color Vector

A simple utility that given two colors in RBG format and a number of desired intervals, returns an array of colors
evenly distributed between (and including) the two starting colors.

## How to use it

Import the ```get_palette``` function and feed it your starting and ending colors as arrays of three integers (e.g. [0,0,0] and [255,255,255]) and an integer representing the number of colors you want in the palette (includes the two colors you gave it).

It will return an array of RBG values that fall on the vector between the starting and ending colors that are equidistant from each other (rounded to the nearest integer).

So, if you give it: ```[0,0,0], [255,255,255], 3```
It will return: ```[(0, 0, 0), (128, 128, 128), (255, 255, 255)]```

### How the math works:

```Point 1:  (1,2,3)    Point 2:  (5, 0, -1).  
To lay out the points from Point 1 to Point 2,
Subtract (5,0,-1) - (1,2,3) to get the direction vector for the line.  In this case, <4, -2, -4>.

Then create the parametric equation for the line <x,y,z> = t * <4, -2, -4> + <1,2,3>

This set up leads to: 
when t = 0, <x,y,z> = 0* <4, -2, -4> + <1,2,3>  = < 1,2,3 >
when t = 1, <x,y,z> = 1* <4, -2, -4> + <1,2,3>  = < 5,0,-1 >

To distribute points evenly along this interval, distribute t evenly at the fractional size you need.  
For example for 6 points between and including both Point 1 and Point 2, divide into 5ths by letting 
t=0, .2, .4, .6, .8, 1.  ```
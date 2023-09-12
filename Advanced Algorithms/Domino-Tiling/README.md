# Domino Tiling
## Description:
Our professor asked us to write an algorithm that solves the domino tiling puzzle. An example of the puzzle is included as a .png file. You are under the assumption that you have exactly 1 domino tile for each possible combination of numbers (1-1, 1-2, ... 1-6, 2-2, 2-3, ... 2-6, 3-1, ... 6-6). Your job is to find a tiling of these dominos that covers the board (where the numbers on each domino matches the number on they are covering. Included is the __C++__ code that does so.

My algorithm:

1. Checks for places where tiles have to go
    - Tiles that only have one place (if there is only one case of 1 being next to 6 then tile 1-6 must go there)
    - Untiled spaces that have 3 sides filled, leaving only open adjacent place, can only be tiled by filling that one adjacent place

2. Tiles the tiles with only one place to go
3. Returns to step one
4. If the board remains unchanged after 2 iterations in a row then we are out of tiles that must be placed. We then would have to recursively solve the problem however this is where the problem becomes NP-complete so we did not solve it this way.

The purpose of this project was to introduce us to linear programming. Our professor wanted us to use a package in c to do so. The package was somewhat clunky and outdated. After the entire class kept coming back to him with questions and problems from using the afformentioned package, he scrapped that part of the project and we just had to submit a physical list of constraints that would be applied if we accomplished the project with linear programming. I am not including that portion since I have a better demonstration of my linear programming abilities in the _linear-programming_ section of my portfolio.

## Results
I recieved an A on this project.
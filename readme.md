#  Image/Text to 3D Model Generator

This project allows you to convert either:
- An **image** (`.jpg` or `.png`) into a 3D model using a grayscale heightmap approach.
- A **text prompt** into a basic 3D model (currently a placeholder cube for demonstration).

## Features

- Background removal from input images using `rembg`
- Converts 2D grayscale image data into a 3D mesh (OBJ and STL)
- Basic 3D model generation from text prompt
- Outputs downloadable `.obj` and `.stl` files
- Simple visualization using `matplotlib` or `pyrender`

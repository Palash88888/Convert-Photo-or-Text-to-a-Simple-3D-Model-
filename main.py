import os
import torch
from rembg import remove
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pyrender
import trimesh
import open3d as o3d

 #   === CONFIGURATION ===
input_type = "image"  # 'image' or 'text'
input_value = "Car.jpg" if input_type == "image" else "A small toy car"
output_obj = "output_model.obj"
output_stl = "output_model.stl"

# === IMAGE PROCESSING FUNCTION ===
def process_image(image_path, output_model_path):
    print(f"Processing image: {image_path}")

    # Load image and remove background
    image = Image.open(image_path).convert("RGBA")
    no_bg = remove(image)

    # Convert to grayscale for heightmap
    gray = no_bg.convert("L")
    arr = np.array(gray).astype(np.float32) / 255.0

    h, w = arr.shape
    vertices, faces = [], []
    for y in range(h):
        for x in range(w):
            z = arr[y, x] * 5  # height scaling
            vertices.append((x, y, z))

    for y in range(h - 1):
        for x in range(w - 1):
            v1 = y * w + x
            v2 = v1 + 1
            v3 = v1 + w
            v4 = v3 + 1
            faces.append((v1, v3, v2))
            faces.append((v2, v3, v4))

    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    mesh.export(output_model_path)
    print(f"3D model saved as OBJ: {output_model_path}")
    return mesh


# === TEXT PROCESSING FUNCTION ===
def process_text(text_prompt, output_model_path):
    print(f"Received text prompt: {text_prompt}")
    mesh = trimesh.creation.box(extents=[1, 1, 1])
    mesh.export(output_model_path)
    print(f"Placeholder 3D cube saved as OBJ: {output_model_path}")
    return mesh


# === MAIN EXECUTION ===
if input_type == "image":
    if not os.path.exists(input_value):
        raise FileNotFoundError(f"Image file not found: {input_value}")
    mesh = process_image(input_value, output_obj)

elif input_type == "text":
    mesh = process_text(input_value, output_obj)

else:
    raise ValueError("input_type must be 'image' or 'text'.")

# === Export STL version ===
mesh.export(output_stl)
print(f"STL version saved as: {output_stl}")


# === VISUALIZATION ===

# 1. Using Matplotlib for basic 3D visualization
def visualize_with_matplotlib(mesh):
    vertices = mesh.vertices
    faces = mesh.faces

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for face in faces:
        v1, v2, v3 = vertices[face[0]], vertices[face[1]], vertices[face[2]]
        x = [v1[0], v2[0], v3[0]]
        y = [v1[1], v2[1], v3[1]]
        z = [v1[2], v2[2], v3[2]]
        ax.plot_trisurf(x, y, z, color='cyan', linewidth=0.2, antialiased=True)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title("3D Model Visualization")
    plt.show()

# 2. Using Pyrender for more advanced rendering
def visualize_with_pyrender(mesh):
    scene = pyrender.Scene()
    mesh_pyrender = pyrender.Mesh.from_trimesh(mesh)
    scene.add(mesh_pyrender)

    viewer = pyrender.Viewer(scene, use_raymond_lighting=True, run_in_thread=True)
    print("3D model visualization window opened (close it to continue).")

# Choose the visualization method
visualize_with_matplotlib(mesh)  # For basic plot
# visualize_with_pyrender(mesh)  # Uncomment for advanced visualization


# === PROVIDE DOWNLOADABLE FILES ===
print(f"Your .obj file is available here: {os.path.abspath(output_obj)}")
print(f"Your .stl file is available here: {os.path.abspath(output_stl)}")
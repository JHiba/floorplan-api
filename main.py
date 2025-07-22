## to convert mat files to pngs

import scipy.io
import numpy as np
import cv2
import os
from glob import glob
import math

def create_door_line(x, y, width, height, orientation):
    # Returns a line segment for a door/window
    if width > 0 and height == 0:
        if orientation == 0: return [(int(x), int(y)), (int(x + width), int(y))]
        elif orientation == 2: return [(int(x), int(y)), (int(x - width), int(y))]
        else: return [(int(x), int(y)), (int(x + width), int(y))]
    elif height > 0 and width == 0:
        if orientation == 1: return [(int(x), int(y)), (int(x), int(y + height))]
        elif orientation == 3: return [(int(x), int(y)), (int(x), int(y - height))]
        else: return [(int(x), int(y)), (int(x), int(y + height))]
    else:
        return [(int(x), int(y)), (int(x), int(y))]


def draw_wall_hatching(img, pt1, pt2, thickness=3, spacing=10, hatch_len=9, angle_deg=45):
    # Convert to float for precision
    x1, y1 = map(float, pt1)
    x2, y2 = map(float, pt2)
    wall_vec = np.array([x2 - x1, y2 - y1])
    wall_len = np.linalg.norm(wall_vec)
    if wall_len == 0:
        return

    wall_dir = wall_vec / wall_len
    # Hatch direction: rotate wall_dir by angle_deg
    theta = np.radians(angle_deg)
    rot_mat = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta), np.cos(theta)]
    ])
    hatch_dir = rot_mat @ wall_dir

    # Draw hatches along the wall
    for t in np.arange(0, wall_len, spacing):
        px, py = x1 + wall_dir[0]*t, y1 + wall_dir[1]*t
        hx1 = int(px - hatch_dir[0]*hatch_len/2)
        hy1 = int(py - hatch_dir[1]*hatch_len/2)
        hx2 = int(px + hatch_dir[0]*hatch_len/2)
        hy2 = int(py + hatch_dir[1]*hatch_len/2)
        cv2.line(img, (hx1, hy1), (hx2, hy2), (60, 60, 60), 1)

def draw_column_markers(img, poly, size=5):
    # poly: array-like of (x, y)
    for x, y in poly:
        cx, cy = int(x), int(y)
        cv2.rectangle(img, (cx - size//2, cy - size//2), (cx + size//2, cy + size//2), (0, 0,0), -1)
        # Optional: use circle instead
        # cv2.circle(img, (cx, cy), size//2, (0, 0, 255), -1)


def mat_to_structgan_png(mat_path, output_path="floorplan_input.png", img_size=256):
    mat = scipy.io.loadmat(mat_path)
    # 'data' field structure may vary, adjust if needed
    data = mat['data'][0, 0]
    polygons = data['rBoundary'][0]    # Room boundaries as polygons

    canvas = np.ones((img_size, img_size, 3), dtype=np.uint8) * 255  # White background

        # Draw walls as gray lines, add hatching and column markers
    for poly in polygons:
        poly = np.array(poly)
        if poly.size == 0 or poly.shape[0] < 2:
            continue
        # Skip polygons with invalid values
        if not np.all(np.isfinite(poly)):
            continue
        pts = poly.astype(np.int32)

        # --- Draw wall segments and hatching ---
        for j in range(len(pts)):
            pt1 = tuple(pts[j % len(pts)])
            pt2 = tuple(pts[(j + 1) % len(pts)])
            cv2.line(canvas, pt1, pt2, (132, 132, 132), 3)  # Main wall
            draw_wall_hatching(canvas, pt1, pt2, thickness=3, spacing=9, hatch_len=5, angle_deg=45)
        # --- Draw columns (vertices) ---
        draw_column_markers(canvas, pts, size=5)


    # Draw doors as blue lines
    if 'doors' in data.dtype.fields:
        for door_entry in np.array(data['doors']).reshape(-1, 6):
            _, x, y, width, height, orientation = door_entry.astype(float)
            pt1, pt2 = create_door_line(x, y, width, height, int(orientation))
            cv2.line(canvas, pt1, pt2, (255, 0, 0), 4)  # Blue

    # Draw windows as green lines
    if 'windows' in data.dtype.fields:
        for win_entry in np.array(data['windows']).reshape(-1, 6):
            _, x, y, width, height, orientation = win_entry.astype(float)
            pt1, pt2 = create_door_line(x, y, width, height, int(orientation))
            cv2.line(canvas, pt1, pt2, (0, 255, 0), 2)  # Green

    # Save image
    cv2.imwrite(output_path, canvas)
    print(f"Saved: {output_path}")

def batch_convert_mat_to_png(mat_dir, output_dir="floorplan_pngs", img_size=256):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    mat_files = glob(os.path.join(mat_dir, "*.mat"))
    print(f"Found {len(mat_files)} .mat files.")

    for mat_path in mat_files:
        base = os.path.splitext(os.path.basename(mat_path))[0]
        png_path = os.path.join(output_dir, f"{base}.png")
        try:
            mat_to_structgan_png(mat_path, png_path, img_size=img_size)
        except Exception as e:
            print(f"Error with {mat_path}: {e}")



if __name__ == "__main__":
    mat_dir = r"C:/Users/hiba2/OneDrive/Desktop/Imarat/columns/matfiles/matfiles"
    output_dir = "floorplan_pngs"
    batch_convert_mat_to_png(mat_dir, output_dir, img_size=256)

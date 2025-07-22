from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import tempfile
import os
from main import create_door_line, draw_wall_hatching, draw_column_markers, mat_to_structgan_png
app = FastAPI()

@app.post("/convert-mat/")
async def convert_mat(file: UploadFile = File(...)):
    # Save the uploaded .mat file to a temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mat") as tmp_mat:
        tmp_mat.write(await file.read())
        tmp_mat.flush()
        mat_path = tmp_mat.name

    # Create a temp file for PNG output
    output_png = mat_path.replace(".mat", ".png")
    
    # Call your function (adapt to not use __main__)
    mat_to_structgan_png(mat_path, output_png, img_size=256)

    # Return the PNG as a file download
    return FileResponse(output_png, media_type="image/png", filename="output.png")

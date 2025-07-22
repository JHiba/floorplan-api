# Floorplan MAT to PNG API

This project converts `.mat` floorplan files into PNG architectural drawings with wall hatching and column markers.

## Features

 Converts MATLAB `.mat` files of room geometry to PNG images.
 Draws load-bearing wall hatching and column markers at room vertices.
 API endpoint for uploading `.mat` files and downloading PNGs.
 (Sample files included for testing.)

## Usage

1. **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```
2. **Start the API server:**
    ```
    uvicorn api:app --reload
    ```
3. **Open your browser to:**  
   [http://localhost:8000/docs](http://localhost:8000/docs)  
   to test the `/convert-mat/` endpoint.

## Sample Files

See the files for example `.mat` and `.png`.

## Project Structure

- `api.py` — FastAPI server for conversion.
- `main.py` — Main conversion logic.
- `matfiles and floorplan_pngs`-sample input/output.


# import pandas as pd
# from fastapi import FastAPI, UploadFile, HTTPException
# from fastapi.responses import FileResponse

# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from starlette.requests import Request

# from classify import classify

# app = FastAPI()




# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")

# @app.get("/", response_class=HTMLResponse)
# async def serve_ui(request: Request):
#     return templates.TemplateResponse("classify_ui.html", {"request": request})


# @app.post("/classify/")
# async def classify_logs(file: UploadFile):
#     if not file.filename.endswith('.csv'):
#         raise HTTPException(status_code=400, detail="File must be a CSV.")
    
#     try:
#         # Read the uploaded CSV
#         df = pd.read_csv(file.file)
#         if "source" not in df.columns or "log_message" not in df.columns:
#             raise HTTPException(status_code=400, detail="CSV must contain 'source' and 'log_message' columns.")

#         # Perform classification
#         df["target_label"] = classify(list(zip(df["source"], df["log_message"])))

#         print("Dataframe:",df.to_dict())

#         # Save the modified file
#         output_file = "resources/output.csv"
#         df.to_csv(output_file, index=False)
#         print("File saved to output.csv")
#         return FileResponse(output_file, media_type='text/csv')
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         file.file.close()
#         # # Clean up if the file was saved
#         # if os.path.exists("output.csv"):
#         #     os.remove("output.csv")



import pandas as pd
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import os

from classify import classify

app = FastAPI()

# Mount static folder for serving static files (e.g., CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def serve_ui(request: Request):
    return templates.TemplateResponse("classify_ui.html", {"request": request})

@app.post("/classify/")
async def classify_logs(file: UploadFile):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV.")
    
    try:
        # Read the uploaded CSV
        df = pd.read_csv(file.file)
        
        # Check if necessary columns are present
        if "source" not in df.columns or "log_message" not in df.columns:
            raise HTTPException(status_code=400, detail="CSV must contain 'source' and 'log_message' columns.")
        
        # Perform classification
        df["target_label"] = classify(list(zip(df["source"], df["log_message"])))

        print("Dataframe:", df.to_dict())

        # Ensure the resources directory exists
        resources_dir = 'resources'
        if not os.path.exists(resources_dir):
            os.makedirs(resources_dir)
        
        # Define the output file path
        output_file = os.path.join(resources_dir, "output.csv")
        print(f"Saving to: {output_file}")
        
        try:
            # Save the dataframe to the output file
            df.to_csv(output_file, index=False)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving the file: {e}")

        # Return the file as a download response
        return FileResponse(output_file, media_type='text/csv', filename="output.csv")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        file.file.close()
        
        # Clean up if the file was saved (Optional: Remove this if you want to keep the file)
        if os.path.exists(output_file):
            # Uncomment the next line if you want to remove the file after sending the response
            # os.remove(output_file)
            pass

from fastapi import FastAPI, Path, HTTPException, Query
import json

app=FastAPI()

def load_patients():
    with open('Patients_2\patients.json','r') as f:
        data= json.load(f)
    return data

@app.get("/")
def home():
    return {
        "message":"Welcome to Patient Record Management System"
    }

@app.get("/view")
def view_patients():
    return load_patients()

@app.get("/view/{patient_id}")
def view_patient(patient_id: str=Path(...,description="Enter patient ID to view it.", example="P001")):
    data = load_patients()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(404,detail="No patient record")

@app.get("/patient/sort")
def sort_patients(sort_by:str=Query(...,description="Sort on the basis of weight, height, and bmi."),\
                  order_by:str=Query('asc',description="Sort in asc or desc order.")):
    valid_fields=['weight','height','bmi']
    if sort_by not in valid_fields:
        raise HTTPException(400,detail=f"Invalid Request. Select from {valid_fields}")
    if order_by not in ['asc','desc']:
        raise HTTPException(400,detail=f"Invalid Request. Select from asc and desc")
    data=load_patients()
    order=True if order_by=="desc" else False
    sorted_data=sorted(data.values(),key=(lambda x: x.get(sort_by,0)),reverse=order)
    return sorted_data
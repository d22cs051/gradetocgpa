#
# def app(event):
#     return "Hello, world!"
from fastapi import FastAPI, Request, Form
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from convert_grade_cgpa import convert

app = FastAPI()


class Grades(BaseModel):
    grades: dict[str, list[int]] = None

# Mounting static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# templating data
templates = Jinja2Templates(directory="templates")


@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    # rendering home page
    return templates.TemplateResponse('index.html',{"request": request})
    # return {'status': 'running', 'up': True}

@app.post('/', response_class=HTMLResponse)
async def root(request: Request,sem:int = Form(...),branch:str = Form(...)):
    # setting subject list as per branch
    if sem == 1:
        if branch == 'AI':
            sub_list = ["ML","AI","IOB/CGT/OTHER","ADSA","ODS","ML-OPS"]
        if branch == 'CS':
            sub_list = ["ML","SDE","IOB/CGT/OTHER","ADSA","ODS2","STATS","LA"]
        if branch == 'DCS':
            sub_list = ["ML","AI/OTHER","IDS","ADSA","ODS1","ODS2","STATS","LA","MODELING","DA_LAB"]
    # nav to grade and course selction page
    return templates.TemplateResponse('grades.html',{"request": request,"sem":sem,"branch":branch,"sub_list":sub_list})

@app.post('/calculate',response_class=HTMLResponse)
async def calculate(request: Request):
    # making dict
    grade_dict = dict()
    # getting form req. data
    form_data = await request.form()
    # print(form_data['ML'])
    # print(form_data['ML_credit'])
    # print(await request.form())
    # processing data for cgpa cal.
    for subject in form_data:
        if len(subject.split('_')) == 1:
            grade_dict[form_data[subject]] = grade_dict.get(form_data[subject],[])
            grade_dict[form_data[subject]].append(int(form_data[subject+'_credit']))
    # print(grade_dict)
    # calculating cgpa
    totals = convert(grade_map=grade_dict)
    cgpa = f"{(totals['total_score']/totals['total_fracs']):.3f}"
    # nav to CGPA page
    return templates.TemplateResponse('cgpa.html',{"request": request,"cgpa":cgpa})


# api for cal cgpa
@app.post('/get_cgpa_api')
async def get_cgpa_api(grade: Grades):
    grade_dict = grade.grades
    # print(grade_dict)
    totals = convert(grade_map=grade_dict)
    return {'cgpa': f"{(totals['total_score']/totals['total_fracs']):.3f}"}
    # return grade_dict


# @app.post("/login")
# async def login(username: str = Form(...), password: str = Form(...)):
#     return {"username": username}

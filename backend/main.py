from typing import List
import fastapi as fastapi
import fastapi.security as security
import sqlalchemy.orm as orm
import services as services, schemas as schemas

app = fastapi.FastAPI()

@app.post("/api/users")
async def createuser(
    user: schemas.UserCreate, db: orm.Session = fastapi.Depends(services.getdb)
):
    db_user = await services.getuserbyemail(user.email, db)
    if db_user:
        raise fastapi.HTTPException(statuscode=400, detail="Email already in use")

    user = await services.createuser(user, db)
    return await services.createtoken(user)


@app.post("/api/token")
async def generatetoken(
    formdata: security.OAuth2PasswordRequestForm = fastapi.Depends(),
    db: orm.Session = fastapi.Depends(services.getdb),
):
    user = await services.authenticateuser(formdata.username, formdata.password, db)

    if not user:
        raise fastapi.HTTPException(statuscode=401, detail="Invalid Credentials")

    return await services.createtoken(user)


@app.get("/api/users/me", responsemodel=schemas.User)
async def getuser(user: schemas.User = fastapi.Depends(services.getcurrentuser)):
    return user


@app.post("/api/leads", responsemodel=schemas.Lead)
async def createlead(
    lead: schemas.LeadCreate,
    user: schemas.User = fastapi.Depends(services.getcurrentuser),
    db: orm.Session = fastapi.Depends(services.getdb),
):
    return await services.createlead(user=user, db=db, lead=lead)


@app.get("/api/leads", responsemodel=List[schemas.Lead])
async def getleads(
    user: schemas.User = fastapi.Depends(services.getcurrentuser),
    db: orm.Session = fastapi.Depends(services.getdb),
):
    return await services.getleads(user=user, db=db)


@app.get("/api/leads/{leadid}", statuscode=200)
async def getlead(
    leadid: int,
    user: schemas.User = fastapi.Depends(services.getcurrentuser),
    db: orm.Session = fastapi.Depends(services.getdb),
):
    return await services.getlead(leadid, user, db)


@app.delete("/api/leads/{leadid}", statuscode=204)
async def deletelead(
    leadid: int,
    user: schemas.User = fastapi.Depends(services.getcurrentuser),
    db: orm.Session = fastapi.Depends(services.getdb),
):
    await services.deletelead(leadid, user, db)
    return {"message", "Successfully Deleted"}


@app.put("/api/leads/{leadid}", statuscode=200)
async def updatelead(
    leadid: int,
    lead: schemas.LeadCreate,
    user: schemas.User = fastapi.Depends(services.getcurrentuser),
    db: orm.Session = fastapi.Depends(services.getdb),
):
    await services.updatelead(leadid, lead, user, db)
    return {"message", "Successfully Updated"}


@app.get("/api")
async def root():
    return {"message": "Awesome Leads Manager"}
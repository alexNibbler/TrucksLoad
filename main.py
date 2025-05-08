from functools import cache

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, delete, update
import logging

from database import get_db
from models import Truck, Package
from schema import TruckResponse, TruckCreate, PackageResponse, PackageCreate, AssignRequest, AssignResponse

app = FastAPI()

@cache
def volume(length, width, height):
    return length * width * height

@app.get("/trucks", tags=["Tracks"], response_model=list[TruckResponse])
def get_all_trucks(db: Session = Depends(get_db)):
    trucks = db.scalars(select(Truck)).all()
    return trucks

@app.post("/trucks", tags=["Tracks"], response_model=TruckResponse, status_code=201)
def add_truck(truck: TruckCreate, db: Session = Depends(get_db)):
    try:
        db_truck = Truck(**truck.model_dump())
        db.add(db_truck)
        db.commit()
        logging.info(f"Truck added: {db_truck}")
        return db_truck
    except SQLAlchemyError as e:
        db.rollback()
        raise e

@app.delete("/trucks/{truck_id}", tags=["Tracks"])
def delete_truck(truck_id: int, db: Session = Depends(get_db)):
    truck = db.get(Truck, truck_id)
    if not truck:
        raise HTTPException(status_code=404, detail="Truck not found")
    db.delete(truck)
    db.commit()
    return {"message": f"Truck {truck_id} deleted"}

@app.delete("/trucks", tags=["Tracks"])
def delete_all_trucks(db: Session = Depends(get_db)):
    db.execute(update(Package).values(truck_id=None))
    db.execute(delete(Truck))
    db.commit()
    return {"message": "All trucks deleted"}


@app.get("/packages", tags=["Packages"], response_model=list[PackageResponse])
def get_all_packages(db: Session = Depends(get_db)):
    packages = db.scalars(select(Package)).all()
    return packages

@app.post("/packages", tags=["Packages"], response_model=PackageResponse, status_code=201)
def add_package(pkg: PackageCreate, db: Session = Depends(get_db)):
    try:
        db_pkg = Package(**pkg.model_dump())
        db.add(db_pkg)
        db.commit()
        logging.info(f"Package added: {db_pkg}")
        return db_pkg
    except SQLAlchemyError as e:
        db.rollback()
        raise e

@app.delete("/packages/{package_id}", tags=["Packages"])
def delete_package(package_id: int, db: Session = Depends(get_db)):
    package = db.get(Package, package_id)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    db.delete(package)
    db.commit()
    return {"message": f"Package {package_id} deleted"}

@app.delete("/packages", tags=["Packages"])
def delete_all_packages(db: Session = Depends(get_db)):
    db.execute(delete(Package))
    db.commit()
    return {"message": "All packages deleted"}

@app.post("/loading", tags=["Delivery"], response_model=AssignResponse)
def load_truck(req: AssignRequest, db: Session = Depends(get_db)):
    stmt = select(Package).where(Package.id.in_(req.package_ids))
    packages = db.scalars(stmt).all()

    if len(packages) != len(req.package_ids):
        raise HTTPException(status_code=400, detail="One or more packages not found")

    total_pkg_volume = sum(volume(p.length, p.width, p.height) for p in packages)

    truck_stmt = select(Truck).where(Truck.available == True)
    for truck in db.scalars(truck_stmt):
        truck_volume = volume(truck.length, truck.width, truck.height)
        if truck_volume >= total_pkg_volume >= 0.8 * truck_volume:
            for pkg in packages:
                pkg.truck_id = truck.id
            truck.available = False
            db.commit()
            return AssignResponse(truck_id = truck.id, package_ids = req.package_ids)

    raise HTTPException(status_code=400, detail="No suitable truck found")

# if __name__ == "__main__":
#     try:
#         uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
#     except KeyboardInterrupt:
#         print("Force exit")
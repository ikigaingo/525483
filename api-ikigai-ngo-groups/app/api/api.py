from fastapi import APIRouter, HTTPException, Depends, FastAPI, Query
from sqlalchemy.orm import Session
from typing import List, Dict
from uuid import UUID

from app import get_db
from app.schemas import GroupCreate, GroupUpdate, Group, PaginatedGroups
from ..crud import crud_groups

app = FastAPI()
router = APIRouter()


@router.post("/groups/", response_model=Group)
def create_group_endpoint(group: GroupCreate, db: Session = Depends(get_db)):
    return crud_groups.create_group(db=db, group=group)


@router.get("/groups/", response_model=PaginatedGroups)
def read_groups(
        page: int = Query(1, ge=1, description="Page number, starting from 1"),
        page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
        db: Session = Depends(get_db)
):
    groups, total_count = crud_groups.get_groups(db=db, page=page, page_size=page_size)
    return {"data": groups, "total_count": total_count}


@router.get("/groups/{group_id}", response_model=Group)
def read_group(group_id: UUID, db: Session = Depends(get_db)):
    db_group = crud_groups.get_group(db=db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group


@router.put("/groups/{group_id}", response_model=Group)
def update_group_endpoint(group_id: UUID, group: GroupUpdate, db: Session = Depends(get_db)):
    db_group = crud_groups.get_group(db=db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return crud_groups.update_group(db=db, db_group=db_group, group=group)


@router.delete("/groups/{group_id}", response_model=Group)
def delete_group_endpoint(group_id: UUID, db: Session = Depends(get_db)):
    return crud_groups.delete_group(db=db, group_id=group_id)

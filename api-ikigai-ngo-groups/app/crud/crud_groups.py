from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from uuid import UUID

from app.models import Group as GroupModel
from app.schemas import GroupCreate, GroupUpdate


def create_group(db: Session, group: GroupCreate) -> GroupModel:
    db_group = GroupModel(**group.dict())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from typing import List, Dict, Tuple

def get_groups(db: Session, page: int = 1, page_size: int = 10) -> Tuple[List[Dict], int]:
    offset = (page - 1) * page_size
    query = text("""
        SELECT g.id, g.name, g.group_data, g.created_at, g.updated_at,
               g.organisation_id, g.country_id,
               o.name AS organisation_name, c.name AS country_name
        FROM "group" g
        LEFT JOIN organisation o ON g.organisation_id = o.id
        LEFT JOIN country c ON g.country_id = c.id
        ORDER BY g.created_at DESC
        LIMIT :limit OFFSET :offset
    """).params(limit=page_size, offset=offset)

    count_query = text("""
        SELECT COUNT(1)
        FROM "group" g
    """)

    result = db.execute(query)
    total_count = db.execute(count_query).scalar()

    groups = [
        {
            "id": row[0],
            "name": row[1],
            "group_data": row[2],
            "created_at": row[3],
            "updated_at": row[4],
            "organisation_id": row[5],
            "country_id": row[6],
            "organisation_name": row[7],
            "country_name": row[8]
        }
        for row in result
    ]

    return groups, total_count



def get_group(db: Session, group_id: UUID) -> GroupModel:
    return db.query(GroupModel).filter(GroupModel.id == group_id).first()


def update_group(db: Session, db_group: GroupModel, group: GroupUpdate) -> GroupModel:
    for key, value in group.dict(exclude_unset=True).items():
        setattr(db_group, key, value)
    db.commit()
    db.refresh(db_group)
    return db_group


def delete_group(db: Session, group_id: UUID) -> GroupModel:
    db_group = db.query(GroupModel).filter(GroupModel.id == group_id).first()
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    db.delete(db_group)
    db.commit()
    return db_group

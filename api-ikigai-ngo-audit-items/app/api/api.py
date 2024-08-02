import os
import boto3
import base64
from typing import List

from fastapi import HTTPException, FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import AuditItem
from app.schemas.schemas import AuditItemCreate, AuditItemInDB

app = FastAPI()
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_S3_ACCESS_KEY_ID', 'SECRET'),
    aws_secret_access_key=os.getenv('AWS_S3_SECRET_ACCESS_KEY', 'SECRET'),
    region_name=os.getenv('AWS_S3_REGION_NAME', 'REGION'),
)

bucket_name = "static-audit-items"


@router.post("/audit-item/", response_model=AuditItemInDB)
async def upload_image_base64(data: AuditItemCreate, db: Session = Depends(get_db)):
    try:
        # Extract base64 part
        base64_str = data.image.split('base64,')[1]
        image_data = base64.b64decode(base64_str)

        # Generate a unique filename for the image
        import uuid
        filename = f"{uuid.uuid4()}.jpg"

        # Upload the image to S3
        s3_client.put_object(Bucket=bucket_name, Key=filename, Body=image_data, ContentType='image/jpeg')

        # Get the URL of the uploaded image
        image_url = f"https://{bucket_name}.s3.amazonaws.com/{filename}"

        # Create a new instance of AuditItem with the image URL
        new_item = AuditItem(category=data.category, image=image_url)
        db.add(new_item)
        db.commit()

        return AuditItemInDB(id=new_item.id, image=image_url, category=new_item.category)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/audit-item/", response_model=List[AuditItemInDB])
def get_audit_items(db: Session = Depends(get_db)):
    try:
        items = db.query(AuditItem).all()
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/audit-item/{item_id}", response_model=AuditItemInDB)
async def delete_audit_item(item_id: int, db: Session = Depends(get_db)):
    try:
        # Find the item in the database
        item = db.query(AuditItem).filter(AuditItem.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")

        # Extract the filename from the URL
        filename = item.image.split('/')[-1]

        # Delete the image from S3
        s3_client.delete_object(Bucket=bucket_name, Key=filename)

        # Delete the item from the database
        db.delete(item)
        db.commit()

        return item
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/audit-item/{item_id}", response_model=AuditItemInDB)
async def update_audit_item(item_id: int, data: AuditItemCreate, db: Session = Depends(get_db)):
    try:
        # Find the item in the database
        item = db.query(AuditItem).filter(AuditItem.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")

        # Check if the image is a base64 string or an S3 URL
        if data.image:
            if data.image.startswith('data:image'):
                # Extract base64 part
                base64_str = data.image.split('base64,')[1]
                image_data = base64.b64decode(base64_str)

                # Generate a unique filename for the new image
                import uuid
                new_filename = f"{uuid.uuid4()}.jpg"

                # Upload the new image to S3
                s3_client.put_object(Bucket=bucket_name, Key=new_filename, Body=image_data, ContentType='image/jpeg')

                # Get the URL of the new uploaded image
                new_image_url = f"https://{bucket_name}.s3.amazonaws.com/{new_filename}"

                # Delete the old image from S3
                old_filename = item.image.split('/')[-1]
                s3_client.delete_object(Bucket=bucket_name, Key=old_filename)

                # Update the image URL in the database
                item.image = new_image_url
            elif data.image.startswith(f"https://{bucket_name}.s3.amazonaws.com/"):
                # The image is already an S3 URL, so we do not update it
                pass
            else:
                raise HTTPException(status_code=400, detail="Invalid image format")

        # Update other fields
        item.category = data.category

        # Commit the changes to the database
        db.commit()
        db.refresh(item)

        return item
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


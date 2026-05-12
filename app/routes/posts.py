from fastapi import APIRouter, HTTPException, File, UploadFile, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import Post, get_async_session
from app.images import imagekit
import shutil
import os
import uuid
import tempfile


router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/upload")
async def upload_file(
        file: UploadFile = File(...),
        caption: str = Form(""),
        session: AsyncSession = Depends(get_async_session)
):
    """
    Upload an image or video file.
    
    - **file**: The file to upload (image or video)
    - **caption**: Optional caption for the post
    """
    temp_file_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

            with open(temp_file_path, "rb") as img_file:
                upload_result = imagekit.files.upload(
                    file=img_file,
                    file_name=file.filename,
                    use_unique_file_name=True,
                    tags=["backend-upload"]
                )

                post = Post(
                    caption=caption,
                    url=upload_result.url,
                    file_type="video" if file.content_type == "video/" else "image",
                    file_name=upload_result.name
                )

                session.add(post)
                await session.commit()
                await session.refresh(post)
                return post

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()


@router.get("/feed")
async def get_feed(
        session: AsyncSession = Depends(get_async_session)
):
    """
    Get all posts ordered by creation date (most recent first).
    
    Returns a list of all posts with their details.
    """
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat()

            }
        )
    return {"posts": posts_data}


@router.delete("/{post_id}")
async def delete_post(post_id: str, session: AsyncSession = Depends(get_async_session)):
    """
    Delete a post by its ID.
    
    - **post_id**: UUID of the post to delete
    """
    try:
        post_uuid = uuid.UUID(post_id)

        result = await session.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalars().first()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        await session.delete(post)
        await session.commit()

        return {"success": True, "message": "Post deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

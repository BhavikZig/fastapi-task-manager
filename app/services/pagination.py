from sqlalchemy import desc
from sqlalchemy.orm import Query
from fastapi import Query as FastAPIQuery
from typing import Optional

def paginate(
        query: Query,
        page: int = FastAPIQuery(1, ge=1),
        limit: int = FastAPIQuery(10, ge=1),
        sort_by: Optional[str] = None,
        order: str = FastAPIQuery("desc", regex="^(asc|desc)$"),
        message: Optional[str] = None
):
    total = query.count()

    # Sorting
    if sort_by and hasattr(query.column_descriptions[0]['entity'], sort_by):
        column = getattr(query.column_descriptions[0]['entity'], sort_by)
        if order == "desc":
            column = desc(column)
        query = query.order_by(column)

    offset = (page - 1) * limit
    items = query.offset(offset).limit(limit).all()

    print("items: ", items)

    return {
        "message": message if message else "Data retrieved successfully",
        "total": total,
        "page": page,
        "limit": limit,
        "items": items
    }
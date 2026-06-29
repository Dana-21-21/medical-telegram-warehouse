from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from api.database import get_db

app = FastAPI(
    title="Medical Telegram Warehouse API",
    description="Analytical API for Ethiopian Medical Telegram Channels",
    version="1.0"
)


# -------------------------------------------------------
# Endpoint 1
# Top Products
# -------------------------------------------------------

@app.get("/api/reports/top-products")
def top_products(limit: int = 10, db: Session = Depends(get_db)):

    query = text("""

SELECT
    LOWER(word) AS product,
    COUNT(*) AS frequency

FROM (

    SELECT
        regexp_split_to_table(
            regexp_replace(message_text,'[^[:alnum:] ]',' ','g'),
            '\\s+'
        ) AS word

    FROM fct_messages

) t

WHERE

length(word) > 3

AND word NOT IN (

'telegram',
'monday',
'tuesday',
'wednesday',
'thursday',
'friday',
'saturday',
'sunday',

'delivery',
'available',
'contact',
'phone',
'address',
'school',
'until',
'open',
'close',
'pharmacy',
'cosmetics',
'medhanialem',
'infront'

)

GROUP BY product

ORDER BY frequency DESC

LIMIT :limit;

""")

    result = db.execute(query, {"limit": limit})

    return [
        dict(row._mapping)
        for row in result
    ]


# -------------------------------------------------------
# Endpoint 2
# Channel Activity
# -------------------------------------------------------

@app.get("/api/channels/{channel_name}/activity")
def channel_activity(channel_name: str,
                     db: Session = Depends(get_db)):

    query = text("""

        SELECT

            c.channel_name,

            COUNT(*) AS total_posts

        FROM fct_messages f

        JOIN dim_channels c

        ON f.channel_key = c.channel_key

        WHERE LOWER(c.channel_name)=LOWER(:channel)

        GROUP BY c.channel_name

    """)

    result = db.execute(
        query,
        {"channel": channel_name}
    ).fetchone()

    if result is None:
        return {"message": "Channel not found"}

    return dict(result._mapping)


# -------------------------------------------------------
# Endpoint 3
# Search Messages
# -------------------------------------------------------

@app.get("/api/search/messages")
def search_messages(query: str,
                    limit: int = 20,
                    db: Session = Depends(get_db)):

    sql = text("""

        SELECT

            message_id,
            message_text

        FROM fct_messages

        WHERE LOWER(message_text)
        LIKE LOWER(:keyword)

        LIMIT :limit

    """)

    rows = db.execute(
        sql,
        {
            "keyword": f"%{query}%",
            "limit": limit
        }
    )

    return [
        dict(r._mapping)
        for r in rows
    ]


# -------------------------------------------------------
# Endpoint 4
# Visual Content Statistics
# -------------------------------------------------------

@app.get("/api/reports/visual-content")
def visual_content(db: Session = Depends(get_db)):

    sql = text("""

        SELECT

            image_category,

            COUNT(*) AS total

        FROM yolo_detections

        GROUP BY image_category

        ORDER BY total DESC

    """)

    result = db.execute(sql)

    return [
        dict(r._mapping)
        for r in result
    ]

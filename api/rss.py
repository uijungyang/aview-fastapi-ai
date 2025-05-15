from fastapi import APIRouter
from fastapi.responses import Response
from datetime import datetime

router = APIRouter()

@router.get("/rss.xml", include_in_schema=False)
def rss_feed():
    # 향후 DB 연동 가능
    items = [
        {
            "title": "AI 인터뷰 시스템 출시",
            "link": "https://job-stick.net/posts/ai-interview",
            "description": "AI 기반 면접 시스템이 출시되었습니다.",
            "pubDate": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        }
        # TODO: DB에서 최근 글 목록 자동화 가능 
    ]

    rss_items = "".join([
        f"""
        <item>
            <title>{item['title']}</title>
            <link:{item['link']}</link>
            <description>{item['description']}</description>
            <pubDate>{item['pubDate']}</pubDate>
        </item>
        """ for item in items
    ])

    rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
        <channel>
            <title>JOBSTICK</title>
            <link>https://job-stick.com</link>
            <description>JOBSTICK - AI 모의 기술 면접을 통해 취업 경쟁력을 높이세요!.</description>
            {rss_items}
        </channel>
    </rss>"""

    return Response(content=rss, media_type="application/xml")
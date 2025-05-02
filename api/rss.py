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
            "link": "https://job-stick.com/posts/ai-interview",
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
            <description>JOBSTICK은 한국 IT 기업 분석 보고서와 AI 모의면접 서비스를 제공하여 보다 많은 사람들에게 양질의 정보를 공유하고 도움을 드릴 수 있도록 최선을 다하겠습니다.</description>
            {rss_items}
        </channel>
    </rss>"""

    return Response(content=rss, media_type="application/xml")
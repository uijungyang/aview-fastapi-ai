from fastapi import APIRouter
from fastapi.responses import Response
from datetime import datetime


router = APIRouter()

@router.get("/sitemap.xml", include_in_schema=False)
def sitemap():
    urls = [
        # ✅ 해당 경로에 pages 폴더가 없으면 주석 처리 -> 추후에 변경 가능
        "/",
        "/account",
        "/account/adminLogin",
        "/account/login",
        "/account/modify",
        "/account/my",
        "/account/register",
        "/account/withdraw",
        "/aiInterview",
        "/aiInterview/llmTest",
        "/aiInterview/result",
        # "/assets",
        # "/authentication",
        "/cart",
        "/companyReport",
        "/companyReport/list",
        "/companyReport/modify",
        "/companyReport/read",
        # "/githubAuthentication",
        # "/googleAuthentication",
        # "/guestAuthentication",
        # "/interviewReady",
        # "/kakaoAuthentication",
        "/management",
        # "/model",
        # "model-spk",
        # "/naverAuthentication",
        "/navigatorBar",
        "/order",
        "/order/list",
        "/order/read",
        "/pages",
        "/payments",
        "/payments/failed",
        "/payments/payment",
        "/payments/succed",
        # "/plugins",
        # "/price",
        # "/public",
        "/review",
        "/review/created",
        "/review/list",
        "/review/register",
        "/review/result",
        "/review/submitted"
        # "/server",
        "/survey",
        # "userLog",
        # "utility"
    ]

    url_entries = "".join([
        f"""
        <url>
            <loc>https://job-stick.com{url}</loc>
            <lastmod>{datetime.utcnow().date()}</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        """ for url in urls
    ])

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    {url_entries}
    </urlset>"""

    return Response(content=sitemap, media_type="application/xml")
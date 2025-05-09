# 회사 설명 및 유사도 기반 DB 접근

class CompanyDescription:
    COMPANY_DESCRIPTION = {
        "danggeun": "당근은 동네 커뮤니티 기반 중고거래 플랫폼이다.",
        "kurly": "컬리는 신선식품을 빠르게 배송하는 이커머스 플랫폼이다.",
        "musinsa": "무신사는 온라인 기반 패션 전문 플랫폼이다.",
        "kmong": "크몽은 프리랜서 전문가 매칭 서비스이다.",
        "zigzag": "지그재그는 여성 쇼핑몰 상품을 통합 제공하는 앱이다.",
        "toss": "토스는 간편송금에서 시작해 다양한 금융 서비스를 제공하는 핀테크 기업이다.",
        "payco": "페이코는 간편결제 및 금융 서비스를 제공하는 NHN의 브랜드이다."
    }

    @classmethod
    def get(cls, company_name: str) -> str:
        return cls.COMPANY_DESCRIPTION.get(company_name, "")

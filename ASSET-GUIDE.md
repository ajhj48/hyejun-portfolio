# 실제 프로젝트 자료 삽입 가이드 (2차 시안)

## 원칙
- 현재 시안은 실제 프로젝트 이미지를 꾸며내지 않고, 교체 위치를 명확하게 표시합니다.
- 게시 가능한 원본 이미지/영상 스틸컷만 사용합니다.
- 성과 수치는 기준일, 집계 범위, 본인 기여도를 확인한 뒤 공개합니다.

## 우선 수집할 파일
1. ON.K: 브랜드 키비주얼 1장, 대표 SNS 콘텐츠 3~6장, 성과 화면 1장
2. BIBIGO: 대표 영상 썸네일 1장, 시리즈별 썸네일 3~5장, 대표 영상 링크
3. CJ ENM: 프로젝트별 대표 썸네일 3~6장, 역할/결과 요약
4. CAMPAIGNS: 광고 시안 4~8장, 핵심 카피와 인사이트
5. BRAND IDENTITY: 로고/키비주얼/적용 이미지 3~5장

## 추천 파일명
- `assets/onk-hero.jpg`
- `assets/onk-social-01.jpg`
- `assets/bibigo-farm-to-table.jpg`
- `assets/cjenm-welcome-store.jpg`
- `assets/campaign-random-cupban.jpg`
- `assets/brand-identity-01.jpg`

## 삽입 방법
HTML의 `<div class="asset-slot ...">...</div>` 영역을 실제 `<img>` 또는 YouTube 임베드로 교체합니다. 이미지 대체 텍스트(alt)를 프로젝트 설명에 맞게 작성하세요.

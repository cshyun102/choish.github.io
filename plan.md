# 발표 계획 — Palantir식 Ontology와 반도체 검사·계측 AI

## 개정 메모 — v_01

사용자 피드백에 따라 시각 요약 중심의 초안을 설명형 기술 발표로 확장한다.

- 존재론을 범주·개체·속성·관계·동일성 기준으로 구체화한다.
- 마르쿠스 가브리엘의 의미장 이론을 “대상은 특정 의미장 안에서 나타난다”는 해석 프레임으로 설명한다.
- 하나의 Wafer가 생산·검사·수율·품질·AI 의미장에서 서로 다른 속성·관계·판단 질문을 갖는다는 사례를 추가한다.
- ETL과 ELT의 처리 순서, 장단점, Ontology와의 역할 차이를 추가한다.
- Palantir Ontology의 데이터–로직–액션 계층을 각각 상세 설명하고 permission·audit가 전 계층을 가로지른다는 점을 명시한다.
- 본문 설명 문장을 늘리되 본문 글자 크기 16pt 이상과 한 슬라이드 한 메시지 원칙은 유지한다.
- 개정본은 `output/presentation_v_01.pptx`로 출력한다.

## 개정 메모 — v_02

- 존재론 5장에 범주·개체·속성·관계·동일성의 정의와 반도체 사례를 함께 표기한다.
- 의미장 이론 뒤에 사람·책·건물의 비반도체 사례를 추가해 개념을 일상적으로 이해하게 한다.
- Palantir Ontology 상세 요소 전에 backing data–Ontology–application/AI의 전체 구조를 보여주는 overall 슬라이드를 추가한다.
- `source/ontology101.pdf`의 Stanford Ontology Development 101을 바탕으로 구축 원칙, 7단계 방법, 반도체 적용 체크리스트를 마지막 3장으로 추가한다.
- 개정본은 `output/presentation_v_02.pptx`로 출력한다.

## 1. 발표 목적

Palantir 제품 소개가 아니라, Palantir식 Ontology의 운영 관점을 반도체 검사·계측 AI 업무에 적용하는 방법을 설명한다. 청중이 발표 후 “무엇을 사야 하는가”보다 “어떤 최소 운영 루프를 먼저 설계하고 검증해야 하는가”를 판단할 수 있게 한다.

## 2. 대상 청중 가정

- 반도체 검사·계측·공정·품질 조직의 기술 리더와 실무 엔지니어
- AI/데이터 플랫폼 아키텍트와 모델 개발자
- PoC 범위와 투자 우선순위를 결정하는 조직 관리자
- Ontology 개념에는 익숙하지 않지만 wafer, lot, defect, inspection, SAT, BF/DF, model run 등의 업무 용어에는 익숙한 내부 기술 청중

## 3. 덱의 핵심 메시지

**Ontology는 AI 결과를 더 잘 보여주는 데이터 모델이 아니라, 분석 결과를 증거·가설·피드백·판단·조치·학습으로 닫는 운영 계층이다.**

첫 구현은 전사 Ontology가 아니라 `Analysis Case`를 중심으로 하나의 반복 업무를 4~8주 안에 닫는 PoC여야 한다.

## 4. 권장 스토리라인

1. **문제 제기** — 데이터와 모델은 많지만 판단의 연결과 종료가 남지 않는다.
2. **개념 정렬** — 철학의 존재론, 정보학 온톨로지, Palantir식 운영 Ontology를 구분해 과장과 혼선을 막는다.
3. **개념 전환** — Palantir식 Ontology는 Object–Link–Function–Action–Permission을 결합한 운영 구조다.
4. **도메인 적용** — 반도체에서는 wafer보다 반복 판단 단위인 Analysis Case가 현실적인 중심 객체다.
5. **작동 메커니즘** — 불확실성을 Evidence, Hypothesis, Assumption, Confidence로 표현하고 feedback/decision/action으로 닫는다.
6. **차별점** — 기존 MES/BI/MLOps를 대체하기보다 공통 판단 객체와 action을 잇는 계층으로 보완한다.
7. **실행안** — SAT void ↔ BF/DF defect 유사성 업무로 4~8주 PoC를 수행한다.
8. **의사결정** — 성공 기준은 모델 정확도 단독이 아니라 case closure와 feedback loop이며, 플랫폼 구매 전에 내부 운영 모델을 정의한다.

## 5. 섹션 구조

- **Opening / Why now**: 1~3장
- **Concept / Mechanism**: 4~7장
- **Semiconductor application**: 8~11장
- **Execution / Decision**: 12~14장
- **Appendix**: 15~17장

## 6. 슬라이드별 아웃라인

| # | 구분 | 주장형 제목 | 한 장의 핵심 메시지 | 권장 시각 형식 | 근거 |
|---:|---|---|---|---|---|
| 1 | 표지 | **Ontology는 AI 분석을 조직의 판단 체계로 전환한다** | 발표의 초점은 Palantir 제품이 아니라 검사·계측 AI의 운영 전환이다. | 미니멀 표지 + 한 줄 부제 | TXT Executive Summary, PDF p.1 |
| 2 | Opening | **검사·계측 AI의 병목은 데이터 부족보다 판단 맥락의 단절에 있다** | 데이터·모델 결과가 흩어진 채 담당자, 근거, 최종 판단, 후속 조치가 연결되지 않는다. | 좌→우 단절 흐름(데이터/모델 → 공백 → 판단/조치) | TXT §5.1~5.3, PDF pp.8~9 |
| 3 | Opening | **운영 성과는 모델 출력이 아니라 판단 루프가 닫힐 때 발생한다** | score/label이 case, evidence, feedback, decision, learning으로 이어져야 조직 학습이 된다. | 모델 중심 vs 운영 루프 비교 | TXT Executive Summary, §5.3, §8 |
| 4 | Concept | **‘존재의 분류’에서 ‘업무의 실행’까지 Ontology의 범위가 확장된다** | 존재론은 무엇이 존재하는지, 정보학 온톨로지는 의미·관계, Palantir식 Ontology는 행동·권한까지 다룬다. | 3단 확장 구조 | 새 PDF pp.3~5; Gruber, W3C OWL, Palantir 공식 문서(소스 내 출처 목록) |
| 5 | Concept | **같은 Wafer도 조직별 의미가 다르므로 공통 판단 좌표가 필요하다** | 공정·검사·AI·품질의 서로 다른 ‘의미장’을 지우지 않고 하나의 업무 객체에 연결해야 한다. | Wafer 중심 4관점 맵 | 새 PDF pp.4~5; 의미장 해석은 발표용 비유임을 명시 |
| 6 | Concept | **Palantir식 Ontology는 데이터·로직·행동·권한을 하나의 의미 계층에 묶는다** | Ontology는 ERD나 용어집을 넘어 Object–Link–Function–Action–Permission을 연결한다. | 5요소 수평 구조도 | TXT §2.3, §3.1~3.5; 새 PDF p.6 |
| 7 | Concept | **Function과 Action이 붙어야 모델 결과가 실제 업무를 변화시킨다** | function은 object 위에서 실행되고 action은 case·요청·승인·종료를 변경하며 audit가 남는다. | 입력→Function→Evidence→Action→Audit 프로세스 | TXT §3.3~3.5, §4; 새 PDF pp.6~7 |
| 8 | Application | **첫 Ontology의 중심은 Wafer보다 Analysis Case가 실용적이다** | 물리 객체보다 ‘왜 열렸고 어떻게 닫혔는지’를 추적하는 운영 객체가 출발점이다. | Analysis Case 중심 방사형 관계도 | TXT §6.1~6.5; 새 PDF pp.8~9 |
| 9 | Application | **최소 설계는 Object–Link–Function–Action 네 층만으로 시작할 수 있다** | 필요한 최소 구성과 대표 예시를 층별로 구분해 구현 범위를 고정한다. | 4층 아키텍처 + 대표 엔티티/기능 | TXT §6.2~6.5; 새 PDF pp.8~9 |
| 10 | Application | **불확실성을 객체화해야 분석 결과를 과장하지 않고 학습할 수 있다** | SAT/BF·DF 매칭은 확정 관계가 아니라 hypothesis, evidence, assumption, confidence를 함께 가져야 한다. | SAT void ↔ BF/DF defect 증거 논리도 | TXT §7; 새 PDF pp.8~9 |
| 11 | Application | **Ontology는 MES·BI·MLOps를 대체하지 않고 판단 경계를 연결한다** | 기존 시스템은 기록·시각화·모델 운영을 담당하고 Ontology는 공통 객체·판단·action을 잇는다. | 시스템별 역할 비교 매트릭스 | 새 PDF pp.6~7 |
| 12 | Execution | **성숙도는 Schema에서 Action으로, Action에서 Closed-loop Learning으로 올라간다** | 전사 완성보다 Level 2~3을 먼저 닫고 Level 4로 확장한다. | 0~5 단계 성숙도 계단 | TXT §9 |
| 13 | Execution | **4~8주 PoC는 SAT void ↔ BF/DF 유사성 Case 한 개를 끝까지 닫아야 한다** | object 정의→데이터 연결→matching/evidence→feedback/decision의 최소 루프를 검증한다. | 4주 핵심 트랙 + 8주 확장 타임라인 | TXT §10.1~10.3; 새 PDF pp.8~9, p.11 |
| 14 | Decision | **PoC의 합격 기준은 정확도보다 운영 종료와 재사용 가능성이다** | closure, response, evidence completeness, reuse를 측정하고 플랫폼 선택은 그 이후에 한다. | KPI 4개 + Build/Buy/Hybrid 의사결정 원칙 | TXT §10.4, §12~13; 새 PDF p.11 |
| 15 | Appendix | **실패는 범위를 크게 잡거나 Action을 빼는 순간 시작된다** | Big Bang, schema rename, dashboard repackaging, model-first, over-rigid modeling을 방어한다. | 실패 패턴–방어 전략 표 | TXT §11; 새 PDF p.10 |
| 16 | Appendix | **핵심 객체·링크·함수·행동은 PoC 경계를 명시하는 계약이다** | 상세 후보 목록을 구현 워크숍의 출발점으로 제공한다. | 4분면 상세 표 | TXT §6.2~6.5 |
| 17 | Appendix | **출처와 해석의 경계를 남겨야 기술 주장의 신뢰가 유지된다** | 공식 제품 문서, 학술·표준 자료, 도메인 자료와 발표자의 설계 제안을 분리한다. | 출처 범주·적용 주장·주의점 표 | 새 PDF pp.11~14; TXT 전체 |

## 7. 본문과 부록의 정보 배치

### 본문에 유지

- 판단 맥락 단절이라는 문제 정의
- 존재론–정보학 온톨로지–Palantir식 Ontology의 최소 구분
- 동일 객체에 대한 조직별 의미 차이와 공통 판단 좌표
- Palantir식 Ontology의 운영적 정의
- Object–Link–Function–Action–Permission 메커니즘
- Analysis Case 중심 최소 설계
- 불확실성 표현 방식
- MES/BI/MLOps와 Ontology의 역할 경계
- 성숙도와 4~8주 PoC
- 운영 KPI와 의사결정 원칙

### 부록으로 이동

- Core Object/Link/Function/Action의 전체 후보 목록
- 5개 실패 패턴의 상세 설명
- 공식·학술·도메인 출처 목록과 해석/제안의 경계
- 세부 KPI 정의와 계산식은 실제 데이터 정의 후 별도 확정

## 8. 근거 추적 원칙

- `source/original_text.txt`를 문장 수준의 1차 콘텐츠 근거로 사용한다.
- `source/책으로만 읽은 팔란티어와 온톨로지 이야기.pdf`는 14페이지 리서치 문서로, 공식·학술·도메인 출처 목록과 URL을 포함한다.
- 새 PDF의 공식 출처(Palantir 문서·공시), 학술/표준 출처(Gruber, Guarino, W3C 등), 도메인 보조 출처를 출처 슬라이드에 범주별로 기록한다.
- `source/original_text.txt`의 `[S1]~[S11]` 표기는 참고문헌 목록이 없으므로 단독 인용하지 않고, 새 PDF의 출처 목록과 대응되는 개념만 사용한다.
- Palantir의 시장 수치, 최근 성장률, valuation 등 시점 민감 정보는 본문에서 제외한다.
- 제품 기능 설명은 “제공된 소스가 설명하는 Palantir식 관점”으로 한정한다.
- PoC 기간, 성숙도, 객체 모델, KPI는 소스가 제안한 설계안이며 실증 결과가 아님을 명시한다.

## 9. 위험·불확실성 및 신중한 표현

1. **공간 유사성은 인과관계가 아니다.** overlap score는 가설의 근거일 뿐 동일 원인을 확정하지 않는다.
2. **layer/stack mapping은 미확정일 수 있다.** coordinate alignment, 검사 시점, 다층 중첩을 가정과 신뢰도로 남긴다.
3. **PoC 기간은 조직·데이터 준비도에 따라 달라진다.** 4~8주는 소스의 권장 범위이지 보장 일정이 아니다.
4. **운영 KPI의 목표값은 제시하지 않는다.** 현재 baseline이 없으므로 지표 정의만 제공한다.
5. **Palantir 도입을 결론으로 만들지 않는다.** Build/Buy/Hybrid는 운영 모델을 정의한 뒤 비교한다.
6. **LLM 자동화의 범위를 과장하지 않는다.** permission, audit, human review가 선행되어야 한다.
7. **의미장 이론은 설계 표준이 아니라 해석 프레임이다.** 철학적 권위로 제품이나 아키텍처를 정당화하지 않는다.
8. **기존 시스템을 불필요하게 폄하하지 않는다.** MES/BI/MLOps와 Ontology는 역할이 다르며 실제 경계는 조직 아키텍처에 따라 달라진다.

## 10. 계획 비판 검토 및 수정 기록

### 1차 검토에서 발견한 약점

- 원 보고서의 장 구성대로 옮기면 ‘책 요약’처럼 보이고 본론 진입이 늦다.
- Ontology의 철학·정보학 정의를 별도 장으로 길게 다루면 내부 기술 청중의 실행 관심을 잃을 수 있다.
- Core Object/Link 목록 전체를 본문에 넣으면 글자가 작아지고 보고서형 슬라이드가 된다.
- 시장 성장 수치는 시점 민감하며 원 참고문헌 목록이 없어 신뢰성 검증이 불가능하다.
- Build vs Buy를 크게 다루면 제품 구매 제안으로 오해될 수 있다.

### 반영한 수정

- 첫 3장에서 데이터/모델과 운영 판단의 단절을 먼저 보여주도록 재구성했다.
- 철학적 정의는 삭제하지 않고 슬라이드 4의 한 문장 맥락으로 축약했다.
- 상세 Object/Link/Function/Action 목록은 부록 15장으로 이동했다.
- 시장 수치와 투자 논의는 제거했다.
- Build vs Buy는 마지막 의사결정 원칙의 보조 요소로 축소했다.
- 새 PDF 추가 후 개념 혼선을 줄이는 2장을 보강하고 기존 중복 비교를 통합해 본문 14장, 부록 3장으로 제한했다.
- 각 슬라이드에 하나의 주장과 하나의 시각 논리만 배정했다.

### 최종 계획 판정

- 문제→개념 정렬→작동 메커니즘→도메인 적용→실행→의사결정의 흐름이 자연스럽다.
- 기술 용어는 4~6장에서 정의한 뒤 7장 이후에 사용한다.
- 본문은 운영 논리와 의사결정에 집중하고, 상세 목록과 방어 전략은 부록으로 분리했다.
- 모든 제목은 주장형이며, 한국 내부 기술 청중에게 익숙한 영문 용어는 한국어 설명과 병기한다.
- `AGENTS.md`와 `style.md`의 간결한 기술·코퍼레이트 스타일, 제한된 색상, 의미 중심 도식, 한국어 렌더링 QA 요건을 충족하도록 설계한다.

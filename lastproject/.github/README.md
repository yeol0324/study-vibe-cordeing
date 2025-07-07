# GitHub Actions 및 자동화 시스템

이 프로젝트는 GitHub Actions을 통해 다양한 자동화 기능을 제공합니다.

## 🔄 자동화된 워크플로우

### 1. 테스트 자동 실행 (`test.yml`)
- **트리거**: `main` 브랜치로의 push 및 PR
- **기능**: 백엔드와 프론트엔드 테스트 자동 실행
- **커버리지**: Codecov 연동을 통한 테스트 커버리지 리포트

### 2. PR 자동 댓글 (`pr-comment.yml`)
- **트리거**: PR 생성 및 재오픈
- **기능**:
  - 웰컴 메시지 및 체크리스트 제공
  - 테스트 결과 자동 업데이트
  - 가이드라인 안내

### 3. PR 자동 할당 (`pr-assigner.yml`)
- **트리거**: PR 생성, 재오픈, 리뷰 준비
- **기능**:
  - 변경된 파일 영역 기반 리뷰어 할당
  - PR 작성자를 assignee로 할당
  - 할당 결과 알림

### 4. PR 라벨 자동 등록 (`pr-labeler.yml`)
- **트리거**: PR 생성, 재오픈, 동기화
- **기능**:
  - 변경된 파일 분석
  - PR 제목/내용 기반 자동 라벨링
  - 크기, 타입, 우선순위 라벨 추가

### 5. PR 코드 리뷰 자동 등록 (`pr-code-review.yml`)
- **트리거**: PR 생성, 재오픈, 동기화 (draft가 아닌 경우)
- **기능**:
  - 코드 스타일 검사 (Black, isort)
  - 코드 품질 검사 (Flake8)
  - 보안 검사 (Bandit)
  - 타입 검사 (MyPy)
  - 복잡도 분석

### 6. 이슈 자동 댓글 (`issue-comment.yml`)
- **트리거**: 이슈 생성 및 재오픈
- **기능**:
  - 이슈 타입별 웰컴 메시지
  - 템플릿 준수 확인
  - 처리 절차 안내

### 7. 이슈 자동 할당 (`issue-assigner.yml`)
- **트리거**: 이슈 생성, 재오픈, 라벨 변경
- **기능**:
  - 라벨 및 키워드 기반 담당자 할당
  - 긴급 이슈 에스컬레이션
  - 할당 결과 알림

### 8. 이슈 라벨 자동 등록 (`issue-labeler.yml`)
- **트리거**: 이슈 생성, 재오픈, 수정
- **기능**:
  - 제목/내용 기반 자동 라벨링
  - 타입, 영역, 우선순위 분류
  - 신규 기여자 감지
  - 마일스톤 자동 할당

## 🏷️ 라벨 시스템

### 타입 라벨
- `type/bug`: 버그 수정
- `type/feature`: 새로운 기능
- `type/enhancement`: 기능 개선
- `type/documentation`: 문서 작업
- `type/test`: 테스트 관련
- `type/refactoring`: 리팩토링
- `type/style`: 코드 스타일

### 영역 라벨
- `area/backend`: 백엔드 (FastAPI)
- `area/frontend`: 프론트엔드 (Streamlit)
- `area/agent`: AI Agent (LangGraph)
- `area/docs`: 문서
- `area/tests`: 테스트
- `area/config`: 설정

### 컴포넌트 라벨
- `component/api`: API 라우터
- `component/models`: 데이터 모델
- `component/services`: 서비스 계층
- `component/agents`: Agent 구현

### 우선순위 라벨
- `priority/high`: 높은 우선순위
- `priority/medium`: 보통 우선순위
- `priority/low`: 낮은 우선순위

### 상태 라벨
- `status/in-progress`: 진행 중
- `status/review`: 리뷰 대기
- `status/blocked`: 차단됨
- `status/wip`: 작업 중

### 크기 라벨 (PR용)
- `size/XS`: 1파일 변경
- `size/S`: 2-5파일 변경
- `size/M`: 6-10파일 변경
- `size/L`: 11-20파일 변경
- `size/XL`: 20파일 이상 변경

## 👥 팀 멤버 설정

현재 설정된 팀 멤버들은 예시입니다. 실제 GitHub 사용자명으로 변경해야 합니다:

### 백엔드 팀
- `backend-dev1`
- `backend-dev2`
- `fullstack-dev`

### 프론트엔드 팀
- `frontend-dev1`
- `frontend-dev2`
- `fullstack-dev`

### 문서/QA 팀
- `tech-writer`
- `qa-engineer`

### 관리 팀
- `project-maintainer`
- `lead-dev`

## ⚙️ 설정 방법

### 1. 팀 멤버 업데이트
각 워크플로우 파일에서 `teamMembers` 객체의 사용자명을 실제 GitHub 사용자명으로 변경하세요.

### 2. 저장소 권한 설정
- Actions 권한: `Settings` > `Actions` > `General`에서 허용
- Write 권한: 모든 팀 멤버에게 저장소 write 권한 부여

### 3. 브랜치 보호 규칙
- `main` 브랜치 보호 활성화
- PR 필수 설정
- 상태 체크 필수 설정

### 4. 라벨 생성
필요한 라벨들이 자동으로 생성되지 않으면 수동으로 생성하세요:
```bash
# GitHub CLI를 사용한 라벨 생성 예시
gh label create "type/bug" --color "d73a4a" --description "버그 수정"
gh label create "area/backend" --color "0052cc" --description "백엔드 관련"
```

## 🔧 문제 해결

### 할당 실패 문제
- 사용자명이 정확한지 확인
- 저장소 접근 권한 확인
- Collaborator로 추가되었는지 확인

### 라벨 생성 실패
- 저장소 관리자 권한 확인
- 라벨이 이미 존재하는지 확인

### Actions 실행 실패
- Actions 권한 설정 확인
- Workflow 파일 문법 확인
- 시크릿 설정 확인 (필요시)

## 📊 모니터링

### Actions 실행 상태 확인
- Repository > Actions 탭에서 확인
- 실패한 워크플로우의 로그 확인

### 자동화 효과 측정
- PR 처리 시간 단축
- 수동 라벨링 작업 감소
- 코드 품질 개선
- 이슈 응답 시간 개선

## 💡 사용 팁

### PR 작성 시
- 명확한 제목 사용 (`[feat]`, `[fix]` 등)
- 템플릿 체크리스트 완료
- 자동 생성된 댓글 확인

### 이슈 작성 시
- 적절한 템플릿 선택
- 필수 정보 포함
- 자동 할당된 라벨 확인

### 코드 품질 관리
- 로컬에서 사전 검사 실행:
  ```bash
  black .
  isort .
  flake8 .
  bandit -r .
  mypy .
  ```

## 🔄 지속적 개선

이 자동화 시스템은 프로젝트 요구사항에 따라 계속 개선될 수 있습니다:

- 새로운 라벨 추가
- 할당 로직 개선
- 추가 코드 품질 검사
- 알림 시스템 연동
- 메트릭 수집 및 분석

문의사항이나 개선 제안이 있으시면 이슈를 생성해 주세요! 
# Simple AI Setup Tool v3.0 (자동 설치 시스템 추가)

**Windows용 AI 개발 환경 자동 설정 도구 - 완전 자동화 지원**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://windows.com)
[![Architecture](https://img.shields.io/badge/Architecture-Brain%20Module%20v4.0-green.svg)](#architecture)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 프로젝트 개요

AI 개발에 필요한 Git, Node.js, Claude CLI를 자동으로 설치하고 PATH를 관리하는 Windows GUI 도구입니다.

### ✨ 주요 특징

- **🆕 User PATH 자동 관리**: npm CLI 도구를 User PATH에 자동 추가 (VSCode 즉시 인식)
- **🆕 3단계 검증 시스템**: 파일 존재 + Registry 확인 + 실행 테스트
- **🆕 환경변수 확장 지원**: %APPDATA%\npm 형식으로 PATH 저장
- **완전 자동 설치 시스템**: 5단계 자동 설치 플로우 (auto_main.py)
- **단일 실행 파일**: AI_Auto_Installer.exe로 모든 도구 자동 설치
- **완전 한국어 인터페이스**: 모든 UI, 메시지, 안내 텍스트 한국어 지원
- **이중 PATH 검증**: Registry 직접 확인 + 실제 실행 테스트로 정확한 상태 파악
- **Windows 명령어 지원**: .cmd 확장자 자동 처리로 npm, claude 명령어 정확 실행
- **즉시 PATH 반영**: 설치 후 새 터미널에서 바로 사용 가능 (재부팅 불필요)
- **VSCode 안내 강화**: PATH 캐싱 문제 설명 및 재시작 가이드 제공
- **패키지 매니저 지원**: Winget 및 Chocolatey 자동 감지 및 사용
- **실시간 로깅**: 모든 작업 과정 실시간 확인
- **간소화된 인터페이스**: 설치 전용 UI로 복잡성 제거
- **프로덕션 최적화**: PowerShell 창 숨김으로 깔끔한 사용자 경험


## 🏛️ 아키텍처

### Brain Module System v4.0 구조

```
modules/
├── core/                    # 핵심 비즈니스 로직
│   ├── config.py           # 설정 관리 시스템
│   ├── installer.py        # 통합 설치 엔진
│   ├── uninstaller.py      # 통합 제거 엔진
│   ├── status_checker.py   # 상태 검사 시스템
│   └── exceptions.py       # 커스텀 예외 처리
├── ui/                     # 사용자 인터페이스
│   ├── components.py       # UI 컴포넌트 빌더
│   └── themes.py          # 색상 시스템
└── utils/                  # 유틸리티 함수
    ├── logger.py          # 로깅 시스템
    ├── path_manager.py    # 통합 PATH 관리 (기본 + 즉시 반영)
    ├── path_repair.py     # PATH 자동 복구
    ├── path_verifier.py   # Registry vs 실행 이중 검증
    └── system_utils.py    # 시스템 유틸리티
```


## 🛠️ 지원 도구

| 도구 | 설명 | 설치 방법 |
|------|------|-----------|
| **Git** | 버전 관리 시스템 | Winget / Chocolatey |
| **Node.js & npm** | JavaScript 런타임 및 패키지 매니저 | Winget / Chocolatey |
| **Claude Code CLI** | Anthropic AI 공식 코딩 어시스턴트 | npm (@anthropic-ai/claude-code) |
| **Google Gemini CLI** | Google AI 코딩 어시스턴트 | npm (@google/generative-ai-cli) |

## 🚀 빠른 시작

### 필수 요구사항

- Windows 10/11
- Python 3.8+
- 관리자 권한 (패키지 매니저 운영용)

### 실행 방법

```bash
# Python으로 직접 실행
python auto_main.py

# 또는 빌드된 실행 파일 사용 (권장)
dist_auto\AI_Auto_Installer.exe
```

### 독립 실행파일 빌드

```bash
# 자동 설치 도구 빌드
python build_auto.py
# 결과물: dist_auto/AI_Auto_Installer.exe (약 11MB)
```


## 📋 주요 기능

### 🆕 자동 설치 시스템 (auto_main.py)

**5단계 완전 자동화 플로우:**
1. **단계 1 (0-20%)**: Chocolatey 설치 및 즉시 적용
2. **단계 2 (20-40%)**: Chocolatey 감지 확인
3. **단계 3 (40-60%)**: Git 자동 설치 및 PATH 설정
4. **단계 4 (60-80%)**: Node.js 자동 설치 및 User PATH 설정 (%APPDATA%\npm)
5. **단계 5 (80-100%)**: Claude/Gemini CLI 설치 및 3단계 검증

**특징:**
- 프로그레스 바로 실시간 진행 상황 표시
- 각 단계별 로그 실시간 출력
- 설치 중단/재시작 기능
- 로그 저장 기능

### 🔍 3단계 검증 시스템 (강화)

**Claude CLI / Gemini CLI 검증:**
- **Stage 1 - 파일 존재 확인**: npm 패키지 설치 디렉토리에서 실행 파일 확인
- **Stage 2 - User PATH Registry**: HKEY_CURRENT_USER\Environment에서 npm 경로 확인
- **Stage 3 - 실행 테스트**: 새 PowerShell 프로세스에서 실제 명령어 실행 테스트

**모든 단계 통과해야 설치 완료로 인정!**

### 📦 스마트 설치 시스템

- **패키지 매니저 자동 선택**: Winget 또는 Chocolatey 자동 감지
- **User PATH 자동 관리**: npm CLI 도구를 User PATH에 추가 (관리자 권한 불필요)
- **환경변수 형식**: %APPDATA%\npm 형식으로 저장하여 사용자 이동 시에도 작동
- **PATH 즉시 반영**: WM_SETTINGCHANGE 브로드캐스트로 새 터미널에서 바로 사용
- **Claude/Gemini CLI 지원**: npm을 통한 자동 설치 및 검증
- **VSCode 재시작 안내**: PATH 캐싱 문제 및 해결 방법 명확히 안내


## 🔧 시스템 요구사항

### 운영체제

- Windows 10 (1909 이상)
- Windows 11 (모든 버전)

### 소프트웨어

- Python 3.8 이상
- tkinter (Python 표준 라이브러리)
- PowerShell 5.0 이상

### 권한

- 관리자 권한 (패키지 매니저 작업용)
- 네트워크 접속 (다운로드용)

## 📈 성능 최적화

### 코드 효율성

- **DRY 원칙 적용**: 코드 중복 90% 제거
- **메모리 최적화**: 불필요한 객체 생성 최소화
- **스레드 안전성**: 백그라운드 작업 시 UI 응답성 유지

### 사용자 경험

- **즉시 피드백**: 사용자 액션에 대한 즉각적 응답
- **진행률 표시**: 설치 과정의 시각적 피드백
- **한국어 오류 메시지**: 사용자 친화적 한글 오류 안내
- **직관적 인터페이스**: 한국어 라벨과 버튼으로 쉬운 사용

## 🧪 개발자 정보

### Brain Module System v4.0 특징

- **의존성 주입**: 컴포넌트 간 느슨한 결합
- **단일 책임 원칙**: 각 모듈의 명확한 역할 분담
- **설정 기반 운영**: 하드코딩 제거를 통한 유연성 확보

### 코드 품질

- **Type Hints**: 타입 힌트를 통한 코드 안정성
- **Docstring**: 모든 함수와 클래스의 상세 문서화
- **Exception Handling**: 커스텀 예외 클래스를 통한 체계적 오류 처리

## 🗂️ 프로젝트 구조

```
new_ai_setup/
├── auto_main.py           # 자동 설치 메인 애플리케이션 (186라인)
├── build_auto.py          # 자동 설치 도구 빌드 스크립트 (115라인)
├── README.md              # 프로젝트 문서 (279라인)
├── filetree.md            # 프로젝트 구조 상세 문서 (284라인)
├── PATH_FIX_PLAN.md       # PATH 수정 계획 문서 (333라인)
├── icon.ico               # 애플리케이션 아이콘
├── manifest.xml           # 애플리케이션 매니페스트
├── auto_main/             # 자동 설치 패키지 (968라인)
│   ├── __init__.py        # 패키지 초기화 (7라인)
│   ├── auto_installer.py  # 5단계 자동 설치 로직 (521라인)
│   └── auto_gui.py        # 자동 설치 GUI (440라인)
├── modules/               # Brain Module System v4.0 (5,118라인)
│   ├── core/              # 핵심 비즈니스 로직 (2,210라인)
│   │   ├── config.py      # 통합 설정 관리 (523라인)
│   │   ├── installer.py   # 통합 설치 로직 (872라인)
│   │   ├── status_checker.py # 상태 검증 시스템 (780라인)
│   │   └── exceptions.py  # 커스텀 예외 (34라인)
│   ├── ui/                # 사용자 인터페이스 (395라인)
│   │   ├── components.py  # UI 컴포넌트 (352라인)
│   │   └── themes.py      # 색상 시스템 (43라인)
│   └── utils/             # 유틸리티 함수 (2,513라인)
│       ├── path_manager.py   # PATH 통합 관리 (768라인)
│       ├── path_verifier.py  # 이중 검증 (717라인)
│       ├── path_repair.py    # 자동 복구 (405라인)
│       ├── system_utils.py   # 시스템 유틸 (277라인)
│       ├── error_logger.py   # 에러 로깅 (174라인)
│       └── logger.py         # 일반 로깅 (123라인)
├── dist_auto/             # 빌드 결과물
│   └── AI_Auto_Installer.exe  # 최종 실행 파일 (11MB)
└── build_auto/            # PyInstaller 빌드 임시 파일
```

**총 코드 라인 수**: 6,387라인 (Python 코드만)


## 🚧 알려진 제한사항

- Windows 전용 (Linux/macOS 미지원)
- 관리자 권한 필수
- 인터넷 연결 필요

## 🔄 최신 업데이트

### v3.1 (현재) - User PATH 자동 관리 시스템
- 🆕 **User PATH 자동 관리**: npm CLI를 User PATH에 자동 추가 (VSCode 즉시 인식!)
- 🆕 **3단계 검증 시스템**: 파일 존재 + User PATH Registry + 실행 테스트 (315줄)
- 🆕 **환경변수 확장 지원**: %APPDATA%\npm 형식으로 PATH 저장 (30줄)
- 🆕 **Gemini CLI 지원**: Google AI CLI 추가 및 검증 로직 통합
- 🆕 **VSCode 안내 강화**: PATH 캐싱 문제 상세 설명 및 재시작 가이드
- 🔧 **에러 처리 개선**: silent failure 제거, 상세 에러 로깅 추가
- 🎯 **UX 개선**: 불필요한 경고 메시지 제거, 설치 완료 팝업 간소화 및 중복 제거
- 🐛 **버그 수정**: error_logger 파라미터 누락 수정, 중복 팝업 방지 플래그 추가
- 📈 **코드 개선**: 총 650+줄 추가/수정, 10개 파일 개선
- 💡 **System/User PATH 분리**: Node.js는 System, npm CLI는 User PATH

### v3.0 - 자동 설치 시스템
- 🆕 **완전 자동 설치 시스템**: 5단계 자동 설치 플로우 구현
- 🆕 **auto_main 패키지**: 자동 설치 전용 모듈 시스템 (968라인)
- 📦 **빌드 단일화**: AI_Auto_Installer.exe 하나로 통합 (11MB)
- 🧵 **스레드 기반 비동기 처리**: GUI 응답성 유지하며 백그라운드 설치
- 💾 **로그 저장 기능**: 설치 과정 로그를 파일로 저장 가능

### v2.8 - 한글화 버전
- 🌏 **완전 한국어 지원**: 383개 이상의 UI 텍스트 한글 번역
- 🎨 **프로덕션 빌드**: PowerShell 창 숨김 지원
- 📦 **빌드 최적화**: 10.26MB 크기 달성

### v2.7 - PATH 관리 개선
- 🔧 **Windows 명령어 개선**: .cmd 확장자 자동 처리
- 🎯 **UI 간소화**: 제거 기능 완전 제거
- ✅ **검증 시스템 강화**: 중복 실행 방지 로직 추가

### v2.6 - 이중 PATH 검증
- 🔍 **이중 검증 시스템**: Registry + 실행 테스트
- ⚠️ **캐싱 감지**: PATH 캐싱 문제 자동 감지
- 📊 **향상된 진단**: 정확한 원인 파악

## 🎯 VSCode에서 CLI 사용하기

### 설치 후 VSCode에서 claude/gemini 사용

**⚠️ 중요: VSCode는 시작 시 PATH를 캐싱합니다!**

1. **VSCode 완전 재시작**
   - 모든 VSCode 창을 닫습니다
   - VSCode를 다시 실행합니다
   - 새 터미널을 열고 `claude --version` 입력

2. **또는 터미널에서 PATH 수동 새로고침**
   ```powershell
   $env:Path = [Environment]::GetEnvironmentVariable('Path','User') + ';' + [Environment]::GetEnvironmentVariable('Path','Machine')
   ```

3. **확인**
   ```bash
   claude --version
   gemini --version
   ```

## 📄 라이선스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🙋‍♂️ 지원

문제가 발생하거나 기능 제안이 있으시면 이슈를 등록해주세요.

---

**Simple AI Setup Tool v3.0** - Windows용 AI 개발 환경 완전 자동 설정 도구
**Read this in other languages: [English](README.md)**
# Service Hub
Linux 시스템을 위한 systemctl 기반 서비스 자동 시작 관리자 (GUI 포함)

## 개요
Service Hub는 systemd 서비스를 자동 시작 기능과 함께 관리할 수 있는 사용자 친화적인 인터페이스를 제공합니다. 애플리케이션은 두 가지 주요 구성 요소로 이루어져 있습니다:

- **Service Hub Daemon**: systemd 서비스를 모니터링하고 관리하는 백그라운드 서비스
- **Service Hub GUI**: 편리한 서비스 관리를 위한 시스템 트레이 애플리케이션

GUI는 시스템 트레이에서 실행되며, 데몬이 백그라운드에서 계속 작동하는 동안 숨기거나 닫을 수 있습니다. 지속적인 작동을 위해서는 데몬 모드 실행을 권장합니다.

## 필요 사항
- systemd가 설치된 Linux 운영 체제
- Python 3.8 이상
- Root 권한 (데몬 실행 시)

## 설치
1. 저장소 복제
```bash
git clone <repository-url>
cd service-hub
```

2. 의존성 설치
```bash
pip install -r requirements.txt
```

## 사용법
### 데몬 시작
데몬은 systemd 서비스와 상호작용하기 위해 root 권한이 필요합니다.
```bash
sudo python service_hub_daemon/service_hubd.py
```

### GUI 시작
**일반 모드:**
```bash
python service_hub_gui/service_hub_gui.py
```

**데몬 모드 (권장):**
```bash
nohup python service_hub_gui/service_hub_gui.py &
```

데몬 모드로 실행하면 터미널 세션에 종속되지 않고 GUI가 시스템 트레이에 지속적으로 유지됩니다.

## 기능
- systemd 서비스 상태 모니터링
- 서비스 자동 시작 설정
- 빠른 접근을 위한 시스템 트레이 통합
- 닫기 시 트레이로 최소화
- 백그라운드 데몬 동작

## 구조
```
service-hub/
├── service_hub_daemon/    # 백그라운드 서비스 모니터
├── service_hub_gui/       # 시스템 트레이 GUI 애플리케이션
└── service_hub_icp/       # 프로세스 간 통신
```

## 라이선스
MIT 라이선스 - 누구나 제한 없이 자유롭게 사용할 수 있습니다.

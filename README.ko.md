<div align="center">
  <img width="256" height="256" alt="Service Hub Icon" src="https://github.com/user-attachments/assets/c5190f09-629c-4359-9a15-3014adc924be" />
  <br><br>
  
  [![AMD64](https://img.shields.io/badge/Download-AMD64-blue?style=for-the-badge)](https://github.com/cheonjiyeoung/service_hub/raw/release/service-hub_1.0.0_amd64.deb)
  [![ARM64](https://img.shields.io/badge/Download-ARM64-green?style=for-the-badge)](https://github.com/cheonjiyeoung/service_hub/raw/release/service-hub_1.0.0_arm64.deb)
  
  <br>
  
  **Read this in other languages: [English](README.md)**
</div>

# Service Hub
## 개요

Service Hub는 systemd 서비스를 자동 시작 기능과 함께 관리할 수 있는 사용자 친화적인 인터페이스를 제공합니다. 시스템 트레이 통합을 통해 깔끔한 GUI를 제공하며, 시스템 서비스를 쉽게 모니터링하고 제어할 수 있습니다.

## 사용 방법

### 서비스 등록
1. "Add" 버튼 클릭
   
   <img width="374" height="292" alt="how_to_register_1" src="https://github.com/user-attachments/assets/adde90ae-0c1a-45c5-a857-080baeba20e3" />

2. 서비스 이름 입력 (systemctl 서비스 파일 이름)
   
  <img width="216" height="183" alt="how_to_register_2" src="https://github.com/user-attachments/assets/bda1271b-3fca-4175-b858-d9decd23b48b" />

3. 텍스트 입력 또는 "Browse" 버튼을 통해 실행할 파일 경로 입력 (현재 .sh 파일만 지원)
   
  <img width="219" height="187" alt="how_to_register_3" src="https://github.com/user-attachments/assets/23d93850-a0a0-45db-a13a-12b975bbf1f3" />

4. 등록된 서비스 확인 (초기에는 중지 상태, 자동 실행 활성화됨)
   
  <img width="211" height="143" alt="how_to_register_4" src="https://github.com/user-attachments/assets/e1e86873-c413-47df-91c1-3058e12f9b67" />
  
  ## 서비스 상태 표시
  - 🔴: 서비스 실행 중이지 않음
  - 🟢: 서비스 실행 중
  - ⚠️: 오류

### 서비스 설정
서비스 이름을 클릭하면 서비스 관리 메뉴가 나타납니다
<img width="611" height="144" alt="setting" src="https://github.com/user-attachments/assets/8b3d91a3-3516-4866-9929-40c2364b1537" />

| 버튼 | 설명 |
|------|------|
| **Start** | 서비스 시작 |
| **Stop** | 서비스 중지 |
| **Restart** | 서비스 재시작 |
| **Enable** | 자동 실행 활성화 |
| **Disable** | 자동 실행 비활성화 |
| **Remove** | 서비스 파일 제거 및 자동 실행 비활성화 |
| **Modify** | 서비스 파일 수정 |
| **View Logs** | 서비스 출력 확인 |

예시)
1. Start 버튼 클릭
<img width="624" height="148" alt="start" src="https://github.com/user-attachments/assets/9e61b6da-654f-40bd-b79c-c599ec2ea1fa" />

2. Modify 버튼 클릭
<img width="832" height="640" alt="configulation" src="https://github.com/user-attachments/assets/8e761411-eb7b-4846-9019-4c800ffd9545" />

3. View Logs 버튼 클릭
<img width="618" height="350" alt="logs" src="https://github.com/user-attachments/assets/17e6ea4c-c7cf-4068-97c3-7f209d4199fe" />

### 시스템 트레이 아이콘 문제
아이콘 표시 버그를 해결하지 못했습니다... "..." 아이콘이 정상적인 아이콘입니다.

<img width="362" height="27" alt="스크린샷, 2025-12-06 21-00-38" src="https://github.com/user-attachments/assets/ea9f05ea-7457-44ae-9dc2-fa18f308cebc" />


## 설치

### 다운로드

아키텍처에 맞는 최신 `.deb` 패키지를 다운로드하세요:

### 설치
```bash
# AMD64
sudo dpkg -i service-hub_1.0.0_amd64.deb
sudo apt-get install -f  # 필요시 의존성 설치

# ARM64
sudo dpkg -i service-hub_1.0.0_arm64.deb
sudo apt-get install -f
```

## 제거
```bash
# 패키지 제거
sudo apt remove service-hub

# 패키지 및 설정 파일 완전 제거
sudo apt purge service-hub
```

## 사용법

### 애플리케이션 시작

데몬은 설치 후 자동으로 시작됩니다. GUI 실행:
```bash
service_hub_gui
```

데몬 모드로 실행:
```bash
nohup service_hub_gui &
```

### 서비스 관리

1. 시스템 트레이에서 Service Hub 아이콘 클릭
2. "Add Service"를 선택하여 새 서비스 등록
3. 각 서비스의 자동 시작 설정 구성
4. 트레이 메뉴에서 서비스 상태 모니터링

## 요구사항

- systemd가 설치된 Linux
- Python 3.8 이상

## 구조
```
Service Hub
├── Daemon (service_hubd)     - 백그라운드 서비스 모니터
├── GUI (service_hub_gui)     - 시스템 트레이 애플리케이션
└── ICP Module                - 프로세스 간 통신
```

## 라이선스

MIT 라이선스 - 누구나 제한 없이 자유롭게 사용할 수 있습니다.

## 링크

- **소스 코드**: [소스 보기](https://github.com/cheonjiyeoung/service_hub/tree/source)
- **릴리즈**: [릴리즈](https://github.com/cheonjiyeoung/service_hub/tree/release)
- **이슈**: [버그 리포트](https://github.com/cheonjiyeoung/service_hub/issues)

---

**버전**: 1.0.0  
**최종 업데이트**: 2025년 12월

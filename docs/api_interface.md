# Kiko API 인터페이스

이 문서는 `src/app.py`에 구현된 FastAPI 엔드포인트의 개요와 요청/응답 형식을 정리한 것입니다. 실제 서비스 연동은 구현되지 않았으며 모두 목(mock) 동작을 수행합니다.

## 인증
### POST `/auth/signup` 및 `/auth/login`
- **요청 본문**: `{ "username": "string", "password": "string" }`
- **응답**: `{ "token": "fake-token" }`

두 엔드포인트 모두 동일한 동작을 하며 사용자를 인증 또는 등록하는 것처럼 보이지만 항상 고정된 토큰을 반환합니다.

## 에피소드 관리
### GET `/episodes`
- **응답**: `Episode` 객체의 배열

### GET `/episodes/{id}`
- **응답**: ID에 해당하는 `Episode`
- **오류**: 존재하지 않는 ID일 경우 `404 Not Found`

`Episode` 객체는 다음 필드를 포함합니다.
```json
{
  "id": 1,
  "title": "Sample Episode",
  "length": 300,
  "script": "こんにちは"
}
```

## 음성 전사
### POST `/transcribe`
- **요청**: `multipart/form-data` 형식의 음성 파일(`file` 필드)
- **응답**: `{ "transcript_id": "123" }`

### GET `/transcribe/{id}`
- **응답**: `{ "text": "dummy text" }`

현재는 외부 STT 서비스와 연동하지 않고 항상 고정된 값을 반환합니다.

## 단어장 관리
### POST `/vocab`
- **요청 본문**: `VocabWord` 객체 `{ "id": int, "word": "string", "meaning": "string" }`
- **응답**: 저장된 `VocabWord`

### GET `/vocab`
- **응답**: 저장된 단어들의 배열

요청 시마다 내부 목록에 단어를 추가하고 동일한 목록을 반환합니다.

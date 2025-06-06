# Kiko API 인터페이스

이 문서는 `src/app.py`에 구현된 FastAPI 엔드포인트의 개요와 요청/응답 형식을 정리한 것입니다. 실제 서비스 연동은 구현되지 않았으며 모두 목(mock) 동작을 수행합니다.

## 인증
### POST `/auth/signup` 및 `/auth/login`
- **요청 본문**: `{ "username": "string", "password": "string" }`
- **응답**: `{ "token": "<jwt>" }`

두 엔드포인트는 JWT 기반 인증을 제공한다. `/auth/signup`은 새 사용자를 등록하고 즉시 토큰을 반환하며, `/auth/login`은 등록된 사용자 정보를 확인 후 토큰을 돌려준다.

### GET `/settings`
- **헤더**: `Authorization: Bearer <jwt>`
- **응답**: `{ "theme": "light", "font_size": 14, "show_translation": true }`

### PUT `/settings`
- **헤더**: `Authorization: Bearer <jwt>`
- **요청 본문**: 위와 동일한 설정 객체
- **응답**: 저장된 설정 값

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
  "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
  "script": "こんにちは"
}
```

## 음성 전사
### POST `/transcribe`
- **요청**: `multipart/form-data` 형식의 음성 파일(`file` 필드)
- **응답**: `{ "transcript_id": "<uuid>" }`

### GET `/transcribe/{id}`
- **응답**: `{ "text": "<transcribed text>" }`

이제 OpenAI Whisper API를 사용해 실제 음성 인식 결과를 반환합니다. 서버에서 `OPENAI_API_KEY` 환경 변수를 사용해 인증하며, 결과는 메모리에 임시 저장되어 조회할 수 있습니다.

## 단어장 관리
### POST `/vocab`
- **요청 본문**: `VocabWord` 객체 `{ "id": int, "word": "string", "meaning": "string", "example": "string?", "episode_id": int? }`
- **응답**: 저장된 `VocabWord`

### GET `/vocab`
- **응답**: 저장된 단어들의 배열

### GET `/vocab/{id}`
- **응답**: ID에 해당하는 `VocabWord`
- **오류**: 존재하지 않는 ID일 경우 `404 Not Found`

### DELETE `/vocab/{id}`
- **응답**: `{ "status": "deleted" }`
- **오류**: 존재하지 않는 ID일 경우 `404 Not Found`

요청 시마다 내부 목록에 단어를 추가하고 동일한 목록을 반환합니다.

## 번역
### POST `/translate`
- **요청 본문**: `{ "text": "string" }`
- **응답**: `{ "text": "<translated text>" }`

`DEEPL_API_KEY` 환경 변수가 설정되어 있어야 실제 DeepL API로 요청하며, 없을 경우
실패 응답을 반환합니다.

## 사전 조회
### GET `/dictionary/{word}`
- **응답**: `{ "word": "<검색어>", "meaning": "<영어 의미>" }`
- **오류**: Jisho API 조회 실패 시 `500` 응답을 반환

이 엔드포인트는 Jisho 공개 API를 통해 일본어 단어의 영어 뜻을 조회합니다.

## 학습 진도 관리
### PUT `/progress/{episode_id}`
- **헤더**: `Authorization: Bearer <jwt>`
- **요청 본문**: `{ "position": int }`
- **응답**: `{ "episode_id": int, "position": int }`

### GET `/progress/{episode_id}`
- **헤더**: `Authorization: Bearer <jwt>`
- **응답**: `{ "episode_id": int, "position": int }`
- **오류**: 저장된 진도가 없을 경우 `404 Not Found`

### GET `/history`
- **헤더**: `Authorization: Bearer <jwt>`
- **응답**: `[{ "episode_id": int, "position": int }, ...]`

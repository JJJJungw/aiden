from datetime import datetime

#안녕하세요!!!!!!!!
def parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))

#깃허브 테스트 3시23분
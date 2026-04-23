from datetime import datetime

#안녕하세요?????????

def parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))

#안녕만나서반가위애뜰아ㄴㄴ

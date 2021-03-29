from json import dumps, loads


def save_json(filename, data: list[dict]) -> None:
    with open(filename, 'w') as db:
        db.write(dumps(data, indent=4, ensure_ascii=False))


def load_json(filename) -> list[dict]:
    with open(filename) as db:
        return loads(db.read())

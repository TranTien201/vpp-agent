import json
from pathlib import Path

def _load_sort_folders_ja_items() -> list[dict[str, str | None]]:
    instruction_path = (
        Path(__file__).resolve().parents[3] / "db" / "instruction" / "sort_folders_ja.json"
    )
    data = json.loads(instruction_path.read_text(encoding="utf-8"))
    items: list[dict[str, str | None]] = []
    for id_str, obj in data.items():
        items.append(
            {
                "id": str(id_str),
                "name": obj.get("name"),
                "description": obj.get("description"),
            }
        )
    return items
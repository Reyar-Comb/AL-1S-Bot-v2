import json
import os

def get_scramble(mode: str = "3") -> str:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    index_path = os.path.join(BASE_DIR, "Index.json")
    scramble_path = os.path.join(BASE_DIR, "scramble" + mode + ".txt")

    with open(index_path, "r") as f:
        data = json.load(f)
        index = data["index"]


    with open(scramble_path, "r", encoding="utf-8") as f:
        scrambles = f.readlines()
        scramble = scrambles[int(index)].strip()

    
    with open(index_path, "w") as f:
        data["index"] = str((int(index) + 1) % len(scrambles))
        json.dump(data, f)

    return scramble

if __name__ == "__main__":
    print(get_scramble())



import json
import urllib.request
import urllib.error

def fetch(url):
    """Gibt die JSON-Antwort als dict zurück, oder None bei 404."""
    try:
        with urllib.request.urlopen(url) as response:
            return json.load(response)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def main():
    with open("requirements.txt") as f:
        lines = [line.strip() for line in f]

    valid = []

    dep_checked = 0
    noPack = 0
    noVers = 0

    for line in lines:
        name, version = line.split("==")

        if fetch(f"https://pypi.org/pypi/{name}/json") is None:
            noPack += 1
            continue

        data = fetch(f"https://pypi.org/pypi/{name}/{version}/json")
        if data is None:
            noVers += 1
        else:
            valid.append((name, version, data))
        dep_checked += 1

    print(f"Dependencies checked: {dep_checked}")
    print(f"Packages not PyPI: {noPack}")
    print(f"Versions not on PyPI: {noVers}")

    oldest = None  # wird ein Tupel (upload_time, name, version)

    for name, version, data in valid:
        upload_time = data["urls"][0]["upload_time"]  # z. B. "2023-05-22T15:12:44"
        if oldest is None or upload_time < oldest[0]:
            oldest = (upload_time, name, version)

    if oldest is not None:
        upload_time, name, version = oldest
        year = upload_time[:4]
        print(f"Oldest pinned release: {name}=={version} ({year})")



if __name__ == "__main__":
    main()
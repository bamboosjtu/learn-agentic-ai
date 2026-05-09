import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


API_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_MODEL = "gpt-4o-mini"


SYSTEM_PROMPT = """You are a professional technical translator.
Translate the user's Markdown document into Simplified Chinese.

Requirements:
- Preserve the original Markdown structure exactly as much as possible.
- Preserve headings, lists, tables, links, image paths, code fences, inline code, HTML tags, and file paths.
- Do not translate code inside fenced code blocks unless it is obviously plain prose comments outside executable logic.
- Keep command lines, API names, class names, function names, protocol names, and product names unchanged unless there is a standard Chinese rendering.
- Translate natural language prose, captions, and explanatory text into clear Simplified Chinese.
- Output only the translated Markdown. Do not add commentary.
"""


def collect_markdown_files(roots: list[Path]) -> list[Path]:
    files: list[Path] = []
    for root in roots:
        for path in root.rglob("*.md"):
            if path.stem.endswith("_cn"):
                continue
            files.append(path)
    return sorted(files)


def target_path(src: Path) -> Path:
    return src.with_name(f"{src.stem}_cn{src.suffix}")


def read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("unknown", b"", 0, 1, f"Unable to decode {path}")


def call_openai(api_key: str, model: str, content: str, rel_path: str) -> str:
    payload = {
        "model": model,
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Translate this Markdown file to Simplified Chinese.\n"
                    f"Source path: {rel_path}\n\n"
                    f"{content}"
                ),
            },
        ],
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as response:
        body = json.loads(response.read().decode("utf-8"))
    return body["choices"][0]["message"]["content"]


def translate_file(path: Path, root: Path, api_key: str, model: str, overwrite: bool) -> str:
    out_path = target_path(path)
    if out_path.exists() and not overwrite:
        return "skip"

    content = read_text(path)
    translated = call_openai(api_key, model, content, str(path.relative_to(root)))
    out_path.write_text(translated, encoding="utf-8")
    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("roots", nargs="+", help="Root directories to translate recursively")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--delay", type=float, default=0.0)
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY is missing", file=sys.stderr)
        return 1

    roots = [Path(p).resolve() for p in args.roots]
    files = collect_markdown_files(roots)
    if not files:
        print("No markdown files found.")
        return 0

    root_map: dict[Path, Path] = {}
    for file in files:
        for root in roots:
            if str(file).startswith(str(root)):
                root_map[file] = root
                break

    total = len(files)
    done = 0
    skipped = 0
    failed = 0

    for index, file in enumerate(files, start=1):
        try:
            status = translate_file(file, root_map[file], api_key, args.model, args.overwrite)
            if status == "skip":
                skipped += 1
                print(f"[{index}/{total}] skip {file}")
            else:
                done += 1
                print(f"[{index}/{total}] ok   {file}")
        except urllib.error.HTTPError as exc:
            failed += 1
            detail = exc.read().decode("utf-8", errors="replace")
            print(f"[{index}/{total}] fail {file} HTTP {exc.code}: {detail[:400]}", file=sys.stderr)
        except Exception as exc:
            failed += 1
            print(f"[{index}/{total}] fail {file}: {exc}", file=sys.stderr)
        if args.delay:
            time.sleep(args.delay)

    print(f"done={done} skipped={skipped} failed={failed} total={total}")
    return 0 if failed == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())

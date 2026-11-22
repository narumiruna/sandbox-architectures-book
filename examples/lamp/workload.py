"""Apply and test the known fix for the fictional LAMP-17 fixture."""

import subprocess
import sys
from difflib import unified_diff
from pathlib import Path
from tempfile import TemporaryDirectory


def main(input_dir: Path, output_dir: Path) -> None:
    before = (input_dir / "total.c").read_text(encoding="utf-8")
    if before.count("left - right") != 1:
        raise SystemExit("expected the unfixed Lamp fixture")
    print("LAMP-17: loaded", flush=True)

    after = before.replace("left - right", "left + right")
    with TemporaryDirectory() as scratch:
        source = Path(scratch) / "total.c"
        executable = Path(scratch) / "total"
        source.write_text(after, encoding="utf-8")
        subprocess.run(
            ["/usr/bin/gcc", "-std=c17", "-Wall", "-Wextra", source, "-o", executable],
            check=True,
            timeout=5,
        )
        actual = subprocess.check_output([executable], text=True, timeout=5)
    if actual != "5\n":
        raise SystemExit(f"expected output '5', got {actual!r}")

    patch = "".join(
        unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile="a/total.c",
            tofile="b/total.c",
        )
    )
    (output_dir / "change.patch").write_text(patch, encoding="utf-8")
    (output_dir / "test.log").write_text("PASS: total(2, 3) = 5\n", encoding="utf-8")
    print("LAMP-17: passed", flush=True)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: workload.py INPUT_DIR OUTPUT_DIR")
    main(Path(sys.argv[1]), Path(sys.argv[2]))

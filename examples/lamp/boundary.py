"""Build the Linux Bubblewrap command used by the Lamp exercises."""

from pathlib import Path

HERE = Path(__file__).resolve().parent
GUEST_PYTHON = ("/usr/bin/python3", "-I", "-B", "-u")
GUEST_WORKLOAD = (*GUEST_PYTHON, "/lab/workload.py", "/lab/input", "/lab/output")


def sandbox_command(
    input_dir: Path,
    output_dir: Path,
    *worker_args: str,
    writable_input: bool = False,
    visible_other: Path | None = None,
    shared_network: bool = False,
) -> list[str]:
    """Run the fixture by default. Relax one rule only for a control probe."""
    argv = [
        "/usr/bin/bwrap",
        "--unshare-user",
        "--disable-userns",
        "--unshare-ipc",
        "--unshare-pid",
        "--unshare-uts",
        "--new-session",
        "--die-with-parent",
        "--clearenv",
        "--setenv",
        "PATH",
        "/usr/bin",
        "--setenv",
        "TMPDIR",
        "/tmp",
        "--ro-bind",
        "/usr",
        "/usr",
        "--symlink",
        "usr/bin",
        "/bin",
        "--symlink",
        "usr/lib",
        "/lib",
        "--symlink",
        "usr/lib64",
        "/lib64",
        "--dev-bind",
        "/dev/null",
        "/dev/null",
        "--tmpfs",
        "/tmp",
        "--ro-bind",
        str(HERE / "workload.py"),
        "/lab/workload.py",
        "--bind" if writable_input else "--ro-bind",
        str(input_dir.resolve()),
        "/lab/input",
        "--bind",
        str(output_dir.resolve()),
        "/lab/output",
    ]
    if visible_other is not None:
        argv.extend(("--ro-bind", str(visible_other.resolve()), "/lab/other"))
    if not shared_network:
        argv.append("--unshare-net")
    argv.extend(("--remount-ro", "/", "--chdir", "/lab", "--"))
    argv.extend(worker_args or GUEST_WORKLOAD)
    return argv

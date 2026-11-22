# Verifying access rules

Test both sides of every rule: the action that should work and the action that should be denied. If a denied request fails for some other reason, such as a service that is already down, the test has not established that the rule works.

## Make a small access matrix

Use dummy data and a test environment. The example applies the rules from the fictional [Lamp issue workflow](../design/from-issue-to-patch.md).

| Rule | Positive check | Negative check |
| --- | --- | --- |
| Workspace view | The Lamp worker reads its own test marker | The worker cannot write through a read-only mount |
| Network | A trusted caller reaches a test service on the host loopback interface | The worker, with a separate network namespace, cannot reach that same host endpoint |
| Tool authorization | The Lamp reviewer reads `LAMP-17` through the example handler | The same reviewer cannot read a Cedar issue |
| Session separation | Each worker can read the marker in its own workspace | Neither can read the other worker's marker |

## Run the local checks

Run from this book's checkout on Linux. The example uses `uv`, Bubblewrap, and `curl` from `/usr`, with the same merged `/usr` layout as [Measuring a sandbox](measuring-a-sandbox.md). It starts a temporary server on a random loopback port and cleans up after itself. This tests a local process sandbox, not the fictional VM. The handler is a local example with a fixed, synthetic identity, not a test of any live service.

```bash
uv run --locked python - <<'PY'
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
from threading import Thread


def check(condition, message):
    if not condition:
        raise SystemExit(f'FAIL: {message}')
    print(f'PASS: {message}')


class Fixture(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'local fixture')

    def log_message(self, *args):
        pass


def worker(workspace, *command):
    return run([
        'bwrap', '--clearenv', '--setenv', 'PATH', '/usr/bin',
        '--unshare-net', '--unshare-pid', '--new-session', '--die-with-parent',
        '--ro-bind', '/usr', '/usr', '--symlink', 'usr/lib', '/lib',
        '--symlink', 'usr/lib64', '/lib64', '--symlink', 'usr/bin', '/bin',
        '--ro-bind', str(workspace), f'/work/{workspace.name}',
        *command,
    ], capture_output=True, text=True)


with TemporaryDirectory() as directory:
    for own in ('lamp', 'cedar'):
        workspace = Path(directory) / own
        workspace.mkdir()
        (workspace / 'marker').write_text(own)
    for own, other in [('lamp', 'cedar'), ('cedar', 'lamp')]:
        workspace = Path(directory) / own
        result = worker(workspace, '/usr/bin/sh', '-ec',
                        'test "$(/usr/bin/cat "$1")" = "$2"',
                        'sh', f'/work/{own}/marker', own)
        check(result.returncode == 0, f'{own} reads its own marker')
        result = worker(workspace, '/usr/bin/sh', '-ec',
                        'test ! -e "$1"', 'sh', f'/work/{other}/marker')
        check(result.returncode == 0, f'{own} cannot see the {other} marker')
    lamp = Path(directory) / 'lamp'
    result = worker(lamp, '/usr/bin/touch', '/work/lamp/new-file')
    check(result.returncode != 0 and 'Read-only file system' in result.stderr
          and not (lamp / 'new-file').exists(), 'worker cannot write the read-only bind')

    with ThreadingHTTPServer(('127.0.0.1', 0), Fixture) as server:
        thread = Thread(target=server.serve_forever)
        thread.start()
        try:
            url = f'http://127.0.0.1:{server.server_port}/'
            command = ['/usr/bin/curl', '--noproxy', '*', '--fail', '--silent',
                       '--show-error', '--max-time', '2', url]
            result = run(command, capture_output=True, text=True)
            check(result.returncode == 0 and result.stdout == 'local fixture',
                  'host reaches the local endpoint')
            result = worker(lamp, *command)
            check(result.returncode == 7, 'worker cannot connect to that host endpoint')
        finally:
            server.shutdown()
            thread.join()


def lookup_as_lamp_reviewer(project, issue):
    if project != 'Lamp':
        raise PermissionError(project)
    return {'LAMP-17': 'Incorrect item total'}[issue]


check(lookup_as_lamp_reviewer('Lamp', 'LAMP-17') == 'Incorrect item total',
      'authorized project lookup succeeds')
try:
    lookup_as_lamp_reviewer('Cedar', 'CEDAR-9')
except PermissionError:
    check(True, 'another project is denied by the tool handler')
else:
    check(False, 'another project is denied by the tool handler')
try:
    lookup_as_lamp_reviewer('Lamp', 'CEDAR-9')
except KeyError:
    check(True, 'the handler does not fall back to another project')
else:
    check(False, 'the handler does not fall back to another project')
PY
```

On the Ubuntu WSL2 host described in [Measuring a sandbox](measuring-a-sandbox.md#interpret-one-run), all ten checks passed using Bubblewrap 0.11.1 and curl 8.18.0. That result confirms these specific checks for this configuration. It does not prove that all paths, network routes, tools, or sessions are isolated. For a real deployment, repeat the matrix against the actual runtime, policy version, and authorization handler. See [Tool authorization](../design/tool-authorization.md) for where to enforce the project rule.

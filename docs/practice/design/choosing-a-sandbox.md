# Choosing a sandbox

Choose a sandbox by asking what you must protect, who can supply code, and what that code must do. In this illustrative comparison, every setup handles the same Lamp task: look up `LAMP-17`, fix the wrong total in a tiny C program, and return a text patch and test output for review. The task is the same, but the people who can submit code and the resources at risk differ.

## Work from the task to the boundary

1. **List what must stay out of reach.** Include the original repository, other projects' data, credentials, and host files. Mark anything the workload may change, such as its own scratch copy.
2. **Identify who controls the code.** Count anyone who can change source files, tests, build instructions, or the scripts an agent generates from input. Permission to submit code does not imply permission to access the host.
3. **List the required actions.** The lookup script needs one read-only tool and can run in a [restricted interpreter](../../glossary/restricted-interpreter.md). Compiling and running the C program needs a separate Linux worker with a compiler and a writable copy. Neither needs repository write access or a general network connection.

## Three starting choices

### Local agent

A developer starts the run on a Linux workstation, but does not assume the agent's proposed edits or test commands are safe. Protect the developer's home directory, credentials, and original Lamp checkout. An [operating-system process sandbox](../../glossary/operating-system-process-sandbox.md) can run the local toolchain while exposing only the tools and disposable copy the test needs. Check that child processes inherit the restrictions. This choice still shares the host kernel. Use a [virtual machine (VM)](../../glossary/virtual-machine.md) if the worker needs a separate kernel.

### Continuous integration (CI) job

A CI system can test proposed changes automatically. Outside contributors can modify the code the tests execute. Protect the machine that runs the jobs, other jobs, and release credentials. On a shared runner host, choose a fresh VM per job so submitted programs run on a guest kernel separate from the host and other jobs. Give the job no release credentials. A VM does not keep the job's output private: the CI system must restrict who can read the patch and logs it exports.

### Multi-tenant service

Unrelated customers can submit programs. Protect other customers' source, job state, and access to shared capacity. Use a fresh VM per run assigned to one [tenant](../../glossary/tenant.md), with no shared writable workspace and with resource limits. The separate guest kernel limits direct interaction between workloads. It cannot correct a host tool or artifact store that grants Lamp access to Cedar data. Check tenant access at those interfaces too.

Validate the choice with both kinds of checks: the compiler and tests must work on the copy, and a harmless file left outside the worker must stay out of reach. These checks cover the tested paths, not every way to cross the boundary. For runtime comparisons, see [How to evaluate a candidate](../../agent-sandbox-architectures.md#how-to-evaluate-a-candidate).

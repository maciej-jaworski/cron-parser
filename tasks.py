from invoke import task


@task
def lint(c):
    c.run("isort . && black .", pty=True)


@task
def test(c):
    c.run("pytest tests -vv", pty=True)

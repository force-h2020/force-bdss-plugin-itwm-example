import click
import subprocess
from subprocess import check_call

DEFAULT_PYTHON_VERSION = "3.6"
PYTHON_VERSIONS = ["3.6"]

ADDITIONAL_CORE_DEPS = ["scipy>=1.2.1"]

PIP_DEPS = [
    "jax",
    "jaxlib==0.1.39"
]


@click.group()
def cli():
    pass


python_version_option = click.option(
    "--python-version",
    default=DEFAULT_PYTHON_VERSION,
    type=click.Choice(PYTHON_VERSIONS),
    show_default=True,
    help="Python version for the environment",
)


@cli.command(name="install", help="Install the plugin and its dependencies")
@python_version_option
def install(python_version):
    env_name = get_env_name(python_version)
    check_call(
        ["edm", "install", "-e", env_name, "--yes"] + ADDITIONAL_CORE_DEPS
    )

    check_call(
        ["edm", "run", "-e", env_name, "--", "pip", "install", "-e", "."]
    )

    if len(PIP_DEPS):
        check_call(
            [
                "edm", "run", "-e", env_name, "--",
                "pip", "install", "--upgrade", "pip"
             ]
        )
        check_call(
            ["edm", "run", "-e", env_name, "--", "pip", "install"] + PIP_DEPS
        )


@cli.command(help="Run the tests")
@python_version_option
def test(python_version):
    env_name = get_env_name(python_version)

    check_call(
        [
            "edm",
            "run",
            "-e",
            env_name,
            "--",
            "python",
            "-m",
            "unittest",
            "discover",
        ]
    )


@cli.command(help="Run flake")
@python_version_option
def flake8(python_version):
    env_name = get_env_name(python_version)

    check_call(["edm", "run", "-e", env_name, "--", "flake8", "."])


@cli.command(help="Runs the coverage")
@python_version_option
def coverage(python_version):
    env_name = get_env_name(python_version)

    returncode = edm_run(
        env_name, ["coverage", "run", "-m", "unittest", "discover"]
    )
    if returncode:
        raise click.ClickException("There were test failures.")

    returncode = edm_run(env_name, ["pip", "install", "codecov"])
    if not returncode:
        returncode = edm_run(env_name, ["codecov"])

    if returncode:
        raise click.ClickException(
            "There were errors while installing and running codecov."
        )


@cli.command(help="Builds the documentation")
@python_version_option
def docs(python_version):
    env_name = get_env_name(python_version)

    check_call(["edm", "run", "-e", env_name, "--", "make", "html"], cwd="doc")


def get_env_name(python_version):
    return "force-py{}".format(remove_dot(python_version))


def remove_dot(python_version):
    return "".join(python_version.split("."))


def edm_run(env_name, cmd, cwd=None):
    return subprocess.call(["edm", "run", "-e", env_name, "--"] + cmd, cwd=cwd)


if __name__ == "__main__":
    cli()

# 3rd party
import pytest
from coincidence.regressions import AdvancedDataRegressionFixture
from consolekit.testing import CliRunner
from domdf_python_tools.paths import PathPlus

# this package
from greppy.__main__ import main

search_terms = ["Dict", r"(typing\.)?Dict", r"collections\.(Sequence|Mapping|Counter)", "CustomType"]


def test_greppy_simple(
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		):

	(tmp_pathplus / "my_package").mkdir()
	(tmp_pathplus / "my_package" / "__init__.py").write_lines(["def foo(path: PathPlus, name: str) -> int: ..."])
	(tmp_pathplus / "my_package" / "extension.c").write_lines(["# foo"])

	runner = CliRunner(mix_stderr=False)
	result = runner.invoke(main, args=["foo", "--dir", tmp_pathplus.as_posix()])

	data = {}

	data["stdout"] = result.stdout.replace(tmp_pathplus.as_posix(), "...")
	data["stderr"] = result.stderr.replace(tmp_pathplus.as_posix(), "...")

	advanced_data_regression.check(data)

	result = runner.invoke(main, args=["FOO", "--ignore-case", "--dir", tmp_pathplus.as_posix()])

	data = {}

	data["stdout"] = result.stdout.replace(tmp_pathplus.as_posix(), "...")
	data["stderr"] = result.stderr.replace(tmp_pathplus.as_posix(), "...")

	advanced_data_regression.check(data)

	result = runner.invoke(main, args=["FOO", "-i", "--dir", tmp_pathplus.as_posix()])

	data = {}

	data["stdout"] = result.stdout.replace(tmp_pathplus.as_posix(), "...")
	data["stderr"] = result.stderr.replace(tmp_pathplus.as_posix(), "...")

	advanced_data_regression.check(data)


def test_greppy_non_utf8(
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		):
	(tmp_pathplus / "my_package").mkdir()
	(tmp_pathplus / "my_package" / "__init__.py").write_lines(
			["# „…†‡ˆ‰Š", "def foo(path: PathPlus, name: str) -> int: ..."],
			encoding="cp1252",
			)

	runner = CliRunner(mix_stderr=False)
	result = runner.invoke(main, args=["foo", "--dir", tmp_pathplus.as_posix()])

	data = {}

	data["stdout"] = result.stdout.replace(tmp_pathplus.as_posix(), "...")
	data["stderr"] = result.stderr.replace(tmp_pathplus.as_posix(), "...")

	advanced_data_regression.check(data)


@pytest.mark.parametrize("search_term", search_terms)
def test_greppy(
		cloned_repos: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		capsys,
		search_term: str,
		):

	runner = CliRunner(mix_stderr=False)
	result = runner.invoke(main, args=[search_term, "--dir", cloned_repos.as_posix()])

	data = {}

	data["stdout"] = result.stdout.replace(cloned_repos.as_posix(), "...")
	data["stderr"] = result.stderr.replace(cloned_repos.as_posix(), "...")

	advanced_data_regression.check(data)


@pytest.mark.parametrize("search_term", search_terms)
def test_greppy_summary(
		cloned_repos: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		capsys,
		search_term: str,
		):

	runner = CliRunner(mix_stderr=False)
	result = runner.invoke(main, args=[search_term, "--dir", cloned_repos.as_posix()])

	data = {}

	data["stdout"] = result.stdout.replace(cloned_repos.as_posix(), "...")
	data["stderr"] = result.stderr.replace(cloned_repos.as_posix(), "...")

	advanced_data_regression.check(data)

# 3rd party
import pytest
from coincidence.regressions import AdvancedDataRegressionFixture
from domdf_python_tools.paths import PathPlus

# this package
from greppy import greppy


def test_greppy_simple(
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		capsys,
		):
	(tmp_pathplus / "my_package").mkdir()
	(tmp_pathplus / "my_package" / "__init__.py").write_lines(["def foo(path: PathPlus, name: str) -> int: ..."])
	(tmp_pathplus / "my_package" / "extension.c").write_lines(["# foo"])

	data = {}

	greppy("foo", tmp_pathplus)

	outerr = capsys.readouterr()
	data["stdout"] = outerr.out.replace(tmp_pathplus.as_posix(), "...")
	data["stderr"] = outerr.err.replace(tmp_pathplus.as_posix(), "...")

	advanced_data_regression.check(data)


def test_greppy_non_utf8(
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		capsys,
		):
	(tmp_pathplus / "my_package").mkdir()
	(tmp_pathplus / "my_package" / "__init__.py").write_lines(
			["# „…†‡ˆ‰Š", "def foo(path: PathPlus, name: str) -> int: ..."],
			encoding="cp1252",
			)

	data = {}

	greppy("foo", tmp_pathplus)

	outerr = capsys.readouterr()
	data["stdout"] = outerr.out.replace(tmp_pathplus.as_posix(), "...")
	data["stderr"] = outerr.err.replace(tmp_pathplus.as_posix(), "...")

	advanced_data_regression.check(data)


search_terms = ["Dict", r"(typing\.)?Dict", r"collections\.(Sequence|Mapping|Counter)", "CustomType"]


@pytest.mark.parametrize("search_term", search_terms)
def test_greppy(
		cloned_repos: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		capsys,
		search_term: str,
		):

	data = {}

	greppy(search_term, cloned_repos)

	outerr = capsys.readouterr()
	data["stdout"] = outerr.out.replace(cloned_repos.as_posix(), "...")
	data["stderr"] = outerr.err.replace(cloned_repos.as_posix(), "...")
	advanced_data_regression.check(data)


@pytest.mark.parametrize("search_term", search_terms)
def test_greppy_summary(
		cloned_repos: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		capsys,
		search_term: str,
		):

	data = {}

	greppy(search_term, cloned_repos, summary=True)

	outerr = capsys.readouterr()
	data["stdout"] = outerr.out.replace(cloned_repos.as_posix(), "...")
	data["stderr"] = outerr.err.replace(cloned_repos.as_posix(), "...")
	advanced_data_regression.check(data)

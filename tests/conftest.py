# stdlib
from subprocess import PIPE, Popen
from typing import Iterator

# 3rd party
import pytest
from domdf_python_tools.paths import PathPlus, TemporaryPathPlus, in_directory, sort_paths
from git import Repo  # type: ignore

pytest_plugins = ("coincidence", )


@pytest.fixture(scope="session")
def cloned_repos() -> Iterator[PathPlus]:
	with TemporaryPathPlus() as tmp_pathplus:
		repo = Repo.clone_from(
				"https://github.com/domdfcoding/domdf_python_tools",
				tmp_pathplus / "domdf_python_tools",
				)
		repo.git.checkout("63648712285eeaac6c26708e817c8c02595e165e")

		with in_directory(tmp_pathplus / "domdf_python_tools"):
			process = Popen(["tox", "-e", "build"], stdout=PIPE, stderr=PIPE)
			(output_, err) = process.communicate()
			exit_code = process.wait()

		repo = Repo.clone_from("https://github.com/sphinx-toolbox/sphinx-toolbox", tmp_pathplus / "sphinx-toolbox")
		repo.git.checkout("fb7841d1d53e6bc9fe5be3ef92391ec78ff77365")

		repo = Repo.clone_from(
				"https://github.com/repo-helper/repo_helper_github",
				tmp_pathplus / "repo_helper_github",
				)
		repo.git.checkout("db0e713882b7d8191e00ce6ed4eeaec47de2773f")

		yield tmp_pathplus


@pytest.fixture()
def fixed_sort_order(monkeypatch) -> None:

	original_iterchildren = PathPlus.iterchildren

	def iterchildren(self, *args, **kwargs):  # noqa: MAN002
		return sort_paths(*original_iterchildren(self, *args, **kwargs))

	monkeypatch.setattr(PathPlus, "iterchildren", iterchildren)

[![PyPI - Downloads](https://img.shields.io/pypi/dm/file-tree)](https://pypi.org/project/file-tree/)
[![Documentation](https://img.shields.io/badge/Documentation-file--tree-blue)](https://open.win.ox.ac.uk/pages/ndcn0236/file-tree/)
[![Documentation](https://img.shields.io/badge/Documentation-fsleyes-blue)](https://open.win.ox.ac.uk/pages/fsl/fsleyes/fsleyes/userdoc/filetree.html)
[![Pipeline status](https://git.fmrib.ox.ac.uk/ndcn0236/file-tree/badges/master/pipeline.svg)](https://git.fmrib.ox.ac.uk/ndcn0236/file-tree/-/pipelines)
[![Coverage report](https://git.fmrib.ox.ac.uk/ndcn0236/file-tree/badges/master/coverage.svg)](https://open.win.ox.ac.uk/pages/ndcn0236/file-tree/htmlcov)

Framework to represent structured directories in python as FileTree objects. FileTrees can be read in from simple text files describing the directory structure. This is particularly useful for pipelines with large number of input, output, and intermediate files. It can also be used to visualise the data in structured directories using FSLeyes or `file-tree` on the command line.

- General documentation: https://open.win.ox.ac.uk/pages/ndcn0236/file-tree/
- FSLeyes documentation on using FileTrees: https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/userdoc/latest/filetree.html

## Running tests
Tests are run using the [pytest](https://docs.pytest.org) framework. After installation (`pip install pytest`) they can be run from the project root as:
```shell
pytest src/tests
```
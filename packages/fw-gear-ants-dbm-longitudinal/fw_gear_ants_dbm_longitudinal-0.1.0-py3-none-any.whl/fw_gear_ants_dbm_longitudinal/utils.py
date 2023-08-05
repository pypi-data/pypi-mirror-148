import logging
import os
import re
import sys
import typing as t
from functools import partial
from pathlib import Path

import backoff
import flywheel
from flywheel_gear_toolkit.utils.curator import HierarchyCurator
from flywheel_gear_toolkit.utils.datatypes import Container, PathLike
from flywheel_gear_toolkit.utils.walker import Walker
from flywheel_gear_toolkit.utils.zip_tools import zip_output
from joblib import Parallel, delayed

logger = logging.getLogger(__name__)


class FileMatcher:
    def __init__(
        self,
        tags: t.List = None,
        regex_pattern: str = None,
        filetype: str = None,
    ):
        """A Class to match flywheel.FileEntry by tags, filename or filetype."""
        self.tags = tags if tags else []
        if not isinstance(self.tags, list):
            raise TypeError(f"Tags must be of type list, {type(self.tags)} found.")

        self.regex_pattern = regex_pattern if regex_pattern else ""
        self.filetype = filetype
        self.reg = None  # regex compiled
        self._preprocess_regex()

    def _preprocess_regex(self):
        """Build regex from `regex_pattern` and `glob_pattern`"""
        regex = self.regex_pattern

        try:
            self.reg = re.compile(regex)
        except re.error:
            logger.error(f"Invalid regular expression {regex}")
            sys.exit(1)

    def match(self, file: flywheel.FileEntry):
        """Returns True if file matches, False otherwise."""
        if self.filetype and file.type != self.filetype:
            return False

        if self.tags and not all([t in file.tags for t in self.tags]):
            return False

        if self.reg and not self.reg.match(file.name):
            return False
        return True


class FileFinder(HierarchyCurator):
    """A curator to find files matching regex filename and tags."""

    def __init__(
        self,
        *args,
        regex_pattern: str = None,
        tags: t.List = None,
        filetype: str = None,
        **kwargs,
    ):
        super(FileFinder, self).__init__(*args, **kwargs)
        self.files_mapping = []
        self.file_matcher = FileMatcher(
            tags=tags,
            regex_pattern=regex_pattern,
            filetype=filetype,
        )

    def curate_session(self, session: flywheel.Session):
        for acquisition in session.acquisitions.iter():
            acquisition = acquisition.reload()
            for f in acquisition.files:
                if self.file_matcher.match(f):
                    self.files_mapping.append((session.label, f))


def find_matching_files(
    parent_container: Container,
    tags: t.List = None,
    regex: str = None,
    filetype: str = None,
):
    """Returns files matching tags/regex"""
    my_walker = Walker(parent_container)
    finder = FileFinder(regex_pattern=regex, tags=tags, filetype=filetype)
    for container in my_walker.walk():
        finder.curate_container(container)
    return finder.files_mapping


def is_error_in(exc, errors=None):
    """Return True if exception status is in errors."""
    if errors is None:
        errors = []
    if hasattr(exc, "status"):
        if exc.status in errors:
            return True
    return False


def is_error_not_in(exc, errors=None):
    """Return True if exception status is NOT in errors."""
    return not is_error_in(exc, errors=errors)


@backoff.on_exception(
    backoff.expo,
    flywheel.rest.ApiException,
    max_tries=5,
    giveup=partial(is_error_not_in, errors=[500, 502, 504]),
)
def download_file(f: flywheel.FileEntry, dst_path: PathLike = None):
    """Download file robustly to dst_path

    Args:
        f (flywheel.FileEntry): A Flywheel file.
        dst_path (PathLike): A Path-like.

    Returns:
        (Path-like): Returns the destination path.
    """
    dst_path = Path(dst_path)
    if dst_path.exists():
        raise ValueError(f"Destination path already exists {f}")
    if not dst_path.parent.exists():
        dst_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info(
        f"Downloading  {f.name} from {f.parent_ref['type']} {f.parent_ref['id']}..."
    )
    f.download(dst_path)
    return dst_path


def download_files(
    files_collection: t.List[t.Tuple[str, flywheel.FileEntry]],
    dest_dir: PathLike = None,
):
    """Download files to destination_dir under file.id / file.name.

    Args:
        files_collection (list): List of tuples that contain session.label and flywheel.FileEntry.
        dest_dir (PathLike): The folder where to download the files.

    Returns:
        list: A list containing all file paths.
    """
    dest_dir = Path(dest_dir)
    if not dest_dir.exists():
        logger.debug(f"Creating destination folder {dest_dir}")
        dest_dir.mkdir(parents=True)

    input_paths_res = Parallel(n_jobs=-1, prefer="threads")(
        delayed(download_file)(f[1], Path(dest_dir) / f"{f[0]}-{f[1].name}")
        for f in files_collection
    )

    return input_paths_res


def generate_directory_listing(destination_path, except_list, target_file):
    """List all subdirectory and files in destination directory and append to targeted file."""

    os.chdir(destination_path.parent)

    with open(target_file, "a+") as f:
        for path, dirs, files in os.walk(destination_path):
            sep = (
                "\n---------- "
                + path.split(os.path.sep)[len(path.split(os.path.sep)) - 1]
                + " ----------"
            )
            f.write(f"{sep}\n")

            for fn in sorted(files):
                if not any(Path(x).name in fn for x in except_list):
                    f.write(f"{fn}\n")

    f.close()


def parse_and_zip_directory(output_dir, summary_file=None):
    """
    Walk through output directory and generate a zip archive.
    If summary_file is provided, a summary of the output directory will be generated.
    """

    template_dir_path = Path(output_dir)
    os.chdir(template_dir_path.parent)
    zip_archive_name = template_dir_path.name + ".zip"

    except_list = list()

    for path_obj in template_dir_path.rglob("*"):
        # find deny file(s)
        if path_obj.is_file():
            if path_obj.name.startswith("."):
                # building proper path to add to list
                deny_fp = path_obj.relative_to(Path.cwd()).as_posix()
                except_list.append(deny_fp)

    try:

        zip_output(
            template_dir_path.parent,
            template_dir_path.name,
            zip_archive_name,
            exclude_files=except_list,
        )
    except Exception:
        logger.exception("Uncaught Exception occurred.")
    else:
        logger.info(f"Successfully created {zip_archive_name}...")

    if summary_file:
        generate_directory_listing(template_dir_path, except_list, summary_file)


def setup_logger(name, log_file, level=logging.INFO):
    """To setup customized logger"""

    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)

    tmp_logger = logging.getLogger(name)
    tmp_logger.setLevel(level)
    tmp_logger.addHandler(handler)

    return tmp_logger

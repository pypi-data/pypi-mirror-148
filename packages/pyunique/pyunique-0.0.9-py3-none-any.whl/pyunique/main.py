"""
main entry point to the program
"""
import os

import pylogconf.core
import tqdm
from pytconf import register_main, config_arg_parse_and_launch, register_endpoint

from pyunique.archive import get_archive
from pyunique.configs import ConfigScan, ConfigAlgo, ConfigLMDB
from pyunique.digest import digest_file_bytes
from pyunique.static import VERSION_STR

from pyunique.utils import get_logger, get_number_of_files


@register_endpoint(
    description="Scan a folder and register it's checksums",
    configs=[
        ConfigScan,
        ConfigAlgo,
        ConfigLMDB,
    ],
)
def scan() -> None:
    archive = get_archive()
    archive.start_write()
    logger = get_logger()
    logger.info("Scanning for number of files...")
    num_files = get_number_of_files(folder=ConfigScan.folder)
    with tqdm.tqdm(total=num_files) as progress_bar:
        for root, _directories, files in os.walk(ConfigScan.folder):
            for file in files:
                filename = os.path.join(root, file)
                filename = os.path.abspath(filename)
                logger.debug(f"doing {filename}")
                if archive.get_digest(filename=filename) is None:
                    digest = digest_file_bytes(filename=filename)
                    archive.add_digest(filename=filename, digest=digest)
                progress_bar.update()
    archive.end_write()
    archive.close()


@register_endpoint(
    description="Scan the DB and remove any entries which are no longer valid",
    configs=[
        ConfigScan,
        ConfigAlgo,
        ConfigLMDB,
    ],
)
def clean_db() -> None:
    logger = get_logger()
    archive = get_archive()
    archive.start_write()
    count = archive.count()
    errors = 0
    with tqdm.tqdm(total=count) as progress_bar:
        for filename, _digest in archive.yield_all_items():
            if not os.path.isfile(filename):
                errors += 1
                logger.debug(f"problem with filename {filename}")
                archive.delete(filename=filename)
            progress_bar.update()
    archive.end_write()
    archive.close()
    logger.info(f"number of errors is {errors}")


@register_endpoint(
    description="Check filenames in a certain folder",
    configs=[
        ConfigScan,
        ConfigAlgo,
        ConfigLMDB,
    ],
)
def check_filenames() -> None:
    logger = get_logger()
    errors = 0
    error_filenames = []
    logger.info("Scanning for number of files...")
    num_files = get_number_of_files(folder=ConfigScan.folder)
    with tqdm.tqdm(total=num_files) as progress_bar:
        for root, _directories, files in os.walk(ConfigScan.folder):
            for file in files:
                filename = os.path.join(root, file)
                filename = os.path.abspath(filename)
                logger.debug(f"doing {filename}")
                try:
                    filename.encode(ConfigAlgo.encoding)
                except UnicodeEncodeError:
                    errors += 1
                    error_filenames.append(filename)
                progress_bar.update()
    logger.info(f"number of errors is {errors}")
    for error_filename in error_filenames:
        logger.info(error_filename)


@register_main(
    main_description="pyunique will help you remove duplicate files",
    app_name="pyunique",
    version=VERSION_STR,
)
def main():
    pylogconf.core.setup()
    config_arg_parse_and_launch()


if __name__ == '__main__':
    main()

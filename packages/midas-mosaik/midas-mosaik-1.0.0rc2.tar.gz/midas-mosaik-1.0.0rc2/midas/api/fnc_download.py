import os
import shutil
from importlib import import_module
from typing import List, Optional

import click
from midas.util.runtime_config import RuntimeConfig

from . import LOG

# from .download.download_commercials import download_commercials
# from .download.download_dlp import download_dlp
# from .download.download_gen import download_gen
# from .download.download_simbench import download_simbench
# # from .download.download_smartnord import download_smart_nord
# from .download.download_weather import download_weather


def download(
    keep_tmp: bool = False,
    force: bool = False,
    modules: Optional[List[str]] = None,
):
    """Download the required datasets.

    There are currently five categories of datasets:
        * Default load profiles from BDEW
        * Commercial dataset from openei.org
        * Simbench data from the simbench grids
        * Smart Nord dataset from the research project Smart Nord
        * Weather dataset from opendata.dwd.de

    The default behavior of this function is to download all missing
    datasets and, afterwards, remove the temporary directory created
    during this process.

    If at least one of the flags is set to *True*, only those datasets
    will be downloaded. If *force* is *True*, the datasets will be
    downloaded regardless of any existing dataset. If *keep_tmp* is
    *True*, the temporary downloaded files will not be removed
    afterwards.

    """
    # # Check parameters
    if not modules:
        if_necessary = True
    else:
        if_necessary = False

    # Create paths
    data_path = RuntimeConfig().paths["data_path"]
    tmp_path = os.path.abspath(os.path.join(data_path, "tmp"))
    os.makedirs(tmp_path, exist_ok=True)

    default_modules = RuntimeConfig().modules["default_modules"]
    for module in default_modules:
        if not if_necessary:
            if module[0] not in modules:
                LOG.info("Skipping module %s.", module[0])
                continue
        LOG.info("Attempting to download data from module %s...", module[0])

        if ":" in module[1]:
            mod = module[1].split(":")[0]
        else:
            mod = module[1].rsplit(".", 1)[0]
        try:
            LOG.debug("Importing module %s...", mod)
            mod = import_module(mod)
        except ImportError:
            LOG.warning(
                "Could not import default module %s. Consider "
                "installing with pip install midas-%s.",
                module[0],
                module[0],
            )
            continue
        try:
            LOG.debug("Calling download function of %s...", module[0])
            mod.download(data_path, tmp_path, if_necessary, force)
        except AttributeError as err:
            LOG.debug(
                "Module %s does not provide any downloads: %s.", module[0], err
            )

    custom_modules = RuntimeConfig().modules["custom_modules"]
    for module in custom_modules:
        if not if_necessary:
            if module[0] not in modules:
                continue

        if ":" in module[1]:
            mod = module[1].split(":")[0]
        else:
            mod = module[1].rsplit(".", 1)[0]
        try:
            mod = import_module(mod)
        except ImportError:
            LOG.warning(
                "Could not import default module %s. Consider "
                "installing with pip install midas-%s.",
                module[0],
                module[0],
            )
            continue
        try:
            mod.download(data_path, tmp_path, if_necessary, force)
        except AttributeError:
            LOG.debug("Module %s does not provide any downloads.", module[0])

    # Clean up
    if not keep_tmp:
        try:
            shutil.rmtree(tmp_path)
        except Exception as err:
            click.echo(
                f"Failed to remove files '{tmp_path}'': {err}. "
                "You have to remove those files manually."
            )
            LOG.warning(
                "Could not remove temporary files at %s. You have to remove "
                "those files by hand. The error is: %s",
                tmp_path,
                err,
            )

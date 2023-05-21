from pathlib import Path
import os
from typing import List
import json
from loguru import logger


def get_all_files(dir_path: Path, file_formats: List[str]) -> List[Path]:
    """Get the image files in the given image directory that have
    the specified image format.

    Parameters
    ----------
    dir_path
    file_formats: The image formats

    Returns
    -------
    An instance of List[Path]
    """

    # load the corrosion images
    files = os.listdir(dir_path)

    files_out: List[Path] = []

    for filename in files:
        if os.path.isfile(dir_path / filename):

            filename_, file_extension = os.path.splitext(filename)

            if file_extension in file_formats:
                files_out.append(dir_path / filename)
            else:
                continue

    return files_out


def build_checkpoint_to_survey_item_map(path_to_checkpoints: Path) -> dict:

    files = get_all_files(dir_path=path_to_checkpoints,
                          file_formats=['.json'])

    if len(files) == 0:
        logger.warning(f"No json files found in path {path_to_checkpoints}")
    else:
        logger.info(f"Found {len(files)} json files in path {path_to_checkpoints}")

    checkpoint_to_survey_item_map={}

    for filename in files:

        logger.info(f"Processing json file {filename}")
        with open(filename, 'r') as f:
            doc = json.load(f)

            checkpoint_types_enum = doc['checkpoint_types_enum']

            for checkpoint in checkpoint_types_enum:
                survey_item_type = checkpoint['survey_item_type']
                checkpoint_type = checkpoint['checkpoint_type']

                if survey_item_type in checkpoint_to_survey_item_map:
                    checkpoint_to_survey_item_map[survey_item_type].append(checkpoint_type)
                else:
                    checkpoint_to_survey_item_map[survey_item_type] = [checkpoint_type]

    return checkpoint_to_survey_item_map

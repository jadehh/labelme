#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : labelmeConfig.py
# @Author   : jade
# @Date     : 2022/6/6 15:11
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
# flake8: noqa

import logging
import sys

from qtpy import QT_VERSION


__appname__ = "labelme"

# Semantic Versioning 2.0.0: https://semver.org/
# 1. MAJOR version when you make incompatible API changes;
# 2. MINOR version when you add functionality in a backwards-compatible manner;
# 3. PATCH version when you make backwards-compatible bug fixes.
__version__ = "4.5.7"

QT4 = QT_VERSION[0] == "4"
QT5 = QT_VERSION[0] == "5"
del QT_VERSION

PY2 = sys.version[0] == "2"
PY3 = sys.version[0] == "3"
del sys

from src.label_file import LabelFile
from src.label_io import lblsave

from src.image import apply_exif_orientation
from src.image import img_arr_to_b64
from src.image import img_b64_to_arr
from src.image import img_data_to_arr
from src.image import img_data_to_pil
from src.image import img_data_to_png_data
from src.image import img_pil_to_data

from src.util_shape import labelme_shapes_to_label
from src.util_shape import masks_to_bboxes
from src.util_shape import polygons_to_mask
from src.util_shape import shape_to_mask
from src.util_shape import shapes_to_label

from src.qt import newIcon
from src.qt import newButton
from src.qt import newAction
from src.qt import addActions
from src.qt import labelValidator
from src.qt import struct
from src.qt import distance
from src.qt import distancetoline
from src.qt import fmtShortcut

import os.path as osp
import shutil

import yaml

from src.logger import logger


here = osp.dirname(osp.abspath(__file__))


def update_dict(target_dict, new_dict, validate_item=None):
    for key, value in new_dict.items():
        if validate_item:
            validate_item(key, value)
        if key not in target_dict:
            logger.warn("Skipping unexpected key in config: {}".format(key))
            continue
        if isinstance(target_dict[key], dict) and isinstance(value, dict):
            update_dict(target_dict[key], value, validate_item=validate_item)
        else:
            target_dict[key] = value


# -----------------------------------------------------------------------------


def get_default_config():
    config_file = osp.join("config", "default_config.yaml")
    with open(config_file) as f:
        config = yaml.safe_load(f)

    # save default config to ~/.labelmerc
    user_config_file = osp.join(osp.expanduser("~"), ".labelmerc")
    if not osp.exists(user_config_file):
        try:
            shutil.copy(config_file, user_config_file)
        except Exception:
            logger.warn("Failed to save config: {}".format(user_config_file))

    return config


def validate_config_item(key, value):
    if key == "validate_label" and value not in [None, "exact"]:
        raise ValueError(
            "Unexpected value for config key 'validate_label': {}".format(
                value
            )
        )
    if key == "shape_color" and value not in [None, "auto", "manual"]:
        raise ValueError(
            "Unexpected value for config key 'shape_color': {}".format(value)
        )
    if key == "labels" and value is not None and len(value) != len(set(value)):
        raise ValueError(
            "Duplicates are detected for config key 'labels': {}".format(value)
        )


def get_config(config_file_or_yaml=None, config_from_args=None):
    # 1. default config
    config = get_default_config()

    # 2. specified as file or yaml
    if config_file_or_yaml is not None:
        config_from_yaml = yaml.safe_load(config_file_or_yaml)
        if not isinstance(config_from_yaml, dict):
            with open(config_from_yaml) as f:
                logger.info(
                    "Loading config file from: {}".format(config_from_yaml)
                )
                config_from_yaml = yaml.safe_load(f)
        update_dict(
            config, config_from_yaml, validate_item=validate_config_item
        )

    # 3. command line argument or specified config file
    if config_from_args is not None:
        update_dict(
            config, config_from_args, validate_item=validate_config_item
        )

    return config

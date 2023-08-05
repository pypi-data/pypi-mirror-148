#  -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>

"""Main module."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ecs_composex.mods_manager import XResourceModule

from ecs_composex.common import build_template
from ecs_composex.common.stacks import ComposeXStack
from ecs_composex.compose.x_resources.helpers import (
    set_lookup_resources,
    set_new_resources,
    set_resources,
)

from .msk_cluster import MskCluster
from .msk_cluster_template import build_msk_clusters


class XStack(ComposeXStack):
    """
    Class to handle MSK resources
    """

    def __init__(self, title: str, settings, module: XResourceModule, **kwargs):
        set_resources(settings, MskCluster, module)
        x_resources = settings.compose_content[module.res_key].values()
        lookup_resources = set_lookup_resources(x_resources)
        if lookup_resources:
            pass
        new_resources = set_new_resources(x_resources, True)
        if new_resources:
            stack_template = build_template(f"{module.res_key} - Root Stack")
            super().__init__(title, stack_template, **kwargs)
            build_msk_clusters(new_resources, stack_template)
        else:
            self.is_void = True
        for resource in x_resources:
            resource.stack = self

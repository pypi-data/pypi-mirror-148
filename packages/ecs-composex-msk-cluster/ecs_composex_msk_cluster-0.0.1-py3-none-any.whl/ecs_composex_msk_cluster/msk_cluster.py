#   -*- coding: utf-8 -*-
#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2022 John Mille <john@compose-x.io>

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ecs_composex.mods_manager import XResourceModule
    from ecs_composex.common.settings import ComposeXSettings

from ecs_composex.compose.x_resources.network_x_resources import NetworkXResource
from ecs_composex.vpc.vpc_params import STORAGE_SUBNETS
from troposphere import GetAtt, Ref

from ecs_composex_msk_cluster.msk_cluster_params import (
    MSK_CLUSTER_ARN,
    MSK_CLUSTER_SG_PARAM,
)


class MskCluster(NetworkXResource):
    """
    Class to manage MSK Cluster resource
    """

    def __init__(
        self,
        name: str,
        definition: dict,
        module: XResourceModule,
        settings: ComposeXSettings,
    ):
        super().__init__(name, definition, module, settings)

        self.security_group_param = MSK_CLUSTER_SG_PARAM
        self.subnets_override = STORAGE_SUBNETS

    def init_outputs(self):
        return {
            MSK_CLUSTER_ARN: (self.logical_name, self.cfn_resource, Ref, None),
            MSK_CLUSTER_SG_PARAM: (
                f"{self.logical_name}{self.security_group_param.title}",
                self.security_group,
                GetAtt,
                self.security_group_param.return_value,
            ),
        }

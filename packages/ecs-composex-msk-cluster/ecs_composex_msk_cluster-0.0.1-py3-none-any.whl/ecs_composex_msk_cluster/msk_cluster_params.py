#   -*- coding: utf-8 -*-
#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2022 John Mille <john@compose-x.io>


from ecs_composex.common.cfn_params import Parameter
from ecs_composex.vpc.vpc_params import SG_ID_TYPE

MSK_CLUSTER_SG_PARAM_T = "MSKClusterSecurityGroup"
MSK_CLUSTER_SG_PARAM = Parameter(
    MSK_CLUSTER_SG_PARAM_T,
    group_label="MSK Settings",
    return_value="GroupId",
    Type=SG_ID_TYPE,
)

MSK_CLUSTER_ARN_T = "MskClusterArn"
MSK_CLUSTER_ARN = Parameter(
    MSK_CLUSTER_ARN_T, group_label="MSK Settings", Type="String"
)

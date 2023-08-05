#   -*- coding: utf-8 -*-
#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2022 John Mille <john@compose-x.io>

from compose_x_common.compose_x_common import set_else_none
from ecs_composex.common.cfn_params import ROOT_STACK_NAME_T
from ecs_composex.resources_import import import_record_properties
from ecs_composex.vpc.vpc_params import VPC_ID
from troposphere import GetAtt, Ref, Sub
from troposphere.ec2 import SecurityGroup
from troposphere.msk import ClientAuthentication, CloudWatchLogs
from troposphere.msk import Cluster as AwsMskCluster

from .msk_cluster_params import MSK_CLUSTER_SG_PARAM


def build_msk_clusters(new_resources, template):
    """
    Creates a new MSK cluster from properties

    :param list[ecs_composex_msk_cluster.msk_cluster.MskCluster] new_resources:
    :param troposhere.Template template:
    """
    for cluster in new_resources:
        cluster.security_group = template.add_resource(
            SecurityGroup(
                f"{cluster.logical_name}SecurityGroup",
                GroupName=Sub(f"${{{ROOT_STACK_NAME_T}}}-{cluster.logical_name}"),
                GroupDescription=Sub(f"${{{ROOT_STACK_NAME_T}}} ${cluster.name}"),
                VpcId=Ref(VPC_ID),
            )
        )
        cluster_sg_id = GetAtt(
            cluster.security_group, MSK_CLUSTER_SG_PARAM.return_value
        )
        cluster_props = import_record_properties(cluster.properties, AwsMskCluster)
        broker_info = set_else_none("BrokerNodeGroupInfo", cluster_props, {})
        security_groups = set_else_none("SecurityGroups", broker_info, [cluster_sg_id])
        if security_groups and cluster_sg_id not in security_groups:
            security_groups.append(
                GetAtt(cluster.security_group, MSK_CLUSTER_SG_PARAM.return_value)
            )
        if broker_info:
            setattr(broker_info, "SecurityGroups", security_groups)
            client_subnets = set_else_none("ClientSubnets", broker_info)
            if not client_subnets:
                setattr(broker_info, "ClientSubnets", Ref(cluster.subnets_override))
        else:
            cluster_props.update(
                {
                    "BrokerNodeGroupInfo": {"SecurityGroups": security_groups},
                    "ClientSubnets": Ref(cluster.subnets_override),
                }
            )
        cluster.cfn_resource = AwsMskCluster(cluster.logical_name, **cluster_props)
        template.add_resource(cluster.cfn_resource)

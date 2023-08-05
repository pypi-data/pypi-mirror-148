
.. meta::
    :description: ECS Compose-X MSK Cluster
    :keywords: AWS, ECS, docker, compose, MSK, kafka

================
msk_cluster
================

.. image:: https://img.shields.io/pypi/v/ecs_composex_msk_cluster.svg
    :target: https://pypi.python.org/pypi/ecs_composex_msk_cluster


This package is an extension to `ECS Compose-X`_ that manages Creation of new MSK clusters and automatically links
to services to grant access and permissions.

Install
==========

.. code-block:: bash

    python3 -m venv venv
    source venv/bin/activate
    # With poetry

    pip install pip poetry -U
    poetry install

    # Via pip
    pip install pip -U
    pip install ecs-composex-msk-cluster

Syntax Reference
==================

.. code-block:: yaml

    x-msk_cluster:
          Properties: {}
          Lookup: {}
          Settings: {}
          Services: {}

Properties
--------------

See `Properties for MSK Cluster`_ in AWS Cloudformation documentation.


Lookup
--------

Lookup is not yet implemented.

Services
---------

Mappings between the MSK cluster and the services. To be implemented.


.. _ECS Compose-X: https://docs.compose-x.io
.. _Properties for MSK Cluster: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html

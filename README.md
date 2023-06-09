# OpenStack CCloud CLI Extension for Placement commands

This plugin adds more commands for handling the
[``Placement``](https://docs.openstack.org/placement/latest/) service as the
``osc-placement`` plugin doesn't expose all the functionality we require.

## Installation

Use the following command to install this extension in the same Python
virtualenv where ``python-openstackclient`` is installed.

```bash
pip install git+https://github.com/sapcc/osc-ccloud-placement-extended
```

The extension should be found automatically. You can check by running any of
the contained commands e.g. ``openstack resource provider trait add --help``.

## Contained Commands

The extension implements the following commands:

#### ``resource provider trait add``

Since ``Placement`` requires the full set of traits to be passed in the API
call and ``openstack resource provider trait set`` implements it the same, it's
hard to add a new trait to a resource provider. ``openstack resource provider
trait add <RP_UUID> <TRAIT>`` works around this shortcoming by fetching all
traits first and then setting all of them including the new one.

#### ``resource provider trait remove``

The command ``openstack resource provider trait remove <RP_UUID> <TRAIT>`` has
the opposite functionality of the above ``openstack resource provider trait
add``.

from typing import Any
from typing import Dict


async def update_ipv6_cidr_blocks(
    hub,
    ctx,
    subnet_id: str,
    old_ipv6_cidr_block: Dict[str, Any],
    new_ipv6_cidr_block: Dict[str, Any],
):
    """
    Update associated ipv6 cidr block of a subnet. This function supports associating an ipv6 cidr block, or updating
     the existing(old) ipv6 cidr block to the new ipv6 cidr block. Disassociating an ipv6 cidr block is not supported,
     due to how an sls file works currently. If ipv6_cidr_block parameter is left as blank, Idem-aws will do no-op
     on the subnet's ipv6 cidr block. To disassociate an ipv6 cidr block, a user will have to delete the subnet and
     re-create it without the ipv6 cidr block.

    Args:
        hub:
        ctx:
        subnet_id: The AWS resource id of the existing subnet
        old_ipv6_cidr_block: The ipv6 cidr block on the existing vpc
        new_ipv6_cidr_block: The expected ipv6 cidr block on the existing vpc

    Returns:
        {"result": True|False, "comment": A message Tuple, "ret": Dict}

    """
    result = dict(comment=(), result=True, ret=None)
    if old_ipv6_cidr_block is None and new_ipv6_cidr_block:
        if ctx.get("test", False):
            result["ret"] = {
                "ipv6_cidr_block": new_ipv6_cidr_block.get("Ipv6CidrBlock")
            }
            return result
        else:
            ret = await hub.exec.boto3.client.ec2.associate_subnet_cidr_block(
                ctx,
                SubnetId=subnet_id,
                Ipv6CidrBlock=new_ipv6_cidr_block.get("Ipv6CidrBlock"),
            )
            result["result"] = ret["result"]
            if result["result"]:
                hub.log.info(
                    f"Add subnet {subnet_id} ipv6 cidr block {new_ipv6_cidr_block.get('Ipv6CidrBlock')}"
                )
                result["ret"] = {
                    "ipv6_cidr_block": new_ipv6_cidr_block.get("Ipv6CidrBlock")
                }
            else:
                result["comment"] = ret["comment"]
            return result
    elif old_ipv6_cidr_block and new_ipv6_cidr_block:
        if old_ipv6_cidr_block.get("Ipv6CidrBlock") != new_ipv6_cidr_block.get(
            "Ipv6CidrBlock"
        ):
            if ctx.get("test", False):
                result["ret"] = {
                    "ipv6_cidr_block": new_ipv6_cidr_block.get("Ipv6CidrBlock")
                }
                return result
            else:
                ret = await hub.exec.boto3.client.ec2.disassociate_subnet_cidr_block(
                    ctx, AssociationId=old_ipv6_cidr_block.get("AssociationId")
                )
                if not ret.get("result"):
                    result["comment"] = ret["comment"]
                    result["result"] = False
                    return result
                ret = await hub.exec.boto3.client.ec2.associate_subnet_cidr_block(
                    ctx,
                    SubnetId=subnet_id,
                    Ipv6CidrBlock=new_ipv6_cidr_block.get("Ipv6CidrBlock"),
                )
                result["result"] = ret["result"]
                if result["result"]:
                    hub.log.info(
                        f"Update subnet {subnet_id} ipv6 cidr block from {old_ipv6_cidr_block.get('Ipv6CidrBlock')}"
                        f" to {new_ipv6_cidr_block.get('Ipv6CidrBlock')}"
                    )
                    result["ret"] = {
                        "ipv6_cidr_block": new_ipv6_cidr_block.get("Ipv6CidrBlock")
                    }
                    return result
                else:
                    result["comment"] = ret["comment"]
    return result


async def update_subnet_attributes(
    hub,
    ctx,
    before: Dict[str, Any],
    resource_id: str,
    map_public_ip_on_launch: bool,
):
    """
    Updates the Subnet Attributes
    Args:
        before: existing resource
        resource_id (Text) -- AWS Subnet ID
        map_public_ip_on_launch (boolean) -- Indicates whether instances launched in this subnet receive a public IPv4 address.

    Returns:
        {"result": True|False, "comment": A message Tuple, "ret": None|Updated Attributes name and value}

    """
    result = dict(comment=(), result=True, ret={})

    if map_public_ip_on_launch is not None and map_public_ip_on_launch != before.get(
        "MapPublicIpOnLaunch"
    ):
        if not ctx.get("test", False):
            update_ret = await hub.exec.boto3.client.ec2.modify_subnet_attribute(
                ctx,
                SubnetId=resource_id,
                MapPublicIpOnLaunch={"Value": map_public_ip_on_launch},
            )
            if not update_ret["result"]:
                result["comment"] = result["comment"] + update_ret["comment"]
                result["result"] = False
                return result
        result["ret"]["map_public_ip_on_launch"] = map_public_ip_on_launch
        result["comment"] = result["comment"] + (
            f"Updated MapPublicIpOnLaunch attribute to {map_public_ip_on_launch} on subnet {resource_id}",
        )

    return result

'''
# cdk-vpc-module

cdk-vpc-module construct library is an open-source extension of the AWS Cloud Development Kit (AWS CDK) to deploy configurable aws vpc  and its individual components in less than 50 lines of code and human readable configuration which can be managed by pull requests!

## :sparkles: Features

* :white_check_mark: Option to configure custom IPv4 CIDR(10.10.0.0/24)
* :white_check_mark: VPC Peering with  route table entry
* :white_check_mark: Configurable NACL as per subnet group
* :white_check_mark: NATGateway as per availabilityZones

Using cdk a vpc can be deployed using the following sample code snippet:

```python
import { Network } from "@smallcase/cdk-vpc-module/lib/constructs/network";
import { aws_ec2 as ec2, App, Stack, StackProps } from "aws-cdk-lib";
import { Construct } from "constructs";

export class VPCStack extends Stack {
  constructor(scope: Construct, id: string, props: StackProps = {}) {
    super(scope, id, props);
    new Network(this, 'NETWORK', {
      vpc: {
        cidr: '10.10.0.0/16',
        subnetConfiguration: [],
      },
      peeringConfigs: {
        "TEST-PEERING": { // this key will be used as your peering id, which you will have to mention below when you configure a route table for your subnets
          peeringVpcId: "vpc-0000",
          tags: {
            "Name": "TEST-PEERING to CREATED-VPC",
            "Description": "Connect"
          }
        }
      },
      subnets: [
        {
          subnetGroupName: 'NATGateway',
          subnetType: ec2.SubnetType.PUBLIC,
          cidrBlock: ['10.10.0.0/28', '10.10.0.16/28', '10.10.0.32/28'],
          availabilityZones: ['ap-south-1a', 'ap-south-1b', 'ap-south-1c'],
          ingressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
          routes: [
          ],
          egressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
        },
        {
          subnetGroupName: 'Public',
          subnetType: ec2.SubnetType.PUBLIC,
          cidrBlock: ['10.10.2.0/24', '10.10.3.0/24', '10.10.4.0/24'],
          availabilityZones: ['ap-south-1a', 'ap-south-1b', 'ap-south-1c'],
          ingressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
          egressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
          routes: [
          ],
          tags: {
            // if you use this vpc for your eks cluster, you have to tag your subnets [read more](https://aws.amazon.com/premiumsupport/knowledge-center/eks-vpc-subnet-discovery/)
            'kubernetes.io/role/elb': '1',
            'kubernetes.io/cluster/TEST-CLUSTER': 'owned',
          },
        },
        {
          subnetGroupName: 'Private',
          subnetType: ec2.SubnetType.PRIVATE_WITH_NAT,
          cidrBlock: ['10.10.5.0/24', '10.10.6.0/24', '10.10.7.0/24'],
          availabilityZones: ['ap-south-1a', 'ap-south-1b', 'ap-south-1c'],
          ingressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
          egressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },

          ],
          routes: [
            {
            // if you use this vpc for your eks cluster, you have to tag your subnets [read more](https://aws.amazon.com/premiumsupport/knowledge-center/eks-vpc-subnet-discovery/)
              routerType: ec2.RouterType.VPC_PEERING_CONNECTION,
              destinationCidrBlock: "<destinationCidrBlock>",
              //<Your VPC PeeringConfig KEY, in this example TEST-PEERING will be your ID>
              existingVpcPeeringRouteKey: "TEST-PEERING"
            }
          ],
          tags: {
            'kubernetes.io/role/internal-elb': '1',
            'kubernetes.io/cluster/TEST-CLUSTER': 'owned',
          },
        },
        {
          subnetGroupName: 'Database',
          subnetType: ec2.SubnetType.PRIVATE_WITH_NAT,
          cidrBlock: ['10.10.14.0/27', '10.10.14.32/27', '10.10.14.64/27'],
          availabilityZones: ['ap-south-1a', 'ap-south-1b', 'ap-south-1c'],
          ingressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
          egressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
          routes: [
          ],
          tags: {
          },
        },
      ],
    });
  }
}
const envDef = {
  account: '<AWS-ID>',
  region: '<AWS-REGION>',
};

const app = new App();

new VPCStack(app, 'TEST', {
  env: envDef,
  terminationProtection: true,
  tags: {
});
app.synth();
```

Please refer [here](/API.md) to check how to use individual resource constructs.

## :clapper: Quick Start

The quick start shows you how to create an **AWS-VPC** using this module.

### Prerequisites

* A working [`aws`](https://aws.amazon.com/cli/) CLI installation with access to an account and administrator privileges
* You'll need a recent [NodeJS](https://nodejs.org) installation

To get going you'll need a CDK project. For details please refer to the [detailed guide for CDK](https://docs.aws.amazon.com/cdk/latest/guide/hello_world.html).

Create an empty directory on your system.

```bash
mkdir aws-quick-start-vpc && cd aws-quick-start-vpc
```

Bootstrap your CDK project, we will use TypeScript, but you can switch to any other supported language.

```bash
npx cdk init sample-vpc  --language typescript
npx cdk bootstrap
```

Install using NPM:

```
npm install @smallcase/cdk-vpc-module
```

Using yarn

```
yarn add @smallcase/cdk-vpc-module
```

Check the changed which are to be deployed

```bash
~ -> npx cdk diff
```

Deploy using

```bash
~ -> npx cdk deploy
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_ec2
import constructs


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.AddRouteOptions",
    jsii_struct_bases=[],
    name_mapping={
        "router_type": "routerType",
        "destination_cidr_block": "destinationCidrBlock",
        "destination_ipv6_cidr_block": "destinationIpv6CidrBlock",
        "enables_internet_connectivity": "enablesInternetConnectivity",
        "existing_vpc_peering_route_key": "existingVpcPeeringRouteKey",
        "router_id": "routerId",
    },
)
class AddRouteOptions:
    def __init__(
        self,
        *,
        router_type: aws_cdk.aws_ec2.RouterType,
        destination_cidr_block: typing.Optional[builtins.str] = None,
        destination_ipv6_cidr_block: typing.Optional[builtins.str] = None,
        enables_internet_connectivity: typing.Optional[builtins.bool] = None,
        existing_vpc_peering_route_key: typing.Optional[builtins.str] = None,
        router_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param router_type: What type of router to route this traffic to.
        :param destination_cidr_block: IPv4 range this route applies to. Default: '0.0.0.0/0'
        :param destination_ipv6_cidr_block: IPv6 range this route applies to. Default: - Uses IPv6
        :param enables_internet_connectivity: Whether this route will enable internet connectivity. If true, this route will be added before any AWS resources that depend on internet connectivity in the VPC will be created. Default: false
        :param existing_vpc_peering_route_key: 
        :param router_id: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "router_type": router_type,
        }
        if destination_cidr_block is not None:
            self._values["destination_cidr_block"] = destination_cidr_block
        if destination_ipv6_cidr_block is not None:
            self._values["destination_ipv6_cidr_block"] = destination_ipv6_cidr_block
        if enables_internet_connectivity is not None:
            self._values["enables_internet_connectivity"] = enables_internet_connectivity
        if existing_vpc_peering_route_key is not None:
            self._values["existing_vpc_peering_route_key"] = existing_vpc_peering_route_key
        if router_id is not None:
            self._values["router_id"] = router_id

    @builtins.property
    def router_type(self) -> aws_cdk.aws_ec2.RouterType:
        '''What type of router to route this traffic to.'''
        result = self._values.get("router_type")
        assert result is not None, "Required property 'router_type' is missing"
        return typing.cast(aws_cdk.aws_ec2.RouterType, result)

    @builtins.property
    def destination_cidr_block(self) -> typing.Optional[builtins.str]:
        '''IPv4 range this route applies to.

        :default: '0.0.0.0/0'
        '''
        result = self._values.get("destination_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_ipv6_cidr_block(self) -> typing.Optional[builtins.str]:
        '''IPv6 range this route applies to.

        :default: - Uses IPv6
        '''
        result = self._values.get("destination_ipv6_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enables_internet_connectivity(self) -> typing.Optional[builtins.bool]:
        '''Whether this route will enable internet connectivity.

        If true, this route will be added before any AWS resources that depend
        on internet connectivity in the VPC will be created.

        :default: false
        '''
        result = self._values.get("enables_internet_connectivity")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def existing_vpc_peering_route_key(self) -> typing.Optional[builtins.str]:
        result = self._values.get("existing_vpc_peering_route_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def router_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("router_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddRouteOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@smallcase/cdk-vpc-module.ISubnetsProps")
class ISubnetsProps(typing_extensions.Protocol):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[builtins.str]:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cidrBlock")
    def cidr_block(self) -> typing.List[builtins.str]:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="subnetGroupName")
    def subnet_group_name(self) -> builtins.str:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="subnetType")
    def subnet_type(self) -> aws_cdk.aws_ec2.SubnetType:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="egressNetworkACL")
    def egress_network_acl(self) -> typing.Optional[typing.List["NetworkACL"]]:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ingressNetworkACL")
    def ingress_network_acl(self) -> typing.Optional[typing.List["NetworkACL"]]:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="routes")
    def routes(self) -> typing.Optional[typing.List[AddRouteOptions]]:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        ...


class _ISubnetsPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "@smallcase/cdk-vpc-module.ISubnetsProps"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availabilityZones"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cidrBlock")
    def cidr_block(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cidrBlock"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="subnetGroupName")
    def subnet_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetGroupName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="subnetType")
    def subnet_type(self) -> aws_cdk.aws_ec2.SubnetType:
        return typing.cast(aws_cdk.aws_ec2.SubnetType, jsii.get(self, "subnetType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="egressNetworkACL")
    def egress_network_acl(self) -> typing.Optional[typing.List["NetworkACL"]]:
        return typing.cast(typing.Optional[typing.List["NetworkACL"]], jsii.get(self, "egressNetworkACL"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ingressNetworkACL")
    def ingress_network_acl(self) -> typing.Optional[typing.List["NetworkACL"]]:
        return typing.cast(typing.Optional[typing.List["NetworkACL"]], jsii.get(self, "ingressNetworkACL"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="routes")
    def routes(self) -> typing.Optional[typing.List[AddRouteOptions]]:
        return typing.cast(typing.Optional[typing.List[AddRouteOptions]], jsii.get(self, "routes"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tags"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISubnetsProps).__jsii_proxy_class__ = lambda : _ISubnetsPropsProxy


class Network(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@smallcase/cdk-vpc-module.Network",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        subnets: typing.Sequence[ISubnetsProps],
        vpc: aws_cdk.aws_ec2.VpcProps,
        peering_configs: typing.Optional[typing.Mapping[builtins.str, "PeeringConfig"]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param subnets: 
        :param vpc: 
        :param peering_configs: 
        '''
        props = VPCProps(subnets=subnets, vpc=vpc, peering_configs=peering_configs)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="createSubnet")
    def create_subnet(
        self,
        option: ISubnetsProps,
        vpc: aws_cdk.aws_ec2.Vpc,
    ) -> typing.List[aws_cdk.aws_ec2.Subnet]:
        '''
        :param option: -
        :param vpc: -
        '''
        peering_connection_id = PeeringConnectionInternalType()

        return typing.cast(typing.List[aws_cdk.aws_ec2.Subnet], jsii.invoke(self, "createSubnet", [option, vpc, peering_connection_id]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="natProvider")
    def nat_provider(self) -> aws_cdk.aws_ec2.NatProvider:
        return typing.cast(aws_cdk.aws_ec2.NatProvider, jsii.get(self, "natProvider"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.Vpc:
        return typing.cast(aws_cdk.aws_ec2.Vpc, jsii.get(self, "vpc"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="natSubnets")
    def nat_subnets(self) -> typing.List[aws_cdk.aws_ec2.PublicSubnet]:
        return typing.cast(typing.List[aws_cdk.aws_ec2.PublicSubnet], jsii.get(self, "natSubnets"))

    @nat_subnets.setter
    def nat_subnets(self, value: typing.List[aws_cdk.aws_ec2.PublicSubnet]) -> None:
        jsii.set(self, "natSubnets", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="pbSubnets")
    def pb_subnets(self) -> typing.List[aws_cdk.aws_ec2.PublicSubnet]:
        return typing.cast(typing.List[aws_cdk.aws_ec2.PublicSubnet], jsii.get(self, "pbSubnets"))

    @pb_subnets.setter
    def pb_subnets(self, value: typing.List[aws_cdk.aws_ec2.PublicSubnet]) -> None:
        jsii.set(self, "pbSubnets", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="pvSubnets")
    def pv_subnets(self) -> typing.List[aws_cdk.aws_ec2.PrivateSubnet]:
        return typing.cast(typing.List[aws_cdk.aws_ec2.PrivateSubnet], jsii.get(self, "pvSubnets"))

    @pv_subnets.setter
    def pv_subnets(self, value: typing.List[aws_cdk.aws_ec2.PrivateSubnet]) -> None:
        jsii.set(self, "pvSubnets", value)


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.NetworkACL",
    jsii_struct_bases=[],
    name_mapping={"cidr": "cidr", "traffic": "traffic"},
)
class NetworkACL:
    def __init__(
        self,
        *,
        cidr: aws_cdk.aws_ec2.AclCidr,
        traffic: aws_cdk.aws_ec2.AclTraffic,
    ) -> None:
        '''
        :param cidr: 
        :param traffic: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "cidr": cidr,
            "traffic": traffic,
        }

    @builtins.property
    def cidr(self) -> aws_cdk.aws_ec2.AclCidr:
        result = self._values.get("cidr")
        assert result is not None, "Required property 'cidr' is missing"
        return typing.cast(aws_cdk.aws_ec2.AclCidr, result)

    @builtins.property
    def traffic(self) -> aws_cdk.aws_ec2.AclTraffic:
        result = self._values.get("traffic")
        assert result is not None, "Required property 'traffic' is missing"
        return typing.cast(aws_cdk.aws_ec2.AclTraffic, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkACL(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.PeeringConfig",
    jsii_struct_bases=[],
    name_mapping={
        "peering_vpc_id": "peeringVpcId",
        "tags": "tags",
        "peer_assume_role_arn": "peerAssumeRoleArn",
        "peer_owner_id": "peerOwnerId",
        "peer_region": "peerRegion",
    },
)
class PeeringConfig:
    def __init__(
        self,
        *,
        peering_vpc_id: builtins.str,
        tags: typing.Mapping[builtins.str, builtins.str],
        peer_assume_role_arn: typing.Optional[builtins.str] = None,
        peer_owner_id: typing.Optional[builtins.str] = None,
        peer_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param peering_vpc_id: 
        :param tags: 
        :param peer_assume_role_arn: 
        :param peer_owner_id: 
        :param peer_region: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "peering_vpc_id": peering_vpc_id,
            "tags": tags,
        }
        if peer_assume_role_arn is not None:
            self._values["peer_assume_role_arn"] = peer_assume_role_arn
        if peer_owner_id is not None:
            self._values["peer_owner_id"] = peer_owner_id
        if peer_region is not None:
            self._values["peer_region"] = peer_region

    @builtins.property
    def peering_vpc_id(self) -> builtins.str:
        result = self._values.get("peering_vpc_id")
        assert result is not None, "Required property 'peering_vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        result = self._values.get("tags")
        assert result is not None, "Required property 'tags' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def peer_assume_role_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("peer_assume_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_owner_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("peer_owner_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_region(self) -> typing.Optional[builtins.str]:
        result = self._values.get("peer_region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PeeringConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.PeeringConnectionInternalType",
    jsii_struct_bases=[],
    name_mapping={},
)
class PeeringConnectionInternalType:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PeeringConnectionInternalType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.VPCProps",
    jsii_struct_bases=[],
    name_mapping={
        "subnets": "subnets",
        "vpc": "vpc",
        "peering_configs": "peeringConfigs",
    },
)
class VPCProps:
    def __init__(
        self,
        *,
        subnets: typing.Sequence[ISubnetsProps],
        vpc: aws_cdk.aws_ec2.VpcProps,
        peering_configs: typing.Optional[typing.Mapping[builtins.str, PeeringConfig]] = None,
    ) -> None:
        '''
        :param subnets: 
        :param vpc: 
        :param peering_configs: 
        '''
        if isinstance(vpc, dict):
            vpc = aws_cdk.aws_ec2.VpcProps(**vpc)
        self._values: typing.Dict[str, typing.Any] = {
            "subnets": subnets,
            "vpc": vpc,
        }
        if peering_configs is not None:
            self._values["peering_configs"] = peering_configs

    @builtins.property
    def subnets(self) -> typing.List[ISubnetsProps]:
        result = self._values.get("subnets")
        assert result is not None, "Required property 'subnets' is missing"
        return typing.cast(typing.List[ISubnetsProps], result)

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.VpcProps:
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.VpcProps, result)

    @builtins.property
    def peering_configs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, PeeringConfig]]:
        result = self._values.get("peering_configs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, PeeringConfig]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VPCProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AddRouteOptions",
    "ISubnetsProps",
    "Network",
    "NetworkACL",
    "PeeringConfig",
    "PeeringConnectionInternalType",
    "VPCProps",
]

publication.publish()

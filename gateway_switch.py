import argparse
from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.containerservice import ContainerServiceClient


def ops_application_gateway(ops, application_gateway_name) -> None:
    """
    Start or stop application Gateway without destroying it.
    :param ops: Start/Stop
    :return: None
    """
    try:
        network_client = NetworkManagementClient(credential, subscription_id)
        if ops == "stop":
            async_operation = network_client.application_gateways.begin_stop(resource_group_name,
                                                                             application_gateway_name)
            async_operation.wait()
            print(f"Application Gateway '{application_gateway_name}' has been stopped.")
        elif ops == "start":
            async_operation = network_client.application_gateways.begin_start(resource_group_name,
                                                                              application_gateway_name)
            async_operation.wait()
            print(f"Application Gateway '{application_gateway_name}' has "
                  f"been started.")
        else:
            print("Please give proper argument.")
    except Exception as e:
        print(f"Unable to {ops} service due to error: {e}")


def ops_aks(ops, cluster_name):
    """
    Start or stop Azure Kubernetes Service without destroying it.
    :param ops: Start/Stop
    :return: None
    """
    container_client = ContainerServiceClient(credential, subscription_id)
    clusters = container_client.managed_clusters.list_by_resource_group(resource_group_name)
    try:
        if ops == "stop":
            for cluster in clusters:
                if cluster == f"{cluster_name}":
                    print(f"Stopping cluster: {cluster_name}")
                    container_client.managed_clusters.begin_stop(resource_group_name, cluster_name).result()
        elif ops == "start":
            for cluster in clusters:
                if cluster == f"{cluster_name}":
                    print(f"Starting cluster: {cluster_name}")
                    container_client.managed_clusters.begin_start(resource_group_name, cluster_name).result()
        else:
            print("Please give proper argument.")

    except Exception as e:
        print(f"Unable to {ops} service due to error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Start or stop Kubernetes services in a specified Azure "
                    "resource group.")

    parser.add_argument("subid", type=str, help="Subscription ID of azure "
                                                "account.")
    parser.add_argument(
        "rg_name",
        type=str,
        help="The name of the Azure resource group."
    )
    parser.add_argument("gw_name",
                        type=str, required=False,
                        help="The name of Gateway.")
    parser.add_argument(
        "cluster_name",
        type=str,
        required=False,
        help="The name of the Kubernetes service (AKS cluster)."
    )
    parser.add_argument(
        "action",
        type=str,
        choices=["start", "stop"],
        help="The action to perform: 'start' or 'stop'."
    )
    args = parser.parse_args()

    subscription_id = args.subid
    resource_group_name = args.rg_name
    application_gateway_name = args.gw_name
    cluster_name = args.cluster_name
    ops = args.action

    credential = DefaultAzureCredential()

    if argparse == application_gateway_name:
        if ops == 'start':
            print(f"Starting {application_gateway_name} service in "
                  f"{resource_group_name}.")
            ops_application_gateway(ops, application_gateway_name)
        elif ops == 'stop':
            print(f"Stopping {application_gateway_name} service in "
                  f"{resource_group_name}.")
            ops_application_gateway(ops, application_gateway_name)
        else:
            print("Please enter valid argument for start/stop action for "
                  "Application Gateway service.")

    if argparse == cluster_name:
        if ops == 'start':
            print(f"Starting {cluster_name} service in {resource_group_name}.")
            ops_aks(ops, cluster_name)
        elif ops == 'stop':
            print(f"Stopping {cluster_name} service in {resource_group_name}.")
            ops_aks(ops, cluster_name)
        else:
            print("Please enter valid argument for start/stop action for "
                  "Azure Kubernetes service.")








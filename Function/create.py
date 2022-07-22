from kubernetes import client, config


def create_service(core_v1_api):
    body = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(
            name="redis-test-svc"
        ),
        spec=client.V1ServiceSpec(
            selector={"app": "redis"},
            cluster_ip="None",
            type="ClusterIP",
            ports=[client.V1ServicePort(
                port=6379,
                target_port=6379
            )]
        )
    )
    # Create the service in specified namespace
    # (Can replace "default" with a namespace you may have created)
    core_v1_api.create_namespaced_service(namespace="default", body=body)


def create_stateful_set_object():
    container = client.V1Container(
        name="sts-redis",
        image="redis",
        image_pull_policy="IfNotPresent",
        ports=[client.V1ContainerPort(container_port=6379)],
    )
    # Template
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "redis"}),
        spec=client.V1PodSpec(containers=[container]))
    # Spec
    spec = client.V1StatefulSetSpec(
        replicas=1,
        service_name="redis-test-svc",
        selector=client.V1LabelSelector(
            match_labels={"app": "redis"}
        ),
        template=template)
    # StatefulSet
    statefulset = client.V1StatefulSet(
        api_version="apps/v1",
        kind="StatefulSet",
        metadata=client.V1ObjectMeta(name="statefulset-redis"),
        spec=spec)

    return statefulset


def create_stateful_set(apps_v1_api, stateful_set_object):
    # Create the Statefulset in default namespace
    # You can replace the namespace with you have created
    apps_v1_api.create_namespaced_stateful_set(
        namespace="default", body=stateful_set_object
    )

def main():
    # Loading the local kubeconfig
    config.load_kube_config()
    apps_v1_api = client.AppsV1Api()
    core_v1_api = client.CoreV1Api()
    stateful_set_obj = create_stateful_set_object()

    create_service(core_v1_api)

    create_stateful_set(apps_v1_api, stateful_set_obj)

if __name__ == "__main__":
    main()

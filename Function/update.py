from kubernetes import client, config


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



def update_stateful_set(apps_v1_api, statefulset):
    # Update container image
    statefulset.spec.template.spec.containers[0].image = "redis:6.2"
    statefulset_name = statefulset.metadata.name
    # Patch the statefulset
    apps_v1_api.patch_namespaced_stateful_set(
        name=statefulset_name, namespace="default", body=statefulset
    )



def main():
    # Loading the local kubeconfig
    config.load_kube_config()
    apps_v1_api = client.AppsV1Api()
    core_v1_api = client.CoreV1Api()
    stateful_set_obj = create_stateful_set_object()
    create_stateful_set(apps_v1_api, stateful_set_obj)

    update_stateful_set(apps_v1_api, stateful_set_obj)


if __name__ == "__main__":
    main()

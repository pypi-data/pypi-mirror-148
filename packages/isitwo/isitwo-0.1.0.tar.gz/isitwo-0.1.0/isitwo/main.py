import boto3
import typer
from boto3_type_annotations.ec2 import Instance, ServiceResource


def get_instance_name(instance_tags: list) -> str:
    tags = list(filter(lambda x: x["Key"] == "Name", instance_tags))
    if tags:
        return tags[0]["Value"]
    return ""


def get_instance_by_name(instance_name: str) -> Instance:
    ec2_instances = list(
        ec2_resource().instances.filter(
            Filters=[{"Name": "tag:Name", "Values": [instance_name]}]
        )
    )
    if ec2_instances:
        return ec2_instances[0]
    else:
        raise ValueError("No instance found with this name")


def ec2_resource() -> ServiceResource:
    ec2: ServiceResource = boto3.resource("ec2")
    return ec2


app = typer.Typer()


@app.command()
def list_instances() -> None:
    for instance in ec2_resource().instances.all():
        print(
            f"""
        Id: {instance.id}
        Name: {get_instance_name(instance.tags)}
        Platform: {instance.platform}
        Type: {instance.instance_type}
        Public IPv4: {instance.public_ip_address}
        AMI: {instance.image.id}
        State: {instance.state}"""
        )


@app.command()
def start_instance(instance_name: str) -> None:
    i = get_instance_by_name(instance_name)
    i.start()
    print(f"Instance started: {i}")


@app.command()
def stop_instance(instance_name: str) -> None:
    i = get_instance_by_name(instance_name)
    i.stop()
    print(f"Instance {i} successfully stopped")


@app.command()
def change_instance_type(instance_name: str, instance_type: str) -> None:
    i = get_instance_by_name(instance_name)
    i.modify_attribute(Attribute="instanceType", Value=instance_type)
    print(f"Instance {i} successfully resized")


if __name__ == "__main__":
    app()

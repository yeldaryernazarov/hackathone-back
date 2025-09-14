import boto3
import json
from urllib.parse import unquote

def carclear(image_path, endpoint_name="canvas-new-deployment-09-14-2025-3-41-AM", region="us-east-1"):
    """
    Send an image to a SageMaker endpoint and return predicted label + probability.
    """

    # Initialize SageMaker runtime client
    sagemaker_runtime = boto3.client("runtime.sagemaker", region_name=region)

    # Read the image file
    with open(image_path, "rb") as f:
        payload = f.read()

    # Invoke the SageMaker endpoint
    response = sagemaker_runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="image/jpeg",
        Accept="application/json",
        Body=payload,
    )

    # Decode JSON result
    result = json.loads(response["Body"].read().decode("utf-8"))

    # Extract only what we need
    filtered = {
        "predicted_label": unquote(result.get("predicted_label", "")),
        "probability": result.get("probability", None)
    }

    return filtered


if __name__ == "__main__":
    output = carclear("/Users/yeldar/Downloads/c93e01as-960.jpg")
    print(json.dumps(output, indent=2))

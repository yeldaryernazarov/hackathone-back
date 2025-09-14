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


def analyze_four_photos(image_paths, endpoint_name="canvas-new-deployment-09-14-2025-3-41-AM", region="us-east-1"):
    """
    Analyze 4 photos in a row and return a list of 4 results.
    
    Args:
        image_paths (list): List of 4 image file paths
        endpoint_name (str): SageMaker endpoint name
        region (str): AWS region
    
    Returns:
        list: List of 4 analysis results, each containing predicted_label and probability
    """
    results = []
    
    for image_path in image_paths:
        try:
            result = carclear(image_path, endpoint_name, region)
            results.append(result)
        except Exception as e:
            # If analysis fails for any image, add error info
            results.append({
                "predicted_label": "ERROR",
                "probability": None,
                "error": str(e)
            })
    
    return results


def count_dirty_words(outputs):
    """
    Count the number of times the word 'dirty' appears in the outputs variable.
    
    Args:
        outputs (list): List of analysis results containing predicted_label and other data
    
    Returns:
        int: Number of times 'dirty' appears in the outputs
    """
    dirty_count = 0
    
    for result in outputs:
        if isinstance(result, dict):
            # Check in predicted_label field
            predicted_label = result.get("predicted_label", "")
            if isinstance(predicted_label, str):
                dirty_count += predicted_label.lower().count("dirty")
            
            # Check in other string fields if they exist
            for key, value in result.items():
                if isinstance(value, str) and key != "predicted_label":
                    dirty_count += value.lower().count("dirty")
        elif isinstance(result, str):
            # If result is a string directly
            dirty_count += result.lower().count("dirty")
    
    return dirty_count
def car_state(dirty_count):
    if dirty_count == 0:
        return 'clean'
    elif dirty_count == 1:
        return 'dirty'
    else:
        return 'very dirty'     

if __name__ == "__main__":
    # Example usage with 4 photos
    image_paths = [
        "/Users/yeldar/Downloads/c93e01as-960.jpg",
        "/Users/yeldar/Downloads/photo2.jpg",
        "/Users/yeldar/Downloads/photo3.jpg", 
        "/Users/yeldar/Downloads/photo4.jpg"
    ]
    
    # Analyze 4 photos
    outputs = analyze_four_photos(image_paths)
    print(json.dumps(outputs, indent=2))
    
    # Count dirty words in outputs
    dirty_count = count_dirty_words(outputs)
    print(f"\nNumber of 'dirty' words found: {dirty_count}")

def cargoodness(image_path):
    from inference_sdk import InferenceHTTPClient

    client = InferenceHTTPClient(
        api_url="https://serverless.roboflow.com",
        api_key="FECoKuz69niGeJR1WuO4"
    )

    result = client.run_workflow(
        workspace_name="car-classifier",
        workflow_id="custom-workflow",
        images={
            "image": image_path
        },
        use_cache=True # cache workflow definition for 15 minutes
    )
    filtered_results = []

# results is a list, so iterate
    for item in result:
        predictions = item.get("model_predictions", {}).get("predictions", [])
        for pred in predictions:
            filtered_results.append({
                "detection_id": pred.get("detection_id"),
                "class": pred.get("class"),
                "confidence": pred.get("confidence")
        })
    return filtered_results


def analyze_eight_photos(image_paths):
    """
    Analyze 8 photos in a row and return a list of 8 results.
    
    Args:
        image_paths (list): List of 8 image file paths
    
    Returns:
        list: List of 8 analysis results, each containing detection_id, class, and confidence
    """
    results = []
    
    for image_path in image_paths:
        try:
            result = cargoodness(image_path)
            results.append(result)
        except Exception as e:
            # If analysis fails for any image, add error info
            results.append([{
                "detection_id": "ERROR",
                "class": "ERROR",
                "confidence": None,
                "error": str(e)
            }])
    
    return results


def count_class_words(outputs):
    """
    Count the number of times the word 'class' appears in the outputs variable.
    
    Args:
        outputs (list): List of analysis results containing class and other data
    
    Returns:
        int: Number of times 'class' appears in the outputs
    """
    class_count = 0
    
    for result in outputs:
        if isinstance(result, list):
            # If result is a list of predictions
            for item in result:
                if isinstance(item, dict):
                    # Check in class field
                    class_value = item.get("class", "")
                    if isinstance(class_value, str):
                        class_count += class_value.lower().count("class")
                    
                    # Check in other string fields if they exist
                    for key, value in item.items():
                        if isinstance(value, str) and key != "class":
                            class_count += value.lower().count("class")
                elif isinstance(item, str):
                    # If item is a string directly
                    class_count += item.lower().count("class")
        elif isinstance(result, dict):
            # If result is a single dictionary
            class_value = result.get("class", "")
            if isinstance(class_value, str):
                class_count += class_value.lower().count("class")
            
            # Check in other string fields if they exist
            for key, value in result.items():
                if isinstance(value, str) and key != "class":
                    class_count += value.lower().count("class")
        elif isinstance(result, str):
            # If result is a string directly
            class_count += result.lower().count("class")
    
    return class_count

def car_condition(class_count):
    if class_count == 0:
        return f'Good car condition. {class_count} damaged regions found.'
    elif class_count == 1:
        return f'Bad car condition. {class_count} damaged regions found.'
    else:
        return f'Very bad car condition. {class_count} damaged regions found.'

if __name__ == "__main__":
    # Example usage with 8 photos
    image_paths = [
        "/Users/yeldar/Downloads/images.jpeg",
        "/Users/yeldar/Downloads/photo2.jpg",
        "/Users/yeldar/Downloads/photo3.jpg",
        "/Users/yeldar/Downloads/photo4.jpg",
        "/Users/yeldar/Downloads/photo5.jpg",
        "/Users/yeldar/Downloads/photo6.jpg",
        "/Users/yeldar/Downloads/photo7.jpg",
        "/Users/yeldar/Downloads/photo8.jpg"
    ]
    
    # Analyze 8 photos
    outputs = analyze_eight_photos(image_paths)
    print("Results for 8 photos:")
    for i, result in enumerate(outputs, 1):
        print(f"Photo {i}: {result}")
    
    # Count class words in outputs
    class_count = count_class_words(outputs)
    print(f"\nNumber of 'class' words found: {class_count}")

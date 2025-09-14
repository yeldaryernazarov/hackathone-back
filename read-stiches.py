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
    print(filtered_results)

cargoodness("/Users/yeldar/Downloads/images.jpeg")

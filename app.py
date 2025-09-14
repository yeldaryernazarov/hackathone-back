#!/usr/bin/env python3
"""
Car Condition Assessment Backend
Integrates read-clean.py and read-stiches.py for photo analysis
"""

import os
import json
import base64
import tempfile
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import traceback

# Import our analysis modules
import importlib.util
import sys

# Import read-clean.py (with hyphen)
spec_clean = importlib.util.spec_from_file_location("read_clean", "read-clean.py")
read_clean = importlib.util.module_from_spec(spec_clean)
spec_clean.loader.exec_module(read_clean)

# Import read-stiches.py (with hyphen)  
spec_stitches = importlib.util.spec_from_file_location("read_stitches", "read-stiches.py")
read_stitches = importlib.util.module_from_spec(spec_stitches)
spec_stitches.loader.exec_module(read_stitches)

# Extract the functions we need
analyze_four_photos = read_clean.analyze_four_photos
count_dirty_words = read_clean.count_dirty_words
car_state = read_clean.car_state
analyze_eight_photos = read_stitches.analyze_eight_photos
count_class_words = read_stitches.count_class_words
car_condition = read_stitches.car_condition

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables to store analysis results
dirty_count = 0
class_count = 0

def save_base64_image(base64_string, filename):
    """Save base64 encoded image to temporary file"""
    try:
        # Remove data URL prefix if present
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        # Decode base64 and save to temporary file
        image_data = base64.b64decode(base64_string)
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        temp_file.write(image_data)
        temp_file.close()
        
        return temp_file.name
    except Exception as e:
        print(f"Error saving base64 image: {e}")
        return None

def cleanup_temp_files(file_paths):
    """Clean up temporary files"""
    for file_path in file_paths:
        try:
            if file_path and os.path.exists(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error cleaning up file {file_path}: {e}")

@app.route('/')
def serve_index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/analyze', methods=['POST'])
def analyze_photos():
    """Analyze uploaded photos for dirtiness and condition"""
    global dirty_count, class_count
    
    temp_files = []
    
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        dirtiness_images = data.get('dirtiness_images', [])
        condition_images = data.get('condition_images', [])
        
        print(f"Received {len(dirtiness_images)} dirtiness images and {len(condition_images)} condition images")
        
        # Process dirtiness images (4 photos)
        dirtiness_results = []
        dirtiness_file_paths = []
        
        for i, img_base64 in enumerate(dirtiness_images):
            if img_base64:
                temp_file = save_base64_image(img_base64, f'dirtiness_{i}.jpg')
                if temp_file:
                    dirtiness_file_paths.append(temp_file)
                    temp_files.append(temp_file)
                else:
                    dirtiness_file_paths.append(None)
            else:
                dirtiness_file_paths.append(None)
        
        # Analyze dirtiness photos
        if any(dirtiness_file_paths):
            print("Analyzing dirtiness photos...")
            dirtiness_results = analyze_four_photos(dirtiness_file_paths)
            dirty_count = count_dirty_words(dirtiness_results)
            print(f"Dirtiness analysis complete. Dirty count: {dirty_count}")
        else:
            print("No dirtiness images to analyze")
            dirtiness_results = []
            dirty_count = 0
        
        # Process condition images (8 photos)
        condition_results = []
        condition_file_paths = []
        
        for i, img_base64 in enumerate(condition_images):
            if img_base64:
                temp_file = save_base64_image(img_base64, f'condition_{i}.jpg')
                if temp_file:
                    condition_file_paths.append(temp_file)
                    temp_files.append(temp_file)
                else:
                    condition_file_paths.append(None)
            else:
                condition_file_paths.append(None)
        
        # Analyze condition photos
        if any(condition_file_paths):
            print("Analyzing condition photos...")
            condition_results = analyze_eight_photos(condition_file_paths)
            class_count = count_class_words(condition_results)
            print(f"Condition analysis complete. Class count: {class_count}")
        else:
            print("No condition images to analyze")
            condition_results = []
            class_count = 0
        
        # Determine overall assessments
        cleanliness_assessment = car_state(dirty_count)
        condition_assessment = car_condition(class_count)
        
        # Create detailed results for each photo
        detailed_dirtiness = create_detailed_dirtiness_results(dirtiness_results, dirtiness_file_paths)
        detailed_condition = create_detailed_condition_results(condition_results, condition_file_paths)
        
        # Prepare response
        response = {
            'dirtiness': cleanliness_assessment,
            'condition': condition_assessment,
            'detailed_results': {
                'dirtiness': detailed_dirtiness,
                'condition': detailed_condition
            }
        }
        
        print(f"Analysis complete. Response: {json.dumps(response, indent=2)}")
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        print(traceback.format_exc())
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500
    
    finally:
        # Clean up temporary files
        cleanup_temp_files(temp_files)

def determine_cleanliness(dirty_count):
    """Determine cleanliness based on dirty count"""
    if dirty_count == 0:
        return 'clean'
    elif dirty_count == 1:
        return 'dirty'
    else:
        return 'very dirty'

def determine_condition(class_count):
    """Determine condition based on class count"""
    if class_count == 0:
        return f'Good car condition. {class_count} damaged regions found.'
    elif class_count == 1:
        return f'Bad car condition. {class_count} damaged regions found.'
    else:
        return f'Very bad car condition. {class_count} damaged regions found.'

def create_detailed_dirtiness_results(results, file_paths):
    """Create detailed results for dirtiness analysis"""
    photo_names = ['front', 'right', 'left', 'back']
    
    details = []
    for i, (result, file_path) in enumerate(zip(results, file_paths)):
        if file_path is None:
            details.append({
                'photo': photo_names[i],
                'predicted_label': 'not_uploaded',
                'probability': None,
                'status': 'not_uploaded'
            })
        else:
            details.append({
                'photo': photo_names[i],
                'predicted_label': result.get('predicted_label', 'unknown'),
                'probability': result.get('probability', 0),
                'status': 'analyzed'
            })
    
    return {
        'result': determine_cleanliness(dirty_count),
        'details': details,
        'dirty_count': dirty_count,
        'total_analyzed': len([f for f in file_paths if f is not None])
    }

def create_detailed_condition_results(results, file_paths):
    """Create detailed results for condition analysis"""
    photo_names = ['front_left', 'front_right', 'back_left', 'back_right', 
                   'left_side_1', 'left_side_2', 'right_side_1', 'right_side_2']
    
    details = []
    total_damaged_areas = 0
    
    for i, (result, file_path) in enumerate(zip(results, file_paths)):
        if file_path is None:
            details.append({
                'photo': photo_names[i],
                'detections': [],
                'damage_count': 0,
                'status': 'not_uploaded'
            })
        else:
            # Count damage detections
            damage_count = len(result) if isinstance(result, list) else 0
            total_damaged_areas += damage_count
            
            # Extract detection details
            detections = []
            if isinstance(result, list):
                for detection in result:
                    if isinstance(detection, dict):
                        detections.append({
                            'class': detection.get('class', 'Unknown'),
                            'confidence': detection.get('confidence', 0)
                        })
            
            details.append({
                'photo': photo_names[i],
                'detections': detections,
                'damage_count': damage_count,
                'status': 'analyzed'
            })
    
    # Determine overall condition
    if total_damaged_areas == 0:
        condition = 'good condition'
    elif total_damaged_areas <= 2:
        condition = 'okay condition'
    else:
        condition = 'bad condition'
    
    return {
        'result': f'{total_damaged_areas} damaged areas - {condition}',
        'details': details,
        'total_damaged_areas': total_damaged_areas,
        'condition': condition
    }

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Car analysis service is running'})

if __name__ == '__main__':
    print("Starting Car Condition Assessment Backend...")
    print("Make sure you have the required AWS credentials configured for SageMaker")
    print("Make sure you have the Roboflow API key configured")
    print("Server will start on http://localhost:5001")
    
    app.run(host='0.0.0.0', port=5001, debug=True)

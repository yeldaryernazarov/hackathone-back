# 🚗 Car Condition Assessment System


## ✨ Features

- **🧽 Dirtiness Analysis**: Analyzes 4 photos to determine car cleanliness using AWS SageMaker
- **🔧 Condition Analysis**: Analyzes 8 photos to detect damage using Roboflow AI
- **🌐 Modern Web Interface**: Responsive HTML interface with drag-and-drop photo upload
- **📊 Real-time Results**: Detailed analysis results with confidence scores and individual photo breakdowns
- **🔄 RESTful API**: Clean API endpoints for integration with other systems
- **📱 Mobile Friendly**: Works on desktop, tablet, and mobile devices

## 🚀 Quick Start Guide

### Prerequisites

- Python 3.8 or higher
- AWS Account (for SageMaker dirtiness analysis)
- Roboflow Account (for condition analysis)
- Modern web browser

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd hackathone-back

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

#### AWS Configuration (Required for Dirtiness Analysis)

```bash
# Option 1: AWS CLI (Recommended)
aws configure

# Option 2: Environment Variables
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

#### Roboflow Configuration (Required for Condition Analysis)

The Roboflow API key is pre-configured in `read-stiches.py`. To update it:

1. Get your API key from [Roboflow](https://roboflow.com)
2. Update the `ROBOFLOW_API_KEY` in `read-stiches.py`

### 3. Run the Application

```bash
# Quick start (recommended)
python run_server.py

# Alternative: Direct Flask execution
python app.py
```

### 4. Access the Application

Open your browser and navigate to: **http://localhost:5001**

## 📖 Usage Instructions

### Photo Requirements

#### Dirtiness Analysis (4 photos)
- **Front view**: Clear shot of the front of the car
- **Right side**: Side view from the right
- **Left side**: Side view from the left  
- **Back view**: Clear shot of the rear of the car

#### Condition Analysis (8 photos)
- **Front left**: Front left corner/area
- **Front right**: Front right corner/area
- **Back left**: Rear left corner/area
- **Back right**: Rear right corner/area
- **Left side 1**: Left side (front portion)
- **Left side 2**: Left side (rear portion)
- **Right side 1**: Right side (front portion)
- **Right side 2**: Right side (rear portion)

### How to Use

1. **Upload Photos**: Drag and drop or click to select photos for each analysis type
2. **Review Uploads**: Ensure all required photos are uploaded and clearly visible
3. **Analyze**: Click "Analyze Car Condition" to start the AI analysis
4. **View Results**: Review detailed results including:
   - Overall cleanliness assessment (Clean/Dirty/Very Dirty)
   - Overall condition assessment (Good/Okay/Bad)
   - Individual photo analysis with confidence scores
   - Damage detection details

## 🏗️ Project Structure

```
hackathone-back/
├── app.py                    # Main Flask backend server
├── read-clean.py            # Dirtiness analysis using SageMaker
├── read-stiches.py          # Condition analysis using Roboflow
├── index.html               # Frontend web interface
├── run_server.py            # Startup script with error handling
├── requirements.txt         # Python dependencies
├── test_integration.py      # Integration tests
├── examples/                # Example images for users
│   ├── dirtiness/          # Example dirtiness photos
│   └── condition/          # Example condition photos
└── README.md               # This documentation
```

## 🔌 API Reference

### Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/` | Serve main HTML interface | None | HTML page |
| `POST` | `/analyze` | Analyze uploaded photos | JSON with base64 images | Analysis results |
| `GET` | `/health` | Health check | None | Status object |

### Request Format

```json
{
  "dirtiness_images": ["base64_string_1", "base64_string_2", ...],
  "condition_images": ["base64_string_1", "base64_string_2", ...]
}
```

### Response Format

```json
{
  "dirtiness": "clean|dirty|very dirty",
  "condition": "good condition|okay condition|bad condition",
  "detailed_results": {
    "dirtiness": {
      "result": "clean",
      "dirty_count": 0,
      "details": [...]
    },
    "condition": {
      "result": "0 damaged areas - good condition",
      "total_damaged_areas": 0,
      "details": [...]
    }
  }
}
```

## ⚠️ Limitations

### Technical Limitations

- **Image Quality**: Analysis accuracy depends on photo quality and lighting
- **Model Accuracy**: AI models may have false positives/negatives
- **File Size**: Large images may cause timeout issues (recommended: <5MB per image)
- **Format Support**: Only JPG/JPEG images are supported
- **Network Dependency**: Requires stable internet for API calls

### Functional Limitations

- **Photo Count**: Exactly 4 photos required for dirtiness, 8 for condition analysis
- **Single Car**: Designed for analyzing one car at a time
- **Damage Types**: Limited to common damage types detected by the Roboflow model
- **Language**: Interface and results in English only

### Performance Limitations

- **Processing Time**: Analysis can take 10-30 seconds depending on image size and network
- **Concurrent Users**: Not optimized for high concurrent usage
- **Storage**: No persistent storage of analysis results

## 🔧 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **AWS Credentials Error** | Run `aws configure` or set environment variables |
| **Roboflow API Error** | Check API key in `read-stiches.py` |
| **Port 5001 in Use** | Change port in `app.py` or kill process using port |
| **Missing Dependencies** | Run `pip install -r requirements.txt` |
| **Images Not Uploading** | Check file format (JPG only) and size (<5MB) |
| **Analysis Fails** | Check console logs for detailed error messages |

### Debug Mode

The application runs in debug mode by default. Check the console for detailed error messages and stack traces.

### Health Check

Test if the service is running:
```bash
curl http://localhost:5001/health
```

## 🛠️ Technical Details

### Architecture

- **Backend**: Flask with CORS support for cross-origin requests
- **AI Models**: 
  - AWS SageMaker endpoint for dirtiness detection
  - Roboflow workflow for damage detection
- **Image Processing**: Base64 encoding/decoding for web uploads
- **Frontend**: Vanilla JavaScript with modern CSS and responsive design
- **Temporary Storage**: Images processed in memory and cleaned up automatically

### Dependencies

- **Flask**: Web framework
- **Flask-CORS**: Cross-origin resource sharing
- **boto3**: AWS SDK for SageMaker integration
- **inference-sdk**: Roboflow inference client
- **Pillow**: Image processing
- **OpenCV**: Computer vision operations
- **NumPy**: Numerical computations

## 📄 Data License

### Training Data

- **Dirtiness Model**: Trained on proprietary dataset via AWS SageMaker
- **Condition Model**: Uses Roboflow's pre-trained damage detection model
- **Example Images**: Provided for demonstration purposes only

### Usage Rights

- **Commercial Use**: Allowed for hackathon and commercial purposes
- **Modification**: Code can be modified and redistributed
- **Attribution**: Credit to original AI model providers (AWS SageMaker, Roboflow)
- **No Warranty**: Provided "as is" without warranty

### Data Privacy

- **Image Processing**: Images are processed temporarily and not stored
- **API Calls**: Data sent to AWS and Roboflow according to their privacy policies
- **Local Storage**: No persistent storage of uploaded images or results

## 📝 License

This project is developed for hackathon purposes and is available under the MIT License. See LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the troubleshooting section above
- Review console logs for error details
- Open an issue in the repository

---

**Built with ❤️ for the hackathon community**

# Car Condition Assessment System

A web application that analyzes car photos to assess cleanliness and condition using AI models.

## Features

- **Dirtiness Analysis**: Analyzes 4 photos to determine car cleanliness using SageMaker
- **Condition Analysis**: Analyzes 8 photos to detect damage using Roboflow AI
- **Web Interface**: Modern, responsive HTML interface for photo upload
- **Real-time Results**: Detailed analysis results with confidence scores

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure AWS Credentials

For the dirtiness analysis (SageMaker), you need AWS credentials:

```bash
aws configure
```

Or set environment variables:
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

### 3. Configure Roboflow API Key

The condition analysis uses Roboflow. The API key is already configured in `read-stiches.py`, but you can update it if needed.

## Running the Application

### Option 1: Using the startup script (Recommended)

```bash
python run_server.py
```

### Option 2: Direct Flask execution

```bash
python app.py
```

The application will be available at: http://localhost:5001

## Usage

1. **Upload Photos**: 
   - Upload 4 photos for dirtiness analysis (front, right, left, back)
   - Upload 8 photos for condition analysis (various angles)

2. **Analyze**: Click the "Analyze Car Condition" button

3. **View Results**: See detailed analysis results with:
   - Overall cleanliness assessment
   - Overall condition assessment
   - Individual photo analysis
   - Confidence scores

## File Structure

```
├── app.py                 # Main Flask backend server
├── read-clean.py         # Dirtiness analysis using SageMaker
├── read-stiches.py       # Condition analysis using Roboflow
├── index.html            # Frontend web interface
├── run_server.py         # Startup script
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## API Endpoints

- `GET /` - Serves the main HTML interface
- `POST /analyze` - Analyzes uploaded photos
- `GET /health` - Health check endpoint

## Troubleshooting

### Common Issues

1. **AWS Credentials Error**: Make sure AWS credentials are properly configured
2. **Roboflow API Error**: Check the API key in `read-stiches.py`
3. **Port Already in Use**: Change the port in `app.py` if 5001 is occupied
4. **Missing Dependencies**: Run `pip install -r requirements.txt`

### Debug Mode

The application runs in debug mode by default. Check the console for detailed error messages.

## Technical Details

- **Backend**: Flask with CORS support
- **AI Models**: 
  - SageMaker endpoint for dirtiness detection
  - Roboflow workflow for damage detection
- **Image Processing**: Base64 encoding/decoding for web uploads
- **Frontend**: Vanilla JavaScript with modern CSS

## License

This project is for hackathon purposes.

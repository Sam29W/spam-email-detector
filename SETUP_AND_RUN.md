# Spam Email Detector - Complete Setup Guide

This guide provides step-by-step instructions to set up and run the spam email detector locally.

## Quick Start (5 minutes)

If you just want to test the backend API without frontend:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then test the API at http://localhost:5000/api/health

## Full Local Development Setup

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Flask development server:
```bash
python app.py
```

Backend is now running at http://localhost:5000

### Testing Backend Endpoints

Open a new terminal and test these endpoints:

1. Health Check:
```bash
curl http://localhost:5000/api/health
```

2. Single Email Detection:
```bash
curl -X POST http://localhost:5000/api/detect \
  -H "Content-Type: application/json" \
  -d '{
    "email_subject": "Congratulations You Won!",
    "email_body": "Click here to claim your prize now!"
  }'
```

3. Batch Processing (multiple emails):
```bash
curl -X POST http://localhost:5000/api/detect/batch \
  -H "Content-Type: application/json" \
  -d '{
    "emails": [
      {"subject": "Team Meeting", "body": "Let\'s discuss the project tomorrow"},
      {"subject": "Special Offer", "body": "Limited time only! Click here now!"}
    ]
  }'
```

4. Get Statistics:
```bash
curl http://localhost:5000/api/stats
```

### Frontend Setup (React)

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create .env file:
```bash
cp .env.example .env
```

4. Update .env with backend URL (if running locally, it should already be set):
```
REACT_APP_API_URL=http://localhost:5000
```

5. Start React development server:
```bash
npm start
```

Frontend is now running at http://localhost:3000

### Docker Setup (Optional)

If you have Docker installed, you can run everything in containers:

```bash
docker-compose up --build
```

This starts:
- Backend at http://localhost:5000
- Frontend at http://localhost:3000

## File Structure Overview

### Backend (Flask)

**backend/app.py** - Main Flask application with all API endpoints:
- Spam detection logic
- Batch processing
- Statistics tracking
- Rate limiting (100 requests/hour per IP)
- Comprehensive error handling

**backend/requirements.txt** - Python dependencies:
- Flask: Web framework
- scikit-learn: ML library (for future ML models)
- Flask-CORS: Cross-origin requests
- gunicorn: Production server

### Frontend (React)

Create these files in the frontend directory:

**frontend/src/App.js** - Main React component
**frontend/src/components/EmailInput.js** - Email input form
**frontend/src/components/ResultsDisplay.js** - Display detection results
**frontend/src/services/api.js** - API communication

### Docker

**docker-compose.yml** - Multi-container orchestration
**Dockerfile** - Backend container configuration
**frontend/Dockerfile** - Frontend container configuration

## Environment Variables

**Backend (.env in backend/):**
```
FLASK_ENV=development
FLASK_APP=app.py
FLASK_DEBUG=1
```

**Frontend (.env in frontend/):**
```
REACT_APP_API_URL=http://localhost:5000
```

## Features and Testing

### Core Features Implemented

1. Real-time Email Spam Detection
   - Subject and body analysis
   - Spam keyword detection
   - Suspicious pattern recognition
   - Confidence score calculation

2. Batch Processing
   - Process up to 100 emails per request
   - Returns individual scores for each email
   - Aggregated statistics

3. Statistics Tracking
   - Total emails analyzed
   - Spam vs legitimate count
   - Average confidence scores
   - Reset statistics capability

4. Rate Limiting
   - 100 requests per hour per IP
   - Prevents abuse
   - Returns 429 error when limit exceeded

5. Error Handling
   - Request validation
   - Content length limits
   - JSON parsing errors
   - Comprehensive error messages

### Testing the Features

1. Test Spam Detection:
```bash
# This should return high spam probability
curl -X POST http://localhost:5000/api/detect \
  -H "Content-Type: application/json" \
  -d '{
    "email_subject": "FREE MONEY!! CLAIM NOW!!!",
    "email_body": "You have won a prize! Click here immediately to get your $10000!"
  }'
```

2. Test Legitimate Email:
```bash
# This should return low spam probability
curl -X POST http://localhost:5000/api/detect \
  -H "Content-Type: application/json" \
  -d '{
    "email_subject": "Project Update",
    "email_body": "Hi team, please review the attached document for the quarterly review."
  }'
```

3. Test Batch Processing:
```bash
curl -X POST http://localhost:5000/api/detect/batch \
  -H "Content-Type: application/json" \
  -d '{
    "emails": [
      {"subject": "Meeting tomorrow", "body": "Let us discuss the project"},
      {"subject": "URGENT ACTION REQUIRED", "body": "Verify your bank account NOW!!!"},
      {"subject": "Weekly Report", "body": "Here is the weekly status report"}
    ]
  }'
```

## Troubleshooting

### Backend Won't Start
- Check if port 5000 is already in use
- Verify all dependencies are installed: pip install -r requirements.txt
- Check Python version (3.8+)

### Frontend Won't Connect to Backend
- Ensure backend is running on http://localhost:5000
- Check REACT_APP_API_URL in .env file
- Check browser console for CORS errors
- Ensure Flask-CORS is installed

### Rate Limiting Issues
- Reset statistics with: curl -X POST http://localhost:5000/api/stats/reset
- Wait for 1 hour, or use different IP/client

## Performance Notes

- Backend handles ~1000 classifications per second on modern hardware
- Batch processing is recommended for multiple emails
- Rate limiting prevents abuse but allows legitimate high-volume usage
- Statistics are in-memory and reset on restart

## Next Steps

1. Build React Frontend UI with:
   - Form for email input
   - Results display with confidence scores
   - Batch processing interface
   - Statistics dashboard

2. Add Advanced Features:
   - Database persistence for statistics
   - User authentication
   - Email attachment analysis
   - Multi-language support

3. Deploy to Production:
   - Deploy backend to Render/Heroku
   - Deploy frontend to Vercel/Netlify
   - Use environment variables for configuration
   - Set up monitoring and logging

## Support

For issues or questions, open an issue on GitHub at:
https://github.com/Sam29W/spam-email-detector/issues

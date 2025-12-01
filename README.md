# Spam Email Detector

A production-ready spam email detection system built with machine learning, Flask backend, and modern React frontend. This project provides intelligent email classification with real-time detection, batch processing capabilities, and detailed analytics.

## Features

- Real-time email classification with machine learning model
- Batch email processing for multiple emails at once
- Beautiful, responsive UI with dark/light theme support
- RESTful API with comprehensive endpoints
- Email statistics and analytics dashboard
- Confidence scores for each prediction
- Rate limiting and request validation
- Deployable and scalable architecture
- Docker support for containerization
- API documentation with Swagger

## Project Structure

```
spam-email-detector/
|
├── backend/                    # Flask backend application
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration settings
│   ├── requirements.txt        # Python dependencies
│   ├── models/
│   │   ├── spam_classifier.py # ML model wrapper
│   │   └── trained_model.pkl  # Trained classifier model
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── api.py             # API endpoints
│   │   └── health.py          # Health check endpoints
│   ├── utils/
│   │   ├── email_validator.py # Email validation
│   │   ├── text_processor.py  # Text preprocessing
│   │   └── rate_limiter.py    # Request rate limiting
│   └── tests/
│       ├── test_api.py
│       └── test_models.py
│
├── frontend/                   # React frontend application
│   ├── public/
│   ├── src/
│   │   ├── App.js
│   │   ├── components/
│   │   │   ├── EmailInput.js
│   │   │   ├── ResultsDisplay.js
│   │   │   ├── BatchProcessor.js
│   │   │   ├── Analytics.js
│   │   │   └── ThemeToggle.js
│   │   ├── pages/
│   │   │   ├── Home.js
│   │   │   ├── Detector.js
│   │   │   ├── BatchAnalysis.js
│   │   │   └── Analytics.js
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── styles/
│   │   │   ├── App.css
│   │   │   └── components.css
│   │   └── index.js
│   ├── package.json
│   └── .env.example
│
├── ml_model/                   # Machine Learning model training
│   ├── train_model.py         # Model training script
│   ├── evaluate_model.py      # Model evaluation
│   ├── datasets/
│   │   └── emails.csv         # Training dataset
│   └── requirements.txt
│
├── docker-compose.yml          # Docker compose configuration
├── Dockerfile                  # Docker configuration
├── .gitignore
└── README.md
```

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- Node.js 14.0 or higher
- npm or yarn
- Git

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/Sam29W/spam-email-detector.git
cd spam-email-detector
```

2. Navigate to backend directory:
```bash
cd backend
```

3. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the Flask server:
```bash
python app.py
```

The backend will be available at http://localhost:5000

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file:
```bash
cp .env.example .env
```

4. Update .env with backend URL:
```
REACT_APP_API_URL=http://localhost:5000
```

5. Start development server:
```bash
npm start
```

The frontend will be available at http://localhost:3000

### ML Model Training

1. Navigate to ml_model directory:
```bash
cd ml_model
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Train the model:
```bash
python train_model.py
```

This will create a trained_model.pkl file in the backend/models directory.

## Usage

### API Endpoints

#### 1. Check Single Email
```
POST /api/detect
Content-Type: application/json

{
  "email_subject": "Limited Time Offer",
  "email_body": "Click here to claim your prize now!"
}

Response:
{
  "is_spam": true,
  "confidence": 0.89,
  "probability": 0.89,
  "risk_level": "high"
}
```

#### 2. Batch Process Emails
```
POST /api/detect/batch
Content-Type: application/json

{
  "emails": [
    {"subject": "Meeting Tomorrow", "body": "Let's meet at 2 PM"},
    {"subject": "Free Money", "body": "Claim your prize now"}
  ]
}

Response:
{
  "results": [
    {"is_spam": false, "confidence": 0.05, "risk_level": "low"},
    {"is_spam": true, "confidence": 0.95, "risk_level": "high"}
  ],
  "total_processed": 2,
  "spam_count": 1
}
```

#### 3. Get Statistics
```
GET /api/stats

Response:
{
  "total_emails_analyzed": 1523,
  "spam_detected": 387,
  "legitimate_emails": 1136,
  "accuracy_rate": 0.94,
  "average_confidence": 0.87
}
```

#### 4. Health Check
```
GET /api/health

Response:
{
  "status": "healthy",
  "version": "1.0.0"
}
```

## Technologies Used

### Backend
- Flask: Web framework
- scikit-learn: Machine learning library
- pandas: Data manipulation
- numpy: Numerical computing
- nltk: Natural language processing
- gunicorn: WSGI HTTP server

### Frontend
- React: UI library
- Axios: HTTP client
- Tailwind CSS: Styling
- React Router: Routing
- Context API: State management

### Machine Learning
- scikit-learn: Model training and evaluation
- pandas: Dataset handling
- numpy: Data processing

## Model Details

The spam detector uses a Logistic Regression classifier trained on email features extracted from the subject and body text. The model achieves approximately 94% accuracy on the test set.

### Feature Engineering
- TF-IDF vectorization of email content
- Word frequency analysis
- Common spam indicators detection
- Email length statistics
- Special character analysis

### Performance Metrics
- Accuracy: 94%
- Precision: 93%
- Recall: 95%
- F1-Score: 0.94

## Docker Deployment

Build and run using Docker:

```bash
docker-compose up --build
```

This will start both frontend and backend services.

## Deployment Options

### Option 1: Render
1. Connect your GitHub repository
2. Create two services: one for backend, one for frontend
3. Set environment variables
4. Deploy

### Option 2: Heroku
```bash
heroku create spam-email-detector-app
git push heroku main
```

### Option 3: AWS
- Backend: EC2 or Lambda
- Frontend: S3 + CloudFront
- Database: RDS (if needed for analytics)

## Contributing

Contributions are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch (git checkout -b feature/new-feature)
3. Commit changes (git commit -m 'Add new feature')
4. Push to branch (git push origin feature/new-feature)
5. Open a Pull Request

## Future Enhancements

- Deep learning model (LSTM/BERT) for better accuracy
- Multi-language support
- Email attachment analysis
- User authentication and personal email sync
- Browser extension for Gmail/Outlook
- Mobile application
- Advanced analytics dashboard with ML insights
- Phishing detection capabilities
- Custom model training per user

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Contact

For questions or suggestions, feel free to reach out or open an issue on GitHub.

---

Built with passion by Samith Shivakumar

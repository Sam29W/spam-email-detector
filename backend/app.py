import os
import json
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.exceptions import BadRequest
import pickle
import re
from collections import defaultdict

app = Flask(__name__)
CORS(app)

requests_log = defaultdict(lambda: {'count': 0, 'timestamp': datetime.now()})
REQUEST_LIMIT = 100
TIME_WINDOW = 3600

stats = {
    'total_emails_analyzed': 0,
    'spam_detected': 0,
    'legitimate_emails': 0,
    'average_confidence': 0.0,
}

def load_model():
    try:
        if os.path.exists('models/trained_model.pkl'):
            with open('models/trained_model.pkl', 'rb') as f:
                return pickle.load(f)
    except:
        pass
    return None

def simple_spam_classifier(email_subject, email_body):
    combined_text = (email_subject + ' ' + email_body).lower()
    
    spam_keywords = [
        'claim', 'prize', 'winner', 'congratulations', 'click here',
        'limited time', 'urgent', 'act now', 'free money', 'guaranteed',
        'risk free', 'no obligation', 'credit card', 'bank account',
        'verify', 'confirm identity', 'update payment', 'special offer',
        'unsubscribe', 'viagra', 'cialis', 'pharmacy', 'casino',
        'lottery', 'inheritance', 'nigerian prince', 'weight loss'
    ]
    
    spam_score = 0
    for keyword in spam_keywords:
        spam_score += combined_text.count(keyword)
    
    suspicious_patterns = [
        r'\b[A-Z]{5,}\b',
        r'!{2,}',
        r'\${1,}\d+',
        r'@{2,}'
    ]
    
    for pattern in suspicious_patterns:
        matches = len(re.findall(pattern, email_subject + email_body))
        spam_score += matches * 2
    
    text_length = len(combined_text)
    if text_length > 2000:
        spam_score += 2
    if text_length < 10:
        spam_score += 1
    
    confidence = min(spam_score / 10.0, 1.0)
    is_spam = confidence > 0.5
    
    return is_spam, confidence

def rate_limit(client_id):
    now = datetime.now()
    request_info = requests_log[client_id]
    
    if (now - request_info['timestamp']).total_seconds() > TIME_WINDOW:
        requests_log[client_id] = {'count': 0, 'timestamp': now}
        request_info = requests_log[client_id]
    
    if request_info['count'] >= REQUEST_LIMIT:
        return False
    
    requests_log[client_id]['count'] += 1
    return True

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/detect', methods=['POST'])
def detect_spam():
    try:
        client_id = request.remote_addr
        if not rate_limit(client_id):
            return jsonify({
                'error': 'Rate limit exceeded. Maximum 100 requests per hour.'
            }), 429
        
        data = request.get_json()
        if not data:
            raise BadRequest('Request body must be JSON')
        
        email_subject = data.get('email_subject', '').strip()
        email_body = data.get('email_body', '').strip()
        
        if not email_subject and not email_body:
            raise BadRequest('At least email_subject or email_body is required')
        
        if len(email_subject) > 1000 or len(email_body) > 10000:
            raise BadRequest('Email content exceeds maximum length')
        
        is_spam, confidence = simple_spam_classifier(email_subject, email_body)
        
        risk_level = 'high' if confidence > 0.7 else 'medium' if confidence > 0.4 else 'low'
        
        stats['total_emails_analyzed'] += 1
        if is_spam:
            stats['spam_detected'] += 1
        else:
            stats['legitimate_emails'] += 1
        
        total_conf = (stats['average_confidence'] * (stats['total_emails_analyzed'] - 1) + confidence)
        stats['average_confidence'] = total_conf / stats['total_emails_analyzed']
        
        return jsonify({
            'is_spam': is_spam,
            'confidence': round(confidence, 3),
            'probability': round(confidence, 3),
            'risk_level': risk_level,
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@app.route('/api/detect/batch', methods=['POST'])
def detect_batch():
    try:
        client_id = request.remote_addr
        if not rate_limit(client_id):
            return jsonify({
                'error': 'Rate limit exceeded. Maximum 100 requests per hour.'
            }), 429
        
        data = request.get_json()
        if not data or 'emails' not in data:
            raise BadRequest('Request must contain "emails" array')
        
        emails = data.get('emails', [])
        if not isinstance(emails, list):
            raise BadRequest('"emails" must be an array')
        
        if len(emails) > 100:
            raise BadRequest('Maximum 100 emails per batch request')
        
        results = []
        spam_count = 0
        
        for email in emails:
            subject = email.get('subject', '').strip()
            body = email.get('body', '').strip()
            
            if not subject and not body:
                results.append({'error': 'Subject or body required'})
                continue
            
            is_spam, confidence = simple_spam_classifier(subject, body)
            risk_level = 'high' if confidence > 0.7 else 'medium' if confidence > 0.4 else 'low'
            
            if is_spam:
                spam_count += 1
            
            stats['total_emails_analyzed'] += 1
            if is_spam:
                stats['spam_detected'] += 1
            else:
                stats['legitimate_emails'] += 1
            
            results.append({
                'is_spam': is_spam,
                'confidence': round(confidence, 3),
                'risk_level': risk_level
            })
        
        total_conf = (stats['average_confidence'] * (stats['total_emails_analyzed'] - len(results)) + sum(r.get('confidence', 0) for r in results if 'confidence' in r))
        if stats['total_emails_analyzed'] > 0:
            stats['average_confidence'] = total_conf / stats['total_emails_analyzed']
        
        return jsonify({
            'results': results,
            'total_processed': len(results),
            'spam_count': spam_count,
            'legitimate_count': len(results) - spam_count,
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    total = stats['total_emails_analyzed']
    if total == 0:
        accuracy = 0.0
    else:
        accuracy = (stats['spam_detected'] + stats['legitimate_emails']) / total if total > 0 else 0.0
    
    return jsonify({
        'total_emails_analyzed': stats['total_emails_analyzed'],
        'spam_detected': stats['spam_detected'],
        'legitimate_emails': stats['legitimate_emails'],
        'spam_percentage': round((stats['spam_detected'] / total * 100), 2) if total > 0 else 0,
        'accuracy_rate': round(accuracy, 3),
        'average_confidence': round(stats['average_confidence'], 3),
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/stats/reset', methods=['POST'])
def reset_stats():
    global stats
    stats = {
        'total_emails_analyzed': 0,
        'spam_detected': 0,
        'legitimate_emails': 0,
        'average_confidence': 0.0,
    }
    return jsonify({'message': 'Statistics reset successfully'}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    os.makedirs('models', exist_ok=True)
    model = load_model()
    app.run(debug=True, host='0.0.0.0', port=5000)

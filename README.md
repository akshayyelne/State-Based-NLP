Insurance Policy & Claims Assistant (NLP + FSM)

An AI-powered conversational insurance assistant built using Natural Language Processing (NLP) and Finite State Machine (FSM) workflow orchestration.

The system simulates real-world insurance operations including:

Policy creation

Claim submission

Claim status tracking

Policy renewal

Admin monitoring

The solution combines Machine Learning intent classification, rule-based entity extraction, and structured workflow automation to guide users through complex insurance processes.

System Overview

The assistant interprets user queries, identifies the intent, extracts key entities, and triggers the appropriate workflow engine.

User Input
     │
     ▼
Intent Classification (TF-IDF + Logistic Regression)
     │
     ▼
Entity Extraction (Regex)
     │
     ▼
Dialogue Manager
     │
     ▼
Workflow FSM
 ├── Policy Creation
 ├── Claim Submission
 └── Policy Renewal
     │
     ▼
SQLite Database
     │
     ▼
Streamlit Interface
Key Features
Policy Creation Workflow

Users can create an insurance policy through a guided conversational process.

Steps include:

Customer identity capture

Date of birth validation

Vehicle information collection

Coverage selection

Premium calculation

Policy issuance

Claim Management Workflow

Customers can submit insurance claims through the chatbot.

The system performs:

Policy validation

Incident data collection

Risk classification

Claim submission

Claim lifecycle simulation:

Submitted
    ↓
Under Review
    ↓
Investigation (High Risk)
    ↓
Approved / Rejected
    ↓
Paid
Policy Renewal

The chatbot supports policy renewal requests by:

Verifying policy details

Retrieving coverage information

Confirming renewal

Updating policy status

Admin Dashboard

The admin interface provides operational visibility:

View all policies

View all claims

Filter claims by status

Export reports as CSV

Technology Stack
Component	Technology
Frontend	Streamlit
NLP Model	TF-IDF + Logistic Regression
Dialogue Management	Finite State Machine
Entity Extraction	Regex-based extraction
Database	SQLite
Programming Language	Python
Project Structure
insurance-chatbot/
│
├── app.py
├── config.py
├── intents.json
│
├── dialogue/
│   └── dialogue_manager.py
│
├── workflows/
│   ├── policy_fsm.py
│   ├── claim_fsm.py
│   └── renewal_fsm.py
│
├── nlp/
│   └── intent_model.py
│
├── utils/
│   └── entity_extractor.py
│
├── engines/
│   ├── payment_engine.py
│   ├── underwriting_engine.py
│   └── validation_engine.py
│
└── database/
    └── insurance.db
How It Works
1. Intent Detection

The user message is converted into numerical features using TF-IDF vectorization.

A Logistic Regression classifier predicts the intent.

Example intents:

create_policy
file_claim
check_claim_status
renew_policy
2. Entity Extraction

The system extracts structured values from text using regex.

Examples:

Policy Number → P12345
Claim ID → CLM1001
Date → 12/03/2025
3. Dialogue Manager

The Dialogue Manager routes the conversation to the correct workflow based on the predicted intent.

4. Workflow Engine (FSM)

Each business process is implemented as a Finite State Machine.

Example:

COLLECT_POLICY
    ↓
COLLECT_DATE
    ↓
COLLECT_TYPE
    ↓
COLLECT_DESC
    ↓
SUBMIT_CLAIM
Running the Project
1. Install dependencies
pip install streamlit scikit-learn pandas
2. Run the application
streamlit run app.py
3. Open in browser
http://localhost:8501
Example Interactions
Create Policy
User: I want to create a policy
Bot: What is your full name?
File Claim
User: I want to file a claim
Bot: Please provide your policy number
Check Claim Status
User: check claim status CLM1023
Bot: Claim CLM1023 status: Under Review
Future Improvements

Possible enhancements for production systems:

LLM-based intent detection

Fraud detection engine

Claims analytics dashboard

Document upload for claims

Real-time policy pricing

Cloud deployment

API integration with external insurers

Author

This project demonstrates how conversational AI can be combined with workflow automation to simulate real-world insurance operations.

It is designed as a learning project for AI, NLP, and workflow-based system design.

If you'd like, I can also help you create:

A GitHub portfolio-level README (much more impressive visually)

Architecture diagrams for the repo

Badges + project highlights to make recruiters notice it.

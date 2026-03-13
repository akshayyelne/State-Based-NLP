**Insurance Policy & Claims Assistant (NLP + FSM)**

     An AI-powered conversational insurance assistant built using Natural Language Processing (NLP) and Finite State Machine (FSM) workflow orchestration.
     
     The system simulates real-world insurance operations including:
     
     1. Policy creation
     
     2. Claim submission
     
     3. Claim status tracking
     
     4. Policy renewal
     
     5. Admin monitoring
     
     The solution combines Machine Learning intent classification, rule-based entity extraction, and structured workflow automation to guide users through complex insurance processes.

**System Overview**

     The assistant interprets user queries, identifies the intent, extracts key entities, and triggers the appropriate workflow engine.
     
     <img width="744" height="451" alt="image" src="https://github.com/user-attachments/assets/ebcd7ce4-a57c-4431-848d-5c530f519d48" />



**Key Features**
     Policy Creation Workflow
     
     Users can create an insurance policy through a guided conversational process.
     
     Steps include:
     
    1.  Customer identity capture
     
    2. Date of birth validation
     
    3. Vehicle information collection
     
    4. Coverage selection
     
    5. Premium calculation
     
    6.  Policy issuance
     
    7. Claim Management Workflow
     
    8. Customers can submit insurance claims through the chatbot.
     
    9.  The system performs:
     
    10. Policy validation
     
    11.  Incident data collection
     
    12.  Risk classification
     
    13.   Claim submission
     
    14. Claim lifecycle simulation:
     
     <img width="561" height="199" alt="image" src="https://github.com/user-attachments/assets/874f2ef9-0754-497c-adbc-0a5c07a30ebe" />

**Policy Renewal**

     The chatbot supports policy renewal requests by:
     
     Verifying policy details
     
     Retrieving coverage information
     
     Confirming renewal
     
     Updating policy status

**Admin Dashboard**

     The admin interface provides operational visibility:
     
     View all policies
     
     View all claims
     
     Filter claims by status
     
     Export reports as CSV

**Technology Stack**
     Component	Technology
     Frontend	Streamlit
     NLP Model	TF-IDF + Logistic Regression
     Dialogue Management	Finite State Machine
     Entity Extraction	Regex-based extraction
     Database	SQLite
     Programming Language	Python
     
**Project Structure**

<img width="762" height="553" alt="image" src="https://github.com/user-attachments/assets/f47bd252-4ccd-4f2d-8f44-876cbdf06958" />

**How It Works**
     1. Intent Detection
     
     The user message is converted into numerical features using TF-IDF vectorization.
     
     A Logistic Regression classifier predicts the intent.
     
                    Example intents:
     
                    create_policy
                    file_claim
                    check_claim_status
                    renew_policy
                    
     **2. Entity Extraction**
     
     The system extracts structured values from text using regex.
     
                    Examples:
                    
                    Policy Number → P12345
                    Claim ID → CLM1001
                    Date → 12/03/2025
                    
**3. Dialogue Manager**

The Dialogue Manager routes the conversation to the correct workflow based on the predicted intent.

**4. Workflow Engine (FSM)**

     Each business process is implemented as a Finite State Machine.

Example:

     <img width="221" height="199" alt="image" src="https://github.com/user-attachments/assets/281bbd59-f1d2-4713-be16-0585fd0c4c76" />


Running the Project

     1. Install dependencies
     
     Run on streamlit
     https://state-based-nlp-csakjxas8cif8vqfvjapfc.streamlit.app/

**Future Improvements**
     
     Possible enhancements for production systems:
     
     LLM-based intent detection
     
     Fraud detection engine
     
     Claims analytics dashboard
     
     Document upload for claims
     
     Real-time policy pricing
     
     Cloud deployment
     
     API integration with external insurers

**Author**

     This project demonstrates how conversational AI can be combined with workflow automation to simulate real-world insurance operations.
     
     It is designed as a learning project for AI, NLP, and workflow-based system design.
     
     

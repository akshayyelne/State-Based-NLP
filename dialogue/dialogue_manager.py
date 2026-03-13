import streamlit as st
from nlp.intent_model import predict_intent
from workflows.policy_fsm import handle_policy
from workflows.claim_fsm import handle_claim
from workflows.renewal_fsm import handle_renewal
from workflows.policy_status_fsm import handle_policy_status
from utils.entity_extractor import extract_entities


class DialogueManager:

    # ==============================
    # INITIALIZATION
    # ==============================
    def __init__(self):

        if "workflow" not in st.session_state:
            st.session_state.workflow = None

        if "state" not in st.session_state:
            st.session_state.state = "START"

        if "slots" not in st.session_state:
            self.reset_slots()

        # Central workflow mapping (scalable)
        self.workflow_handlers = {
            "policy": handle_policy,
            "claim": handle_claim,
            "renewal": handle_renewal,
            "status_change": self.handle_status_change,
            "policy_status": handle_policy_status
        }

        # Intent → workflow mapping
        self.intent_workflow_map = {
            "create_policy": ("policy", "COLLECT_NAME",
                              "What is your full name?"),
            "file_claim": ("claim", "COLLECT_POLICY",
                           "Please provide your policy number."),
            "check_claim_status": ("claim", "CHECK_STATUS",
                                   "Please provide your claim ID."),
            "renew_policy": ("renewal", "RENEW_VERIFY_POLICY",
                             "Please provide your policy number."),
            "activate_policy": ("status_change", "COLLECT_POLICY_ACTIVATE", "Please provide the policy number you want to activate."),
            "deactivate_policy": ("status_change", "COLLECT_POLICY_DEACTIVATE", "Please provide the policy number you want to deactivate."),
            "check_policy_status": ("policy_status", "CHECK_POLICY_STATUS", "Please provide the policy number to check.")
        }
        
    def handle_status_change(self, state, slots, entities, user_input):
        from services.policy_service import update_policy_status
        import sqlite3
        from config import DB_PATH
        
        if "policy_number" in entities:
            policy = entities["policy_number"]
            action = "Inactive" if "DEACTIVATE" in state else "Active"
            
            # Check if policy exists
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT customer_name FROM Policies WHERE policy_number=?", (policy,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                update_policy_status(policy, action)
                verb = "deactivated" if action == "Inactive" else "activated"
                return "END", f"Policy {policy} has been successfully {verb}."
            else:
                return state, "Policy not found. Please provide a valid policy number."
        
        return state, "I couldn't find a policy number in your message. Please provide one (e.g., P12345)."

    # ==============================
    # RESET FUNCTIONS
    # ==============================
    def reset_slots(self):
        st.session_state.slots = {
            "customer_name": None,
            "dob": None,
            "vehicle_make": None,
            "vehicle_year": None,
            "coverage": None,
            "premium": None,
            "policy_number": None,
            "incident_date": None,
            "incident_type": None,
            "description": None,
            "claim_id": None
        }

    def reset(self, refresh=False):
        st.session_state.workflow = None
        st.session_state.state = "START"
        self.reset_slots()
        if refresh:
            st.session_state.chat_history = []
            st.rerun()

    # ==============================
    # MAIN HANDLER
    # ==============================
    def handle(self, user_input):

        text = user_input.lower()
        entities = extract_entities(user_input)

        # --------------------------
        # Goodbye / Reset Handling
        # --------------------------
        if any(word in text for word in ["goodbye", "bye", "exit", "quit"]):
            self.reset(refresh=True)
            return "Goodbye! Have a great day."

        if "cancel" in text:
            self.reset()
            return "Process cancelled."

        # --------------------------
        # Workflow Selection
        # --------------------------
        if st.session_state.workflow is None:

            intent = predict_intent(text)

            if intent in self.intent_workflow_map:
                workflow, state, message = self.intent_workflow_map[intent]
                st.session_state.workflow = workflow
                st.session_state.state = state
                return message

            return "How can I assist you?"

        # --------------------------
        # Active Workflow Execution
        # --------------------------
        workflow = st.session_state.workflow

        if workflow not in self.workflow_handlers:
            self.reset()
            return "System error: Unknown workflow."

        handler = self.workflow_handlers[workflow]

        try:
            new_state, response = handler(
                st.session_state.state,
                st.session_state.slots,
                entities,
                user_input
            )
        except TypeError:
            try:
                # For FSMs that don't use entities
                new_state, response = handler(
                    st.session_state.state,
                    st.session_state.slots,
                    user_input
                )
            except Exception as e:
                import logging
                logging.error(f"Workflow handler error: {e}")
                return "Something went wrong. Please try again."
        except Exception as e:
            import logging
            logging.error(f"Workflow handler error: {e}")
            return "Something went wrong. Please try again."

        # --------------------------
        # END Handling
        # --------------------------
        if new_state == "END":
            self.reset()
        else:
            st.session_state.state = new_state

        return response

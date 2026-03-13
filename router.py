# ==============================
# ROUTER
# ==============================

def route_workflow(intent):

    if intent == "file_claim":
        return (
            "claim",
            "COLLECT_POLICY",
            "Please provide your policy number (e.g., P12345)."
        )

    elif intent == "check_claim_status":
        return (
            "claim",
            "CHECK_STATUS",
            "Please provide your claim ID."
        )

    elif intent == "create_policy":
        return (
            "policy",
            "COLLECT_NAME",
            "Let's create a new policy. What is your full name?"
        )

    elif intent == "renew_policy":
        return (
            "renewal",
            "RENEW_VERIFY_POLICY",
            "Please provide your policy number to renew."
        )

    elif intent == "goodbye":
        return None, "START", "Goodbye!"

    return None, "START", "How can I assist you?"
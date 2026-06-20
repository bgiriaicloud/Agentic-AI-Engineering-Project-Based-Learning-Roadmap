import re

class PIIRedactor:
    """
    Analyzes and redacts personally identifiable information (PII).
    Integrates Microsoft Presidio with regex fallback mechanisms for offline simplicity.
    """
    def __init__(self):
        self.use_presidio = False
        try:
            from presidio_analyzer import AnalyzerEngine
            from presidio_anonymizer import AnonymizerEngine
            self.analyzer = AnalyzerEngine()
            self.anonymizer = AnonymizerEngine()
            self.use_presidio = True
            print("Microsoft Presidio Engines loaded successfully.")
        except Exception as e:
            print(f"[PII Warning] Could not load Microsoft Presidio: {e}. Falling back to Regex Redaction.")

    def redact(self, text: str) -> str:
        """
        Intercepts input text and redacts sensitive PII (emails, cards, phones).
        """
        if self.use_presidio:
            try:
                results = self.analyzer.analyze(text=text, language="en")
                anonymized_result = self.anonymizer.anonymize(text=text, analyzer_results=results)
                return anonymized_result.text
            except Exception as e:
                print(f"[PII Engine Warning] Presidio run failed: {e}. Using regex fallback.")

        # Heuristic Regex Fallback
        redacted = text
        # Email matching
        redacted = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '<EMAIL>', redacted)
        # Credit Card numbers (simple 16 digit check)
        redacted = re.sub(r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b', '<CREDIT_CARD>', redacted)
        # Phone numbers (US/Int standard matching)
        redacted = re.sub(r'\b\+?\d{1,3}[- .]?\(?\d{3}\)?[- .]?\d{3}[- .]?\d{4}\b', '<PHONE_NUMBER>', redacted)
        
        return redacted

if __name__ == "__main__":
    redactor = PIIRedactor()
    test_text = (
        "My name is John Doe. Send the details to john.doe@example.com. "
        "My phone number is +1 (555) 019-2834, and my credit card is 1234-5678-9012-3456."
    )
    print("\nOriginal text:")
    print(test_text)
    print("\nRedacted Output:")
    print(redactor.redact(test_text))
# Output should replace sensitive parts with tags.

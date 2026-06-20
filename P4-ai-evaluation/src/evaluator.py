import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

class RAGEvaluator:
    """
    Evaluates generated LLM responses against context and ground truth.
    Provides API-based LLM evaluations with local heuristic fallback.
    """
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

    def _call_gemini_scorer(self, prompt: str) -> float:
        """
        Uses Gemini to grade a response on a scale of 0.0 to 1.0 based on criteria.
        """
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            # Extract number from response
            match = re.search(r'([0-9\.]+)', response.text)
            if match:
                score = float(match.group(1))
                return min(max(score, 0.0), 1.0)
        except Exception as e:
            print(f"[Scorer Warning] Gemini API evaluation failed: {e}. Using local fallback.")
        return -1.0

    def evaluate_faithfulness(self, context: str, response: str) -> float:
        """
        Measures if the response is fully grounded in the context (no hallucination).
        Scale: 0.0 (fully hallucinated) to 1.0 (perfectly faithful).
        """
        if self.api_key:
            prompt = (
                "You are an AI model evaluation judge. Rate the FAITHFULNESS of the response based ONLY on the provided context.\n"
                "Faithfulness means the response contains NO claims that are unsupported by the context.\n"
                f"Context: {context}\n"
                f"Response: {response}\n"
                "Output ONLY a decimal number representing the score between 0.0 and 1.0. Do not write explanation."
            )
            score = self._call_gemini_scorer(prompt)
            if score >= 0:
                return score

        # Local fallback heuristic: Token overlap of nouns/verbs in response supported by context
        resp_words = set(re.findall(r'\b\w+\b', response.lower()))
        context_words = set(re.findall(r'\b\w+\b', context.lower()))
        
        # Stopwords filter
        stopwords = {"the", "is", "at", "which", "on", "for", "a", "an", "and", "or", "in", "of", "to", "are", "be"}
        resp_filtered = resp_words - stopwords
        context_filtered = context_words - stopwords
        
        if not resp_filtered:
            return 1.0
            
        supported = resp_filtered.intersection(context_filtered)
        return len(supported) / len(resp_filtered)

    def evaluate_answer_relevance(self, query: str, response: str) -> float:
        """
        Measures how well the generated response directly answers the user query.
        """
        if self.api_key:
            prompt = (
                "You are an AI model evaluation judge. Rate the RELEVANCY of the response to the user query.\n"
                "A response is relevant if it directly addresses the query, regardless of correctness.\n"
                f"Query: {query}\n"
                f"Response: {response}\n"
                "Output ONLY a decimal number representing the score between 0.0 and 1.0. Do not write explanation."
            )
            score = self._call_gemini_scorer(prompt)
            if score >= 0:
                return score

        # Local fallback heuristic: query token intersection in response
        query_words = set(re.findall(r'\b\w+\b', query.lower())) - {"what", "is", "how", "the", "at", "for", "to"}
        resp_words = set(re.findall(r'\b\w+\b', response.lower()))
        
        if not query_words:
            return 1.0
            
        overlap = query_words.intersection(resp_words)
        return len(overlap) / len(query_words)

    def run_suite(self, dataset_path: str):
        if not os.path.exists(dataset_path):
            print(f"Error: {dataset_path} not found.")
            return []
            
        with open(dataset_path, "r") as f:
            test_cases = json.load(f)
            
        results = []
        print(f"\n--- Running Evaluation Suite on {len(test_cases)} cases ---")
        
        for case in test_cases:
            print(f"\nTest Case: {case['id']}")
            print(f"Query: {case['query']}")
            
            # Evaluate v1 (Normal)
            faith_v1 = self.evaluate_faithfulness(case["context"], case["generated_output_v1"])
            rel_v1 = self.evaluate_answer_relevance(case["query"], case["generated_output_v1"])
            
            # Evaluate v2 (Hallucinated)
            faith_v2 = self.evaluate_faithfulness(case["context"], case["generated_output_v2_hallucinated"])
            rel_v2 = self.evaluate_answer_relevance(case["query"], case["generated_output_v2_hallucinated"])
            
            results.append({
                "id": case["id"],
                "query": case["query"],
                "v1_faithfulness": round(faith_v1, 2),
                "v1_relevance": round(rel_v1, 2),
                "v2_faithfulness": round(faith_v2, 2),
                "v2_relevance": round(rel_v2, 2),
            })
            
            print(f"  V1: Faithfulness={faith_v1:.2f}, Relevance={rel_v1:.2f}")
            print(f"  V2: Faithfulness={faith_v2:.2f}, Relevance={rel_v2:.2f} (Hallucinated)")
            
        # Write results
        output_path = "./data/evaluation_results.json"
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nResults written to '{output_path}'.")
        return results

if __name__ == "__main__":
    evaluator = RAGEvaluator()
    evaluator.run_suite("./data/golden_dataset.json")

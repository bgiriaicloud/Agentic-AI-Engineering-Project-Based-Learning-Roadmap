import os
import json
import re
import asyncio
from dotenv import load_dotenv
from google.antigravity import Agent, LocalAgentConfig

load_dotenv()

class RAGEvaluator:
    """
    Evaluates google-antigravity Agent outputs against contexts and ground truths.
    """
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

    def _call_gemini_scorer(self, prompt: str) -> float:
        """
        Uses Gemini to grade a response on a scale of 0.0 to 1.0.
        """
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            match = re.search(r'([0-9\.]+)', response.text)
            if match:
                score = float(match.group(1))
                return min(max(score, 0.0), 1.0)
        except Exception as e:
            print(f"[Scorer Warning] Gemini API evaluation failed: {e}. Using local fallback.")
        return -1.0

    def evaluate_faithfulness(self, context: str, response: str) -> float:
        """
        Checks for hallucinations (if output is grounded in context).
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

        # Fallback metric: token overlap
        resp_words = set(re.findall(r'\b\w+\b', response.lower()))
        context_words = set(re.findall(r'\b\w+\b', context.lower()))
        stopwords = {"the", "is", "at", "which", "on", "for", "a", "an", "and", "or", "in", "of", "to", "are", "be"}
        resp_filtered = resp_words - stopwords
        context_filtered = context_words - stopwords
        if not resp_filtered:
            return 1.0
        supported = resp_filtered.intersection(context_filtered)
        return len(supported) / len(resp_filtered)

    def evaluate_answer_relevance(self, query: str, response: str) -> float:
        """
        Measures query-to-answer relevancy.
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

        # Fallback metric: query words intersection
        query_words = set(re.findall(r'\b\w+\b', query.lower())) - {"what", "is", "how", "the", "at", "for", "to"}
        resp_words = set(re.findall(r'\b\w+\b', response.lower()))
        if not query_words:
            return 1.0
        overlap = query_words.intersection(resp_words)
        return len(overlap) / len(query_words)

    async def get_agent_response(self, query: str, context: str) -> str:
        """
        Executes a google-antigravity Agent query with mock context bound in instructions.
        """
        config = LocalAgentConfig(
            system_instructions=(
                "You are an internal helper. Answer the user question using ONLY the provided context.\n"
                f"Context: {context}"
            )
        )
        async with Agent(config=config) as agent:
            response = await agent.chat(query)
            return await response.text()

    def run_suite(self, dataset_path: str):
        if not os.path.exists(dataset_path):
            print(f"Error: {dataset_path} not found.")
            return []
            
        with open(dataset_path, "r") as f:
            test_cases = json.load(f)
            
        results = []
        print(f"\n--- Running Evaluation Suite on {len(test_cases)} Antigravity Agent configurations ---")
        
        for case in test_cases:
            print(f"\nTest Case: {case['id']}")
            print(f"Query: {case['query']}")
            
            # Fetch response dynamically using Antigravity Agent if API key exists
            generated_ans = case["generated_output_v1"]
            if self.api_key:
                try:
                    generated_ans = asyncio.run(self.get_agent_response(case["query"], case["context"]))
                except Exception as e:
                    print(f"Failed to fetch live ADK response: {e}. Using golden dataset candidate.")
            
            # Evaluate v1
            faith_v1 = self.evaluate_faithfulness(case["context"], generated_ans)
            rel_v1 = self.evaluate_answer_relevance(case["query"], generated_ans)
            
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
            
            print(f"  Live/Golden V1: Faithfulness={faith_v1:.2f}, Relevance={rel_v1:.2f}")
            print(f"  Hallucinated V2: Faithfulness={faith_v2:.2f}, Relevance={rel_v2:.2f}")
            
        # Write results
        output_path = "./data/evaluation_results.json"
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nResults written to '{output_path}'.")
        return results

if __name__ == "__main__":
    evaluator = RAGEvaluator()
    evaluator.run_suite("./data/golden_dataset.json")

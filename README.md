1.	Problem Understanding
The objective of this project was to build an AI-powered assistant capable of recommending suitable SHL assessments based on a user's hiring requirements. The assistant needed to go beyond simple keyword matching by understanding natural language queries, retrieving relevant assessments from the official SHL product catalog, and generating conversational responses grounded in factual information. Using RAG System where the LLM reasons over the information provided.
2.	System Architecture
 
3.	Design Choices using RAG

Rather than asking the language model to recommend assessments directly, the assistant first retrieves relevant SHL products and then provides those results as context to the LLM.
This design was chosen because:
•	recommendations remain grounded in official SHL products 
•	hallucinations are reduced 
•	responses remain consistent 
•	new catalog updates require only replacing the JSON file

Sentence Transformer used was “all-MiniLM-L6-v2” from MistralAI that often describe roles naturally rather than using exact assessment names.
      FAISS: All embeddings are stored inside FAISS vector index where the query embedding is generated and compared against other indexed assessments vectors to get top K most relevant assessments.

4.	Prompt Engineering
The prompt plays a critical role in ensuring grounded responses.
Instead of allowing the language model to answer freely, the prompt explicitly instructs it to:
•	use only retrieved assessment information 
•	recommend the single best assessment first 
•	explain why it matches 
•	mention at most two alternatives 
•	avoid hallucinating features 
•	avoid markdown 
•	produce concise responses 
Providing structured assessment metadata (description, job levels, duration, categories, remote support, etc.) significantly improved response quality compared to passing only assessment names.

5.	Additional Features
To make the assistant more conversational, several modules were introduced beyond retrieval.
Intent Detection
Recognizes whether the user is requesting recommendations, refining previous results, or comparing assessments.

Clarification Module
Requests additional information whenever the initial query is too ambiguous.
Example:
User: We need a solution for senior leadership.
Assistant: Is this for hiring candidates or developing existing leaders?
Refinement Module
Allows users to modify previous recommendations.
Example: Remove personality assessments.
The assistant filters the retrieved results accordingly instead of starting a new search.
Comparison Module
Supports queries such as Compare OPQ32r and Global Skills Assessment.
The assistant summarizes similarities and differences using official catalog information.
Conversation Completion
Detects closing messages such as
•	Thanks 
•	Perfect 
•	That's exactly what we need 
and returns end_of_conversation = true making the interaction more natural.
6.	. Evaluation
The system was evaluated using:
•	SHL sample conversations 
•	Swagger API testing 
•	manual testing 
•	Render deployment testing 
The evaluation focused on
•	retrieval relevance 
•	recommendation quality 
•	clarification behavior 
•	comparison responses 
•	JSON schema correctness 
•	response consistency 


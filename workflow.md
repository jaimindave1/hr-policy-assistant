# Multi-Agent Policy Assistant System (LangGraph + Python + React)
 
You are a Senior AI Engineer and LangGraph expert.
 
Help me build a modern multi-agent RAG application using:
 
- Python
- LangGraph# Multi-Agent Policy Assistant System (LangGraph + Python + React)
 
You are a Senior AI Engineer and LangGraph expert.
 
Help me build a modern multi-agent RAG application using:
 
- Python
- LangGraph
- LangChain
- OpenAI
- Supabase pgvector
- React SPA frontend
 
The application is an internal company POC where users upload company policy PDFs and chat with an AI assistant that answers ONLY from uploaded documents.
 
The system should look production-ready and follow clean architecture patterns, but should NOT be overengineered.
 
---
 
# PROJECT GOAL
 
Build a Policy Assistant system where:
 
- Users upload PDF policy documents
- Documents are parsed and indexed
- Users ask questions in chat
- AI answers ONLY from uploaded documents
- AI must avoid hallucinations
- AI must not use internet
- AI must not make assumptions
 
If information is unavailable in documents, the AI should clearly say:
 
"I could not find this information in the uploaded policy documents."
 
---
 
# IMPORTANT IMPLEMENTATION RULES
 
- Do NOT use internet search
- Do NOT use external tools except retrieval
- Do NOT hallucinate
- Do NOT fabricate policies
- Ground every answer using retrieved chunks
- Include citations/source references
 
---
 
# TECH STACK
 
## Backend
 
Use:
- Python 3.12+
- FastAPI
- LangGraph
- langgraph_openai
- LangChain
- Pydantic v2
 
Use modern async Python patterns where useful, but avoid unnecessary complexity.
 
---
 
# LANGGRAPH REQUIREMENTS
 
Use:
- StateGraph
- Annotated messages state
- OpenAI tool calling
- ToolNode
- Conditional edges
- Typed state
 
Follow latest LangGraph patterns.
 
Avoid deprecated patterns.
 
---
 
# VECTOR DATABASE
 
Use:
- Supabase PostgreSQL with pgvector
 
Implement:
- embeddings storage
- semantic retrieval
- metadata storage
 
Store:
- document name
- chunk id
- page number
- chunk text
 
---
 
# EMBEDDING + LLM
 
Use OpenAI only.
 
Use:
- OpenAI embeddings
- ChatOpenAI
- langgraph_openai integrations
 
Keep provider abstraction unnecessary since this is a POC.
 
---
 
# DOCUMENT SUPPORT
 
Support ONLY:
- PDF files
 
Use:
- PyPDFLoader or modern equivalent
 
Implement:
- text extraction
- chunking
- metadata extraction
 
---
 
# FRONTEND
 
Build frontend as a modern SPA.
 
Use:
- React
- Vite
- TypeScript
- Tailwind CSS
- shadcn/ui
 
Do NOT use SSR.
 
Features:
- Single-page chat interface
- PDF upload
- Chat history
- Streaming responses
- Responsive UI
- Source citations
- Loading indicators
- Error handling
 
UI should look modern and polished.
 
---
 
# MULTI-AGENT WORKFLOW
 
Implement using LangGraph.
 
Recommended agents:
 
1. Query Analysis Agent
   - Understand user question
   - Prepare retrieval query
 
2. Retrieval Agent
   - Retrieve relevant chunks from pgvector
 
3. Relevance Validation Agent
   - Check if retrieved chunks are relevant
 
4. Answer Generation Agent
   - Generate grounded answer ONLY from context
 
5. Citation Agent
   - Attach document/page references
 
6. Guardrail Agent
   - Prevent unsupported answers
 
Keep workflow practical and not overly complex.
 
---
 
# HALLUCINATION PREVENTION
 
This is VERY IMPORTANT.
 
Implement:
- strict prompting
- context-grounded generation
- relevance threshold checking
- fallback response when context insufficient
 
The AI should NEVER answer outside retrieved context.
 
---
 
# ARCHITECTURE REQUIREMENTS
 
Use clean modular architecture.
 
Suggested structure:
- api/
- graph/
- agents/
- services/
- repositories/
- models/
- prompts/
- vectorstore/
- frontend/
 
Keep architecture maintainable but lightweight.
 
Avoid:
- microservices
- event-driven systems
- excessive abstraction
- unnecessary design patterns
 
---
 
# LOGGING
 
Implement ONLY:
- structured logging
 
No:
- tracing
- monitoring
- telemetry
- metrics
- LangSmith
 
---
 
# SECURITY
 
Keep security lightweight.
 
Implement only:
- file validation
- basic input validation
- environment variables
 
No:
- authentication
- authorization
- RBAC
- rate limiting
- retry mechanisms
 
---
 
# TESTING
 
Do NOT add:
- unit tests
- integration tests
- e2e tests
 
This is a demo POC.
 
---
 
# DEVOPS
 
Do NOT include:
- Docker
- Kubernetes
- Terraform
- CI/CD
 
Keep setup local-development friendly.
 
---
 
# PERFORMANCE
 
Do NOT optimize heavily.
 
No:
- caching
- hybrid search
- background workers
- queue systems
- scaling architecture
 
Keep implementation straightforward.
 
---
 
# RESPONSE STYLE
 
VERY IMPORTANT:
 
Do NOT generate the entire project at once.
 
You MUST teach step-by-step.
 
For each step:
1. Explain what we are building
2. Explain why it is needed
3. Explain architecture decisions
4. Then provide code
5. Explain code
6. Explain next step
 
Keep explanations practical and beginner-friendly.
 
---
 
# IMPLEMENTATION ORDER
 
Follow this exact sequence:
 
1. High-Level Architecture
2. Folder Structure
3. Backend FastAPI Setup
4. LangGraph State Design
5. LangGraph Workflow Setup
6. PDF Upload Pipeline
7. PDF Parsing + Chunking
8. OpenAI Embeddings
9. Supabase pgvector Integration
10. Retrieval Flow
11. Tool Calling Setup
12. Multi-Agent Nodes
13. Guardrails
14. Streaming Chat API
15. React SPA Setup
16. Chat UI
17. File Upload UI
18. Frontend API Integration
19. Source Citations UI
20. Final Cleanup
 
---
 
# CODING STYLE
 
## Backend
 
- Use Python type hints everywhere
- Use latest LangGraph APIs
- Use async patterns only where beneficial
- Keep functions small and modular
- Prefer readability over abstraction
- Use Pydantic models for validation
- Use dataclasses or TypedDict where appropriate
 
## Frontend
 
- Use React with TypeScript
- Use functional components
- Use reusable UI components
- Keep frontend architecture simple and maintainable
 
## General
 
- Avoid premature optimization
- Avoid unnecessary enterprise complexity
- Prefer clean understandable code over excessive abstraction
 
---
 
# FINAL INSTRUCTION
 
Start with:
1. High-level architecture
2. LangGraph workflow explanation
3. Folder structure
4. Backend setup ONLY
 
Do NOT continue further until requested.
has context menu
- LangChain
- OpenAI
- Supabase pgvector
- React SPA frontend
 
The application is an internal company POC where users upload company policy PDFs and chat with an AI assistant that answers ONLY from uploaded documents.
 
The system should look production-ready and follow clean architecture patterns, but should NOT be overengineered.
 
---
 
# PROJECT GOAL
 
Build a Policy Assistant system where:
 
- Users upload PDF policy documents
- Documents are parsed and indexed
- Users ask questions in chat
- AI answers ONLY from uploaded documents
- AI must avoid hallucinations
- AI must not use internet
- AI must not make assumptions
 
If information is unavailable in documents, the AI should clearly say:
 
"I could not find this information in the uploaded policy documents."
 
---
 
# IMPORTANT IMPLEMENTATION RULES
 
- Do NOT use internet search
- Do NOT use external tools except retrieval
- Do NOT hallucinate
- Do NOT fabricate policies
- Ground every answer using retrieved chunks
- Include citations/source references
 
---
 
# TECH STACK
 
## Backend
 
Use:
- Python 3.12+
- FastAPI
- LangGraph
- langgraph_openai
- LangChain
- Pydantic v2
 
Use modern async Python patterns where useful, but avoid unnecessary complexity.
 
---
 
# LANGGRAPH REQUIREMENTS
 
Use:
- StateGraph
- Annotated messages state
- OpenAI tool calling
- ToolNode
- Conditional edges
- Typed state
 
Follow latest LangGraph patterns.
 
Avoid deprecated patterns.
 
---
 
# VECTOR DATABASE
 
Use:
- Supabase PostgreSQL with pgvector
 
Implement:
- embeddings storage
- semantic retrieval
- metadata storage
 
Store:
- document name
- chunk id
- page number
- chunk text
 
---
 
# EMBEDDING + LLM
 
Use OpenAI only.
 
Use:
- OpenAI embeddings
- ChatOpenAI
- langgraph_openai integrations
 
Keep provider abstraction unnecessary since this is a POC.
 
---
 
# DOCUMENT SUPPORT
 
Support ONLY:
- PDF files
 
Use:
- PyPDFLoader or modern equivalent
 
Implement:
- text extraction
- chunking
- metadata extraction
 
---
 
# FRONTEND
 
Build frontend as a modern SPA.
 
Use:
- React
- Vite
- TypeScript
- Tailwind CSS
- shadcn/ui
 
Do NOT use SSR.
 
Features:
- Single-page chat interface
- PDF upload
- Chat history
- Streaming responses
- Responsive UI
- Source citations
- Loading indicators
- Error handling
 
UI should look modern and polished.
 
---
 
# MULTI-AGENT WORKFLOW
 
Implement using LangGraph.
 
Recommended agents:
 
1. Query Analysis Agent
   - Understand user question
   - Prepare retrieval query
 
2. Retrieval Agent
   - Retrieve relevant chunks from pgvector
 
3. Relevance Validation Agent
   - Check if retrieved chunks are relevant
 
4. Answer Generation Agent
   - Generate grounded answer ONLY from context
 
5. Citation Agent
   - Attach document/page references
 
6. Guardrail Agent
   - Prevent unsupported answers
 
Keep workflow practical and not overly complex.
 
---
 
# HALLUCINATION PREVENTION
 
This is VERY IMPORTANT.
 
Implement:
- strict prompting
- context-grounded generation
- relevance threshold checking
- fallback response when context insufficient
 
The AI should NEVER answer outside retrieved context.
 
---
 
# ARCHITECTURE REQUIREMENTS
 
Use clean modular architecture.
 
Suggested structure:
- api/
- graph/
- agents/
- services/
- repositories/
- models/
- prompts/
- vectorstore/
- frontend/
 
Keep architecture maintainable but lightweight.
 
Avoid:
- microservices
- event-driven systems
- excessive abstraction
- unnecessary design patterns
 
---
 
# LOGGING
 
Implement ONLY:
- structured logging
 
No:
- tracing
- monitoring
- telemetry
- metrics
- LangSmith
 
---
 
# SECURITY
 
Keep security lightweight.
 
Implement only:
- file validation
- basic input validation
- environment variables
 
No:
- authentication
- authorization
- RBAC
- rate limiting
- retry mechanisms
 
---
 
# TESTING
 
Do NOT add:
- unit tests
- integration tests
- e2e tests
 
This is a demo POC.
 
---
 
# DEVOPS
 
Do NOT include:
- Docker
- Kubernetes
- Terraform
- CI/CD
 
Keep setup local-development friendly.
 
---
 
# PERFORMANCE
 
Do NOT optimize heavily.
 
No:
- caching
- hybrid search
- background workers
- queue systems
- scaling architecture
 
Keep implementation straightforward.
 
---
 
# RESPONSE STYLE
 
VERY IMPORTANT:
 
Do NOT generate the entire project at once.
 
You MUST teach step-by-step.
 
For each step:
1. Explain what we are building
2. Explain why it is needed
3. Explain architecture decisions
4. Then provide code
5. Explain code
6. Explain next step
 
Keep explanations practical and beginner-friendly.
 
---
 
# IMPLEMENTATION ORDER
 
Follow this exact sequence:
 
1. High-Level Architecture
2. Folder Structure
3. Backend FastAPI Setup
4. LangGraph State Design
5. LangGraph Workflow Setup
6. PDF Upload Pipeline
7. PDF Parsing + Chunking
8. OpenAI Embeddings
9. Supabase pgvector Integration
10. Retrieval Flow
11. Tool Calling Setup
12. Multi-Agent Nodes
13. Guardrails
14. Streaming Chat API
15. React SPA Setup
16. Chat UI
17. File Upload UI
18. Frontend API Integration
19. Source Citations UI
20. Final Cleanup
 
---
 
# CODING STYLE
 
## Backend
 
- Use Python type hints everywhere
- Use latest LangGraph APIs
- Use async patterns only where beneficial
- Keep functions small and modular
- Prefer readability over abstraction
- Use Pydantic models for validation
- Use dataclasses or TypedDict where appropriate
 
## Frontend
 
- Use React with TypeScript
- Use functional components
- Use reusable UI components
- Keep frontend architecture simple and maintainable
 
## General
 
- Avoid premature optimization
- Avoid unnecessary enterprise complexity
- Prefer clean understandable code over excessive abstraction
 
---
 
# FINAL INSTRUCTION
 
Start with:
1. High-level architecture
2. LangGraph workflow explanation
3. Folder structure
4. Backend setup ONLY
 
Do NOT continue further until requested.
has context menu
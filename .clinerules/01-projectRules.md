# Project Guardrails

## Purpose
Keep scope tight and outcomes predictable. Align with the written specs before coding.

---

## Source of truth
- Follow `docs/Functional_Specification_Document.md` and `docs/Product_Requirement_Document.md` strictly.  
- Do not add features, entities, or pages beyond scope.  
- If something is unclear, propose the minimal assumption and record it in an **“Open Questions”** note in the Product_Requirement_Document.  
- Do not expand scope.  

---

## Plan before code (Cline Plan mode)
- Restate the goal and acceptance criteria for this step.  
- List files to create/edit and why.  
- Call out validations, error behaviors, and edge cases.  
- Define verification steps (curl/UI) you’ll run after the change.  
- Only then generate/edit code.  

---

## Functional expectations
<!-- ### Backend (Spring Boot + H2) -->
### Backend (Python FastAPI uvcorn openAI microservices)
Features:

Ticket Categorization & Routing:
- NLP-based classification of incoming tickets.
- Auto-routing to appropriate IT agents based on skill and availability.
- Knowledge Base Optimization:
- ML-driven gap analysis in KB articles.
- Generative AI to suggest/update articles.
- Chatbot integration for self-service resolution.

- Implement endpoints exactly as specified.  
- No entity relationships/mappings; all tables/entities are independent.  
- Preload initial data from `data.json`.  
- Keep error semantics simple and consistent.  

### Frontend (React + Material-UI with SAP Fiori theme)
<!-- - Pages: Dashboard, Travel Requests, Expense Submission, Approvals, Profile.  -->
- Pages: Dashboard for agents to view assigned tickets, React forms for ticket submission, KB search and chatbot interface.
- Features: forms with validation, file uploads, search & filter, charts, notifications, mobile-friendly layout.  
- Use React Router for navigation.  
- Use Context API or Redux for state management.  
- Build with `.js` files only.  

### Authentication
- Not in scope.  

---

## Definition of done
- Build runs, lint clean.  
- Acceptance criteria met.  
- Verification steps/tests pass locally.  
- README and docs updated if behavior changed.  
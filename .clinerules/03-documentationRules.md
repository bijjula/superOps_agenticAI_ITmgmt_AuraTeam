# Documentation & Testing

## Purpose
Keep documentation in sync and verify behavior with concrete, repeatable steps.

---

## Documentation Expectations
- Update `docs/Product_Requirement_Document.md` and `docs/Functional_Specification_Document.md` if behavior, interfaces, or assumptions change.  
- Keep `README.md` prompts and guardrails aligned to the latest **Product_Requirement_Document** and **Functional_Specification_Document**.  
- Add or adjust examples and routes in `README.md` whenever backend endpoints or frontend flows change.  

---

## Testing Expectations
- Provide `curl` examples for each backend endpoint, including expected request/response payloads.  
- Include negative tests for validation errors, bad requests, and not-found cases.  
- Document UI manual test steps such as navigation flows, form validations, dialogs, and notifications.  
- Verify responsiveness and mobile-friendly layout across supported screen sizes.  

---

## Change Management
- Summarize all user-visible changes at the end of Pull Requests (PRs).  
- Note new environment variables or configuration keys in both `README.md` and `.env.example`.  
- Ensure changes remain within the scope of **Product_Requirement_Document** and **Functional_Specification_Document**.  
# Coding Standards

## Purpose
<!--Produce clear, maintainable code that aligns with Spring Boot and React best practices, while staying consistent with the **Functional_Specification_Document** and **Product_Requirement_Document**. -->
Produce clear, maintainable code that aligns with Python FastAPI uvcorn based MCP microservices and React best practices, while staying consistent with the **Functional_Specification_Document** and **Product_Requirement_Document**.

---

## Naming & Structure
- Use meaningful names (no 1–2 letter identifiers).  
- Keep functions/methods short and single-purpose.  
- Prefer early returns; avoid deep nesting.  
- Organize code into clear modules (controllers, services, repositories, components).  

---

## Type & Data Handling
- Backend: keep DTO fields aligned with **Functional_Specification_Document**.  
- Do not use entity relationships/mappings between tables.  
- Validate inputs for APIs; guard against null/undefined.  
- Apply formatting/rounding rules only where **Product_Requirement_Document** specifies.  

---

## Error Handling
- Use clear error messages with actionable context.  
- Return appropriate HTTP status codes (e.g., `400` for validation errors, `404` for not found).  
- Do not swallow errors; log unexpected failures once at the boundary layer.  

---

## React (Frontend) Practices
<!-- - Use Material-UI with SAP Fiori styling for components.  -->
- Use `.js` files only (no `.ts` or `.tsx`).  
- Keep components focused; extract reusable ones.  
- Use React Router for navigation.  
- Use Context API or Redux for state management.  
- Show success/error notifications for actions; validate form inputs.  
- Avoid manual DOM manipulation; rely on React state and props.  
- Ensure responsive, mobile-friendly layouts.  

---

## Project Specifics
- Do not introduce new entities, pages, or features beyond what is defined in **Functional_Specification_Document** and **Product_Requirement_Document**.  
<!-- - Pages: Dashboard, Travel Requests, Expense Submission, Approvals, Profile.  -->
- Pages: Dashboard, Assigned Case list, child page for knowledge for the selected case
- Features: forms with validation, file uploads, search & filter, charts, notifications.  
- Keep implementation minimal, modern, and user-friendly.  
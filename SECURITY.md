# Security and product boundary

This foundation runs locally without network services, external model calls or credentials.
Do not expose a future development server publicly without authentication, authorization,
upload limits, error/log redaction and appropriate deployment review.

Threat boundaries: future CSV intake is untrusted; SQL is application-owned; any future LLM
gets bounded calculated evidence and no executable SQL, arbitrary tools or raw customer data.
Prompt filtering alone cannot establish safety. Validate outputs against evidence contracts.

Report security issues privately to the repository owner through an available verified channel;
no private reporting feature or contact address is asserted here. Do not post sensitive payloads.
OWASP-informed practices are documented in docs/RESEARCH.md; no certification is claimed.

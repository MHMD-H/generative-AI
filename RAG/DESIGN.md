# AI Commerce Copilot Design

## Goal

Build an AI-powered platform for E-commerce businesses that combines a Retrieval-Augmented Generation (RAG) system with an AI Agent. The system will answer customer questions using company knowledge, assist store owners with business insights, analyze sales and operational data, recommend decisions, and support approved business actions.

## Users

### Customer

- Ask about products.
- Ask about return policies.
- Ask about shipping.
- Ask about warranties.
- Receive grounded answers from company knowledge.

### Store Owner

- Analyze sales.
- Analyze products.
- Analyze orders.
- Compare business performance.
- Receive recommendations.
- Approve AI actions.

### Marketing Manager

- Analyze campaigns.
- Improve ROAS.
- Review recommendations.
- Execute marketing actions safely.

## APIs

The system will use REST API over HTTP for normal request and response operations.

The system will use Server-Sent Events (SSE) for streaming chat responses.

### API Format

- Protocol: HTTPS
- API style: REST API
- Data format: JSON
- Streaming: SSE
- Authentication: `/auth`

## Endpoints
- `/auth`
- `/users`
- `/products`
- `/orders`
- `/sales`
- `/campaigns`
- `/documents`
- `/documents/{id}/chunks`
- `/conversations`
- `/conversations/{id}/messages`
- `/chat`
- `/chat/stream`
- `/search`
- `/feedback`
- `/agent/tools`
- `/agent/actions`
- `/agent/actions/{id}/approval`

### Endpoint Purpose

- `/auth`: login, register, logout, and authentication.
- `/users`: manage customer, store owner, and marketing manager users.
- `/products`: query and analyze product data.
- `/orders`: query and analyze order data.
- `/sales`: retrieve sales metrics and sales analysis.
- `/campaigns`: retrieve and analyze marketing campaign data.
- `/documents`: upload and manage company knowledge documents.
- `/documents/{id}/chunks`: retrieve document chunks used by RAG.
- `/conversations`: create and retrieve conversations.
- `/conversations/{id}/messages`: create and retrieve conversation messages.
- `/chat`: normal chatbot request and response.
- `/chat/stream`: streaming chatbot response using SSE.
- `/search`: search company knowledge, products, orders, sales, and campaigns.
- `/feedback`: collect user feedback on AI answers.
- `/agent/tools`: list or call available agent tools.
- `/agent/actions`: create and review AI actions.
- `/agent/actions/{id}/approval`: approve or reject AI actions.

## Authentication

- Authentication Provider: Supabase Auth
- Authentication Method: JWT
- Token Transport: Bearer Token
- Access Token: Issued to every authenticated user
- Refresh Token: Issued to every authenticated user
- Token Refresh: Managed by Supabase Auth
- JWT Validation: FastAPI
## Authorization

### Authorization Model

The system shall use a hybrid authorization model consisting of:

- Role-Based Access Control (RBAC)
- Resource-Based Authorization (ACL)

RBAC is responsible for high-level user roles.

Resource-Based Authorization (ACL) is responsible for fine-grained permissions within each business (tenant).

---

### Role-Based Access Control (RBAC)

The system shall support the following roles:

- Customer
- Store Owner
- Marketing Manager
- Team Member
- Admin

Each role shall have predefined permissions.

| Role | Permissions |
|------|-------------|
| Customer | View own orders and interact with the AI assistant |
| Store Owner | Full access to business resources |
| Marketing Manager | Manage campaigns and view marketing analytics |
| Team Member | Access assigned business resources |
| Admin | Platform administration |

---

### Resource-Based Authorization (ACL)

Resource-Based Authorization (ACL) provides resource-level permissions inside each business.

Business owners can grant specific permissions to team members without changing their assigned roles.

Examples of resource permissions:

- View Products
- Manage Products
- View Orders
- Manage Orders
- View Sales Analytics
- Manage Campaigns
- Upload Documents
- Manage Knowledge Base

---

### Tenant Isolation

Every request shall be scoped to the authenticated business (tenant).

The system shall prevent users from accessing resources belonging to another tenant.

Every protected resource shall validate:

- User ID
- Tenant ID
- User Role
- Required Permission
- Resource Ownership

---

### Authorization Flow

For every protected request:

1. Validate the JWT.
2. Extract the authenticated user.
3. Identify the tenant.
4. Validate the user's RBAC role.
5. Validate the required ACL permission.
6. Validate resource ownership.
7. Allow or deny the request.

## Databases

The system will use PostgreSQL for tables database.

The system will use Chroma for vector database.

### PostgreSQL

PostgreSQL stores structured business and application data:

- Users
- Products
- Orders
- Sales
- Campaigns
- Documents metadata
- Conversations
- Messages
- Feedback
- Agent actions
- Approval records

### Chroma

Chroma stores vector embeddings for RAG retrieval:

- Document chunks
- Product documentation chunks
- Company policies
- SOPs
- Marketing guidelines
- Historical reports

## Data Model

### users

- `id`
- `name`
- `email`
- `role`
- `created_at`
- `updated_at`

### products

- `id`
- `name`
- `description`
- `category`
- `status`
- `created_at`
- `updated_at`

### orders

- `id`
- `user_id`
- `status`
- `total_amount`
- `created_at`
- `updated_at`

### sales

- `id`
- `order_id`
- `product_id`
- `amount`
- `created_at`

### campaigns

- `id`
- `name`
- `channel`
- `spend`
- `revenue`
- `roas`
- `created_at`
- `updated_at`

### documents

- `id`
- `title`
- `type`
- `source`
- `created_at`
- `updated_at`

### document_chunks

- `id`
- `document_id`
- `chunk_index`
- `content`
- `chroma_vector_id`
- `metadata`
- `created_at`

### conversations

- `id`
- `user_id`
- `status`
- `created_at`
- `updated_at`

### messages

- `id`
- `conversation_id`
- `sender`
- `content`
- `sources`
- `created_at`

### feedback

- `id`
- `user_id`
- `conversation_id`
- `message_id`
- `rating`
- `comment`
- `created_at`

### agent_tools

- `id`
- `name`
- `description`
- `created_at`

### agent_actions

- `id`
- `user_id`
- `type`
- `status`
- `approval_status`
- `created_at`
- `updated_at`

## Chat Flow

1. User sends a request to `/chat` or `/chat/stream`.
2. System identifies the user role.
3. System stores the user message in PostgreSQL.
4. System retrieves relevant company knowledge from Chroma.
5. System retrieves structured business data from PostgreSQL when needed.
6. AI Agent selects the needed tool if the request requires orders, products, sales, campaigns, or actions.
7. System generates a grounded answer using retrieved knowledge and business data.
8. If the response is streamed, `/chat/stream` sends the answer using SSE.
9. If the request needs action execution, the Agent creates a pending action.
10. Store Owner or Marketing Manager approves or rejects the action through `/agent/actions/{id}/approval`.
11. System stores the assistant response in PostgreSQL.
12. User can submit feedback through `/feedback`.

## Requirements

# DESIGN.md

# AI Commerce Copilot — System Requirements

## 1. Project Overview

AI Commerce Copilot is an AI-powered platform for E-commerce businesses that combines a **Retrieval-Augmented Generation (RAG)** system with an **AI Agent**.

The system evolves incrementally through multiple versions, starting as a knowledge assistant and gradually becoming an autonomous business copilot capable of reasoning over business data, consulting company knowledge, and safely executing actions with human approval.

---

# 2. Vision

Build a production-grade AI platform that can:

- Answer customer questions accurately using company knowledge.
- Assist store owners with business insights.
- Analyze operational and sales data.
- Recommend business decisions.
- Execute approved business actions.
- Eventually operate as an autonomous AI copilot.

---

# 3. Target Users

## Customer

Uses the assistant to:

- Ask about products.
- Ask about return policies.
- Ask about shipping.
- Ask about warranties.
- Receive grounded answers from company knowledge.

---

## Store Owner

Uses the assistant to:

- Analyze sales.
- Analyze products.
- Analyze orders.
- Compare business performance.
- Receive recommendations.
- Approve AI actions.

---

## Marketing Manager

Uses the assistant to:

- Analyze campaigns.
- Improve ROAS.
- Review recommendations.
- Execute marketing actions safely.

---

# 4. High-Level Architecture

The system consists of two major components.

## RAG Layer

Responsible for:

- Knowledge ingestion
- Document processing
- Retrieval
- Grounded answer generation

---

## Agent Layer

Responsible for:

- Planning
- Tool calling
- Data analysis
- Decision making
- Action execution
- Human approval workflow

---

# 5. Functional Requirements

---

# Version 1 — Basic AI Assistant

## Objective

Provide a basic AI assistant for both customers and store owners.

---

## Customer Requirements

The system shall allow customers to:

- Ask questions about products.
- Ask questions about company policies.
- Receive answers grounded in uploaded documents.

---

## Store Owner Requirements

The system shall allow store owners to:

- Retrieve simple business metrics.
- Query orders.
- Query products.
- Query sales.

---

## RAG Requirements

The RAG system shall:

- Support document upload.
- Support PDF parsing.
- Support DOCX parsing.
- Support TXT parsing.
- Chunk documents.
- Generate embeddings.
- Store vectors.
- Retrieve relevant chunks.
- Generate grounded answers.

---

## Agent Requirements

The Agent shall:

- Use an LLM.
- Support basic tool calling.
- Select the appropriate tool.
- Return tool results naturally.

Example tools:

- get_sales()
- get_orders()
- get_products()

---

# Version 2 — Smart Assistant

## Objective

Support more complex reasoning and retrieval.

---

## Customer Requirements

The system shall:

- Answer questions requiring multiple documents.
- Combine multiple company policies.
- Retrieve information from several knowledge sources.

---

## Store Owner Requirements

The system shall:

- Compare multiple business metrics.
- Aggregate information from several tools.
- Answer analytical business questions.

---

## RAG Requirements

The RAG system shall support:

- Hybrid Retrieval
- Semantic Search
- Keyword Search
- Metadata Filtering
- Query Rewriting
- Improved Chunking

---

## Agent Requirements

The Agent shall:

- Execute multiple tools in one task.
- Aggregate outputs.
- Produce summarized business answers.

---

# Version 3 — AI Business Analyst

## Objective

Transform the AI Agent into a business analyst.

---

## Customer Requirements

The system shall maintain all previous customer capabilities.

---

## Store Owner Requirements

The system shall:

- Analyze business performance.
- Explain sales drops.
- Detect possible causes.
- Produce analytical reports.

---

## RAG Requirements

The RAG system shall support:

- Context Selection
- Reranking
- Source Citations
- Source Display
- Unknown-answer behavior

---

## Agent Requirements

The Agent shall:

- Decompose tasks.
- Plan execution.
- Select tools dynamically.
- Analyze retrieved data.
- Retry failed operations.
- Recover from tool failures.

---

# Version 4 — AI Business Copilot

## Objective

Combine business data with enterprise knowledge.

---

## Store Owner Requirements

The system shall:

- Analyze business metrics.
- Retrieve company SOPs.
- Retrieve marketing guidelines.
- Generate recommendations aligned with company policies.

---

## RAG Requirements

The knowledge base shall contain:

- SOPs
- Marketing Guidelines
- Company Policies
- Product Documentation
- Historical Reports

The RAG system shall expose a reusable retrieval interface that can be invoked by the AI Agent.

---

## Agent Requirements

The Agent shall:

- Understand user goals.
- Create execution plans.
- Retrieve structured data.
- Retrieve enterprise knowledge.
- Combine both sources.
- Generate business recommendations.

---

# Version 5 — AI Operator

## Objective

Allow the Agent to safely execute business operations.

---

## Store Owner Requirements

The system shall allow owners to:

- Request operational changes.
- Review pending actions.
- Approve or reject AI decisions.

---

## RAG Requirements

The knowledge system shall validate whether requested actions comply with company policies.

---

## Agent Requirements

The Agent shall:

- Execute operational tools.
- Request human approval.
- Integrate with external APIs.
- Verify completed actions.
- Produce audit logs.
- Handle failures safely.

---

# Version 6 — Autonomous Growth Copilot

## Objective

Create an autonomous business assistant capable of continuous monitoring.

---

## Store Owner Requirements

The system shall:

- Monitor business performance.
- Detect anomalies.
- Detect opportunities.
- Generate recommendations.
- Prepare executable actions.
- Request approval before execution.
- Produce business reports.

---

## RAG Requirements

The RAG system shall evolve into an Enterprise Knowledge Engine supporting:

- Multi-tenant knowledge bases
- Document permissions
- Versioning
- Advanced Retrieval
- Reranking
- Citations
- Evaluation
- Access Control
- Historical Knowledge

---

## Agent Requirements

The Agent shall support:

- Long-term memory
- Autonomous monitoring
- Scheduled tasks
- Planning
- Tool orchestration
- Business actions
- Guardrails
- Approval policies
- Verification
- Observability

---

# 6. Non-Functional Requirements

The system shall:

- Be modular.
- Be production-ready.
- Support scalability.
- Support observability.
- Support authentication.
- Support authorization.
- Isolate tenant data.
- Log all important operations.
- Handle failures gracefully.
- Be extensible.
- Be testable.
- Be secure by default.

---

# 7. Milestones

| Version | Goal |
|----------|------|
| V1 | Basic AI Assistant |
| V2 | Smart Assistant |
| V3 | AI Business Analyst |
| V4 | AI Business Copilot |
| V5 | AI Operator |
| V6 | Autonomous Growth Copilot |

---

# 8. Portfolio Strategy

- **V2** delivers a solid RAG + Agent demonstration suitable for showcasing core AI engineering skills.
- **V3** demonstrates business reasoning and analytical capabilities.
- **V4** represents the primary portfolio milestone and recommended first production target.
- **V5** introduces production-safe action execution suitable for freelance client demonstrations.
- **V6** represents the long-term SaaS vision with autonomous business operations.

---

# 9. Current Target

The immediate project objective is to complete **Version 4 (AI Business Copilot)**.

This version provides the best balance between:

- Production readiness
- Portfolio quality
- Freelancing opportunities
- Future SaaS extensibility

Subsequent versions (V5 and V6) extend the platform toward a fully autonomous commercial AI product without requiring major architectural redesign.

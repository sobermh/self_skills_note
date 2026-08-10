# Curriculum Patterns Reference

Use this reference when building a new learning path.

## Curriculum Design Rules

A strong curriculum should progress through:

1. **Foundation**: vocabulary, mental model, prerequisites.
2. **Core Mechanism**: how the system actually works.
3. **Hands-on Practice**: commands, code, labs, or case studies.
4. **Production Concerns**: security, reliability, operations, cost, evaluation.
5. **Project Integration**: a milestone project that combines the stage.
6. **Review and Interview**: concise explanations and tradeoff answers.

Each stage should produce an artifact: a document, demo, lab, small service, test suite, deployment, or portfolio project.

## Time Estimates

Give ranges instead of fake precision.

- 2-hour production-readiness sprint: enough for a high-level map, core mechanisms, common traps, a production-shaped implementation plan, and a hard readiness gate; independent production ownership still requires real project practice unless the learner already has strong engineering experience.
- Beginner basics: 1-2 weeks.
- Practical working level: 4-8 weeks.
- Production-ready prototype: 2-4 months.
- Independent engineering ownership: often 6+ months, depending on prior engineering skill.

Always adjust estimates using:

- Current baseline.
- Daily/weekly study time.
- Whether the target is interview, work project, certification, or deep production competence.

## 2-Hour Crash Course Pattern

Use this pattern when the learner asks for "2 小时吃透", "快速掌握", "速成", "2 小时具备生产级别熟练度", or wants to start development immediately.

Do not try to cover everything at equal depth. Optimize for:

- A complete mental map.
- The smallest production-shaped working example.
- The main safety and production boundaries.
- A concrete next development checklist.
- A hard diagnostic quiz that reveals gaps.

Default structure:

```text
0-8 min: baseline, target, scope cuts
8-25 min: full architecture map
25-45 min: core runtime and mechanisms
45-65 min: safety, permissions, and evidence boundaries
65-85 min: production workflow, state, retries, approval, audit
85-105 min: minimum production-shaped implementation
105-115 min: development plan and acceptance checks
115-120 min: hard quiz and readiness grade
```

Required sections in the answer or artifact:

- "2-hour goal": what the learner can realistically do after this session.
- "Embedded Todo": a checklist that tracks progress inside the same tutorial document.
- "Production-readiness gate": what the learner must answer or build to be considered ready to start production-style work under review.
- "Not included": what cannot be independently owned after only 2 hours.
- "Must know": the concepts that cannot be skipped.
- "Build now": the minimal implementation path.
- "Dangerous to ignore": production risks and safety boundaries.
- "Next 7 days": focused follow-up practice.

When the learner requests a single tutorial document, keep the full sprint in one Markdown file. Do not create separate lesson files unless the learner later asks to expand the course.

## Docker to Kubernetes Example

If the learner says "I have Docker basics and want to learn Kubernetes", use a path like this:

### Stage 1: Kubernetes Mental Model

Learn:

- Cluster, node, control plane.
- Pod, container, workload.
- Desired state and reconciliation.
- kubectl basics.

Deliverable:

- Run a local cluster and deploy a simple app.

### Stage 2: Core Workloads and Networking

Learn:

- Deployment, ReplicaSet, StatefulSet, DaemonSet.
- Service, ClusterIP, NodePort, LoadBalancer.
- Ingress basics.
- ConfigMap and Secret.

Deliverable:

- Deploy a web app with config and internal/external access.

### Stage 3: Storage, Scheduling, and Reliability

Learn:

- Volume, PVC, StorageClass.
- Requests and limits.
- Probes.
- Rolling update and rollback.
- Affinity, taints, tolerations.

Deliverable:

- Deploy a stateful demo and perform an update/rollback.

### Stage 4: Helm and Environment Management

Learn:

- Helm chart structure.
- values.yaml.
- dev/staging/prod values.
- release upgrade and rollback.

Deliverable:

- Package the app as a Helm chart.

### Stage 5: Observability and Troubleshooting

Learn:

- logs, describe, events.
- metrics and health checks.
- common failure modes: ImagePullBackOff, CrashLoopBackOff, Pending, DNS failure.

Deliverable:

- Troubleshooting playbook with reproducible failures.

### Stage 6: Production and Security

Learn:

- RBAC.
- namespaces.
- network policies.
- secret handling.
- resource quotas.
- CI/CD deployment basics.

Deliverable:

- Production-style deployment checklist.

Final project:

- Deploy a small service to Kubernetes with Helm, config, secrets, probes, resource limits, ingress, rollback, and troubleshooting notes.

## Enterprise Agent Example

For Agent learning paths, include:

- LLM API basics.
- messages, system prompt, temperature, token.
- structured output.
- tool calling.
- Agent loop.
- memory.
- RAG.
- retrieval, rerank, citation.
- refusal and hallucination control.
- permissions.
- workflow and human confirmation.
- queues, retries, timeouts.
- API service, database, observability, evaluation, deployment.

Final project:

- Enterprise Agent service with tool calling, RAG, permissions, audit logs, evaluation set, and deployment instructions.

## 2-Hour Enterprise Agent Production-Readiness Sprint

If the learner says "2 小时掌握 Agent 然后开发" or "2 小时具备生产级 Agent 熟练度", use this compressed path:

### 0-8 min: What an Agent Is

Teach:

- Agent = LLM + tools + state/memory + loop/workflow + guardrails.
- LLM decides or proposes; program validates and executes.
- A production Agent is a controlled system, not just a prompt.

Output:

- One architecture map and one sentence defining the model/program safety boundary.

### 8-25 min: Core Runtime Loop

Teach:

- messages and system prompt.
- tool schema.
- model tool selection.
- program-side tool execution.
- tool result returned to model.
- max steps and stop conditions.

Output:

- Minimal loop pseudocode with max steps, stop conditions, and audit events.

### 25-45 min: Tools and Safety

Teach:

- typed parameters.
- validation.
- permissions.
- error handling.
- audit logs.
- high-risk action blocking.

Output:

- One safe tool contract with allowed roles, blocked actions, validation rules, and audit fields.

### 45-65 min: RAG and Knowledge

Teach:

- document loading, chunking, metadata.
- embedding and vector search.
- retrieval, rerank, citation.
- refusal when evidence is weak.
- permission filtering before context injection.

Output:

- Minimal RAG pipeline checklist with permission filtering before context injection and citation checks.

### 65-85 min: Workflow and Human Confirmation

Teach:

- state, node, edge, transition.
- task planning.
- blocked/skipped/completed.
- approval request.
- queue/retry/timeout/idempotency for real tools.

Output:

- High-risk workflow sketch with approved, rejected, waiting, retry, timeout, and failed states.

### 85-105 min: Production-Shaped Implementation

Create:

- file structure.
- first runnable CLI/API demo.
- tool registry.
- RAG module.
- workflow module.
- audit log model.
- verification commands.

Output:

- Implementation checklist and minimal acceptance tests.

### 105-115 min: Development Kickoff

Create:

- backlog for the first implementation session.
- risk register.
- observability checklist.
- evaluation dataset outline.
- rollout and rollback checklist.

Output:

- A "start coding now" checklist.
- If creating artifacts, keep this 2-hour sprint as one detailed tutorial document with Todo, knowledge sections, implementation skeleton, acceptance checks, and the production-readiness gate.

### 115-120 min: Production-Readiness Gate

Ask:

1. What does the model decide, and what must the program execute?
2. Why must tool parameters be validated?
3. When should RAG refuse to answer?
4. Why must permission filtering happen before context injection?
5. Why do high-risk tools need human confirmation?
6. Why do queues need retry limits and idempotency keys?
7. What must be logged for audit and debugging?
8. What tests prove the Agent is safe enough to release behind a gate?

Pass condition:

- The learner can explain the model/program boundary, tool loop, RAG evidence boundary, permission filtering, human confirmation, and async execution risks in their own words.
- Grade 90+: ready to own a narrow Agent module with senior review.
- Grade 80-89: ready to build production-style features under review.
- Grade 60-79: ready to build demos and pair on production work.
- Grade below 60: review the crash track before coding.

## Grading Rubric

Grade answers on:

- Correctness: Does it answer the question?
- Completeness: Does it include the key fields or mechanisms?
- Boundary awareness: Does it distinguish model responsibility from system responsibility?
- Production awareness: Does it mention security, reliability, observability, or operations where relevant?
- Expression: Can the learner explain it clearly in interviews or design reviews?

Use pass with supplement when the answer captures the core idea but misses details. Request re-answer when the learner misses the main concept or reverses an important safety boundary.

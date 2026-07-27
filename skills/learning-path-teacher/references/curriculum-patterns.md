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

- Beginner basics: 1-2 weeks.
- Practical working level: 4-8 weeks.
- Production-ready prototype: 2-4 months.
- Independent engineering ownership: often 6+ months, depending on prior engineering skill.

Always adjust estimates using:

- Current baseline.
- Daily/weekly study time.
- Whether the target is interview, work project, certification, or deep production competence.

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

## Grading Rubric

Grade answers on:

- Correctness: Does it answer the question?
- Completeness: Does it include the key fields or mechanisms?
- Boundary awareness: Does it distinguish model responsibility from system responsibility?
- Production awareness: Does it mention security, reliability, observability, or operations where relevant?
- Expression: Can the learner explain it clearly in interviews or design reviews?

Use pass with supplement when the answer captures the core idea but misses details. Request re-answer when the learner misses the main concept or reverses an important safety boundary.

# Living Forward Deployed Engineering Learning Track

Give this file to the agent responsible for `learn.BeeRad.buzz`, SherpaMD learning content, or any worker researching Forward Deployed Engineering. The goal is not to reproduce or pirate any paid curriculum. The goal is to build a continually improving, source-linked, hands-on FDE learning system from public information, original exercises, and real hiring requirements.

## Mission

Build a living Forward Deployed Engineering curriculum that teaches someone to take an ambiguous customer problem from discovery through production deployment, prove the system works, operate it safely, and hand it over cleanly.

Do not optimize for a certificate. Optimize for demonstrable capability and portfolio evidence.

The learning system must remain open-ended: new FDE roles, tools, protocols, failure modes, courses, public tutorials, and interview patterns should be added as they appear.

## Core principle

FDE is not just “learn AI.” The target loop is:

`discover → clarify → scope → design → build → integrate → evaluate → secure → deploy → observe → troubleshoot → prove value → hand over`

Every major part of the curriculum should eventually exercise that loop.

## Non-negotiable rules

1. Link to upstream public material rather than copying it.
2. Never reproduce paid lessons, proprietary course content, paywalled articles, employer-confidential material, or interview questions that are not public.
3. Prefer primary sources: official docs, official job descriptions, open-source repositories, engineering posts, standards, and public courses.
4. Preserve attribution and direct links.
5. Record `last_verified` for fast-changing sources.
6. Mark stale, broken, or superseded material instead of silently deleting useful history.
7. Every lesson needs a practical objective, not just reading.
8. Every substantial lesson should produce evidence: code, an architecture sketch, test output, an eval result, a scope document, a runbook, or another artifact.
9. Mobile sessions should default to short lessons, quizzes, review, diagrams, flash cards, and planning. Heavy coding labs should be clearly marked `DESKTOP_RECOMMENDED` rather than crammed into a phone screen.
10. Use stars to show content maturity and gaps:
   - ★☆☆☆☆ stub / source captured
   - ★★☆☆☆ basic explanation
   - ★★★☆☆ usable lesson + exercise
   - ★★★★☆ tested lab + assessment
   - ★★★★★ strong lesson + tested lab + rubric + current sources
11. A topic with weak coverage is an invitation for workers to improve it.
12. Do not claim a lesson, lab, mobile view, login flow, or progress feature is finished until it has actually been checked in the relevant interface.

## Role map: teach the family, not one title

Current hiring shows several overlapping branches. Treat them as one skill graph with different emphasis.

### FDE Generalist

Own customer discovery, technical scoping, system design, implementation, production rollout, adoption, eval-driven improvement, and customer communication.

Reference: OpenAI Forward Deployed Engineering roles.

https://openai.com/careers/search/?q=forward+deployed

### Forward Deployed Software Engineer / FDSE

Heavier software-engineering and decomposition track. Rapidly understand customer problems, work with business-critical data, build production systems, and operate close to the customer.

Reference: Palantir FDSE.

https://jobs.lever.co/palantir/dab396d4-2f14-4796-aac0-0d82883dccf0

### Applied AI Engineer / Applied AI Architect

Similar customer-facing production work under different naming. Include these roles when mining job requirements.

Reference: Anthropic Applied AI and FDE roles.

https://www.anthropic.com/careers/jobs

### ML / Inference FDE

Deep specialization in inference engines, model serving, GPU/workload characteristics, fine-tuning/post-training pipelines, benchmarks, latency, throughput, and cost.

References:

https://job-boards.greenhouse.io/togetherai
https://jobs.ashbyhq.com/modal/9fadb51f-ce11-41b1-84d5-470e66cc8ee9
https://jobs.ashbyhq.com/baseten/84c1801c-1a65-49fb-aaaa-beeafd530e7e

### Reliability / Security / Hard-Deployment FDE

Teach constrained environments, observability, incident ownership, auth, multi-tenancy, network boundaries, offline/edge environments, and operational handoff.

Also mine titles containing:

- Forward Deployed Reliability Engineer
- Forward Deployed Security Engineer
- Technical Deployment Lead
- Field Engineer
- Customer Engineer
- Solutions Architect
- Deployment Engineer
- AI Solutions Engineer
- Enterprise AI Architect

## Learning architecture

Do not force a rigid 23-week calendar. Use a skill graph with a recommended path. A learner should be able to go deeper where needed and skip material they can already prove.

### Track 0 — Builder foundation

Goal: become comfortable enough with the basic engineering substrate that AI does not hide missing fundamentals.

Topics:

- Python fundamentals
- reading and modifying unfamiliar code
- Git and GitHub
- Linux shell
- files, processes, environment variables
- JSON, YAML, CSV
- HTTP and REST APIs
- authentication basics
- SQL and relational data
- basic frontend/web concepts
- testing and debugging
- logging
- Docker
- networking fundamentals: DNS, TCP, TLS, proxies, ports

Evidence:

- build a small Python API
- call it from a second program
- add tests
- containerize it
- diagnose a deliberately broken configuration

### Track 1 — LLM application fundamentals

Topics:

- model/API basics
- prompts vs program logic
- structured outputs
- function/tool calling
- context windows
- model selection
- latency/cost/quality trade-offs
- retries, timeouts, rate limits
- prompt injection awareness
- deterministic code around nondeterministic models

Evidence:

- build an LLM feature with typed structured output
- add retry and timeout behavior
- record latency, token use, and failure cases

### Track 2 — Retrieval and enterprise data

Topics:

- embeddings
- chunking
- lexical vs vector vs hybrid retrieval
- metadata filtering
- reranking
- citations and provenance
- permissions-aware retrieval
- document ingestion
- messy enterprise data
- RAG evaluation
- stale-data handling

Evidence:

- build RAG over a deliberately ugly document set
- create a small evaluation set
- compare two retrieval strategies
- document failure cases

### Track 3 — Agentic systems

Topics:

- tools
- planning
- state
- memory
- reflection and verification
- human-in-the-loop
- approval boundaries
- resumable tasks
- orchestration patterns
- manager vs handoff patterns
- multi-agent systems
- long-running jobs
- artifact-producing agents

Primary public learning sources:

https://huggingface.co/learn/agents-course/en/unit0/introduction
https://www.deeplearning.ai/courses/agentic-ai
https://academy.langchain.com/courses/intro-to-langgraph
https://openai.github.io/openai-agents-python/

Evidence:

- build one agent using tools
- add a human approval step
- make interruption/resume work
- build a second implementation using a different orchestration style
- explain why the chosen pattern is appropriate

### Track 4 — MCP, A2A, APIs, and integration

Topics:

- API integration
- tool schemas
- MCP client/server concepts
- MCP security and permission boundaries
- agent discovery
- A2A task lifecycle
- agent-to-tool vs agent-to-agent responsibilities
- streaming and asynchronous work
- integration testing

Primary sources:

https://huggingface.co/learn/mcp-course/en/unit0/introduction
https://a2a-protocol.org/
https://www.deeplearning.ai/short-courses/a2a-the-agent2agent-protocol/

Evidence:

- build an MCP server around a real or mock business API
- connect an agent to it
- build two small agents that communicate through A2A or an equivalent explicit protocol
- demonstrate a stateful task that can be interrupted and resumed

### Track 5 — Evals, observability, and production quality

Topics:

- golden datasets
- task-level success metrics
- LLM-as-judge limits
- deterministic graders
- regression testing
- traces
- tool-call inspection
- error taxonomies
- production feedback
- CI eval gates
- cost budgets
- latency SLOs
- adoption metrics

Primary source:

https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

Also use tracing/evaluation material from the active agent framework being taught.

Evidence:

- define success before changing the system
- build an eval harness
- intentionally introduce a regression
- show the gate catching it
- build a dashboard or report summarizing quality, latency, cost, and failure categories

### Track 6 — Security, auth, governance, and enterprise boundaries

Topics:

- OAuth/OIDC concepts
- service accounts
- secrets management
- least privilege
- RBAC/ABAC concepts
- tenant isolation
- audit trails
- data classification
- prompt injection and tool abuse
- egress restrictions
- retention and privacy
- threat modeling
- security review packets
- human approval for consequential actions

Evidence:

- multi-user app with role-based access
- explicit authorization checks at tool/data boundaries
- threat model
- security review checklist
- audit log for important actions

### Track 7 — Deployment, cloud, infrastructure, and reliability

Topics:

- containers
- Docker images
- CI/CD
- cloud deployment concepts
- queues and workers
- databases and caches
- object storage
- Kubernetes fundamentals
- scaling
- health checks
- rollback
- feature flags
- canary releases
- backups
- incident response
- runbooks

Public starting point:

https://kubernetes.io/docs/tutorials/
https://fullstackdeeplearning.com/llm-bootcamp/

Evidence:

- deploy a working service
- add health checks and logs
- break it intentionally
- recover from a runbook
- perform a rollback

### Track 8 — Customer discovery and FDE delivery

This track is mandatory and should receive as much attention as the AI material.

Topics:

- discovery interviews
- turning vague asks into measurable outcomes
- stakeholder mapping
- constraints and non-goals
- reading the customer environment
- defining the smallest useful release
- assumptions and risk register
- POC vs pilot vs production
- build-vs-buy decisions
- architecture trade-offs
- defining acceptance criteria
- estimating and sequencing work
- Statements of Work / SOW concepts
- pricing and cost awareness
- communicating bad news
- executive-friendly status reporting
- proving value
- handover and training

Curriculum references:

https://interviewkickstart.com/courses/forward-deployed-engineering
https://fdeinterviews.com/courses
https://www.tryexponent.com/courses/intro-fde-interviews

Evidence:

- receive a deliberately ambiguous customer request
- run a written or simulated discovery session
- produce a one-page problem statement
- define success metrics
- write a four-week thin-slice plan
- identify the riskiest assumption
- produce architecture and acceptance criteria
- present the plan to a hostile reviewer

### Track 9 — Hard deployments

Topics:

- environments you did not design
- poor documentation
- broken data
- private networks
- limited or no internet
- constrained hardware
- edge deployments
- legacy integrations
- multi-tenant isolation
- customer-owned infrastructure
- emergency troubleshooting
- partial outages
- vendor dependency failures
- migrating a failing pilot into production

Evidence:

- lab begins with incomplete documentation and multiple symptoms
- learner must diagnose before changing code
- final deliverable includes root cause, fix, validation, rollback path, and customer explanation

### Track 10 — Specializations

Allow optional branches after the core.

#### Generalist FDE

Balance customer discovery, full-stack build, AI, integration, security, and deployment.

#### FDSE

Add deeper algorithms/data structures, backend design, frontend competence, data modeling, system decomposition, and unfamiliar-codebase work.

#### Applied AI

Add deeper RAG, model behavior, prompting, fine-tuning/post-training concepts, data quality, and evaluation.

#### Inference / ML FDE

Add GPU fundamentals, model serving, batching, quantization concepts, inference engines, profiling, latency/throughput, distributed inference, fine-tuning pipelines, and benchmark design.

#### Reliability FDE

Add SRE concepts, capacity planning, tracing, fault injection, incident command, disaster recovery, and observability.

#### Security / Regulated FDE

Add identity, network segmentation, audit, compliance evidence, privacy, secure architecture, threat modeling, and approval controls.

### Track 11 — Interview and portfolio

The course is continued education first, but the same work should create interview evidence automatically.

Topics:

- practical coding
- unfamiliar codebase debugging
- architecture interrogation
- agentic system design
- decomposition/case rounds
- customer scenarios
- project deep dives
- trade-off defense
- behavioral stories
- security/procurement conversations

Current public references:

https://fdeinterviews.com/
https://interviewkickstart.com/blogs/articles/how-does-the-forward-deployed-engineer-interview-process-work
https://github.com/cma0232/fde-interview-prep

Do not blindly memorize reported interview loops. Company processes change. Teach the underlying capabilities.

## Required project ladder

Create at least these projects. More are welcome.

1. **Tool-using assistant** — typed tools, errors, tests, cost/latency notes.
2. **Messy-data RAG system** — ingestion, retrieval comparison, citations, eval set.
3. **MCP integration** — custom MCP server around a business workflow.
4. **Resumable agent workflow** — approvals, interruptions, durable state, audit trail.
5. **Multi-agent system** — explicit orchestration plus A2A or equivalent inter-agent contract.
6. **Enterprise boundary lab** — users/roles, tenant isolation, permissions-aware tools/data.
7. **Production incident drill** — seeded failures, tracing, diagnosis, fix, rollback, postmortem.
8. **Ambiguous-customer capstone** — discovery → scoped plan → implementation → evals → security → deployment → handover.

Optional specialization projects:

- inference optimization benchmark
- offline/edge agent
- security review and red-team exercise
- multi-cloud deployment comparison
- cost-reduction exercise
- legacy system integration
- voice/multimodal field assistant
- agent workflow with a real physical-world or field-service use case

## Artifact portfolio

The site should preserve useful outputs from projects so progress becomes a portfolio.

Recommended artifacts:

- problem statement
- discovery notes
- success metrics
- architecture diagram
- ADR / decision record
- scope and non-goals
- risk register
- estimate
- SOW-style project outline
- source code
- tests
- eval dataset
- eval report
- security checklist
- deployment runbook
- incident postmortem
- customer handover document
- short demo video or screenshots
- retrospective: what would change in v2

## Lesson format

Every normal lesson should have:

1. **Why it matters to an FDE**
2. **Concept**
3. **Real job connection**
4. **Public source links**
5. **10-minute check**
6. **Hands-on task**
7. **Proof / artifact**
8. **Common failure modes**
9. **Stretch task**
10. **Next prerequisite or branch**

For mobile, provide a compact version with the first five items and defer heavy labs where appropriate.

## Progress model

Track capability, not time spent.

Suggested states:

- `NOT_STARTED`
- `READ`
- `PRACTICED`
- `PROVED`
- `NEEDS_REFRESH`

A skill becomes `PROVED` only when there is evidence or a passed assessment.

Skills can decay to `NEEDS_REFRESH` when source material changes materially or the learner has not exercised the skill in a long period.

## Source registry

Each source entry should record:

```yaml
name: Human-readable source name
url: https://example.com
kind: official-docs | employer-role | public-course | open-source | engineering-article | interview-reference
skills:
  - evals
  - customer-discovery
access: free | mixed | paid
last_verified: YYYY-MM-DD
status: active | stale | broken | superseded
notes: short original summary
```

Never mark paid material as required when an adequate free path exists. Paid sources may be listed as optional enrichment.

## Seed source bank

Start with these and continue expanding.

### Hiring / role reality

- OpenAI FDE search — https://openai.com/careers/search/?q=forward+deployed
- Anthropic jobs / Applied AI / FDE — https://www.anthropic.com/careers/jobs
- Palantir FDSE — https://jobs.lever.co/palantir/dab396d4-2f14-4796-aac0-0d82883dccf0
- Scale AI FDE, GenAI — https://scale.com/careers/4593571005
- Together AI FDE / inference — https://job-boards.greenhouse.io/togetherai
- Baseten FDE — https://jobs.ashbyhq.com/baseten/84c1801c-1a65-49fb-aaaa-beeafd530e7e
- Modal FDE ML — https://jobs.ashbyhq.com/modal/9fadb51f-ce11-41b1-84d5-470e66cc8ee9

### FDE curricula / decomposition / interview practice

- Interview Kickstart FDE — https://interviewkickstart.com/courses/forward-deployed-engineering
- FDEInterviews curriculum — https://fdeinterviews.com/courses
- FDEInterviews question bank — https://fdeinterviews.com/
- Exponent FDE introduction — https://www.tryexponent.com/courses/intro-fde-interviews
- Open FDE prep repo — https://github.com/cma0232/fde-interview-prep

### Agent engineering

- Hugging Face Agents Course — https://huggingface.co/learn/agents-course/en/unit0/introduction
- DeepLearning.AI Agentic AI — https://www.deeplearning.ai/courses/agentic-ai
- LangGraph Academy — https://academy.langchain.com/courses/intro-to-langgraph
- OpenAI Agents SDK — https://openai.github.io/openai-agents-python/

### MCP / interoperability

- Hugging Face MCP Course — https://huggingface.co/learn/mcp-course/en/unit0/introduction
- A2A official docs — https://a2a-protocol.org/
- DeepLearning.AI A2A course — https://www.deeplearning.ai/short-courses/a2a-the-agent2agent-protocol/

### Production quality

- Anthropic agent evals — https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- Full Stack LLM Bootcamp — https://fullstackdeeplearning.com/llm-bootcamp/
- Kubernetes tutorials — https://kubernetes.io/docs/tutorials/

## Continuous harvesting loop

Run this periodically and whenever new FDE material is discovered.

1. Search current jobs for the role families above.
2. Extract skills, responsibilities, tools, deployment patterns, and customer-facing requirements.
3. Compare them with the current skill graph.
4. Add or raise priority on missing skills.
5. Search for high-quality public learning resources for each gap.
6. Add source registry entries with verification date.
7. Create or improve lessons.
8. Add a practical exercise and proof requirement.
9. Increase the topic star rating only after the content is actually stronger.
10. Recheck mobile usability for new lessons.
11. Never overwrite an existing strong lesson merely because a fashionable framework appeared; teach stable concepts first and frameworks as implementations.

## Current priority order

1. Customer discovery, decomposition, and scoping
2. Python/API/software fluency
3. Agent tools, state, and orchestration
4. RAG and enterprise data
5. Evals and observability
6. MCP/A2A and integrations
7. Auth/RBAC/security
8. Containers/deployment/reliability
9. Incident ownership and handover
10. Specialization depth
11. Interview drills

## Definition of done for the first usable release

The first release is usable only when all of these are true:

- skill graph exists
- at least 30 lessons are navigable
- at least 10 lessons have hands-on exercises
- at least 4 projects are runnable
- at least one project includes customer discovery and a written scope
- at least one project includes evals
- at least one project includes authentication/authorization
- at least one project includes deployment and a recovery/runbook exercise
- progress can be stored per signed-in user without the site storing user passwords directly
- mobile layout is actually tested at common phone widths
- heavy labs are clearly marked for desktop
- source links are visible
- source registry has verification dates
- weak sections display low star ratings instead of pretending to be complete

## Expansion target

Do not stop at the first release. Grow toward:

- 100+ lessons
- 20+ labs
- 8+ substantial portfolio projects
- 6 specialization branches
- a rotating library of ambiguous customer scenarios
- periodic incident drills
- current job-skill heat maps
- an interview practice mode
- a public source contribution workflow
- downloadable lesson/project markdown where licensing permits

## Final receipt for an implementing agent

Report:

| Check | Status | Evidence |
|---|---|---|
| Skill graph created | PASS/PARTIAL/BLOCKED | Path or URL |
| Source registry created | PASS/PARTIAL/BLOCKED | Path or URL |
| Lessons added | PASS/PARTIAL/BLOCKED | Count + path |
| Labs added | PASS/PARTIAL/BLOCKED | Count + path |
| Projects added | PASS/PARTIAL/BLOCKED | Count + path |
| Progress tracking | PASS/PARTIAL/BLOCKED | Tested behavior |
| Mobile tested | PASS/PARTIAL/BLOCKED | Widths/devices checked |
| Source freshness system | PASS/PARTIAL/BLOCKED | Method |
| Job-skill harvesting | PASS/PARTIAL/BLOCKED | Method |
| Repository commit/push | PASS/BLOCKED | Commit SHA |
| Production verification | PASS/PARTIAL/BLOCKED | URL and checks |

A handoff is not complete merely because files were generated. Complete means the scoped changes were committed, pushed, validated, and checked where users will actually see them.
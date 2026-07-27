# Learning Artifacts Reference

Use these templates when creating persistent study materials.

## Recommended Layout

Default layout for a new topic:

```text
docs/learning/<topic-slug>/
  00_learning_plan.md
  TODO.md
  lessons/
    01_<lesson>.md
    02_<lesson>.md
  projects/
    01_<project>.md
```

If the repository already has `docs/lessons/`, `docs/projects/`, or another course structure, reuse it.

## Learning Plan Template

~~~markdown
# <Topic> Learning Plan

> Goal: <What the learner should be able to do after completion.>

## Baseline

- Current knowledge: <known baseline>
- Target level: <target>
- Time budget: <daily/weekly estimate>
- Learning style: <hands-on / interview / production / certification>

## Reality Check

Completion means practical readiness for the stated target, not guaranteed job placement, promotion, certification, or hiring.

## Roadmap

### Stage 1: <Stage Name>

Estimated time: <range>

You will learn:

- <concept>
- <concept>

Deliverable:

- <artifact/project/demo>

### Stage N: <Stage Name>

...

## Final Capability Standard

By the end, the learner should be able to:

- Explain the architecture.
- Build the core workflow.
- Debug common failures.
- Discuss production risks and tradeoffs.
- Present at least one portfolio-level project.
~~~

## Todo Template

~~~markdown
# <Topic> Learning Todo

Updated: YYYY-MM-DD

## Current Status

- Current stage: <stage>
- Current lesson: <lesson>
- Current goal: <goal>

## Stages

### Stage 1: <Stage Name>

- [ ] Lesson 1: <title>
- [ ] Lesson 2: <title>
- [ ] Stage project: <title>

## Completion Standard Per Lesson

- [ ] I can explain the core idea in my own words.
- [ ] I completed the exercise.
- [ ] I understand the production risks.
- [ ] I ran or reviewed the lab/demo when applicable.
- [ ] Progress was recorded.

## Recent Study Log

| Date | Content | Status | Note |
| --- | --- | --- | --- |
| YYYY-MM-DD | Created learning plan | In progress | Started from lesson 1 |
~~~

## Lesson Template

~~~markdown
# Lesson N: <Title>

## 1. What You Will Learn

After this lesson, you should answer:

1. <question>
2. <question>

## 2. Core Concept

Explain the concept with intuition first, then precise terms.

## 3. Practical or Production Context

Explain where this matters in real work.

## 4. Lab or Example

Include code, commands, diagrams, or concrete examples when useful.

## 5. Common Mistakes

- <mistake>
- <mistake>

## 6. Interview or Review Answer

Provide a concise professional answer.

## 7. Lesson Summary

State the core takeaways.

## 8. Exercise

Ask 3-6 questions that force the learner to explain in their own words.
~~~

## Grading Record Template

Append this to the lesson after the learner answers.

~~~markdown
## <N>. Exercise Grading Record

Record date: YYYY-MM-DD

### Overall Evaluation

Lesson passed / Needs re-answer.

<brief evaluation>

### Question 1: <question>

Learner answer:

```text
<original answer>
```

Evaluation:

<what is right and what is missing>

Standard answer:

```text
<corrected answer>
```

### Lesson Conclusion

<pass/fail and next step>
~~~

## Project Template

~~~markdown
# Stage N Project: <Project Name>

## 1. Project Goal

<what this project validates>

## 2. Functional Scope

Current version supports:

- <feature>

Current version does not support:

- <future production feature>

## 3. Structure

```text
<files>
```

## 4. Run or Review

```powershell
<commands>
```

## 5. Production Thinking

- <risk>
- <tradeoff>

## 6. Acceptance Questions

1. <question>
2. <question>
~~~

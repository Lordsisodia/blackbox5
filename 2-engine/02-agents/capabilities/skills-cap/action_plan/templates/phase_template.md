# Phase: {{phase_name}}

**Phase ID:** {{phase_id}}
**Order:** {{order}} of {{total_phases}}
**Status:** {{status}}

---

## Description
{{description}}

---

## First Principles Analysis

### What problem are we ACTUALLY solving in this phase?
{{true_problem}}

### Fundamental Truths
{% for truth in fundamental_truths %}
- {{truth}}
{% endfor %}

### Assumptions
{% for assumption in assumptions %}
- **{{assumption.text}}** (confidence: {{assumption.confidence}})
  - *Validation:* {{assumption.test}}
{% endfor %}

### Essential Requirements for this Phase
{% for requirement in essential_requirements %}
- {{requirement}}
{% endfor %}

---

## Dependencies
This phase depends on:
{% for dep_id in dependencies %}
- Phase: {{dep_id}}
{% endfor %}

---

## Exit Criteria
This phase is complete when:
{% for criterion in exit_criteria %}
- {{criterion}}
{% endfor %}

---

## Tasks in this Phase
{% for task in tasks %}
### {{task.status.value.upper()}}: {{task.title}}
{{task.description}}

**Subtasks:**
{% for subtask in task.subtasks %}
- {{subtask.status.value.upper()}}: {{subtask.title}}
{% endfor %}

{% endfor %}

---

## Notes
{{metadata}}

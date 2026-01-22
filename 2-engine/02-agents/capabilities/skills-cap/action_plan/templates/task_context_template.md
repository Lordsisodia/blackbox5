# Task Context: {{task_title}}

**Phase:** {{phase_name}}
**Task ID:** {{task_id}}
**Created:** {{created_at}}

---

## Objective
{{objective}}

---

## First Principles Analysis

### What problem are we ACTUALLY solving?
{{true_problem}}

### What do we know to be TRUE?
{% for truth in fundamental_truths %}
- {{truth}}
{% endfor %}

### What are we assuming?
{% for assumption in assumptions %}
- **{{assumption.text}}** (confidence: {{assumption.confidence}})
  - *Validation:* {{assumption.test}}
{% endfor %}

### What MUST be included?
{% for requirement in essential_requirements %}
- {{requirement}}
{% endfor %}

### What can we eliminate?
{% for optional in optional_elements %}
- {{optional}}
{% endfor %}

---

## Constraints

### Hard Constraints (Cannot violate)
{% for constraint in constraints %}
{% if constraint.type == 'hard' %}
- **{{constraint.text}}**
  - *Source:* {{constraint.source}}
{% endif %}
{% endfor %}

### Soft Constraints (Can negotiate)
{% for constraint in constraints %}
{% if constraint.type == 'soft' %}
- {{constraint.text}}
  - *Source:* {{constraint.source}}
{% endif %}
{% endfor %}

---

## Success Criteria
{% for criterion in success_criteria %}
- {{criterion}}
{% endfor %}

---

## Resources
{% for resource in resources %}
- {{resource}}
{% endfor %}

---

## Thinking Process
{{thinking_process}}

---

## Next Steps

1. Review the first principles analysis above
2. Identify any additional assumptions not listed
3. Validate assumptions against constraints
4. Execute task following success criteria
5. Document thinking process and decisions
6. Mark task as complete with results

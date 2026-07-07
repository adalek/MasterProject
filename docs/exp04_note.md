# Experiment 04 – Copy to Points

## Objective

Evaluate whether Qwen2.5-Coder-7B can correctly generate a basic Copy to Points SOP network.

---

## Prompt

```text
Generate only executable Houdini Python code.

Do not use markdown code fences.
Do not explain your solution.

Create:
- one geometry container under /obj

Create the following SOP network:

Grid
↓

Scatter
↓

Copy to Points

Copy one Box SOP onto the scattered points.

Layout the nodes.

Output executable Python only.
```

---

## Result

**Status:** Partial Success

### Attempt 1

- Generated **Grid** and **Scatter** nodes
- Display flag remained on **Grid** which is the first node
- Result: only partial nodes created

### Attempt 2

- Generated **Grid**, **Scatter**, **Copy to Points**, missing **Box**
- **Copy to Points** inputs connect to **Grid** and **Scatter** 
- **Copy to Points** inputs reversed

### Attempt 3

- Generated the correct node network.
- However, the inputs of **Copy to Points** were reversed.
- Manual correction produced the expected result.

### Attempt 4 revision01
- Failure Type:
Invalid multi-input node connection

Error:
hou.InvalidInput

- Observation:
The model attempted to create a Copy to Points network but connected inputs incorrectly or used an invalid input index.

### Attempt 5 revision02
- Failure Type:
syntax error, returned ''' python
- Reason possibly:
context too long?
- Solution:
use clean_code() in houdini_run_llm.py

### Attempt 6 revision02 clean_code()
- nodes are complete but no connection at all

### Attempt 7 revision03 clean_code()
- Success
- Create use node name
- connect use pseudocode format
---


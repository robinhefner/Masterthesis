---
Author: "[[Cheng Ning]]"
Journal: "[[ICLR]]"
Title: "CRITIC–ADVISER–REVISER CYCLIC REFINEMENT: TOWARDS HIGH-QUALITY EMR CORPUS GENERA- TION WITH LLMS"
---

# [[Ning et al., 2026.pdf|CRITIC–ADVISER–REVISER CYCLIC REFINEMENT: TOWARDS HIGH-QUALITY EMR CORPUS GENERATION WITH LLMS]]

### Research Gap:

> ([[Ning et al., 2026.pdf#page=2&annotation=783R|Ning et al., 2026, p.2]])
> We propose LLM-CARe, a stage-wise [[Multi Agent Architektur|multi-agent framework ]]for high-quality EMR synthesis that employs cyclic refinement based on clinical quality principles.

### Methodik:
> ([[Ning et al., 2026.pdf#page=3&annotation=786R|Ning et al., 2026, p.3]])
> e focus on five principles across three levels: demographic typicality (plausible population patterns), knowledge coverage (sufficient breadth of clinical conditions), content completeness (each section includes its essential information), medical correctness (information is clinically valid), and context consistency (sections do not contradict one another)

3 Agents:
- Critic, who evaluates drafts against stage-specific objectives [[Ning et al., 2026.pdf#page=3&annotation=789R|Ning et al., 2026, p.3]]
  [[Qwen2.5-7B-Instruct]] 
- Adviser, who pinpoints areas for improvement and suggests strategies [[Ning et al., 2026.pdf#page=3&annotation=792R|Ning et al., 2026, p.3]]
  [[Qwen2.5-32B-Instruct]] 
- Reviser, who incorporates feedback to update the drafts [[Ning et al., 2026.pdf#page=3&annotation=795R|Ning et al., 2026, p.3]]
  [[Qwen2.5- 0.5B-Instruct]] 





### Main Finding:

> ([[Ning et al., 2026.pdf#page=10&annotation=798R|Ning et al., 2026, p.10]])
> Experiments on a large real-world dataset demonstrate that LLM-CARe substantially improves the quality of EMRs across all granularities.

> ([[Ning et al., 2026.pdf#page=10&annotation=801R|Ning et al., 2026, p.10]])
> These results show the effectiveness of LLM-CARe in generating [[Synthetische Patiendendaten|synthetic]] EMRs that are both high-quality and clinically meaningful, offering a reliable and privacy-preserving foundation for healthcare AI development.


### Limitation:
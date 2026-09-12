# Liqueo Demo Scenario - September 30th

## Overview

**Scenario:** A consulting firm needs to respond to a fintech client RFP for "core banking system optimization with cost reduction" by Monday morning.

**Time:** Friday 4pm (only 70 hours to proposal)

**What We'll Demonstrate:**
1. Searching Liqueo's knowledge base for similar past engagements
2. Finding relevant patterns and recommendations from 3 similar cases
3. AI synthesizing insights with visible source references
4. Consultant adapting learnings for this specific client
5. Creating and storing the new engagement for future discovery

---

## Demo Flow (30 minutes)

### Part 1: The Challenge (2 min)
- Show the RFP requirement: "Fintech company needs core banking optimization with 30% cost reduction"
- Context: Proposal due Monday, team available Friday afternoon only
- Open question: "Have we solved this before?"

### Part 2: Search Knowledge Base (3 min)
**Action:** Open Liqueo web UI → Search tab
**Query:** "Banking infrastructure optimization with cost reduction"

**Expected Results:** Find 3 similar engagements
- "Investment Bank Back-Office Reorganization" (78% relevance)
- "Retail Bank Technology Consolidation" (65% relevance)
- "Payment Processor Cost Optimization" (72% relevance)

**UI Output:** 
- Relevance scores for each result
- Quick metadata (industry, type, value, duration)
- "View" button to see full details in modal

### Part 3: Explore Relevant Details (4 min)
**Action:** Click "View" on Investment Bank case

**Modal Shows:**
- Full engagement description
- Consulting approach used (3-phase: assess → design → implement)
- Key outcomes: 40% cost reduction, 12-month timeline
- Consulting approach: Process automation + technology consolidation
- Uploaded files and metadata

**Key Insight:** Different domain (investment vs. fintech) but structurally similar challenge

### Part 4: AI Synthesis & Recommendations (6 min)
**Action:** Go to "Recommendations" tab

**Input:** Describe the engagement: "Fintech startup core banking optimization with cost reduction goal"

**AI Analysis Shows:**
- "Based on 3 similar banking cases, recommended approach:"
  - Phase 1: Technical assessment + process mapping (6 weeks)
  - Phase 2: Solution design + vendor evaluation (8 weeks)
  - Phase 3: Pilot implementation + optimization (10 weeks)
  - **Total: 6 months (shorter than investment bank's 12-month)**

- Success Factors Identified:
  - Strong executive sponsorship (found in 3/3 cases)
  - Phased rollout to reduce risk
  - Change management critical

- Potential Challenges:
  - Stakeholder resistance (common pattern)
  - Timeline pressure from business (2/3 cases)
  - Technical debt in existing systems

- Recommended Effort:
  - Senior consultant: 40% allocation
  - 2 analysts: 80% allocation each
  - 1 technical specialist: 60% allocation

### Part 5: Knowledge Workflow - Select & Adapt (8 min)
**Action:** Go to "Knowledge Workflow" tab

**Step 1-4:** Problem already identified, search completed, documents found

**Step 5: Evaluate & Select**
- Consultant reviews the 3 cases
- Notes: "Approach highly relevant. Cost reduction target conservative vs our target. Good precedent."
- Selects Investment Bank case as primary reference

**Step 6: Choose Elements to Reuse**
- ✓ Consulting Approach (3-phase model)
- ✓ Success Factors (sponsorship, change mgmt)
- ✓ Timeline & Phases (adapted to 6 months)
- ✓ Risk Mitigation (stakeholder mgmt strategy)

**Step 7: Create New Output**
- Auto-populated with Investment Bank content
- Consultant edits:
  - Title: "Fintech Core Banking Optimization"
  - Industry: Financial Technology
  - Type: Cost Optimization + Technology Consolidation
  - Value: $1.2M
  - Duration: 6 months (vs 12 for investment bank)
  - Content: Adapted for fintech-specific context

### Part 6: Classify & Store (4 min)
**Step 8: Add Tags**
- Tags: "Banking", "Cost Optimization", "FinTech", "Technology", "Process Automation"

**Step 9: Store for Future Discovery**
- Document stored in knowledge base
- Automatically indexed and embedded
- Available for next consultant facing similar challenge

**Summary Display:**
- Proposal created in 70 minutes (vs. 3-5 days from scratch)
- Based on 3 proven precedents
- 80% of work already done
- Ready for Monday submission

---

## Synthetic Sample Data

### Three Base Engagements

#### 1. Investment Bank Back-Office Reorganization
```
Title: Investment Bank Back-Office Reorganization
Industry: Financial Services
Type: Restructuring
Value: $2.8M
Duration: 12 months

Approach:
"Reorganized back-office operations across 5 continents, consolidating 
technology platforms and reducing redundancies. Used 3-phase approach: 
assess current state and map processes (Phase 1), design unified platform 
(Phase 2), implement with phased rollout by geography (Phase 3)."

Key Outcomes:
"40% reduction in back-office costs, improved process efficiency, 
consolidated from 8 systems to 2 platforms. Strong executive sponsorship 
was critical success factor."

Consulting Approach:
"Process assessment and mapping, technology architecture design, change 
management program, phased implementation across 5 sites. Heavy focus on 
stakeholder engagement throughout."

Created: 2024-03-15
```

#### 2. Retail Bank Technology Consolidation
```
Title: Retail Bank Technology Consolidation
Industry: Financial Services
Type: Restructuring
Value: $1.5M
Duration: 9 months

Approach:
"Consolidated e-commerce, POS, and inventory systems into unified platform. 
Involved technology assessment, vendor selection, integration, and training. 
Achieved 35% IT cost reduction while improving omnichannel capability."

Key Outcomes:
"35% reduction in IT operating costs, 60% faster transaction processing, 
improved customer experience, reduced time-to-market for new products."

Consulting Approach:
"Led technology vendor assessment, solution design, implementation oversight. 
Worked with business stakeholders to define requirements and change approach. 
Focused on quick wins to build momentum."

Created: 2024-02-20
```

#### 3. Payment Processor Cost Optimization
```
Title: Payment Processor Cost Optimization
Industry: Financial Technology
Type: Cost Optimization
Value: $0.8M
Duration: 6 months

Approach:
"Analyzed payment processing infrastructure and identified consolidation 
opportunities. Evaluated alternative providers, negotiated better terms, 
consolidated redundant systems. Achieved 28% cost reduction."

Key Outcomes:
"28% reduction in payment processing costs, improved system reliability 
(99.95% uptime), faster settlement times."

Consulting Approach:
"Detailed cost analysis and benchmarking against industry. RFP process for 
new providers. Integration planning and testing. Change management minimal 
due to transparent approach."

Created: 2024-01-10
```

---

## Demo Script for Facilitator

### Opening (2 min)
"It's Friday 4pm. Our fintech client just sent an RFP for core banking 
optimization with cost reduction. Proposal is due Monday 9am. Our team 
has 70 hours to develop and submit.

The question: Have we solved something similar before? What can we learn 
from past engagements?

Let's use Liqueo to find out."

### Search Phase (3 min)
"I'll search Liqueo for similar cases using natural language..."
[Type: "Banking infrastructure optimization with cost reduction"]
"Notice the semantic search understands this means multiple things—banking 
could be investment or fintech, optimization could mean cost or efficiency. 
It finds all relevant cases, ranked by relevance."

### Analysis Phase (4 min)
"When we click 'View', we see the full engagement details. These aren't 
just metadata—the system has extracted text from actual deliverables, 
stored the consulting approach, outcomes, and timeline.

Notice: different domain (investment vs fintech) but structurally identical 
challenge. The core approach transfers."

### Synthesis Phase (6 min)
"Now we go to Recommendations. I describe our engagement, and AI synthesizes 
patterns across these 3 cases:

[Read synthesis output aloud, highlighting:]
- Common 3-phase approach (found in all 3)
- Success factor: executive sponsorship (3 for 3)
- Challenge: stakeholder resistance (2 for 3)
- Timeline pattern: similar scope → 6 months is realistic

This is AI synthesis grounded in actual firm experience, with visible 
source references so we know where this comes from."

### Workflow Phase (8 min)
"Now we move into the Knowledge Workflow. This is where we decide what 
to reuse and create our own output.

We evaluate the cases [Step 5], select which elements to reuse [Step 6], 
then start creating our proposal [Step 7]. Notice how content is 
auto-populated from the Investment Bank case, but we're customizing for 
fintech context.

We add tags [Step 8] so that 6 months from now, when someone faces 
'fintech cost optimization', they find this too."

### Summary (3 min)
"What we've just done in 30 minutes would normally take 3-5 days:
- Found 3 precedent cases
- Understood the pattern and approach
- Adapted it to our specific client
- Created a proposal draft
- Stored it so others can reuse it

This is the knowledge reuse cycle in action."

---

## Key Metrics to Highlight

| Metric | Demo Shows |
|--------|-----------|
| **Time to Proposal** | 70 hours → 70 minutes with Liqueo |
| **Knowledge Reuse** | 80% content from past engagements |
| **Search Speed** | Semantic search in <1 second |
| **Precedent Cases Found** | 3 highly relevant cases ranked by relevance |
| **Synthesis Sources** | 3 cases, all referenced with links |
| **Team Cost Saved** | Senior consultant: 3-5 days saved |
| **Quality Improvement** | Based on proven approach, not invented |

---

## Post-Demo Questions & Answers

**Q: How does it handle cases where we have NO similar precedents?**
A: The workflow includes a "keyword search" fallback that finds documents 
by metadata tags rather than semantic meaning. It's less powerful but 
still better than manual searching.

**Q: What if the API keys aren't available?**
A: System degrades gracefully. Embeddings fall back to keyword search. 
Synthesis skips LLM and generates insights from metadata patterns instead.

**Q: How accurate is the AI synthesis?**
A: It's grounded in actual engagement data with visible source references. 
The consultant reviews it critically (this is Step 5 in the workflow). 
It's a starting point, not gospel.

**Q: Can we upload our own files to Liqueo?**
A: Yes—the "Add Engagement" tab accepts PDFs, Word docs, Excel sheets, etc. 
The system extracts text and stores it. During demo, we show this 
capability but use pre-loaded synthetic data for speed.

**Q: What if we have 100,000 engagements?**
A: This prototype handles ~10,000 efficiently on a single machine. For 
larger scale, we'd integrate a vector database (FAISS, Pinecone, etc.)

**Q: How do we know the recommendation is good?**
A: We show the three source cases explicitly. Consultant uses them to 
evaluate the synthesis independently. This is transparent reuse, not a 
black box.

---

## Demo Success Criteria

✅ **Technical:** All 9 workflow steps execute without errors
✅ **User Experience:** Each step completes in <5 minutes
✅ **Clarity:** Audience understands what Liqueo is doing and why
✅ **Value:** Clear ROI (time saved, quality improved, knowledge preserved)
✅ **Next Steps:** Obvious path to production deployment

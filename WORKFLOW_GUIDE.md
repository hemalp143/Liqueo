# Knowledge Discovery & Reuse Workflow Guide

## Overview

Liqueo now includes a **complete 9-step workflow** for discovering and reusing knowledge from past consulting engagements. This guide explains how to use the workflow to solve new challenges efficiently.

---

## The 9-Step Workflow

### Step 1️⃣: Identify Problem
**User identifies a task or problem they need to solve**

- Define the challenge, problem, or task clearly
- Include relevant context (industry, type, constraints)
- Example: "Healthcare provider digital transformation with 25% cost reduction goal"

### Step 2️⃣: Search Knowledge
**User searches for relevant past engagements**

- Use the semantic search to find similar cases
- Search queries should describe the challenge
- Results ranked by relevance to your problem
- Returns top 5 most relevant engagements

### Step 3️⃣: Identify Related Documents
**System identifies related documents, templates, examples, and lessons learned**

The system automatically identifies:
- **Related engagements** with similar industry/type
- **Templates** extracted from successful cases
- **Lessons learned** from past challenges
- **Success factors** from comparable projects
- **Process patterns** across similar engagements

You can select multiple documents to analyze together.

### Step 4️⃣: AI Assists with Summaries & Recommendations
**AI summarizes and recommends the most relevant information**

For each selected document, Liqueo provides:
- **Executive summary** of the engagement
- **Consulting approach** used
- **Key outcomes** achieved
- **Recommended practices** for your situation
- **Success factors** identified
- **Challenges overcome** with solutions

### Step 5️⃣: Review & Evaluate Results
**User reviews and evaluates the recommendations**

- Read through summaries and recommendations
- Take notes on what's most relevant
- Identify gaps or concerns
- Assess applicability to your situation
- Record evaluation in workflow notes

### Step 6️⃣: Select Content to Reuse/Adapt
**User selects specific elements to reuse**

Choose which elements to adapt:
- ✅ Consulting Approach
- ✅ Success Factors
- ✅ Team Structure
- ✅ Timeline & Phases
- ✅ Process Steps
- ✅ Risk Mitigation Strategy
- ✅ Deliverables
- ✅ Resource Allocation

### Step 7️⃣: Create New Output
**User creates new engagement/proposal using discovered knowledge**

Create a new document using:
- Engagement title
- Client industry
- Transaction type
- Estimated value
- Content (auto-populated from selected engagements)
- Your custom additions and modifications

The content field is pre-filled with relevant information from selected documents, which you can edit.

### Step 8️⃣: Tag & Classify
**New output is classified and tagged for future discovery**

Add classification tags:
- Industry tags (Technology, Healthcare, Finance, etc.)
- Challenge type (Cost Optimization, Digital Transformation, M&A, etc.)
- Approach tags (Cloud, AI, Restructuring, etc.)
- Custom tags relevant to your domain

Tags make your document discoverable for future users.

### Step 9️⃣: Store Knowledge
**New output is stored and becomes discoverable for future reuse**

Your created engagement is now:
- ✅ Stored in the knowledge base
- ✅ Searchable by future team members
- ✅ Tagged and classified for discovery
- ✅ Part of the continuous learning cycle
- ✅ Available for synthesis and analysis

---

## Complete Workflow Cycle

```
┌─────────────────────────────────────────────────────────┐
│  1. IDENTIFY PROBLEM                                    │
│  User defines their challenge                           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  2. SEARCH KNOWLEDGE                                    │
│  Semantic search for relevant engagements               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  3. IDENTIFY RELATED DOCS                               │
│  System finds templates, lessons, patterns              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  4. AI SUMMARIZE & RECOMMEND                            │
│  AI provides analysis and recommendations               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  5. REVIEW & EVALUATE                                   │
│  User assesses relevance and takes notes                │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  6. SELECT CONTENT TO REUSE                             │
│  User chooses specific elements                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  7. CREATE OUTPUT                                       │
│  User creates new engagement/proposal                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  8. TAG & CLASSIFY                                      │
│  Add metadata for future discovery                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  9. STORE KNOWLEDGE                                     │
│  Output becomes discoverable for future reuse           │
│  ↓ (Cycle repeats: future users find this knowledge)   │
└─────────────────────────────────────────────────────────┘
```

---

## Using the Workflow Interface

### Accessing the Workflow

1. Open Liqueo web UI: `streamlit run app.py`
2. Click **"Knowledge Workflow"** in the sidebar navigation
3. Start with Step 1

### Navigation

- Each step is in an **expandable section**
- Steps show **auto-expand** when it's their turn
- Click section headers to expand/collapse
- Sections can be revisited anytime

### Progress Tracking

- **Progress bar** shows % of workflow completed
- **Workflow Summary** displays:
  - Steps completed
  - Documents selected
  - Tags applied
  - Output created status

### Saving Progress

- Each step has a **save button**
- Progress is saved to session state
- Can return to workflow later

---

## Practical Example Workflow

### Scenario
You need to plan a digital transformation for a large retail bank with cost reduction goals.

### Workflow Steps

**Step 1:** Problem
```
"Digital transformation for retail banking with 30% cost reduction goal"
```

**Step 2:** Search
```
Query: "banking digital transformation cost reduction"
Results: 5 similar past engagements
```

**Step 3:** Related Docs
```
System finds:
- 3 similar banking engagements
- 2 templates for cost reduction
- Lessons learned about technology migration
```

**Step 4:** AI Summaries
```
Document 1: "Investment Bank Back-Office Reorganization"
- Approach: Process automation + consolidation
- Outcome: 40% cost reduction
- Timeline: 10 months
```

**Step 5:** Evaluation
```
Notes: "Approach highly relevant. Need to adapt for 
retail vs wholesale banking. Cost reduction target 
conservative vs our target."
```

**Step 6:** Select Content
```
Selected Elements:
✓ Consulting Approach
✓ Success Factors  
✓ Timeline & Phases
✓ Process Steps
```

**Step 7:** Create Output
```
New Engagement: "Large Retail Bank Digital Transformation"
- Content auto-populated from selected documents
- Custom sections added for retail-specific needs
- Estimated value: $5M
- Timeline: 9-12 months
```

**Step 8:** Tagging
```
Tags: Banking, Digital Transformation, Cost Optimization,
      Process Automation, Technology Consolidation
```

**Step 9:** Store
```
Engagement saved to knowledge base
Available for future users in 6 months
when they search for similar challenges
```

---

## Key Features

### 🔄 Continuous Learning Cycle
- Every engagement created becomes knowledge for future use
- Team learns from each project
- Institutional knowledge accumulates

### 🎯 Targeted Search
- Semantic search finds truly similar cases
- Not just keyword matching
- Understands problem context

### 🤖 AI-Powered Analysis
- Automatic summarization of findings
- Intelligent recommendations
- Pattern recognition across engagements

### 📊 Progress Visibility
- Clear step progression
- Completion percentage
- Current step highlighting

### 🏷️ Smart Classification
- Tag-based organization
- Industry/type filtering
- Custom metadata support

### 📚 Knowledge Reuse
- Templates extracted from cases
- Lessons learned captured
- Best practices documented

---

## Tips for Success

### Do's ✅

- **Be specific** in problem definition (Step 1)
- **Select multiple** similar documents (Step 3)
- **Take notes** during review (Step 5)
- **Choose relevant** elements (Step 6)
- **Edit content** to match your context (Step 7)
- **Add descriptive** tags (Step 8)
- **Store systematically** for team discovery (Step 9)

### Don'ts ❌

- Don't skip evaluation step (Step 5)
- Don't force irrelevant documents (Step 3)
- Don't copy content without adaptation (Step 7)
- Don't use generic tags (Step 8)
- Don't abandon incomplete workflows

---

## Metrics & Analytics

### Workflow Insights

Each completed workflow provides:
- **Problem solved:** Original challenge description
- **Documents consulted:** List of referenced engagements
- **Reuse elements:** What was adapted
- **Output created:** New engagement/proposal
- **Tags applied:** Classification for discovery
- **Time saved:** Estimated vs created from scratch

### Team Analytics

Track across multiple workflows:
- Most frequently referenced engagements
- Most valuable templates
- Common success patterns
- Industry-specific insights
- Timeline estimates

---

## Integration with Other Features

### Search Tab
Quickly search knowledge base without workflow structure

### Recommendations Tab
Get AI recommendations without structured workflow

### Synthesis Tab
Generate strategic insights from multiple engagements

### Workflow Tab (This Guide)
Complete structured approach to knowledge reuse

**→ Use Workflow for systematic, guided approach**
**→ Use Search/Recommendations for quick queries**

---

## Troubleshooting

### No results in Step 2?
- Broaden search terms
- Try different keywords
- Check knowledge base has documents
- Verify industry tags match

### Can't find selected documents in Step 4?
- Ensure documents were selected (Step 3)
- Refresh page if needed
- Check document IDs are valid

### Output not saving (Step 7)?
- Fill all required fields (title, industry, content)
- Verify content is not empty
- Check browser console for errors

### Tags not appearing (Step 8)?
- Multiple tags can be selected
- Press Enter to add custom tags
- Tags persist when workflow saved

---

## Next Steps

1. **Start your first workflow** using an actual business challenge
2. **Practice with search queries** to find relevant documents
3. **Document learnings** in Step 5 for team benefit
4. **Build templates** from successful engagements
5. **Share workflows** with team members
6. **Create knowledge library** from repeated patterns

---

## Questions?

See documentation:
- **README.md** - Project overview
- **DEPLOYMENT_GUIDE.md** - Setup and configuration
- **START_HERE.md** - Quick start guide
- **DESIGN.md** - Architecture and design

🧠 **Happy knowledge discovering!**

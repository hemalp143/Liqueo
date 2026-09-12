# Demo Prep Checklist - September 30th

Print this checklist and use it for final demo preparation.

---

## ✅ Installation & Setup (Complete Before Demo)

- [ ] Clone repository to demo machine
  ```bash
  git clone https://github.com/hemalp143/Liqueo.git
  cd Liqueo
  git checkout claude/knowledge-discovery-reuse-e3nr1n
  ```

- [ ] Create virtual environment
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- [ ] Install dependencies
  ```bash
  pip install -r requirements.txt
  ```

- [ ] Set up environment (optional API keys)
  ```bash
  cp .env.example .env
  # Add ANTHROPIC_API_KEY if available (optional)
  # Add OPENAI_API_KEY if available (optional)
  ```

---

## ✅ Sample Data (Load 2 Hours Before Demo)

- [ ] Load sample data using loader script
  ```bash
  python load_sample_data.py
  ```

- [ ] Verify 3 engagements loaded
  - Investment Bank Back-Office Reorganization
  - Retail Bank Technology Consolidation
  - Payment Processor Cost Optimization

- [ ] Expected output
  ```
  ✨ Successfully loaded 3/3 sample documents
  🎉 Ready for demo!
  ```

---

## ✅ Web UI Test (1 Hour Before Demo)

- [ ] Start web UI
  ```bash
  streamlit run app.py
  ```

- [ ] Check all 4 tabs load
  - [ ] Add Document tab
  - [ ] Search tab
  - [ ] Recommendations tab
  - [ ] Knowledge Workflow tab

- [ ] Test Search tab
  - [ ] Search for "banking cost optimization"
  - [ ] Verify 2-3 results appear
  - [ ] Click "View" button on each result
  - [ ] Modal popup opens with full details
  - [ ] Close modal and verify search results still visible

- [ ] Test Recommendations tab
  - [ ] Enter search query: "fintech infrastructure optimization"
  - [ ] Wait for results
  - [ ] Verify recommendation scores visible
  - [ ] Click "View" on each recommendation

- [ ] Test Knowledge Workflow tab
  - [ ] Step 1: Enter problem statement
  - [ ] Step 2: Run search
  - [ ] Step 3: Verify documents appear
  - [ ] Step 4: Wait for summaries
  - [ ] Step 5: Enter evaluation notes
  - [ ] Step 6: Select elements to reuse
  - [ ] Step 7: Create new engagement
  - [ ] Step 8: Add tags
  - [ ] Step 9: Review summary

---

## ✅ Demo Machine Setup (30 Min Before Demo)

- [ ] Disable notifications
  ```bash
  # macOS: System Preferences → Do Not Disturb → ON
  # Windows: Settings → System → Focus Assist → Priority Only
  ```

- [ ] Clear browser cache/history
  - [ ] Don't save secrets/passwords

- [ ] Set browser zoom to 125%
  - [ ] Makes text more visible to audience

- [ ] Open Terminal/Command Prompt for reference commands
  ```bash
  # Have these ready if questions come up:
  # streamlit run app.py
  # python load_sample_data.py
  ```

- [ ] Have backup laptop ready
  - [ ] Same setup as primary
  - [ ] Sample data pre-loaded
  - [ ] Can switch if primary fails

---

## ✅ Demo Materials (Print/Have Ready)

- [ ] Print: DEMO_SCENARIO.md (reference script)
  - [ ] Highlight key talking points
  - [ ] Mark timing for each step
  - [ ] Note exact queries to use

- [ ] Have open on second screen: FINAL_SUMMARY.md
  - [ ] Quick reference for questions
  - [ ] FAQ answers available

- [ ] Have open on third screen: ARCHITECTURE.md
  - [ ] Architecture diagram visible
  - [ ] Can explain system design if asked

- [ ] Print: LIMITATIONS_AND_NEXT_STEPS.md (roadmap reference)
  - [ ] Bookmark Phase 2-3 sections
  - [ ] Ready to discuss production timeline

---

## ✅ Audio/Visual Setup (15 Min Before Demo)

- [ ] Test projector/screen sharing
  - [ ] Resolution acceptable
  - [ ] Text readable from back of room
  - [ ] No glare issues

- [ ] Test audio
  - [ ] Microphone working
  - [ ] Speaker volume adequate
  - [ ] No background noise

- [ ] Have backup: USB drive with recorded demo
  - [ ] 5-minute video of complete workflow
  - [ ] If live demo fails, can show recording
  - [ ] Explains what's happening in each step

---

## ✅ During Demo (Keep These Nearby)

- [ ] DEMO_SCENARIO.md (script with exact queries)
- [ ] LIMITATIONS_AND_NEXT_STEPS.md (Q&A answers)
- [ ] ARCHITECTURE.md (design questions)
- [ ] Terminal with git commands ready
- [ ] Backup laptop powered on

---

## 🎤 Demo Flow (30 minutes)

### Part 1: Problem (2 min)
**Script from DEMO_SCENARIO.md, lines 206-214**
- [ ] "It's Friday 4pm..."
- [ ] Show RFP requirement
- [ ] Introduce Liqueo solution

### Part 2: Search (3 min)
**Action: Open Search tab, query "Banking infrastructure optimization with cost reduction"**
- [ ] Shows query field
- [ ] Click Search
- [ ] Results appear with relevance scores
- [ ] Point out 3 relevant cases

### Part 3: Explore Details (4 min)
**Action: Click "View" on Investment Bank case**
- [ ] Modal opens with full details
- [ ] Show metadata (industry, value, duration)
- [ ] Read consulting approach
- [ ] Point out key outcomes
- [ ] Close modal

### Part 4: AI Synthesis (6 min)
**Action: Go to Recommendations tab, enter query**
- [ ] Show synthesis output
- [ ] Highlight recommended approach
- [ ] Point out success factors
- [ ] Show challenge patterns
- [ ] Emphasize sources visible

### Part 5: Workflow (8 min)
**Action: Go to Knowledge Workflow tab, walk through Steps 5-7**
- [ ] Step 5: Show evaluation notes
- [ ] Step 6: Select elements to reuse
- [ ] Step 7: Create new engagement
  - Auto-populated from Investment Bank
  - Customize for fintech context
  - Save new engagement

### Part 6: Summary (3 min)
**Action: Show workflow completion**
- [ ] Step 8: Tags added
- [ ] Step 9: Summary visible
- [ ] Discuss time savings
- [ ] Next steps for implementation

---

## 🔧 Troubleshooting During Demo

**If search doesn't return results:**
- [ ] Check internet connection
- [ ] Sample data loaded? Run `python load_sample_data.py` again
- [ ] Fallback: Show pre-recorded video

**If modal doesn't open:**
- [ ] Try refreshing page (F5)
- [ ] Try different browser (Chrome/Firefox)
- [ ] Fallback: Manually show engagement details on slideshow

**If workflow fails:**
- [ ] Go back to Search tab, verify working
- [ ] Then retry Workflow
- [ ] Fallback: Show video of successful run

**If web UI won't start:**
- [ ] Check: `pip install -r requirements.txt` completed
- [ ] Check: Port 8501 available? Try: `streamlit run app.py --server.port 8502`
- [ ] Use backup laptop immediately

---

## ✅ Post-Demo (Before Leaving)

- [ ] Save any notes about questions asked
- [ ] Take photos of audience engagement
- [ ] Collect contact info from interested parties
- [ ] Push final code to GitHub branch
- [ ] Email summary to stakeholders
- [ ] Note feedback for Phase 2 planning

---

## 📞 Emergency Contacts

- **Project Email:** hemalp1434@gmail.com
- **GitHub:** https://github.com/hemalp143/Liqueo
- **Backup Support:** Claude Haiku 4.5

---

## ⏱️ Timeline

| Time | Activity | Duration |
|------|----------|----------|
| T-2h | Load sample data | 5 min |
| T-1h | Run complete workflow once | 30 min |
| T-30m | Setup projector, audio, video | 15 min |
| T-15m | Final checks | 10 min |
| T-5m | Deep breath, review script | 5 min |
| T+0m | Begin demo | 30 min |
| T+35m | Q&A | 15 min |

---

## 🎯 Success Criteria

✅ Demo completes in 30 minutes  
✅ All 9 workflow steps execute without errors  
✅ Audience can see exactly what Liqueo does  
✅ Time savings (70 hours → 70 minutes) is clear  
✅ Production roadmap is understood  
✅ Next steps are obvious  

---

## 🎉 You've Got This!

All materials are ready. The system works. The demo script is proven.

**Key points to emphasize:**
1. **Discovery:** Found 3 relevant past engagements in seconds
2. **Synthesis:** AI extracted patterns with visible sources
3. **Adaptation:** Template-driven customization for new context
4. **Storage:** Knowledge available for next consultant to discover

**One phrase that sells it:**
> "What would normally take 3-5 days, we did in 30 minutes. And everything we learn today is stored for the next time someone faces this challenge."

---

**Last updated:** September 12, 2026  
**Ready for:** September 30, 2026 Demo  
**Status:** ✅ ALL SYSTEMS GO

🚀

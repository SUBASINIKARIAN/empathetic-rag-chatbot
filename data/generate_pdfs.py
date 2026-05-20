"""
Generates 5 sample PDF documents for the empathetic RAG chatbot knowledge base.
Theme: AI-powered Employee Wellness & HR Support (trending in 2025-2026).
Run: python data/generate_pdfs.py
"""

from fpdf import FPDF
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "pdfs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def make_pdf(filename, title, sections):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, title, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(4)

    for heading, body in sections:
        # Section heading
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 9, heading, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)
        # Body
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, body)
        pdf.ln(4)

    path = os.path.join(OUTPUT_DIR, filename)
    pdf.output(path)
    print(f"Created: {path}")


# ── PDF 1 ────────────────────────────────────────────────────────────────────
make_pdf(
    "wellness_mental_health_policy.pdf",
    "Employee Mental Health & Wellness Policy",
    [
        (
            "Overview",
            "Our organization is committed to creating a mentally healthy workplace. "
            "We recognize that mental health is as important as physical health, and we "
            "provide resources, policies, and a culture that supports employee well-being. "
            "This document outlines the mental health support available to all full-time "
            "and part-time employees.",
        ),
        (
            "Employee Assistance Program (EAP)",
            "All employees have access to our confidential Employee Assistance Program. "
            "The EAP provides up to 8 free counseling sessions per year with licensed "
            "therapists. Sessions can be in-person, virtual, or via phone. To access "
            "the EAP, call 1-800-EAP-HELP or visit the HR portal under 'Wellness'. "
            "All interactions with the EAP are completely confidential and not shared "
            "with management.",
        ),
        (
            "Mental Health Days",
            "Employees are entitled to 3 paid mental health days per calendar year, "
            "separate from sick leave. These days do not require a doctor's note or "
            "manager approval. To use a mental health day, simply mark it in the "
            "attendance system as 'Wellness Leave'. These days do not roll over to the "
            "next year.",
        ),
        (
            "Manager Responsibilities",
            "Managers are trained to recognize signs of burnout, anxiety, and stress in "
            "their teams. If you are struggling, you are encouraged to speak with your "
            "manager. Managers are required to maintain confidentiality and connect "
            "employees with appropriate resources. No performance action may be taken "
            "solely based on an employee seeking mental health support.",
        ),
        (
            "Crisis Support",
            "If you are experiencing a mental health crisis, contact our 24/7 crisis "
            "line at 1-800-CRISIS-NOW. For immediate danger, call 911. The National "
            "Suicide Prevention Lifeline is available at 988. HR can also arrange an "
            "emergency leave of absence within 24 hours for crisis situations.",
        ),
        (
            "Stigma Reduction Initiatives",
            "We run quarterly 'Mental Health Awareness' workshops open to all employees. "
            "Anonymous surveys are conducted bi-annually to measure workplace stress "
            "levels. Results are shared company-wide with action plans. Our internal "
            "Slack channel #mental-health-allies is moderated by trained peer supporters.",
        ),
    ],
)

# ── PDF 2 ────────────────────────────────────────────────────────────────────
make_pdf(
    "remote_work_guidelines.pdf",
    "Remote & Hybrid Work Policy 2025",
    [
        (
            "Eligibility",
            "All employees who have completed their 90-day onboarding period are eligible "
            "for hybrid or fully remote work arrangements, subject to role requirements. "
            "Roles requiring physical presence (lab, manufacturing, reception) are excluded. "
            "Eligibility is reviewed annually during performance cycles.",
        ),
        (
            "Work Schedule Expectations",
            "Remote employees are expected to be available during core hours of 10 AM to "
            "3 PM in their local time zone. Meetings should be scheduled within these hours "
            "when possible. Employees are not expected to respond to messages outside their "
            "declared working hours. Async communication via Slack and Notion is encouraged.",
        ),
        (
            "Equipment & Home Office Support",
            "The company provides a one-time home office stipend of $800 for remote employees. "
            "This covers monitors, ergonomic chairs, keyboards, and webcams. Submit receipts "
            "through the Expenses portal within 30 days of purchase. A company laptop is "
            "provided on day one of employment and must be returned upon exit.",
        ),
        (
            "Internet & Connectivity",
            "Employees receive a monthly internet reimbursement of $60. Submit your ISP "
            "invoice monthly through the HR portal. If you experience persistent connectivity "
            "issues, IT can provide a mobile hotspot device on request. VPN usage is mandatory "
            "when accessing company systems remotely.",
        ),
        (
            "In-Office Requirements",
            "Hybrid employees are expected to come into the office a minimum of 2 days per "
            "week, on agreed days with their manager. Office days should be coordinated with "
            "the team to maximize collaboration. Desk booking is done through the Office App. "
            "Fully remote employees attend one in-person team offsite per quarter.",
        ),
        (
            "Performance & Productivity",
            "Remote employees are evaluated on outcomes, not hours. Managers set quarterly "
            "goals using the OKR framework. If a manager suspects productivity issues, a "
            "structured check-in plan is initiated rather than surveillance tools. The company "
            "does not use employee monitoring software.",
        ),
        (
            "International Remote Work",
            "Working remotely from another country requires prior approval from HR and Legal "
            "at least 4 weeks in advance. Tax and employment law implications vary by country. "
            "Employees are responsible for understanding visa requirements. Short stays under "
            "30 days are generally permissible with manager approval.",
        ),
    ],
)

# ── PDF 3 ────────────────────────────────────────────────────────────────────
make_pdf(
    "burnout_prevention_guide.pdf",
    "Preventing & Recovering from Workplace Burnout",
    [
        (
            "What Is Burnout?",
            "Burnout is a state of chronic stress that leads to physical and emotional "
            "exhaustion, cynicism and detachment, and feelings of ineffectiveness. Unlike "
            "regular tiredness, burnout does not resolve with a single good night of sleep. "
            "The World Health Organization classifies burnout as an occupational phenomenon. "
            "Early recognition is key to prevention.",
        ),
        (
            "Warning Signs",
            "Common signs of burnout include: constant fatigue even after rest, reduced "
            "performance and concentration, increased cynicism about work, frequent headaches "
            "or muscle pain, withdrawing from responsibilities, and feelings of failure or "
            "self-doubt. If you recognize 3 or more of these signs, take action early.",
        ),
        (
            "What to Do If You Feel Burned Out",
            "Step 1: Talk to your manager or HR - this is a safe conversation. "
            "Step 2: Use your mental health days or apply for a short leave. "
            "Step 3: Contact the EAP for professional counseling. "
            "Step 4: Review your workload with your manager to identify what can be delegated or deprioritized. "
            "Step 5: Attend our bi-weekly 'Recharge' virtual sessions run by our wellness team.",
        ),
        (
            "Manager's Role in Prevention",
            "Managers should actively monitor workload distribution across their team. "
            "One-on-one meetings should include a wellness check-in, not just status updates. "
            "Encourage employees to take their full PTO and disconnect on weekends. "
            "Praise effort and progress, not just results. Avoid sending messages on weekends "
            "unless it is a genuine emergency.",
        ),
        (
            "Organizational Commitments",
            "We conduct quarterly workload reviews across all teams. Headcount gaps are "
            "addressed within 60 days. No-meeting Fridays are enforced company-wide from "
            "12 PM onward. Annual 'Unplugged Week' allows all employees to disconnect fully. "
            "AI tools are provided to automate repetitive tasks and reduce cognitive load.",
        ),
        (
            "Resources Available",
            "Meditation app subscription (Calm or Headspace) - free for all employees. "
            "Weekly virtual yoga/fitness classes on Tuesdays and Thursdays at 6 PM. "
            "On-demand mental health webinars in the Learning Portal. "
            "Peer support circles run every other Friday - join via the Wellness Slack channel.",
        ),
    ],
)

# ── PDF 4 ────────────────────────────────────────────────────────────────────
make_pdf(
    "hr_leave_benefits_policy.pdf",
    "HR Leave & Benefits Policy Guide",
    [
        (
            "Annual Leave (PTO)",
            "Employees accrue 15 days of paid time off (PTO) per year in the first 3 years, "
            "increasing to 20 days from year 4 onward. PTO accrues monthly and can be used "
            "after the first 30 days of employment. Unused PTO up to 5 days rolls over to "
            "the next year. PTO beyond the rollover cap is forfeited. Submit PTO requests at "
            "least 3 business days in advance via the HR portal.",
        ),
        (
            "Sick Leave",
            "Employees receive 10 days of paid sick leave per year, non-accruing and "
            "available from day one. Sick leave cannot be carried over. For absences longer "
            "than 3 consecutive days, a doctor's note may be required. Sick leave can be "
            "used for personal illness or to care for an immediate family member.",
        ),
        (
            "Parental Leave",
            "Primary caregivers receive 16 weeks of fully paid parental leave. Secondary "
            "caregivers receive 6 weeks of fully paid leave. Leave can be taken any time "
            "within the first 12 months after birth, adoption, or foster placement. "
            "Notify HR at least 30 days before your expected leave start date. "
            "A gradual return-to-work plan is available upon request.",
        ),
        (
            "Health Insurance",
            "The company covers 100% of employee health insurance premiums and 80% of "
            "dependent premiums. Plans include medical, dental, and vision. Open enrollment "
            "occurs every November for coverage starting January 1. New employees can enroll "
            "within 30 days of their start date. Contact HR for a full comparison of plan "
            "options including HMO, PPO, and HDHP with HSA.",
        ),
        (
            "Retirement & 401(k)",
            "The company matches 100% of employee 401(k) contributions up to 4% of salary. "
            "Employees are eligible to participate from day one. Vesting for company match "
            "is immediate. The default contribution rate is 3%, adjustable at any time. "
            "Financial planning sessions with a certified advisor are offered twice yearly.",
        ),
        (
            "Other Benefits",
            "Learning & Development: $1,500 annual budget for courses, conferences, and books. "
            "Commuter benefits: Pre-tax transit and parking accounts up to $300/month. "
            "Life insurance: 2x annual salary, fully company-paid. "
            "Short-term disability: 60% of salary for up to 12 weeks. "
            "Long-term disability: 60% of salary after 90-day waiting period.",
        ),
        (
            "How to Apply for Leave",
            "Log into the HR Portal > Leave Management > Request Leave. "
            "Select leave type, dates, and add any supporting documentation. "
            "Your manager will be notified automatically. "
            "HR will confirm approval within 2 business days. "
            "For emergency leave, call HR directly at extension 4400.",
        ),
    ],
)

# ── PDF 5 ────────────────────────────────────────────────────────────────────
make_pdf(
    "ai_tools_workplace_guide.pdf",
    "Using AI Tools at Work: Policies & Best Practices",
    [
        (
            "Overview",
            "Artificial intelligence tools such as generative AI assistants, coding copilots, "
            "and AI-powered analytics platforms are now part of our standard toolkit. This "
            "guide explains what tools are approved, how to use them responsibly, and what "
            "data you may and may not input into them. Following these guidelines protects "
            "both employees and the company.",
        ),
        (
            "Approved AI Tools",
            "Currently approved tools include: Google Gemini (via Workspace), GitHub Copilot "
            "(for engineering teams), Notion AI (for documentation), and Otter.ai (for meeting "
            "transcription with consent). All other AI tools require IT and Legal approval "
            "before use with company data. Personal AI accounts (e.g., ChatGPT free tier) "
            "must not be used for company work.",
        ),
        (
            "What Data Can Be Entered into AI Tools",
            "You MAY input: publicly available information, anonymized data, your own draft "
            "documents, and general business process questions. "
            "You MUST NOT input: customer PII, financial projections, unreleased product plans, "
            "source code marked confidential, legal documents, or employee personal data. "
            "When in doubt, ask your manager or email security@company.com before proceeding.",
        ),
        (
            "AI Output Review Requirements",
            "All AI-generated content used in official communications, reports, or code "
            "must be reviewed and verified by the employee before submission. AI can hallucinate "
            "facts, misinterpret context, or produce biased output. You are responsible for "
            "the accuracy of any content you submit, regardless of how it was generated. "
            "Do not cite AI as a source in external documents.",
        ),
        (
            "Intellectual Property",
            "Content generated using company-approved AI tools during work hours is considered "
            "company intellectual property. Do not share proprietary AI-generated content "
            "externally without approval. If you use AI to assist with a patentable invention, "
            "disclose this to the IP team immediately. The legal landscape for AI-generated "
            "IP is evolving - stay updated via the Legal team's quarterly briefings.",
        ),
        (
            "Bias & Fairness",
            "AI tools can reflect biases present in their training data. Do not use AI "
            "tools to make or inform hiring, promotion, or performance decisions. Do not "
            "use AI to evaluate or rank employees. If you observe biased output from an "
            "approved tool, report it to the AI Ethics team at ai-ethics@company.com. "
            "We conduct bi-annual audits of AI tool outputs for bias.",
        ),
        (
            "Training & Support",
            "Monthly 'AI at Work' lunch-and-learn sessions are open to all employees. "
            "On-demand tutorials are available in the Learning Portal under 'AI Literacy'. "
            "The #ai-tools Slack channel is monitored by our AI Champions team for questions. "
            "If you discover a more efficient use of an approved AI tool, share it in "
            "#ai-tools - great ideas get featured in our monthly AI Newsletter.",
        ),
    ],
)

print("\nAll 5 PDFs generated successfully in data/pdfs/")

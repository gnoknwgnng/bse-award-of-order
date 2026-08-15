"""
Known BSE "Company Update" subcategories -> ntfy topic slug.

This list was captured live from BSE's announcements API (SUBCATNAME field)
across ~6 weeks of data. BSE occasionally introduces new subcategories;
any subcategory NOT in this map still gets alerted, just routed to the
"uncategorized" fallback topic instead of its own dedicated one, so nothing
is ever silently dropped.

Regenerate this list periodically with `python discover_subcategories.py`.
"""

SUBCATEGORY_SLUGS = {
    "Acquisition": "acquisition",
    "Allotment of ESOP / ESPS": "allotment-of-esop-esps",
    "Allotment of Equity Shares": "allotment-of-equity-shares",
    "Amendments to Memorandum & Articles of Association": "amendments-to-memorandum-articles-of-association",
    "Analyst / Investor Meet": "analyst-investor-meet",
    "Appointment of Company Secretary / Compliance Officer": "appointment-of-company-secretary-compliance-officer",
    "Appointment of Statutory Auditor/s": "appointment-of-statutory-auditor-s",
    "Approval of Resolution plan by Tribunal": "approval-of-resolution-plan-by-tribunal",
    "Award of Order / Receipt of Order": "award-of-order-receipt-of-order",
    "Board Meeting Cancelled": "board-meeting-cancelled",
    "Board Meeting Rescheduled": "board-meeting-rescheduled",
    "Certificate under Reg. 74 (5) of SEBI (DP) Regulations, 2018": "certificate-under-reg-74-5-of-sebi-dp-regulations-2018",
    "Cessation": "cessation",
    "Change in Corporate Office Address": "change-in-corporate-office-address",
    "Change in Directorate": "change-in-directorate",
    "Change in Management": "change-in-management",
    "Change in Registered Office Address": "change-in-registered-office-address",
    "Code of Conduct under SEBI (PIT) Regulations, 2015": "code-of-conduct-under-sebi-pit-regulations-2015",
    "Credit Rating": "credit-rating",
    "Diversification / Disinvestment": "diversification-disinvestment",
    "Earnings Call Transcript": "earnings-call-transcript",
    "General": "general",
    "Intimation of meeting of Committee of Creditors": "intimation-of-meeting-of-committee-of-creditors",
    "Investor Presentation": "investor-presentation",
    "Issue of Securities": "issue-of-securities",
    "List of Creditors": "list-of-creditors",
    "Meeting Updates": "meeting-updates",
    "Memorandum of Understanding /Agreements": "memorandum-of-understanding-agreements",
    "Monitoring Agency Report": "monitoring-agency-report",
    "Monthly Business Updates": "monthly-business-updates",
    "Newspaper Publication": "newspaper-publication",
    "Open Offer - Updates": "open-offer-updates",
    "Outcome of meeting of Committee of Creditors": "outcome-of-meeting-of-committee-of-creditors",
    "Press Release / Media Release": "press-release-media-release",
    "Press Release / Media Release (Revised)": "press-release-media-release-revised",
    "Raising of Funds": "raising-of-funds",
    "Reg. 32 (1), (3) - Statement of Deviation & Variation": "reg-32-1-3-statement-of-deviation-variation",
    "Reg.24(A)-Annual Secretarial Compliance": "reg-24-a-annual-secretarial-compliance",
    "Resignation of Chairman and Managing Director": "resignation-of-chairman-and-managing-director",
    "Resignation of Chief Executive Officer (CEO)": "resignation-of-chief-executive-officer-ceo",
    "Resignation of Chief Financial Officer (CFO)": "resignation-of-chief-financial-officer-cfo",
    "Resignation of Company Secretary / Compliance Officer": "resignation-of-company-secretary-compliance-officer",
    "Resignation of Director": "resignation-of-director",
    "Resignation of Managing Director": "resignation-of-managing-director",
    "Resignation of Statutory Auditors": "resignation-of-statutory-auditors",
    "Scheme of Arrangement": "scheme-of-arrangement",
    "Strikes /Lockouts / Disturbances": "strikes-lockouts-disturbances",
}

FALLBACK_SLUG = "uncategorized"

# CallAide: Call Summary Delivery Format

To meet our strict KPI of **delivering call summaries in under 60 seconds** after a call ends, CallAide formats and sends captured lead data across three channels: **SMS (Urgent Actions)**, **Email (Detailed Records)**, and **JSON Webhook (CRM Automation)**.

This document outlines the standard delivery formats for each of these channels.

---

## 1. SMS Notification Format (Urgent Actions)

Designed for busy business owners on job sites or in meetings. It is short, optimized for quick mobile reading, and contains direct-dial links.

```text
📞 [CallAide Alert] New Lead Captured!
🏢 Business: {{company_name}}
👤 Customer: {{caller_name_first}} {{caller_name_last}}
📱 Phone: {{caller_phone}} (Tap to call)
🛠️ Request: {{service_category}} - {{caller_notes_brief}}
📅 Requested Slot: {{preferred_date}} @ {{preferred_time_slot}}
🚨 Priority: [{{priority_level}}] (e.g., URGENT / ROUTINE)
⚡ Status: {{call_status}} (e.g., Scheduling Request Logged / Human Escalated)

Click here to view full transcript & notes: https://app.callaide.com/calls/{{call_id}}
```

---

## 2. Email Notification Format (Detailed Records)

A beautifully structured, professional email sent to the business owner and their admin staff immediately after a call ends.

```markdown
Subject: 📞 New CallAide Lead: {{caller_name_first}} {{caller_name_last}} - {{service_category}} [{{priority_level}}]

Dear {{owner_or_manager_name}},

Your CallAide 24/7 AI Receptionist just handled a call for {{company_name}}. Here is the structured summary and lead information:

### 👤 CALLER CONTACT CARD
*   **Full Name:** {{caller_name_first}} {{caller_name_last}}
*   **Phone Number:** {{caller_phone}}
*   **Email Address:** {{caller_email}}
*   **Service Address:** {{street_address}}, {{city}}, {{state_province}} {{postal_code}}
*   **Customer Type:** {{is_existing_customer_label}} (New / Existing)

---

### 📋 TRANSACTION DETAILS
*   **Call ID:** `{{call_id}}`
*   **Date/Time:** {{timestamp_formatted}}
*   **Duration:** {{call_duration_seconds}} seconds
*   **Service Category:** **{{service_category}}**
*   **Urgency/Priority:** **[{{priority_level}}]**
*   **Action Taken:** **{{call_status_detailed}}** (e.g., Preferred slot logged, awaiting your confirmation)

---

### 📝 BRIEF SUMMARY
"{{caller_name_first}} called reporting that {{caller_notes}}. They have requested an appointment slot for {{preferred_date}} in the {{preferred_time_slot}} and are awaiting your team's confirmation call."

---

### 📅 REQUESTED BOOKING / CALLBACK SLOT
*   **Preferred Date:** {{preferred_date}}
*   **Preferred Time:** {{preferred_time_slot}}
*   **Awaiting Confirmation?** Yes - Please call the customer to lock in this slot.

---

### 💬 FULL CALL TRANSCRIPT
> **[00:01] AI:** "Thanks for calling {{company_name}}! My name is Amy. How can I help you today?"
> **[00:08] Caller:** "Hi, I have a major leak under my kitchen sink and need a plumber to come out."
> **[00:14] AI:** "Oh, I'm sorry to hear that. I'd be happy to log a request for you. May I have your name, please?"
> ... (full verbatim transcript populated here) ...

---

**Next Action Recommended:** Click the button below to call the customer back and finalize the booking:
[ Call Customer: {{caller_phone}} ]

Best regards,
The CallAide Team
www.callaide.com
```

---

## 3. JSON Webhook Payload Format (CRM & Zapier)

This structured JSON payload is sent via a POST request to the client's webhook URL (or Zapier/Make.com) to instantly update systems like Salesforce, HubSpot, ServiceTitan, or Housecall Pro.

```json
{
  "event": "call.completed",
  "call_id": "8c3b1740-fa20-4e3a-9677-4b7b3be6d6f2",
  "timestamp": "2026-06-18T07:48:12Z",
  "duration_seconds": 104,
  "business": {
    "company_name": "{{company_name}}",
    "industry": "{{industry}}"
  },
  "lead": {
    "first_name": "{{caller_name_first}}",
    "last_name": "{{caller_name_last}}",
    "phone": "{{caller_phone}}",
    "email": "{{caller_email}}",
    "is_existing_customer": false,
    "address": {
      "street": "{{street_address}}",
      "city": "{{city}}",
      "state": "{{state_province}}",
      "zip": "{{postal_code}}"
    }
  },
  "request_details": {
    "category": "{{service_category}}",
    "notes": "{{caller_notes}}",
    "priority": "{{priority_level}}",
    "is_emergency": false,
    "escalated_to_human": false
  },
  "scheduling": {
    "booking_requested": true,
    "preferred_date": "{{preferred_date}}",
    "preferred_time_slot": "{{preferred_time_slot}}"
  },
  "transcript": [
    { "speaker": "AI", "text": "Thanks for calling {{company_name}}! My name is Amy. How can I help you today?", "timestamp": "00:01" },
    { "speaker": "Caller", "text": "Hi, I have a major leak under my kitchen sink and need a plumber to come out.", "timestamp": "00:08" }
  ]
}
```

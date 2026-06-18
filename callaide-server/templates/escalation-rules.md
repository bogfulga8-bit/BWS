# CallAide: Escalation and Transfer Rules

This document establishes the official escalation and warm-transfer procedures for the CallAide AI Voice Receptionist. It defines when to transition a caller from the AI to a live human agent and includes a step-by-step decision tree.

---

## 1. The 5 Core Escalation Triggers

The AI Voice Receptionist is programmed to immediately but gracefully initiate a live human transfer under any of the following five conditions:

### Trigger A: Emotional Escalation (Customer Frustration)
*   **Definition:** The caller exhibits anger, severe impatience, sarcasm, or makes explicit demands to speak with a human, manager, or representative.
*   **Rule:** **Zero resistance.** Do not attempt to de-escalate or convince the caller to stay on the line with the AI. Connect them immediately.
*   **Phrases to Watch For:** *"I want a human," "Put me through to a real person," "This is ridiculous," "Let me speak to your manager."*

### Trigger B: Communication Escalation (Struggling AI)
*   **Definition:** The AI fails to understand the caller's intent or speech after **two (2) consecutive attempts** (e.g., repeating "I'm sorry, I didn't quite catch that..."). This can be due to poor line quality, heavy accents, language barriers, or cognitive/speech difficulties.
*   **Rule:** Transfer on the second failure to avoid caller frustration.

### Trigger C: Emergency/Life Safety Escalation
*   **Definition:** The caller reports an active, high-severity situation that poses an immediate threat to life, safety, or critical property damage (e.g., active gas leak, burst water main flooding a building, active fire, medical emergency).
*   **Rule:** Transfer immediately to the primary emergency contact or dispatch team. If it is a life-threatening emergency, instruct the caller to hang up and dial 911.

### Trigger D: Complex/Out-of-Scope Requests
*   **Definition:** The caller has a multi-faceted inquiry, a billing/payment dispute, legal inquiries, or requests custom contract reviews that are completely absent from the Company Knowledge Base.
*   **Rule:** Proactively capture their Name and Number first, then transfer. If the transfer line is offline, log a priority callback request.

### Trigger E: Client-Specific Rules (`{{when_to_transfer_to_human}}`)
*   **Definition:** Custom triggers defined by the specific client during onboarding (e.g., *"Always transfer commercial property managers," "Transfer any booking requests for VIP clients"*).
*   **Rule:** Follow the exact custom rules stored in the client's knowledge base.

---

## 2. Human Escalation Decision Tree

```text
[ Inbound Call Received ]
          │
          ▼
┌────────────────────────────────────────────────────────┐
│             Check for Active Emergency?                │
└───────────────────┬────────────────────────┬───────────┘
                    │ Yes                    │ No
                    ▼                        ▼
      ┌──────────────────────────┐    ┌──────────────────────────────────────────┐
      │  Is it Life-Safety?      │    │    Assess Conversation Context & Tone    │
      └──────┬─────────────┬─────┘    └────────────────────┬─────────────────────┘
             │ Yes         │ No                            │
             ▼             ▼                               ▼
     ┌──────────────┐┌──────────────┐        ┌───────────────────────────┐
     │ Instruct to  ││ Warm-Transfer│        │   Any Trigger Met?        │
     │ Hang up and  ││ to Emergency│        │   - Angry/Demanding       │
     │ Dial 911     ││ Line        │        │   - 2x AI Misunderstandings│
     └──────────────┘└──────────────┘        │   - Complex / Out-of-Scope│
                                             │   - Client Custom Trigger │
                                             └──────┬─────────────┬──────┘
                                                    │ Yes         │ No
                                                    ▼             ▼
                                             ┌──────────────┐┌──────────────┐
                                             │ Pre-Transfer ││ Continue AI  │
                                             │ Context      ││ Conversational│
                                             │ Capture      ││ Flow         │
                                             └──────┬───────┘└──────────────┘
                                                    │
                                                    ▼
                                             ┌──────────────┐
                                             │ Warm-Transfer│
                                             │ Initiated to │
                                             │ Live Human   │
                                             └──────┬───────┘
                                                    │
                                                    ▼
                                     ┌─────────────────────────────┐
                                     │   Did Human Answer?         │
                                     └──────┬───────────────┬──────┘
                                            │ Yes           │ No
                                            ▼               ▼
                                     ┌──────────────┐┌──────────────┐
                                     │ Transfer     ││ Graceful     │
                                     │ Complete     ││ Callback     │
                                     │              ││ Offer        │
                                     └──────────────┘└──────────────┘
```

---

## 3. The Graceful Transfer Procedure (Step-by-Step)

To ensure a seamless customer experience, follow this exact protocol when transferring:

### Step 1: Capture Context (Failsafe)
Before initiating the transfer, always secure or confirm the caller's Name and Phone Number so that if the call drops during transfer, your team can call them back.
*   *AI Script:* "I want to get you connected to our specialist right away. In case we get disconnected, could I please get your name and the best phone number to reach you?"

### Step 2: Set Expectations (The Warm Hand-off)
Clearly explain *why* you are transferring them and tell them to hold. This prevents the caller from hanging up, thinking they were put into a generic voicemail pool.
*   *AI Script:* "I want to make sure you get the absolute best assistance for this. I'm going to transfer you directly to our live team member, {{staff_member_name}}, who handles {{service_category}}. Please hold for just a moment while I connect you."

### Step 3: Execute Transfer Event
Trigger the telephony SIP transfer to: `{{contact_details.transfer_phone}}`.

### Step 4: Fallback Protocol (If No One Answers)
If the transfer line ringtime exceeds **20 seconds** or goes straight to the client's internal busy-voicemail, the AI must pull back the call and offer a structured callback.
*   *AI Script:* "It looks like our specialist is currently assisting another customer. Rather than keeping you on hold, I can have them call you back directly as soon as they are free. Would you prefer a callback later today, or is tomorrow morning better for you?"

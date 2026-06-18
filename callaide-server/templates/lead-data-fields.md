# CallAide: Lead Data Fields Schema

This document defines the structured schema for lead data captured by the AI Voice Receptionist during a call. 

The schema is presented as a **Markdown Table** (for business owners and CRM integration planners) and as a **JSON Schema** (for developers and technical systems).

---

## 1. Lead Data Fields Table

| Field Name | Data Type | Requirement | Description / Format |
| :--- | :--- | :--- | :--- |
| `call_id` | String | **Required** | Unique identifier for the phone call session. |
| `timestamp` | String (ISO 8601) | **Required** | Date and time the call occurred (e.g., `YYYY-MM-DDTHH:MM:SSZ`). |
| `caller_phone` | String | **Required** | The phone number of the caller, in E.164 format (e.g., `+12345678901`). |
| `caller_name_first` | String | **Required** | The first name of the caller, capitalized. |
| `caller_name_last` | String | **Required** | The last name of the caller, capitalized (if provided). |
| `caller_email` | String | Optional | The email address of the caller. |
| `street_address` | String | Optional | The street address for the service request (crucial for trades/home services). |
| `city` | String | Optional | The city associated with the street address. |
| `state_province` | String | Optional | The state or province associated with the address. |
| `postal_code` | String | Optional | ZIP or Postal Code. |
| `is_existing_customer` | Boolean | **Required** | `true` if the caller has done business with the company before; `false` otherwise. |
| `service_category` | String (Enum) | **Required** | Broad category of the request (e.g., `Plumbing`, `HVAC`, `Electrical`, `Booking`, `Inquiry`, `Billing`). |
| `caller_notes` | String | **Required** | A clear, detailed description of the caller's issue or inquiry. |
| `preferred_date` | String (ISO Date) | Optional | The caller's preferred date for booking (e.g., `YYYY-MM-DD`). |
| `preferred_time_slot` | String (Enum) | Optional | Preferred time of day: `Morning` (8am-12pm), `Afternoon` (12pm-5pm), `Evening` (5pm-8pm), or `Anytime`. |
| `is_emergency` | Boolean | **Required** | `true` if the request is flagged as an active emergency/disaster; `false` otherwise. |
| `escalated_to_human` | Boolean | **Required** | `true` if the call was warm-transferred to a live human during the call; `false` otherwise. |

---

## 2. JSON Schema Definition (draft-07)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CallAideLeadData",
  "description": "Schema representing structured lead and call metadata collected by the CallAide AI Voice Receptionist.",
  "type": "object",
  "properties": {
    "call_id": {
      "type": "string",
      "description": "Unique UUID for the call session."
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp when the call ended."
    },
    "caller_phone": {
      "type": "string",
      "pattern": "^\\+?[1-9]\\d{1,14}$",
      "description": "E.164 formatted telephone number."
    },
    "caller_name_first": {
      "type": "string",
      "minLength": 1,
      "description": "Caller's first name."
    },
    "caller_name_last": {
      "type": "string",
      "description": "Caller's last name (if provided)."
    },
    "caller_email": {
      "type": "string",
      "format": "email",
      "description": "Caller's email address."
    },
    "service_address": {
      "type": "object",
      "properties": {
        "street_address": { "type": "string" },
        "city": { "type": "string" },
        "state_province": { "type": "string" },
        "postal_code": { "type": "string" }
      },
      "additionalProperties": false,
      "description": "The physical address where the work or appointment is requested."
    },
    "is_existing_customer": {
      "type": "boolean",
      "description": "Indicates if the caller has a prior relationship with the business."
    },
    "service_category": {
      "type": "string",
      "description": "The broad classification of the caller's intent."
    },
    "caller_notes": {
      "type": "string",
      "description": "Summary of the caller's specific problem, request, or question."
    },
    "scheduling_preference": {
      "type": "object",
      "properties": {
        "preferred_date": {
          "type": "string",
          "format": "date",
          "description": "Target date (YYYY-MM-DD)."
        },
        "preferred_time_slot": {
          "type": "string",
          "enum": ["Morning", "Afternoon", "Evening", "Anytime"],
          "description": "Preferred window of the day."
        }
      },
      "additionalProperties": false,
      "description": "Target schedule requested by the caller."
    },
    "is_emergency": {
      "type": "boolean",
      "description": "Flag indicating if the issue is a critical, life-safety, or active property-damage emergency."
    },
    "escalated_to_human": {
      "type": "boolean",
      "description": "Indicates if the call was warm-transferred to a human staff member during the session."
    }
  },
  "required": [
    "call_id",
    "timestamp",
    "caller_phone",
    "caller_name_first",
    "is_existing_customer",
    "service_category",
    "caller_notes",
    "is_emergency",
    "escalated_to_human"
  ],
  "additionalProperties": false
}
```

# AQI Reflex Agent (Go CLI)

A modular Go CLI application that acts as a **Simple Reflex Agent** to fetch real-time Air Quality Index (AQI) data using Google APIs and provide health recommendations based on AQI levels.

---

## What This Project Does

1. Takes **State** and **Country** as CLI input
2. Uses **Google Geocoding API** to convert location → latitude & longitude
3. Uses **Google Air Quality API** to fetch real-time AQI
4. Applies **Simple Reflex Agent rules**
5. Prints AQI and health advisory

This project follows a clean modular architecture:

```
aqi-agent/
│
├── main.go      → CLI entry point
├── agent/       → Reflex decision logic
├── api/         → External API calls
├── models/      → Response structures
└── go.mod
```

---

## ⚙️ Prerequisites

- Go 1.20+
- Google Cloud account
- Internet connection

---

## How To Get a Google API Key

### Step 1 — Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a **New Project**
3. Select the project

### Step 2 — Enable Required APIs

Go to **APIs & Services → Library** and enable:

- **Geocoding API**
- **Air Quality API**

### Step 3 — Create an API Key

1. Go to **APIs & Services → Credentials**
2. Click **Create Credentials**
3. Select **API Key**
4. Copy the generated key

### (Recommended) Restrict Your API Key

Click your API key → Add restrictions:

- **Restrict by API:**
  - Geocoding API
  - Air Quality API
- **Optional:** Restrict by IP address

This prevents misuse if the key is accidentally exposed.

---

## Set Your API Key

You must export your API key before running the program.

### Mac / Linux

```bash
export GOOGLE_API_KEY="your_actual_api_key_here"

# Verify it's set
echo $GOOGLE_API_KEY
```

---

## How To Run

From the project root:

```bash
go run main.go Hyderabad India
```

---

## Reflex Agent Logic

The system uses rule-based decision logic:

| AQI Range | Decision                        |
|-----------|---------------------------------|
| 0 – 50    | Good                            |
| 51 – 100  | Moderate                        |
| 101 – 150 | Unhealthy for Sensitive Groups  |
| 151 – 200 | Unhealthy                       |
| 201 – 300 | Very Unhealthy                  |
| 300+      | Hazardous                       |

The agent reacts only to the current AQI value.  
No memory. No prediction.  
This is a textbook **Simple Reflex Agent**.

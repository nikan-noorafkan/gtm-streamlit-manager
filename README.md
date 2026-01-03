# GTM API Manager (Streamlit)

A lightweight, educational, and privacy-first web tool for managing **Google Tag Manager (GTM)** using the **official GTM API**.

This tool is designed for:

* Learning how the GTM API works
* Workshops and training sessions
* Internal tools and prototypes
* Developers and advanced marketers

---

## 🚀 Key Features

* 🔐 **User-owned OAuth (No shared credentials)**
* 🧠 Works with **your own Google Tag Manager access**
* 🧩 List GTM Accounts, Containers, Workspaces
* 🏷️ Create and manage GTM Tags (Workspace-safe)
* ☁️ Runs fully in the browser via Streamlit Cloud
* ❌ No Google OAuth verification required
* ❌ No data storage, no tracking, no database

---

## 🔐 Privacy & Security Model (Important)

This tool **does NOT store**:

* Your email
* Your Google tokens
* Your GTM account IDs
* Your OAuth credentials

### How authentication works:

* Each user creates **their own Google OAuth Client**
* OAuth credentials are used **only in the current browser session**
* Tokens live in memory only and are discarded on refresh
* The app can only access **what you already have access to in GTM**

This is the same permission model used by Google Tag Manager itself.

---

## 🧭 How the Tool Works (High Level)

```
You
 └── Your Google Account
      └── Your OAuth Client
           └── Google Tag Manager API
                └── Your GTM Accounts & Containers
```

The app is just a UI layer — it never becomes the owner of your data.

---

## 📦 Requirements

To use this tool, you need:

* A Google account
* Access to at least one Google Tag Manager account
* Ability to create a Google Cloud project (free)

---

## 🛠️ Step-by-Step Setup Guide

### Step 1 — Create a Google Cloud Project

1. Go to [https://console.cloud.google.com](https://console.cloud.google.com)
2. Click **New Project**
3. Name it (e.g. `gtm-api-manager`)
4. Create the project

---

### Step 2 — Enable Google Tag Manager API

1. In the project, go to **APIs & Services → Library**
2. Search for **Google Tag Manager API**
3. Click **Enable**

---

### Step 3 — Configure OAuth Consent Screen

1. Go to **APIs & Services → OAuth consent screen**
2. User Type: **External**
3. App name: anything you like
4. User support email: your email
5. Developer contact email: your email
6. Save and continue

#### Scopes

Add the following scopes:

```
https://www.googleapis.com/auth/tagmanager.readonly
https://www.googleapis.com/auth/tagmanager.edit.containers
```

> ⚠️ Do NOT publish the consent screen
> Keeping it in **Testing** mode is expected and correct.

---

### Step 4 — Create OAuth Client ID

1. Go to **APIs & Services → Credentials**
2. Click **Create Credentials → OAuth Client ID**
3. Application type: **Web application**
4. Name: `GTM API Manager`

#### Authorized Redirect URI

Use **exactly** the redirect URI shown inside the app UI.

Example:

```
https://gtm-api-manager-app.streamlit.app/oauth2callback
```

5. Save

---

### Step 5 — Copy OAuth Credentials

From the OAuth client page, copy:

* **Client ID**
* **Client Secret**

You will paste these into the app.

---

## ▶️ Using the App

1. Open the app URL
2. Expand **“Google OAuth Setup”**
3. Paste:

   * Client ID
   * Client Secret
4. Click **Save OAuth Credentials**
5. Click **Login with Google**
6. Grant access
7. Start managing your GTM resources 🎉

---

## 🧪 What You Can Do

* View all GTM accounts you have access to
* Browse containers and workspaces
* Create and manage tags safely inside workspaces
* Experiment with GTM API without touching production

---

## ⚠️ Important Notes

* Changes are made **only inside workspaces**
* Nothing is auto-published
* You are responsible for publishing versions in GTM UI
* Closing or refreshing the page clears the session

---

## ❓ Why This Tool Does NOT Require Google Verification

Because:

* Each user brings their own OAuth client
* No shared or centralized credentials exist
* The app never requests access on behalf of other users
* This matches Google’s recommended developer tooling model

---

## 🧑‍🏫 Educational Use

This tool is ideal for:

* Teaching GTM API concepts
* Showing real-world OAuth flows
* Demonstrating scalable GTM management
* Hands-on workshops

---

## 🧩 Roadmap (Optional Ideas)

* Bulk tag operations
* Tag cloning between containers
* Workspace diff & preview
* Export GTM structure
* Read-only mode
* Step-by-step wizard UI

---

## ⚖️ Disclaimer

This is an **educational and developer-focused tool**.
Use responsibly and ensure you understand GTM permissions before making changes.

---

## 📬 Feedback & Contributions

Issues, suggestions, and pull requests are welcome.

# Research Findings for Josekamau Trading AI Agent

## 1. Automation Platforms
- **ManyChat**: Best for Instagram/Facebook DM and comment automation. Supports AI triggers, keyword detection, and structured flows.
- **Zapier/Make**: Useful for connecting ManyChat with other services (like email or Google Sheets) if needed.
- **Telegram Bot API**: Can be used to manage the "Pips Lab" channel invites and webinar reminders.

## 2. HFM (HotForex) Integration
- **Affiliate Link**: Uses a `ref-id` tracking code. Format is typically `https://www.hfm.com/?refid=[YOUR_ID]`.
- **Verification**: Users need to register and verify their email. The AI agent should ask for the email used and a screenshot of the dashboard.
- **Affiliate Support**: Assignments can be requested via `affiliates.ke@hfm.com` if a user already has an account but wants to join the affiliate group.

## 3. Telegram "Pips Lab" & Webinar
- **Invite Link**: Can be a permanent link or a bot-generated unique link.
- **Webinar Reminders**: Can be scheduled using a Telegram bot or a simple recurring message in the channel.

## 4. Conversation Flow Logic
1. **Trigger**: Comment or DM.
2. **Greeting & Info Collection**: Ask Name and Reason for reaching out.
3. **Service Interest**: Ask about Copy Trading or Classes.
4. **HFM Status Check**:
   - If NO: Send HFM link.
   - If YES: Ask for registration email and screenshot.
5. **Channel Access**: Provide Pips Lab Telegram link.
6. **Closing**: Remind about Sunday Webinar.

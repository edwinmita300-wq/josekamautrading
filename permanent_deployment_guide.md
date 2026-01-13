# Josekamau Trading AI Agent: Permanent Deployment Guide

This guide provides instructions for permanently deploying your Josekamau Trading AI Agent to a production-ready environment. The previous deployment was in a temporary sandbox. For a persistent solution, you will need to use a cloud hosting provider. This guide will focus on two popular platforms: **Render** and **Heroku**, but the principles can be applied to other platforms like AWS, Google Cloud, or DigitalOcean.

## 1. Overview of Provided Files

You have been provided with the following files:

*   `app.py`: The core Flask application containing the AI agent's logic and webhook endpoint. It is configured to read sensitive information (HFM link, Pips Lab link, Josekamau email) from environment variables for security and flexibility.
*   `requirements.txt`: A list of Python dependencies required by the `app.py` (Flask, Flask-Cors, Gunicorn).
*   `Procfile`: A file that tells platforms like Render and Heroku how to run your web application using Gunicorn, a production-ready WSGI HTTP server.

## 2. Choosing a Hosting Platform

Both Render and Heroku are excellent choices for deploying Python web applications. They offer free tiers for basic usage, which can be a good starting point.

*   **Render**: Known for its ease of use, automatic deployments from Git, and generous free tier for web services.
*   **Heroku**: A long-standing Platform-as-a-Service (PaaS) with a robust ecosystem, also offering a free tier (though it may require credit card verification).

## 3. General Deployment Steps (Common to Most Platforms)

1.  **Version Control (Git)**: Initialize a Git repository for your project and commit the `app.py`, `requirements.txt`, and `Procfile` to it. Push this repository to a service like GitHub, GitLab, or Bitbucket.
2.  **Create an Account**: Sign up for an account on your chosen hosting platform (Render or Heroku).
3.  **Create a New Web Service/App**: Follow the platform's instructions to create a new web service or application.
4.  **Connect to Git Repository**: Link your hosting platform to your Git repository. This enables automatic deployments whenever you push changes to your repository.
5.  **Configure Environment Variables**: This is a crucial step for security and flexibility. You **MUST** set the following environment variables on your hosting platform:
    *   `HFM_AFFILIATE_LINK`: Your complete HFM affiliate link (e.g., `https://www.hfm.com/ke/en/?refid=30427623`)
    *   `PIPS_LAB_LINK`: The invite link to your Pips Lab Telegram channel (e.g., `https://t.me/pipsllab`)
    *   `JOSE_EMAIL`: The email address for HFM account verification (e.g., `Josekamautrading@gmail.com`)
    *   `PORT`: (Optional, but good practice) Some platforms automatically set this, but if not, set it to `5000` or the port your application listens on.
6.  **Build and Deploy**: The platform will automatically detect your `requirements.txt` and `Procfile` to build and deploy your application. It will install dependencies and start the Gunicorn server as specified in the `Procfile`.
7.  **Obtain Public URL**: Once deployed, the platform will provide a public URL for your web service. This will be your permanent AI Agent Webhook URL.

## 4. Platform-Specific Instructions

### 4.1. Deploying to Render

1.  **Sign Up/Log In**: Go to [Render.com](https://render.com/) and sign up or log in.
2.  **New Web Service**: From your dashboard, click 
`New +` -> `Web Service`.
3.  **Connect Repository**: Select your Git provider (GitHub, GitLab, etc.) and choose the repository containing your AI agent code.
4.  **Configure Service**: 
    *   **Name**: Choose a unique name for your service (e.g., `josekamau-ai-agent`).
    *   **Region**: Select a region close to your users.
    *   **Branch**: Specify the branch to deploy from (e.g., `main` or `master`).
    *   **Root Directory**: Leave blank if your `app.py`, `requirements.txt`, and `Procfile` are in the root of your repository.
    *   **Runtime**: `Python 3`.
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `gunicorn app:app --workers=4 --bind 0.0.0.0:$PORT` (This comes from your `Procfile`)
5.  **Environment Variables**: Go to the `Environment` section and add the three required variables:
    *   `HFM_AFFILIATE_LINK`
    *   `PIPS_LAB_LINK`
    *   `JOSE_EMAIL`
6.  **Create Web Service**: Click `Create Web Service`. Render will automatically build and deploy your application. Once deployed, you will get a public URL.

### 4.2. Deploying to Heroku

1.  **Sign Up/Log In**: Go to [Heroku.com](https://www.heroku.com/) and sign up or log in.
2.  **Install Heroku CLI**: If you haven't already, install the Heroku Command Line Interface (CLI) on your local machine.
3.  **Log in to Heroku CLI**: Open your terminal and run `heroku login`.
4.  **Create a New App**: From your project directory (where `app.py`, `requirements.txt`, `Procfile` are located), run:
    ```bash
    heroku create your-app-name-here # Replace with a unique app name
    ```
5.  **Set Environment Variables**: Use the Heroku CLI to set your configuration variables:
    ```bash
    heroku config:set HFM_AFFILIATE_LINK="https://www.hfm.com/ke/en/?refid=30427623"
    heroku config:set PIPS_LAB_LINK="https://t.me/pipsllab"
    heroku config:set JOSE_EMAIL="Josekamautrading@gmail.com"
    ```
6.  **Deploy Code**: Push your Git repository to Heroku:
    ```bash
    git push heroku main # Or 'master' if that's your main branch
    ```
7.  **Open App**: Once deployed, you can open your app in the browser to get its public URL:
    ```bash
    heroku open
    ```

## 5. Post-Deployment Steps

Once your AI agent is permanently deployed and you have its public URL:

1.  **Update Social Media Integrations**: Go to your social media automation platform (e.g., ManyChat) and update the webhook URL to the new, permanent URL provided by Render or Heroku.
2.  **Update Telegram Bot**: If your Telegram bot is integrated with the webhook, update its configuration with the new URL. For scheduled reminders, ensure your bot or scheduling service is pointing to the correct channel.
3.  **Monitoring**: Set up monitoring and logging on your chosen platform to ensure the AI agent is running smoothly and to troubleshoot any issues.

This permanent deployment ensures your AI agent remains active and responsive to your users without interruption.

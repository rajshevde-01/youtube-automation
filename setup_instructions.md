# YouTube Short Automation Setup

Follow these steps to deploy your 100% FREE YouTube Shorts automation pipeline:

## 1. Local Testing

It's highly recommended you run this locally once to generate your YouTube credentials.

1. **Install Python environment**: Make sure you have Python 3.11 installed.
2. **Setup virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
3. **Database Setup**: Running `python main.py` for the first time will create the local `youtube_automation.db`.

## 2. Setting Up YouTube Credentials

Because you are doing a zero-cost stack, you'll use Google Cloud console to get YouTube API credentials.

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new Project (e.g., "YouTube Shorts Bot").
3. Navigate to **APIs & Services > Library** and enable the **YouTube Data API v3**.
4. Go to **OAuth consent screen** and configure it as "External". Test status is fine. 
5. Go to **Credentials > Create Credentials > OAuth client ID**.
6. Set Application type to "Desktop app".
7. Download the JSON file. It contains your `client_id` and `client_secret`.
8. To get the `refresh_token`, you can temporarily use Google's OAuth 2.0 Playground:
   - Go to [OAuth 2.0 Playground](https://developers.google.com/oauthplayground/).
   - Click the gear icon > check "Use your own OAuth credentials". Paste your Client ID and Client Secret.
   - In Step 1 on the left, select "YouTube Data API v3", and specifically `https://www.googleapis.com/auth/youtube.upload`.
   - Click "Authorize APIs".
   - You will be redirected to log into your YouTube channel account. Click continue/accept.
   - In Step 2, click "Exchange authorization code for tokens".
   - Copy the `Refresh token`.

**Never share these 3 values with anyone.**

## 3. GitHub Actions Setup

Now we will push the code to a private GitHub repository and set up the Action.

1. Init Git locally and push to your remote:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   # Add your GitHub repository URL
   git remote add origin https://github.com/your-username/youtube-automation.git
   git branch -M main
   git push -u origin main
   ```

2. Go to your GitHub repository > **Settings > Secrets and variables > Actions**.
3. Create three new Repository Secrets:
   - `YOUTUBE_CLIENT_ID`: Paste your Client ID.
   - `YOUTUBE_CLIENT_SECRET`: Paste your Client Secret.
   - `YOUTUBE_REFRESH_TOKEN`: Paste the refresh token.

## 4. How it Runs

- The pipeline will run automatically every day at 1:30 PM UTC (7:00 PM IST).
- It will select a topic, generate the audio locally on the GitHub Runner, encode video, and upload to YouTube.
- You can manually trigger the workflow from the "Actions" tab in GitHub to test it immediately.
- To override the random topic, push a text file named `manual_topic.txt` to the root of the repository with your chosen topic before the scheduled time.

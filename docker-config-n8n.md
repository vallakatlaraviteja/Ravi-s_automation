# n8n Docker Configuration Guide

## Fix OAuth Redirect URL Issue

If you're experiencing OAuth redirect URL issues (like Google Sheets or Gmail not connecting), you need to set the `WEBHOOK_URL` environment variable in your n8n Docker container.

## Current Setup

Your n8n is running on: `http://localhost:9848`

## Solution: Set WEBHOOK_URL Environment Variable

### Method 1: Docker Run Command

If you started n8n with `docker run`, stop the container and restart it with the `WEBHOOK_URL` environment variable:

```bash
# Stop existing container
docker stop n8n
docker rm n8n

# Start with WEBHOOK_URL configured
docker run -d \
  --name n8n \
  -p 9848:5678 \
  -e WEBHOOK_URL=http://localhost:9848/ \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

**Important:** Note the trailing slash in `WEBHOOK_URL=http://localhost:9848/`

### Method 2: Docker Compose

If you're using Docker Compose, update your `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  n8n:
    image: n8nio/n8n
    container_name: n8n
    ports:
      - "9848:5678"
    environment:
      - WEBHOOK_URL=http://localhost:9848/
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - N8N_HOST=localhost
      - N8N_EDITOR_BASE_URL=http://localhost:9848
    volumes:
      - ~/.n8n:/home/node/.n8n
    restart: unless-stopped
```

Then restart the container:

```bash
docker-compose down
docker-compose up -d
```

### Method 3: Update Existing Container (Not Recommended)

You cannot update environment variables on a running container. You must recreate it using Method 1 or 2.

## Verify the Configuration

After restarting n8n with the `WEBHOOK_URL` set:

1. Open n8n: `http://localhost:9848`
2. Go to **Settings** > **Community Nodes** (or any settings page)
3. Check the n8n logs to confirm the webhook URL is set:

```bash
docker logs n8n
```

You should see something like:
```
n8n ready on http://localhost:9848
Editor is now accessible via:
http://localhost:9848/
```

## OAuth Setup After Configuration

Once `WEBHOOK_URL` is set, you can configure OAuth credentials:

### Google Sheets OAuth2

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **Google Sheets API**
4. Go to **Credentials** > **Create Credentials** > **OAuth 2.0 Client ID**
5. Application type: **Web application**
6. Authorized redirect URIs:
   - `http://localhost:9848/rest/oauth2-credential/callback`
7. Copy **Client ID** and **Client Secret**
8. In n8n: **Credentials** > **Add Credential** > **Google Sheets OAuth2 API**
9. Paste Client ID and Secret, click **Connect**

### Gmail OAuth2

Follow the same steps as Google Sheets, but:
- Enable **Gmail API** in Google Cloud Console
- Use the same OAuth client or create a new one
- Add redirect URI: `http://localhost:9848/rest/oauth2-credential/callback`
- In n8n: **Credentials** > **Add Credential** > **Gmail OAuth2 API**

## Production Deployment

If you plan to deploy n8n to production (not localhost), update the `WEBHOOK_URL` to your public domain:

```bash
docker run -d \
  --name n8n \
  -p 80:5678 \
  -e WEBHOOK_URL=https://yourdomain.com/ \
  -e N8N_PROTOCOL=https \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

## Troubleshooting

### Issue: OAuth still not working after setting WEBHOOK_URL

**Solution:**
1. Clear n8n cache and restart:
   ```bash
   docker exec n8n rm -rf /home/node/.n8n/.cache
   docker restart n8n
   ```
2. Delete and recreate OAuth credentials in n8n
3. Make sure Google Cloud Console redirect URI matches exactly: `http://localhost:9848/rest/oauth2-credential/callback`

### Issue: Port already in use (9848)

**Solution:**
1. Check what's using the port:
   ```bash
   lsof -i :9848
   ```
2. Stop the conflicting process or use a different port:
   ```bash
   docker run -d --name n8n -p 9849:5678 -e WEBHOOK_URL=http://localhost:9849/ -v ~/.n8n:/home/node/.n8n n8nio/n8n
   ```

### Issue: Cannot access n8n after restart

**Solution:**
1. Check container status:
   ```bash
   docker ps -a | grep n8n
   ```
2. View logs for errors:
   ```bash
   docker logs n8n
   ```
3. If container is stopped, start it:
   ```bash
   docker start n8n
   ```

## Your Emails

Based on your User Config, you have two Gmail accounts set up:
- **Primary:** raviintouch2@gmail.com
- **Secondary:** ravitejavallakatla7@gmail.com

You'll need to create OAuth credentials for both accounts:
1. Create one OAuth client in Google Cloud Console (or two separate ones)
2. In n8n, create two Gmail OAuth2 credentials:
   - One for raviintouch2@gmail.com (primary)
   - One for ravitejavallakatla7@gmail.com (secondary)
3. Update the workflow's credential IDs to match the n8n credential IDs

## Next Steps

After fixing the OAuth redirect:
1. Import the workflow: `workflow/ENHANCED-MASTER-workflow.json`
2. Configure all credentials (Groq, Google Sheets, Gmail primary/secondary, Telegram)
3. Create Google Sheet with the required columns
4. Update User Config node with your profile
5. Test the workflow by manually triggering each branch

For detailed setup instructions, see: `guides/COMPLETE-SETUP-GUIDE.md`

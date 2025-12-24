# Screencast Steps - Final Project

## What "Checking Out Application Source Code" Means

"Checking out application source code from your course repository" means:
- **Cloning or pulling your GitLab repository** to show you're accessing the code from the remote repository
- Demonstrating that the code exists in your GitLab repository (not just locally)
- This can be done by:
  - Using `git clone <repository-url>` in a fresh terminal/directory
  - OR showing the repository on GitLab web interface
  - OR using `git pull` if you already have it cloned
- The purpose is to show the code comes from your version-controlled repository

---

## Step-by-Step Guide: Creating Screencast via Zoom

### Pre-Recording Setup

1. **Prepare Your Environment**
   - Ensure all code is committed and pushed to GitLab
   - Have your Cloud Run deployment ready
   - Test your client application to ensure it works
   - Prepare a list of features to demo
   - Have your GitLab repository URL ready

2. **Prepare Your Screen**
   - Close unnecessary applications
   - Open the applications you'll need:
     - Terminal/Command Prompt
     - Web browser (for GitLab)
     - Your code editor (optional, for code walkthrough)
     - Google Cloud Console (for deployment demo)
   - Arrange windows so they're visible

3. **Test Your Setup**
   - Test screen sharing in Zoom
   - Test your microphone
   - Ensure good lighting if showing your face

---

### Recording Steps (Follow Exact Order from Instructions)

#### 1. Start Recording with Video of Yourself

**Steps:**
- Open Zoom and log in with your PSU account
- Start a new meeting (just yourself)
- **Enable your camera** - show yourself on screen initially
- Click "Record" → "Record on this Computer" (or "Record to Cloud" if available)
- **Narrate**: "This is [Your Name] presenting my final project for CS430"

**What to Show:**
- Your face on camera (required at the start)
- Brief introduction of yourself and the project

---

#### 2. Checking Out Application Source Code

**Steps:**
- Switch to screen share (you can minimize/hide your video after intro)
- Open a terminal/command prompt
- Navigate to a clean directory (or create a new one)
- Show the GitLab repository URL
- Execute one of these:
  ```bash
  # Option 1: Clone the repository
  git clone <your-gitlab-repo-url>
  cd <repo-name>/final
  
  # Option 2: If already cloned, show the repository
  cd <path-to-repo>/final
  git pull
  ```

**What to Narrate:**
- "I'm now checking out the application source code from my course repository on GitLab"
- Show the repository structure
- Point out the `final` directory and its contents

---

#### 3. Describing Setup Steps

**Steps:**
- Open a document or have notes ready
- Walk through the setup requirements:
  - Google Cloud project setup
  - Service accounts and IAM roles
  - API keys setup (Alpha Vantage, FRED, etc.)
  - Environment variables configuration
  - Required software packages (Python, dependencies)
  - BigQuery setup and permissions

**What to Narrate:**
- "To run this project, you would need to..."
- List each setup step clearly
- Mention where API keys should be stored (environment variables, Secrets Manager)
- Explain any service account permissions needed

**What to Show:**
- Google Cloud Console (if showing IAM/service accounts)
- Your `.env` file structure (without showing actual keys)
- `requirements.txt` files
- Any setup documentation

---

#### 4. Building and Deploying Container

**Steps:**
- Open terminal
- Navigate to `final/server` directory
- Show the Dockerfile
- Execute build command:
  ```bash
  gcloud builds submit --tag gcr.io/<project-id>/final
  ```
- Execute deployment command:
  ```bash
  gcloud run deploy final \
    --image gcr.io/<project-id>/final \
    --region us-west1 \
    --platform managed \
    --allow-unauthenticated \
    --set-env-vars ALPHA_VANTAGE_API_KEY=<key>,FRED_API_KEY=<key>
  ```

**What to Narrate:**
- "I'm now building the Docker container..."
- "Deploying to Cloud Run..."
- **PAUSE THE RECORDING** while deployment completes (to save time)
- Resume recording once deployment is done
- Show the Cloud Run service URL

**What to Show:**
- Dockerfile contents
- Build command execution
- Deployment command execution
- Cloud Run console showing the deployed service

---

#### 5. Demo Client Agent Functionality

**Steps:**
- Open terminal
- Navigate to `final/client` directory
- Show your client code structure
- Run the client:
  ```bash
  python client.py
  ```
- **Step through ALL functionality:**
  - Test each MCP tool (BigQuery, REST Countries, Alpha Vantage, FRED, Fake Store)
  - Show different query types
  - Demonstrate agent's ability to compose multiple tool calls
  - Show comprehensive analysis reports

**What to Narrate:**
- "Now I'll demonstrate the client agent..."
- Explain what each tool does as you test it
- Show how agents intelligently select tools
- Demonstrate the comprehensive analysis output

**What to Show:**
- Terminal output showing tool calls
- Agent responses and analysis
- Different project descriptions and their analyses

---

#### 6. Source Code Walkthrough (GitLab Website)

**Steps:**
- Open web browser
- Navigate to your GitLab repository: `https://gitlab.cecs.pdx.edu/<username>/<repo-name>`
- Navigate to the `final` directory
- Walk through each file:
  - `server/server.py` - MCP server implementation
  - `server/tools/*.py` - Individual tool implementations
  - `server/Dockerfile` - Container configuration
  - `client/client.py` - Main client entry point
  - `client/mcp_client.py` - MCP client implementation
  - `client/agents/*.py` - Agent definitions
  - `client/agents/tools.py` - Tool wrappers

**What to Narrate:**
- "Let me walk through the source code..."
- Explain how each feature is implemented
- Point out key design decisions
- Explain the MCP protocol usage
- Show tool descriptions and their importance

**What to Show:**
- GitLab file browser
- Code files with syntax highlighting
- Key code sections (zoom in if needed)

---

#### 7. Git Commit History Walkthrough

**Steps:**
- In GitLab, navigate to "Repository" → "Commits"
- Click through commits in chronological order
- For each commit:
  - Click on the commit to see the diff
  - Show the Python code changes
  - Explain what was added/changed

**What to Narrate:**
- "Now let me show the git commit history..."
- "This commit added the BigQuery tool implementation..."
- "This commit added the REST Countries tool..."
- "This commit refactored the tool architecture..."
- Explain your incremental development process
- **Ensure you show at least one commit per MCP tool**

**What to Show:**
- GitLab commit history page
- Individual commit diffs
- Code changes highlighted
- File additions/modifications

---

### Post-Recording Steps

#### 8. Stop Recording

**Steps:**
- Click "Stop Recording" in Zoom
- Wait for Zoom to process the recording
- Recording will be automatically uploaded to PSU MediaSpace

#### 9. Access Recording in MediaSpace

**Steps:**
- Go to PSU MediaSpace: https://mediaspace.psu.edu
- Log in with your PSU credentials
- Click "My Media" in the top menu
- Find your recording (may take a few minutes to appear)
- Click on the video

#### 10. Publish as Unlisted

**Steps:**
- In the video page, click the "Publish" tab
- Select "Unlisted" option
- Click "Save"
- Copy the video URL from the address bar

#### 11. Update Repository

**Steps:**
- Open `final/screencast_url.txt`
- Paste the MediaSpace URL
- Commit and push:
  ```bash
  git add final/screencast_url.txt
  git commit -m "Add screencast URL"
  git push
  ```

---

## Tips for a Good Screencast

1. **Keep it under 15 minutes** - Pause during long operations (deployment, builds)
2. **Speak clearly** - Narrate what you're doing as you do it
3. **Show your face initially** - Required to prove it's you
4. **Use zoom/zoom in** - Make code readable on screen
5. **Test beforehand** - Do a practice run to ensure everything works
6. **Have notes ready** - Don't rely on memory for all the steps
7. **Check audio quality** - Ensure your microphone is working well
8. **Show all features** - Don't skip any functionality
9. **Be thorough with commits** - Show at least one commit per tool
10. **Follow the exact order** - Match the order specified in instructions

---

## Checklist Before Recording

- [ ] All code committed and pushed to GitLab
- [ ] Cloud Run service deployed and working
- [ ] Client application tested and working
- [ ] All MCP tools tested individually
- [ ] GitLab repository accessible
- [ ] Zoom account logged in
- [ ] Microphone and camera working
- [ ] Screen sharing tested
- [ ] Notes prepared for narration
- [ ] Browser bookmarks ready (GitLab, Cloud Console, MediaSpace)

---

## Common Issues and Solutions

**Issue**: Recording not appearing in MediaSpace
- **Solution**: Wait 10-15 minutes, refresh "My Media" page

**Issue**: Screencast too long
- **Solution**: Pause recording during deployment/builds, edit out long waits

**Issue**: Code not readable
- **Solution**: Zoom in on code sections, use larger font in editor

**Issue**: Audio quality poor
- **Solution**: Use a good microphone, record in quiet environment

**Issue**: Forgot to show face initially
- **Solution**: Re-record the beginning, or add face video at start

---

## Time Estimates

- Introduction with face: 30 seconds
- Checking out code: 1 minute
- Setup description: 2-3 minutes
- Building/deploying (with pause): 2-3 minutes
- Client demo: 4-5 minutes
- Code walkthrough: 3-4 minutes
- Commit history: 2-3 minutes
- **Total: ~15 minutes**


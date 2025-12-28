# Process Documentation for Creating Lab Markdown Files

## Steps Used to Create lab01_2.md

### 1. Navigate to the Codelabs Webpage
- Open the browser and navigate to the CS 430 codelabs page
- Find the specific lab (e.g., "01.2: ARP, Wireshark, Netsim")
- Click on the lab to open it

### 2. Identify All Sections
- Review the table of contents in the left sidebar
- Note all section numbers and titles
- For lab01_2, there were 4 sections:
  - Section 1: ARP (linux.cs.pdx.edu)
  - Section 2: - (continuation of section 1)
  - Section 3: ARP (Cloud)
  - Section 4: Netsim

### 3. Navigate Through Each Section
- Click on each section in the table of contents OR use Next/Back buttons
- Navigate to each section using URL hash fragments (#0, #1, #2, #3)
- Scroll through each section completely (use PageDown, End key, or scroll)
- Take full-page screenshots of each section to capture all content

### 4. Extract Content from Screenshots
- Review screenshot descriptions to identify:
  - Instructions and text content
  - Code blocks with commands
  - Questions and bullet points
  - Diagrams or images
  - Any special formatting

### 5. Capture Images/Diagrams
- Identify any diagrams or images in the sections
- Take element-specific screenshots of diagrams
- Save images to an `images/` folder within the lab folder
- Use descriptive filenames (e.g., `netsim_diagram.png`)

### 6. Create Markdown File Structure
- Create the markdown file with naming convention: `lab01_X.md` (where X is the lab number)
- Structure with proper headings:
  ```markdown
  # Lab 01.X: Lab Title
  
  ## 1. Section Title
  [content]
  
  ## 2. Section Title
  [content]
  ```

### 7. Add All Content in Correct Order
- Replicate content exactly as it appears on the webpage
- Include all instructions, code blocks, and questions
- Maintain the exact order of content
- Format code blocks with proper syntax highlighting (bash, python, etc.)
- Use bullet points for questions and instructions

### 8. Add Images to Markdown
- Reference images using markdown image syntax:
  ```markdown
  ![Image Description](images/filename.png)
  ```
- Place images in appropriate locations within the content

### 9. Verify Completeness
- Check that all sections are included
- Verify all questions are present
- Ensure all code blocks are complete
- Confirm images are properly referenced
- Review that content order matches the webpage

### 10. Commit and Push
- Stage all new files (markdown and images)
- Commit with descriptive message
- Push to GitHub repository

## Key Points to Remember

- **Scroll through entire sections** - Content may extend beyond initial view
- **Capture all subsections** - Some sections may have multiple parts
- **Preserve exact order** - Content order matters
- **Include all questions** - Every question and instruction must be captured
- **Save images separately** - Create images folder and reference properly
- **Use proper markdown formatting** - Code blocks, headings, lists, etc.


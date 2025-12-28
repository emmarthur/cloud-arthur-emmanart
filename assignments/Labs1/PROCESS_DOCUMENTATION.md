# Process Documentation for Creating Lab Markdown Files

## ⚠️ MAIN NOTE: SCROLLING IS CRITICAL ⚠️

**YOU MUST SCROLL THROUGH EVERY SECTION COMPLETELY FROM TOP TO BOTTOM TO CAPTURE ALL CONTENT AND IMAGES. DO NOT ASSUME ALL CONTENT IS VISIBLE ON INITIAL LOAD.**

### Why Scrolling is Essential:
- Sections often contain multiple options (e.g., "Option #1" and "Option #2") that may not be visible initially
- Images and diagrams can be located anywhere within a section, not just at the top
- Text content extends beyond the initial viewport
- Missing content will result in incomplete documentation

### Scrolling Procedure:
1. **Always start at the top**: Press `Home` key to ensure you're at the beginning
2. **Scroll incrementally**: Use `PageDown` multiple times to scroll through the entire section
3. **Go to the end**: Press `End` key to ensure you've reached the bottom
4. **Take full-page screenshots**: Capture the entire section after scrolling
5. **Verify completeness**: Compare screenshot descriptions with markdown content to ensure nothing is missing

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
- **CRITICAL: Scroll through each section completely** (use PageDown, End key, or scroll)
  - **Step 1**: Press `Home` key to go to the top
  - **Step 2**: Press `PageDown` multiple times to scroll through the entire section
  - **Step 3**: Press `End` key to ensure you've reached the bottom
  - **Step 4**: Take a full-page screenshot after scrolling
  - **Step 5**: Review the screenshot description to identify ALL content (text, images, options, subsections)
- Take full-page screenshots of each section to capture all content

### 4. Extract Content from Screenshots
- **CRITICAL: Review screenshot descriptions thoroughly** to identify:
  - **ALL options** (e.g., "Option #1", "Option #2", etc.) - sections may have multiple options
  - **ALL subsections** (e.g., "Operating system and storage", "Clean-up", etc.)
  - Instructions and text content (including text that appears after scrolling)
  - Code blocks with commands
  - Questions and bullet points
  - Diagrams or images (may be at the top, middle, or bottom of the section)
  - Any special formatting
  - **Compare with existing markdown**: If content exists in screenshot but not in markdown, it's missing!

### 5. Capture Images/Diagrams
- **CRITICAL: Scroll up and down through each section page to detect ALL images**
- **After scrolling through the entire section**, identify any diagrams or images
- Take full-page screenshots of each section to capture all images
- Take element-specific screenshots of individual diagrams if needed
- Save images to an `images/` folder within the lab folder
- Use descriptive filenames (e.g., `section2_marketplace_ui.png`, `section3_nmap_scan.png`, `section2_complete.png`)
- **Place images in the markdown file exactly where they appear in the browser section**
- **Save complete section screenshots** (e.g., `section2_complete.png`) to verify all content was captured

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
- **CRITICAL: Include ALL options and subsections** (e.g., if section has "Option #1" and "Option #2", include BOTH)
- Replicate content exactly as it appears on the webpage
- Include all instructions, code blocks, and questions
- **Include ALL text content** that appears after scrolling (don't stop at initial viewport)
- Maintain the exact order of content as it appears on the webpage
- Format code blocks with proper syntax highlighting (bash, python, etc.)
- Use bullet points for questions and instructions
- **Verify completeness**: After adding content, compare with screenshot descriptions to ensure nothing is missing

### 8. Add Images to Markdown
- Reference images using markdown image syntax:
  ```markdown
  ![Image Description](images/filename.png)
  ```
- Place images in appropriate locations within the content

### 9. Verify Completeness
- **CRITICAL: Compare markdown with screenshot descriptions** to identify missing content
- Check that all sections are included
- **Verify ALL options are included** (e.g., Option #1 AND Option #2 if both exist)
- **Verify ALL subsections are included** (e.g., "Operating system and storage", "Clean-up", etc.)
- Verify all questions are present
- Ensure all code blocks are complete
- Confirm images are properly referenced
- Review that content order matches the webpage
- **Check for text that appears after scrolling** - ensure it's all included

### 10. Commit and Push
- Stage all new files (markdown and images)
- Commit with descriptive message
- Push to GitHub repository

## Key Points to Remember

### ⚠️ CRITICAL REQUIREMENTS ⚠️

1. **SCROLLING IS MANDATORY** - You MUST scroll through every section completely
   - Always start at the top (Home key)
   - Scroll incrementally (PageDown multiple times)
   - Go to the end (End key)
   - Content may extend far beyond initial view
   - Multiple options (Option #1, Option #2) may exist in the same section
   - Images can be anywhere in the section, not just at the top

2. **Capture ALL Content** - Not just what's visible initially
   - All options (Option #1, Option #2, etc.)
   - All subsections (e.g., "Operating system and storage", "Clean-up")
   - All text that appears after scrolling
   - All images and diagrams throughout the section

3. **Verify Completeness** - Always compare with screenshots
   - Compare markdown content with screenshot descriptions
   - If content exists in screenshot but not in markdown, it's missing!
   - Check for all options and subsections

### Standard Requirements

- **Place images correctly** - Images must be placed in the markdown file exactly where they appear in the browser section
- **Capture all subsections** - Some sections may have multiple parts
- **Preserve exact order** - Content order matters, including image placement
- **Include all questions** - Every question and instruction must be captured
- **Save images separately** - Create images folder and reference properly
- **Use proper markdown formatting** - Code blocks, headings, lists, etc.
- **Update process documentation** - Whenever new requirements are added (like scrolling for images), update PROCESS_DOCUMENTATION.md

## Common Mistakes to Avoid

1. **Assuming all content is visible initially** - Always scroll!
2. **Missing multiple options** - Sections may have Option #1, Option #2, etc.
3. **Missing subsections** - Look for subsections like "Operating system and storage", "Clean-up", etc.
4. **Not comparing with screenshots** - Screenshot descriptions reveal missing content
5. **Stopping at initial viewport** - Content extends beyond what you see first


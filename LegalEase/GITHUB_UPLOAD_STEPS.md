# Upload EduGenie to GitHub

## 1. Create a GitHub repository
Create a new empty repository named `EduGenie`.

## 2. Open this folder in VS Code
Open the extracted `EduGenie_GitHub_Submission` folder.

## 3. Initialize Git

```bash
git init
git add .
git commit -m "Initial EduGenie project"
git branch -M main
```

## 4. Connect the repository

Replace the URL with your own GitHub repository URL:

```bash
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

## 5. Verify
Refresh the GitHub repository and confirm that all eight phase folders and `README.md` are visible.
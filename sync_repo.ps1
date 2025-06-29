#!/usr/bin/env pwsh
# xtrium_platform GitHub Sync Script
# Created by Cascade AI Assistant

# Set error action preference to stop on errors
$ErrorActionPreference = "Stop"

# Define colors for output
$GREEN = [ConsoleColor]::Green
$RED = [ConsoleColor]::Red
$YELLOW = [ConsoleColor]::Yellow
$CYAN = [ConsoleColor]::Cyan

# Function to display colored messages
function Write-ColorMessage {
    param (
        [string]$message,
        [ConsoleColor]$color = [ConsoleColor]::White
    )
    Write-Host $message -ForegroundColor $color
}

# Function to check if git is installed
function Check-GitInstalled {
    try {
        $gitVersion = git --version
        Write-ColorMessage "Git detected: $gitVersion" $CYAN
        return $true
    } catch {
        Write-ColorMessage "Error: Git is not installed or not in PATH. Please install Git and try again." $RED
        return $false
    }
}

# Function to check repository status
function Check-RepoStatus {
    Write-ColorMessage "`n[1/5] Checking repository status..." $CYAN
    
    # Check for uncommitted changes
    $status = git status --porcelain
    if ($status) {
        Write-ColorMessage "Uncommitted changes detected:" $YELLOW
        git status --short
        
        $choice = Read-Host "Do you want to commit these changes? (y/n)"
        if ($choice -eq "y") {
            $commitMessage = Read-Host "Enter commit message"
            
            # Stage all changes
            git add .
            
            # Commit changes
            git commit -m "$commitMessage"
            if ($LASTEXITCODE -ne 0) {
                Write-ColorMessage "Error: Failed to commit changes." $RED
                exit 1
            }
            Write-ColorMessage "Changes committed successfully." $GREEN
        } else {
            Write-ColorMessage "Sync aborted. Please commit your changes before syncing." $YELLOW
            exit 0
        }
    } else {
        Write-ColorMessage "No uncommitted changes detected." $GREEN
    }
}

# Function to pull latest changes
function Pull-LatestChanges {
    Write-ColorMessage "`n[2/5] Pulling latest changes from remote repository..." $CYAN
    
    # Fetch all branches and tags
    git fetch --all --tags
    if ($LASTEXITCODE -ne 0) {
        Write-ColorMessage "Error: Failed to fetch from remote repository." $RED
        exit 1
    }
    
    # Get current branch
    $currentBranch = git rev-parse --abbrev-ref HEAD
    Write-ColorMessage "Current branch: $currentBranch" $CYAN
    
    # Pull latest changes
    git pull origin $currentBranch
    if ($LASTEXITCODE -ne 0) {
        Write-ColorMessage "Error: Failed to pull latest changes. There might be merge conflicts." $RED
        
        $choice = Read-Host "Do you want to abort the merge? (y/n)"
        if ($choice -eq "y") {
            git merge --abort
            Write-ColorMessage "Merge aborted. Please resolve conflicts manually and try again." $YELLOW
            exit 1
        } else {
            Write-ColorMessage "Please resolve the conflicts manually, then commit the changes." $YELLOW
            exit 1
        }
    }
    
    Write-ColorMessage "Successfully pulled latest changes." $GREEN
}

# Function to check for merge conflicts
function Check-MergeConflicts {
    Write-ColorMessage "`n[3/5] Checking for merge conflicts..." $CYAN
    
    $conflicts = git diff --name-only --diff-filter=U
    if ($conflicts) {
        Write-ColorMessage "Merge conflicts detected in the following files:" $RED
        Write-Host $conflicts
        Write-ColorMessage "Please resolve these conflicts manually, then commit the changes." $YELLOW
        exit 1
    }
    
    Write-ColorMessage "No merge conflicts detected." $GREEN
}

# Function to push changes
function Push-Changes {
    Write-ColorMessage "`n[4/5] Pushing changes to remote repository..." $CYAN
    
    # Get current branch
    $currentBranch = git rev-parse --abbrev-ref HEAD
    
    # Push changes
    git push origin $currentBranch
    if ($LASTEXITCODE -ne 0) {
        Write-ColorMessage "Error: Failed to push changes to remote repository." $RED
        exit 1
    }
    
    Write-ColorMessage "Successfully pushed changes to remote repository." $GREEN
}

# Function to display summary
function Display-Summary {
    Write-ColorMessage "`n[5/5] Sync summary:" $CYAN
    
    # Get last commit
    $lastCommit = git log -1 --pretty=format:"%h - %s (%cr) <%an>"
    Write-ColorMessage "Last commit: $lastCommit" $CYAN
    
    # Get current branch and status
    $currentBranch = git rev-parse --abbrev-ref HEAD
    Write-ColorMessage "Current branch: $currentBranch" $CYAN
    
    # Get remote URL
    $remoteUrl = git remote get-url origin
    Write-ColorMessage "Remote URL: $remoteUrl" $CYAN
    
    Write-ColorMessage "`nSync completed successfully!" $GREEN
}

# Main execution
Write-ColorMessage "===== Xtrium Platform GitHub Sync Script =====" $CYAN
Write-ColorMessage "Starting sync process..." $CYAN

# Check if git is installed
if (-not (Check-GitInstalled)) {
    exit 1
}

# Navigate to repository root
$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot
Write-ColorMessage "Repository path: $repoRoot" $CYAN

# Execute sync steps
Check-RepoStatus
Pull-LatestChanges
Check-MergeConflicts
Push-Changes
Display-Summary

Write-ColorMessage "`nThank you for using the Xtrium Platform GitHub Sync Script!" $CYAN

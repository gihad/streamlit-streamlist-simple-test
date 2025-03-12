import streamlit as st
import pandas as pd
from github import Github
from datetime import datetime, timedelta

# Function to fetch GitHub statistics
def fetch_github_statistics(org_name, token, start_date, end_date):
    g = Github(token)
    org = g.get_organization(org_name)
    repos = org.get_repos()

    repo_stats = []
    user_stats = {}
    for repo in repos:
        repo_stats.append({
            "name": repo.name,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "open_issues": repo.open_issues_count,
            "watchers": repo.watchers_count,
            "subscribers": repo.subscribers_count,
            "size": repo.size
        })

        # Fetch code review comments
        pulls = repo.get_pulls(state='all')
        for pr in pulls:
            if pr.created_at >= start_date and pr.created_at <= end_date:
                comments = pr.get_review_comments()
                for comment in comments:
                    user = comment.user.login
                    if user not in user_stats:
                        user_stats[user] = 0
                    user_stats[user] += 1

    return repo_stats, user_stats

# Streamlit app
st.title("Streamlit App")
st.write("Welcome to my Streamlit app!")

# GitHub API token input
token = st.text_input("Enter your GitHub API token:", type="password")

if token:
    org_name = "uken"
    
    # Date picker for selecting date range
    end_date = st.date_input("End date", datetime.now())
    start_date = st.date_input("Start date", datetime.now() - timedelta(days=7))
    
    stats, user_stats = fetch_github_statistics(org_name, token, start_date, end_date)
    
    st.write(f"GitHub Statistics for Organization: {org_name}")
    st.write(stats)
    
    st.write("User Statistics (Code Review Comments):")
    st.write(user_stats)
    
    # Display the user with the most code review comments
    if user_stats:
        top_reviewer = max(user_stats, key=user_stats.get)
        st.write(f"Top Reviewer: {top_reviewer} with {user_stats[top_reviewer]} comments")

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Student Performance Analysis", layout="wide")

# Load dataset
df = pd.read_csv("student_performance.csv")

# Calculate average score column upfront
df['average_score'] = df[['math_score', 'english_score', 'biology_score',
                          'physics_score', 'chemistry_score']].mean(axis=1)

# Sidebar Navigation Menu
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", [
    "Overview", 
    "Math Score Distribution", 
    "Study Hours vs Average Score", 
    "Summary Statistics",
    "Correlation Heatmap",
    "Score Distribution by Study Hour Group",
    "Top Performers",
    "Subject Score Comparison"
])

# Overview Section
if menu == "Overview":
    st.title("Student Performance Analysis")
    st.markdown("""
    This app analyzes student performance based on self-study hours and subject scores.
    You can explore:
    - Distribution of math scores
    - Relationship between weekly self-study hours and average scores
    - Summary statistics of the dataset
    - Correlation between variables
    - Score distribution by study hour groups
    - Top performing students
    - Average scores by subject
    
    Use the navigation panel on the left to explore each section.
    """)
    st.write("---")

# Math Score Distribution Section
elif menu == "Math Score Distribution":
    st.title("Distribution of Math Scores")

    min_hours = st.slider("Minimum Weekly Self-Study Hours", 0, 20, 5)
    filtered_df = df[df['weekly_self_study_hours'] >= min_hours]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(filtered_df['math_score'], bins=20, color='skyblue', edgecolor='black')
    ax.set_title('Distribution of Math Scores')
    ax.set_xlabel('Math Score')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

# Study Hours vs Average Score Section
elif menu == "Study Hours vs Average Score":
    st.title("Weekly Self-Study Hours vs Average Score")

    min_hours = st.slider("Minimum Weekly Self-Study Hours", 0, 20, 5)
    filtered_df = df[df['weekly_self_study_hours'] >= min_hours]

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=filtered_df, x='weekly_self_study_hours', y='average_score', ax=ax)
    ax.set_title("Weekly Self-Study Hours vs Average Score")
    ax.set_xlabel("Weekly Self-Study Hours")
    ax.set_ylabel("Average Score")
    st.pyplot(fig)

# Summary Statistics Section
elif menu == "Summary Statistics":
    st.title("Summary Statistics")

    min_hours = st.slider("Minimum Weekly Self-Study Hours", 0, 20, 0)
    filtered_df = df[df['weekly_self_study_hours'] >= min_hours]

    st.write(f"Showing summary statistics for students with at least {min_hours} weekly self-study hours.")
    st.dataframe(filtered_df.describe().T.style.format("{:.2f}"))

# Correlation Heatmap Section
elif menu == "Correlation Heatmap":
    st.title("Correlation Heatmap of Scores and Study Hours")

    corr_cols = ['math_score', 'english_score', 'biology_score', 'physics_score', 'chemistry_score', 'weekly_self_study_hours', 'average_score']
    corr = df[corr_cols].corr()

    fig, ax = plt.subplots(figsize=(10, 7))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    ax.set_title("Correlation Heatmap")
    st.pyplot(fig)

# Score Distribution by Study Hour Group Section
elif menu == "Score Distribution by Study Hour Group":
    st.title("Score Distribution by Study Hour Group")

    max_hours = df['weekly_self_study_hours'].max()

    # Fix for duplicate edges
    if max_hours <= 20:
        last_bin = 21
    else:
        last_bin = max_hours + 1

    bins = [0, 5, 10, 15, 20, last_bin]
    labels = ['0-5', '6-10', '11-15', '16-20', '21+']

    df['study_hour_group'] = pd.cut(df['weekly_self_study_hours'], bins=bins, labels=labels, include_lowest=True)

    subject = st.selectbox("Select Subject", ['math_score', 'english_score', 'biology_score', 'physics_score', 'chemistry_score'])

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x='study_hour_group', y=subject, ax=ax)
    ax.set_title(f"{subject.replace('_', ' ').title()} Distribution by Study Hour Group")
    ax.set_xlabel("Weekly Self-Study Hours Group")
    ax.set_ylabel(f"{subject.replace('_', ' ').title()} Score")
    st.pyplot(fig)


# Top Performers Section
elif menu == "Top Performers":
    st.title("Top Performing Students")

    threshold = st.slider("Minimum Average Score", 0, 100, 80)
    top_students = df[df['average_score'] >= threshold].sort_values(by='average_score', ascending=False)

    st.write(f"Students with average scores greater than or equal to {threshold}:")
    st.dataframe(top_students[['math_score', 'english_score', 'biology_score', 'physics_score', 'chemistry_score', 'average_score']])


# Subject Score Comparison Section
elif menu == "Subject Score Comparison":
    st.title("Average Scores by Subject")

    subjects = ['math_score', 'english_score', 'biology_score', 'physics_score', 'chemistry_score']
    avg_scores = df[subjects].mean().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=avg_scores.values, y=avg_scores.index, palette="viridis", ax=ax)
    ax.set_xlabel("Average Score")
    ax.set_ylabel("Subject")
    ax.set_title("Average Scores by Subject")
    st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("Developed by Khusbu Banjade | Student Performance Analysis Project")

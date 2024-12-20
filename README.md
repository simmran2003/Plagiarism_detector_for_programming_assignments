# Plagiarism Detection in Source Codes using ASTs

## Overview
This project, developed by Simmran Agarwal,Jatin Gupta and Aman Kulshrestha, focuses on detecting plagiarism in source codes using **Abstract Syntax Trees (ASTs)**. We implemented an algorithm that evaluates source codes based on three key features: **operation similarity**, **control flow similarity**, and **parameter similarity**. The system then constructs ASTs to facilitate accurate plagiarism detection.

We also built a platform called **Class Forge** using the MERN stack, designed to be a comprehensive solution for both students and teachers. It functions like Google Classroom, allowing teachers to post assignments, evaluate submissions, and check for plagiarism, while students can solve and submit assignments seamlessly.

## Features
- **AST Creation**: Automatically generates ASTs for each source code submission.
- **Feature-Based Evaluation**: Codes are evaluated on operation, control flow, and parameter similarity.
- **Plagiarism Detection**: Detects plagiarism by comparing ASTs of submitted codes.
- **Class Forge**: A platform built using the MERN stack for educational use, including assignment posting, evaluation, and plagiarism checking.

## How It Works
1. **AST Creation**: We parse the source code to generate its AST, capturing the structure and relationships between elements like functions, loops, and variables.
2. **Feature Extraction**: The code’s features are extracted, including basic blocks, control flow graphs, method characteristics, and variable occurrences.
3. **Plagiarism Check**: The ASTs of two codes are compared based on similarity metrics. If the similarity score exceeds a certain threshold, it is flagged as a potential plagiarism case.
4. **Class Forge Integration**: The system integrates with Class Forge, allowing teachers and students to interact with the plagiarism detection system seamlessly.

## Platform - Class Forge
- **Teacher Features**:
  - Post assignments with specific guidelines.
  - Evaluate student submissions with real-time plagiarism detection.
  - Generate reports on plagiarism findings.
- **Student Features**:
  - Submit assignments with code files.
  - View plagiarism reports.
  - Access learning resources and assignments.

## Project Setup
To set up this project locally, follow these steps:

### Prerequisites
- Python 3.x
- Node.js (for MERN stack setup)
- MongoDB (for database storage)
- Django (for backend services)
- React (for frontend development)
- Basic understanding of Git

### Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/simmran2003/Plagiarism_detector_for_programming_assignments
   cd Major_Project
2. **Run the Django Server**:
   ```bash
   python manage.py runserver
   
## Usage
### For Teachers:
Post assignments on the platform.
Use the built-in code editor to evaluate submissions.
Check for plagiarism by uploading multiple student submissions.
### For Students:
Solve and submit assignments directly through the platform.
Receive real-time plagiarism check results.

## Documentation
- [Project Documentation](https://drive.google.com/file/d/1KsZVZapVirh5D_6_0Fq4P8PEc5Znc7TR/view?usp=drive_link)- Link to the detailed documentation covering implementation specifics, algorithm details, and user guide.

## Demo Video
- [Watch the video demo here](https://drive.google.com/file/d/1QA_84t12iG9MGyhV9bQ22hpREKUIBOrC/view?usp=drive_link)

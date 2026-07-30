pipeline {
    agent any

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '30'))
    }

    environment {
        PROJECT_NAME = 'DevSecOps-MERN-Pipeline'
        PYTHONPATH   = '.'
    }

    stages {
        stage('Checkout Source Code') {
            steps {
                echo '=== Stage 1: Checkout Code from GitHub ==='
                checkout scm
            }
        }

        stage('Pre-Build Security Gate (PR Check)') {
            parallel {
                stage('Gitleaks Secrets Scan') {
                    steps {
                        echo '=== 1. Gitleaks: Scanning Git History for Secrets ==='
                        sh './security/run_pipeline.sh pre-build gitleaks'
                    }
                }
                stage('Hadolint Dockerfile Linter') {
                    steps {
                        echo '=== 2. Hadolint: Linting Dockerfiles Before Build ==='
                        sh './security/run_pipeline.sh pre-build hadolint'
                    }
                }
            }
        }

        stage('Build MERN Application Containers') {
            steps {
                echo '=== Stage 2: Building Containers via Docker Compose ==='
                sh 'docker-compose build'
            }
        }

        stage('Post-Build Container Vulnerability Scan') {
            steps {
                echo '=== Stage 3: Trivy Image CVE Scan ==='
                sh './security/run_pipeline.sh post-build trivy'
            }
        }

        stage('Orchestrator Gate, Risk Engine & Reporting') {
            steps {
                echo '=== Stage 4: Orchestrator Gate Evaluation & HTML/PDF Report Generation ==='
                sh './security/run_pipeline.sh gate'
            }
        }
    }

    post {
        always {
            echo '=== Post-Pipeline: Archiving All Compliance & Security Reports in Jenkins UI ==='
            archiveArtifacts artifacts: 'compliance/reports/**/*', allowEmptyArchive: true
            archiveArtifacts artifacts: 'compliance/master_reports/**/*', allowEmptyArchive: true
        }
        success {
            echo '✅ DEVSECOPS PIPELINE PASSED: All Security & Policy Checks Satisfied!'
        }
        failure {
            echo '❌ DEVSECOPS PIPELINE FAILED: Security Gate or Policy Violation Detected.'
        }
    }
}

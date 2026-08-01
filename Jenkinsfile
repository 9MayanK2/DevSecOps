pipeline {
    agent any

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '30'))
    }

    environment {
        PROJECT_NAME = 'SentinelOps'
        PYTHONPATH   = '.'
    }

    stages {
        stage('Checkout Source Code') {
            steps {
                echo '=== Stage 1: Checkout Code from GitHub ==='
                checkout scm
            }
        }
	
	stage('Generating Backend Environment') {
	   steps {
		echo '============Generating .env ===================='
		withCredentials([
                    string(credentialsId: 'MONGO_URL', variable: 'MONGO_URL'),
                    string(credentialsId: 'JWT_SECRET', variable: 'JWT_SECRET'),
                    string(credentialsId: 'EMAIL_USER', variable: 'EMAIL_USER'),
                    string(credentialsId: 'EMAIL_PASS', variable: 'EMAIL_PASS')
                ]){
		sh '''
                    cat > app/server/.env <<EOF
PORT=5000
MONGO_URL=${MONGO_URL}
JWT_SECRET=${JWT_SECRET}
EMAIL_USER=${EMAIL_USER}
EMAIL_PASS=${EMAIL_PASS}
EOF
                    '''
		}
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

        stage('DAST Web Vulnerability Scan') {
            steps {
                echo '=== Stage 4: OWASP ZAP DAST Scanning Live Endpoints ==='
                sh './security/run_pipeline.sh dast zap'
            }
        }

        stage('Orchestrator Gate, Risk Engine & Reporting') {
            steps {
                echo '=== Stage 5: Orchestrator Gate Evaluation & HTML/PDF Report Generation ==='
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

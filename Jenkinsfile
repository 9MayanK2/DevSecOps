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

        /********************************************************************
         * Stage 1 : Checkout Source
         ********************************************************************/
        stage('Checkout Source Code') {
            steps {
                echo '========== CHECKOUT SOURCE =========='
                checkout scm
            }
        }

        /********************************************************************
         * Stage 2 : Generate Backend Environment
         ********************************************************************/
        stage('Generate Backend Environment') {
            steps {
                echo '========== GENERATING .ENV =========='
                withCredentials([
                    string(credentialsId: 'MONGO_URL', variable: 'MONGO_URL'),
                    string(credentialsId: 'JWT_SECRET', variable: 'JWT_SECRET'),
                    string(credentialsId: 'EMAIL_USER', variable: 'EMAIL_USER'),
                    string(credentialsId: 'EMAIL_PASS', variable: 'EMAIL_PASS')
                ]) {
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

        /********************************************************************
         * Stage 3 : Cleanup Previous Build
         ********************************************************************/
        stage('Cleanup Previous Deployment') {
            steps {
                echo '========== CLEANUP =========='
                sh 'docker-compose down --remove-orphans || true'
            }
        }

        /********************************************************************
         * Stage 4 : Pre-Build Security
         ********************************************************************/
        stage('Pre-Build Security Scans') {
            parallel {
                stage('Gitleaks Secrets Scan') {
                    steps {
                        echo '========== GITLEAKS =========='
                        sh './security/run_pipeline.sh pre-build gitleaks'
                    }
                }

                stage('Hadolint Dockerfile Scan') {
                    steps {
                        echo '========== HADOLINT =========='
                        sh './security/run_pipeline.sh pre-build hadolint'
                    }
                }
            }
        }

        /********************************************************************
         * Stage 5 : Build Images
         ********************************************************************/
        stage('Build Docker Images') {
            steps {
                echo '========== BUILDING DOCKER IMAGES =========='
                sh 'docker-compose build'
            }
        }

        /********************************************************************
         * Stage 6 : Trivy Scan
         ********************************************************************/
        stage('Trivy Container Scan') {
            steps {
                echo '========== TRIVY =========='
                sh './security/run_pipeline.sh post-build trivy'
            }
        }

        /********************************************************************
         * Stage 7 : Start Containers
         ********************************************************************/
        stage('Start MERN Application') {
            steps {
                echo '========== STARTING APPLICATION =========='
                sh 'docker-compose up -d --force-recreate'
            }
        }

        /********************************************************************
         * Stage 8 : Health Check
         ********************************************************************/
        stage('Application Health Check') {
            steps {
                echo '========== WAITING FOR BACKEND =========='
                sh '''
                for i in {1..30}
                do
                    if curl -fs http://localhost:5000/health > /dev/null
                    then
                        echo "Backend is healthy."
                        exit 0
                    fi
                    echo "Waiting for backend..."
                    sleep 5
                done
                echo "Backend failed to start."
                exit 1
                '''
            }
        }

        /********************************************************************
         * Stage 9 : OWASP ZAP
         ********************************************************************/
        stage('OWASP ZAP DAST Scan') {
            steps {
                echo '========== OWASP ZAP =========='
                sh './security/run_pipeline.sh dast zap'
            }
        }

        /********************************************************************
         * Stage 10 : Generate Security Reports
         ********************************************************************/
        stage('Generate Security Reports') {
            steps {
                echo '========== GENERATING REPORTS =========='
                sh './security/run_pipeline.sh report'
            }
        }

        /********************************************************************
         * Stage 11 : Security Gate Evaluation
         ********************************************************************/
        stage('Security Gate Evaluation') {
            steps {
                echo '========== SECURITY GATE EVALUATION =========='
                sh './security/run_pipeline.sh gate'
            }
        }

        /********************************************************************
         * Stage 12 : Cosign PKI Digital Signing (Post-Gate)
         ********************************************************************/
        stage('Cosign PKI Digital Signing') {
            steps {
                echo '========== COSIGN DIGITAL SIGNING =========='
                sh './security/run_pipeline.sh sign'
            }
        }

        /********************************************************************
         * Stage 13 : Cosign Signature Verification (Post-Gate)
         ********************************************************************/
        stage('Verify Digital Signatures') {
            steps {
                echo '========== SIGNATURE VERIFICATION =========='
                sh './security/run_pipeline.sh verify'
            }
        }

        /********************************************************************
         * Stage 14 : Publish Images to Amazon ECR (Reserved)
         ********************************************************************/
        stage('Publish Images to Amazon ECR') {
            steps {
                echo '========== PUBLISHING TO AMAZON ECR =========='
                sh '''
                # Future implementation: AWS ECR Login & Docker Push
                echo "[INFO] ECR Stage reserved for AWS integration."
                '''
            }
        }

    }

    /********************************************************************
     * POST ACTIONS
     ********************************************************************/
    post {
        always {
            echo '========== CLEANING UP =========='
            sh 'docker-compose down --remove-orphans || true'

            echo '========== ARCHIVING REPORTS & SIGNATURES =========='
            archiveArtifacts artifacts: 'compliance/reports/**/*', allowEmptyArchive: true
            archiveArtifacts artifacts: 'compliance/master_reports/**/*', allowEmptyArchive: true
            archiveArtifacts artifacts: 'compliance/logs/**/*', allowEmptyArchive: true
            archiveArtifacts artifacts: 'compliance/reports/signing/**/*', allowEmptyArchive: true
        }

        success {
            echo '''
==================================================
      SENTINELOPS PIPELINE COMPLETED SUCCESSFULLY
==================================================
            '''
        }

        failure {
            echo '''
==================================================
      SENTINELOPS PIPELINE FAILED
==================================================
            '''
        }
    }
}

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
                echo '========== CHECKOUT =========='
                checkout scm
            }
        }

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

        stage('Pre-Build Security Scans') {

            parallel {

                stage('Gitleaks') {
                    steps {
                        echo '========== GITLEAKS =========='
                        sh './security/run_pipeline.sh pre-build gitleaks'
                    }
                }

                stage('Hadolint') {
                    steps {
                        echo '========== HADOLINT =========='
                        sh './security/run_pipeline.sh pre-build hadolint'
                    }
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                echo '========== BUILD =========='
                sh 'docker-compose build'
            }
        }

        stage('Trivy Image Scan') {
            steps {
                echo '========== TRIVY =========='
                sh './security/run_pipeline.sh post-build trivy'
            }
        }

        stage('Start MERN Application') {
            steps {
                echo '========== START APPLICATION =========='
                sh 'docker-compose up -d'
            }
        }

        stage('Application Health Check') {
            steps {
                echo '========== WAITING FOR BACKEND =========='

                sh '''
                timeout=120

                until curl -f http://localhost:5000/health
                do
                    timeout=$((timeout-5))

                    if [ $timeout -le 0 ]; then
                        echo "Backend failed to start."
                        exit 1
                    fi

                    sleep 5
                done
                '''
            }
        }

        stage('OWASP ZAP DAST Scan') {
            steps {
                echo '========== OWASP ZAP =========='
                sh './security/run_pipeline.sh dast zap'
            }
        }

        stage('Generate Reports') {
            steps {
                echo '========== GENERATING REPORTS =========='

                /*
                 * Generates:
                 *  - Master Report
                 *  - Executive Report
                 *  - HTML Report
                 *  - PDF Report
                 *  - Compliance Matrix
                 *
                 * Does NOT enforce Security Gate.
                 */

                sh './security/run_pipeline.sh report'
            }
        }

    }

    post {

        always {

            echo '========== STOPPING APPLICATION =========='

            sh '''
            docker-compose down || true
            '''

            echo '========== ARCHIVING REPORTS =========='

            archiveArtifacts artifacts: 'compliance/reports/**/*', allowEmptyArchive: true
            archiveArtifacts artifacts: 'compliance/master_reports/**/*', allowEmptyArchive: true
        }

        success {
            echo '✅ SentinelOps Pipeline Completed Successfully.'
        }

        failure {
            echo '❌ SentinelOps Pipeline Failed.'
        }
    }
}

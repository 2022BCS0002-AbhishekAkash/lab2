pipeline {
    agent any

    environment {
        REPO_URL     = "https://github.com/2022BCS0002-AbhishekAkash/lab2.git"
        BRANCH_NAME  = "main"
        IMAGE_NAME   = "abhishekakash/wine_predict_2022bcs0002"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: "${BRANCH_NAME}",
                    credentialsId: 'git-creds',
                    url: "${REPO_URL}"
            }
        }

        stage('Setup Python Virtual Environment') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Train Model') {
            steps {
                sh '''
                . venv/bin/activate
                python train.py
                '''
            }
        }

        stage('Read Accuracy') {
            steps {
                script {
                    def metrics = readJSON file: 'outputs/results.json'
                    env.CURRENT_ACC = metrics.accuracy.toString()
                    echo "Current Accuracy: ${env.CURRENT_ACC}"
                }
            }
        }

        stage('Compare Accuracy') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'best-accuracy', variable: 'BEST_ACC')]) {

                        echo "Best Accuracy Stored in Jenkins: ${BEST_ACC}"

                        if (env.CURRENT_ACC.toFloat() <= BEST_ACC.toFloat()) {
                            error("❌ 2022BCS0002 ---- Accuracy did not improve. Stopping pipeline.")
                        } else {
                            echo "✅ Accuracy improved. Proceeding to Docker build + push."
                        }
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.withRegistry('', 'dockerhub-creds') {
                        sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
                        sh "docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest"
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('', 'dockerhub-creds') {
                        sh "docker push ${IMAGE_NAME}:${BUILD_NUMBER}"
                        sh "docker push ${IMAGE_NAME}:latest"
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'outputs/**', fingerprint: true
        }
        success {
            echo "✅ Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed!"
        }
    }
}

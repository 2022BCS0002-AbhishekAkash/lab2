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

        stage('Read Metric (Best R2)') {
            steps {
                script {
                    def metrics = readJSON file: 'outputs/results.json'

                    double bestR2 = -9999.0

                    metrics.each { modelName, values ->
                        if (values != null && values.r2 != null) {
                            double r2Value = values.r2 as Double

                            if (r2Value > bestR2) {
                                bestR2 = r2Value
                            }
                        }
                    }

                    env.CURRENT_R2 = bestR2.toString()
                    echo "Best R2 Score (Current Run): ${env.CURRENT_R2}"
                }
            }
        }

        stage('Compare With Best Metric') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'best-accuracy', variable: 'BEST_R2')]) {

                        echo "Best R2 Stored in Jenkins: (hidden)"

                        if (env.CURRENT_R2.toFloat() <= BEST_R2.toFloat()) {
                            error("❌ 2022BCS0002 ---- R2 Score did not improve. Stopping pipeline.")
                        } else {
                            echo "✅ R2 Score improved. Proceeding to Docker build + push."
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

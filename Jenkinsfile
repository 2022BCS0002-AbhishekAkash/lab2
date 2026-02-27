pipeline {
    agent any

    environment {
        IMAGE_NAME     = "abhishekakash/wine_predict_2022bcs0002:latest"
        CONTAINER_NAME = "wine-api-test"
    }

    stages {

        stage('Clean Old Container') {
            steps {
                sh "docker stop ${CONTAINER_NAME} || true"
                sh "docker rm ${CONTAINER_NAME} || true"
            }
        }

        stage('Pull Image') {
            steps {
                sh "docker pull ${IMAGE_NAME}"
            }
        }

        stage('Run Container') {
            steps {
                sh """
                docker run -d \
                --name ${CONTAINER_NAME} \
                -p 8000:8000 \
                ${IMAGE_NAME}
                """
            }
        }

        stage('Wait for Service Readiness') {
            steps {
                script {
                    sleep 10
                }
            }
        }

        stage('Send Valid Inference Request') {
            steps {
                sh """
                python - <<EOF
import requests
import sys

url = "http://localhost:8000/predict"

data = {
    "fixed_acidity": 7.4,
    "volatile_acidity": 0.7,
    "citric_acid": 0.0,
    "residual_sugar": 1.9,
    "chlorides": 0.076,
    "free_sulfur_dioxide": 11.0,
    "total_sulfur_dioxide": 34.0,
    "density": 0.9978,
    "pH": 3.51,
    "sulphates": 0.56,
    "alcohol": 9.4
}

r = requests.post(url, json=data)

if r.status_code != 200:
    sys.exit(1)

if "prediction" not in r.json():
    sys.exit(1)
EOF
                """
            }
        }

        stage('Send Invalid Request') {
            steps {
                sh """
                python - <<EOF
import requests
import sys

url = "http://localhost:8000/predict"

data = {
    "fixed_acidity": "wrong"
}

r = requests.post(url, json=data)

if r.status_code == 200:
    sys.exit(1)
EOF
                """
            }
        }

        stage('Stop Container') {
            steps {
                sh "docker stop ${CONTAINER_NAME}"
                sh "docker rm ${CONTAINER_NAME}"
            }
        }
    }
}
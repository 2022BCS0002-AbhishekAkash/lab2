pipeline {
    agent any

    environment {
        IMAGE_NAME     = "abhishekakash/wine_predict_2022bcs0002:latest"
        CONTAINER_NAME = "wine-api-test"
        PORT           = "8000"
    }

    stages {

        stage('Pull Image') {
            steps {
                sh "docker pull ${IMAGE_NAME}"
            }
        }

        stage('Run Container') {
            steps {
                sh """
                docker run -d -p ${PORT}:8000 \
                --name ${CONTAINER_NAME} \
                ${IMAGE_NAME}
                """
            }
        }

        stage('Wait for Service Readiness') {
            steps {
                script {
                    echo "Waiting for API to start..."
                    sleep 15
                }
            }
        }

        stage('Send Valid Inference Request') {
            steps {
                sh '''
                echo "Sending valid request..."

                RESPONSE=$(curl -s -w "\\n%{http_code}" \
                -X POST http://localhost:8000/predict \
                -H "Content-Type: application/json" \
                -d @valid_input.json)

                BODY=$(echo "$RESPONSE" | head -n 1)
                STATUS=$(echo "$RESPONSE" | tail -n 1)

                echo "Status Code: $STATUS"
                echo "Response Body: $BODY"

                if [ "$STATUS" != "200" ]; then
                    echo "❌ Valid request failed"
                    exit 1
                fi

                echo "$BODY" | grep prediction
                '''
            }
        }

        stage('Send Invalid Request') {
            steps {
                sh '''
                echo "Sending invalid request..."

                RESPONSE=$(curl -s -w "\\n%{http_code}" \
                -X POST http://localhost:8000/predict \
                -H "Content-Type: application/json" \
                -d @invalid_input.json)

                STATUS=$(echo "$RESPONSE" | tail -n 1)

                echo "Invalid Request Status Code: $STATUS"

                if [ "$STATUS" = "200" ]; then
                    echo "❌ Invalid request should NOT succeed"
                    exit 1
                fi
                '''
            }
        }

        stage('Stop Container') {
            steps {
                sh "docker stop ${CONTAINER_NAME} || true"
                sh "docker rm ${CONTAINER_NAME} || true"
            }
        }
    }

    post {
        success {
            echo "✅ Inference Validation Pipeline PASSED"
        }
        failure {
            echo "❌ Inference Validation Pipeline FAILED"
        }
        always {
            sh "docker stop ${CONTAINER_NAME} || true"
            sh "docker rm ${CONTAINER_NAME} || true"
        }
    }
}
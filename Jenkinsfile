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
                docker run -d --network host \
                --name ${CONTAINER_NAME} \
                ${IMAGE_NAME}
                """
            }
        }

        stage('Wait for Service Readiness') {
            steps {
                script {
                    echo "Checking API readiness..."

                    timeout(time: 1, unit: 'MINUTES') {
                        waitUntil {
                            def status = sh(
                                script: "curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/",
                                returnStdout: true
                            ).trim()

                            return (status == "200")
                        }
                    }

                    echo "API is ready ✅"
                }
            }
        }

        stage('Send Valid Inference Request') {
            steps {
                sh """
                RESPONSE=\$(curl -s -w "\\n%{http_code}" \
                -X POST http://localhost:8000/predict \
                -H "Content-Type: application/json" \
                -d @valid_input.json)

                BODY=\$(echo "\$RESPONSE" | head -n 1)
                STATUS=\$(echo "\$RESPONSE" | tail -n 1)

                if [ "\$STATUS" != "200" ]; then
                    exit 1
                fi

                echo "\$BODY" | grep prediction > /dev/null
                if [ \$? -ne 0 ]; then
                    exit 1
                fi
                """
            }
        }

        stage('Send Invalid Request') {
            steps {
                sh """
                RESPONSE=\$(curl -s -w "\\n%{http_code}" \
                -X POST http://localhost:8000/predict \
                -H "Content-Type: application/json" \
                -d @invalid_input.json)

                STATUS=\$(echo "\$RESPONSE" | tail -n 1)

                if [ "\$STATUS" = "200" ]; then
                    exit 1
                fi
                """
            }
        }

        stage('Stop Container') {
            steps {
                sh "docker stop ${CONTAINER_NAME} || true"
                sh "docker rm ${CONTAINER_NAME} || true"
            }
        }
    }
}



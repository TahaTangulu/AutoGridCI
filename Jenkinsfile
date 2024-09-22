pipeline {
    agent any

    parameters {
        string(name: 'BUILD_NAME', defaultValue: 'Build_Name_1', description: 'Set Build Name')
        choice(name: 'NODE_COUNT', choices: ['1', '2', '3', '4', '5'], description: 'Select node count')
    }

    environment {
        WEBHOOK_URL = "https://webhook.site/db172d7c-ecf7-48b3-ae8b-a1d6be599869"
        GRID_STATUS_URL = "http://localhost:4444/status"
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/TahaTangulu/AutoGridCI.git'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'python3 run_tests.py ${NODE_COUNT}'
            }
        }
        stage('Check Grid Status and Send to Webhook') {
            steps {
                script {
                    def gridStatus = sh(script: "curl -s ${GRID_STATUS_URL}", returnStdout: true)
                    sh(script: """
                        curl -X POST -H "Content-Type: application/json" \
                        -d '${gridStatus}' ${WEBHOOK_URL}
                    """)
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'test-results.json', allowEmptyArchive: true, fingerprint: true
        }
    }
}

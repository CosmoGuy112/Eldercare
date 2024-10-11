pipeline {
    agent any
    environment {
        POSTGRES_NAME = 'eldercare'
        POSTGRES_USER = 'postgres'
        POSTGRES_PASSWORD = 'guyza1234*'
        POSTGRES_HOST = 'db'
        POSTGRES_PORT = '5432'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out repository...'
                git url: 'https://github.com/aomati145/Devtools.git',
                    branch: 'master',
                    credentialsId: 'github'
            }
        }

        stage('Create .env File') {
            steps {
                script {
                    sh '''
                        cat <<EOF > .env
                        POSTGRES_NAME=${POSTGRES_NAME}
                        POSTGRES_USER=${POSTGRES_USER}
                        POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
                        POSTGRES_HOST=${POSTGRES_HOST}
                        POSTGRES_PORT=${POSTGRES_PORT}
                        EOF
                    '''
                    echo '.env file created.'
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    sh 'docker compose build'
                }
            }
        }

        stage('Run Docker Containers') {
            steps {
                script {
                    sh 'docker compose up -d'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline execution failed.'
        }
        always {
            echo 'Pipeline execution completed.'
        }
    }
}
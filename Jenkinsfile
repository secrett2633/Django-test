pipeline {
    agent any
    
    environment {
        DOCKER_COMPOSE_VERSION = '3.8'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build and Deploy') {
            steps {
                bash '''
                    docker compose down
                    docker compose pull
                    docker compose up --build -d
                '''
            }
        }
        
        stage('Health Check') {
            steps {
                script {
                    sleep 30  // 서비스 시작 대기
                    bash 'docker compose ps'
                }
            }
        }
    }
    
    post {
        failure {
            bash 'docker compose logs'
        }
    }
}
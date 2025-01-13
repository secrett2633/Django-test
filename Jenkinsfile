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
                script {
                    bat 'docker-compose down'
                    bat 'docker-compose pull'
                    bat 'docker-compose up --build -d'
                }
            }
        }
        
        stage('Health Check') {
            steps {
                script {
                    sleep 30  // 서비스 시작 대기
                    bat 'docker-compose ps'
                }
            }
        }
    }
    
    post {
        failure {
            script {
                bat 'docker-compose logs'
            }
        }
    }
}
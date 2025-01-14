pipeline {
    agent any
    
    environment {
        DOCKER_COMPOSE_VERSION = '3.8'
        WORKSPACE = "${env.WORKSPACE}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Start Infrastructure') {
            steps {
                script {
                    // 기본 인프라 시작 (Nginx, Postgres, Redis)
                    bat 'docker-compose up -d'
                }
            }
        }
        
        stage('Determine Deploy Target') {
            steps {
                script {
                    def blueContainerExists = bat(script: 'docker ps -q -f name=test-dev-blue', returnStdout: true).trim()
                    
                    env.CURRENT_COLOR = blueContainerExists ? 'blue' : 'green'
                    env.DEPLOY_COLOR = blueContainerExists ? 'green' : 'blue'
                    env.CURRENT_PORT = blueContainerExists ? '8000' : '8001'
                    env.DEPLOY_PORT = blueContainerExists ? '8001' : '8000'
                    
                    echo "Current running on ${env.CURRENT_COLOR} with port ${env.CURRENT_PORT}"
                    echo "Deploying to ${env.DEPLOY_COLOR} with port ${env.DEPLOY_PORT}"
                }
            }
        }
        
        stage('Deploy New Version') {
            steps {
                script {
                    // 새로운 버전 배포 (기본 compose 파일과 함께 실행)
                    bat "docker-compose -f docker-compose.yml -f docker-compose.${env.DEPLOY_COLOR}.yml up -d --build"
                }
            }
        }
        
        stage('Health Check') {
            steps {
                script {
                    def maxAttempts = 10
                    def attempts = 0
                    def healthy = false
                    
                    while (!healthy && attempts < maxAttempts) {
                        attempts++
                        try {
                            def response = bat(
                                script: "curl -s http://localhost:${env.DEPLOY_PORT}/api/v1/test",
                                returnStdout: true
                            ).trim()
                            
                            if (response) {
                                healthy = true
                                echo "New version is healthy!"
                            }
                        } catch (Exception e) {
                            echo "Attempt ${attempts}/${maxAttempts} failed"
                            if (attempts < maxAttempts) {
                                sleep 10
                            }
                        }
                    }
                    
                    if (!healthy) {
                        error "New version failed health check after ${maxAttempts} attempts"
                    }
                }
            }
        }
        
        stage('Switch Traffic') {
            steps {
                script {
                    // Nginx 설정 업데이트
                    bat """
                        echo upstream app { > ${WORKSPACE}/nginx/service-url.inc
                        echo     server localhost:${env.DEPLOY_PORT}; >> ${WORKSPACE}/nginx/service-url.inc
                        echo } >> ${WORKSPACE}/nginx/service-url.inc
                    """
                    
                    // Nginx 재시작
                    bat 'docker exec test-proxy nginx -s reload'
                }
            }
        }
        
        stage('Cleanup Old Version') {
            steps {
                script {
                    if (env.CURRENT_COLOR != null) {
                        // 이전 버전이 있다면 종료 (기본 compose 파일과 함께 실행)
                        bat "docker-compose -f docker-compose.${env.CURRENT_COLOR}.yml down"
                    }
                }
            }
        }
    }
    
    post {
        failure {
            script {
                // 배포 실패시 로그 확인
                bat "docker-compose -f docker-compose.yml -f docker-compose.${env.DEPLOY_COLOR}.yml logs"
                
                // 롤백 - 새 버전 종료
                bat "docker-compose -f docker-compose.yml -f docker-compose.${env.DEPLOY_COLOR}.yml down"
                
                // Nginx 설정 원복
                if (env.CURRENT_COLOR) {
                    bat """
                        echo upstream app { > ${WORKSPACE}/nginx/service-url.inc
                        echo     server localhost:${env.CURRENT_PORT}; >> ${WORKSPACE}/nginx/service-url.inc
                        echo } >> ${WORKSPACE}/nginx/service-url.inc
                    """
                    bat "docker exec test-proxy nginx -s reload"
                }
            }
        }
    }
}
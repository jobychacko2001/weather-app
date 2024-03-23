pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('docker_cred')
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python3 manage.py test'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("jobychacko/weather-app:${env.BUILD_ID}")
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                echo 'Testing..'
                withCredentials([usernamePassword(credentialsId: 'docker_cred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        
                        docker tag jobychacko/weather-app:${env.BUILD_ID} jobychacko/weather-app:latest
                        docker push jobychacko/weather-app:latest
                    """
                }
            }
        }
    }
}

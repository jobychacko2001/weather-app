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
                echo 'env.BUILD_ID'
                    withCredentials([usernamePassword(credentialsId: 'docker_cred', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                      sh '''
                        docker login -u $USERNAME -p $PASSWORD'
                        docker tag source-image:tag use-name/repo-name:tag
                        docker push use-name/repo-name:tag
                        '''
                }
            }
        }
    }
}

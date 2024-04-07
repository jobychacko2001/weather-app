pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('docker_cred')
        EC2_CREDENTIALS = credentials('ec2_cred')
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
        stage('Deploy to EC2') {
            steps {
                sshagent(credentials: ['ec2_cred']) {
                    script {
                        // Execute the deployment command and capture the exit code
                        env.DEPLOYMENT_EXIT_CODE = sh(script: """
                            ssh -o StrictHostKeyChecking=no -i ${env.KEY_PATH} ubuntu@${env.EC2_IP} '
                                docker pull jobychacko/weather-app:latest
                                docker run -d -p 8000:8000 jobychacko/weather-app:latest
                                echo $?
                            '
                        """, returnStdout: true).trim()
                    }
                }
            }
        } 
        stage('Check Deployment Status') {
            steps {
                script {
                    // Use the stored exit code to determine the deployment status
                    if (env.DEPLOYMENT_EXIT_CODE.toInteger() != 0) {
                        error("Deployment failed with exit code: ${env.DEPLOYMENT_EXIT_CODE}")
                    }
                }
            }
        }
    }
}

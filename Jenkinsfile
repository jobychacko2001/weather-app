pipeline {
    agent any

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
                    dockerImage = docker.build("env.DOCKERHUB_USERNAME/weather-app")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker_cred', usernameVariable: 'env.DOCKERHUB_USERNAME', passwordVariable: 'env.DOCKERHUB_PASSWORD')]) {
                        sh '''
                        docker login -u $DOCKERHUB_USERNAME -p $DOCKERHUB_PASSWORD
                        docker push DOCKERHUB_USERNAME/weather-app
                        '''
                    }
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: 'ec2_cred', keyFileVariable: 'EC2_SSH_KEY')]) {
                        sh '''
                        ssh -i $EC2_SSH_KEY ec2-user@your-ec2-ip-address <<EOF
                        docker pull your-dockerhub-username/your-repo-name:your-tag-name
                        docker run -d -p 8000:8000 your-dockerhub-username/your-repo-name:your-tag-name
                        EOF
                        '''
                    }
                }
            }
        }
    }
}

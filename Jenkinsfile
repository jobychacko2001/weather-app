pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('docker_cred')
        //EC2_CREDENTIALS = credentials('ec2_cred')
        privateKey = credentials('dev_server_cred')
        //GIT_CREDENTIALS = credentials('git_cred')
        EC2_PROD_Key = credentials('EC2_PROD_Key')
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
       
        stage('Deploy to DEV_EC2') {
            steps {
                
                    script {
                         
                        // Execute the deployment command and capture the exit code
                        def deploymentOutput = sh(script: """
                        ssh -v -o StrictHostKeyChecking=no -i ${privateKey} ubuntu@${env.EC2_IP} '
                          sudo docker pull jobychacko/weather-app:latest
                          sudo docker run -d -p 8000:8000 jobychacko/weather-app:latest
                          echo \$? 
                        '
                      """, returnStdout: true).trim()
                        def lines = deploymentOutput.split("\\n")
                        def exitCodeLine = lines[-1]
                        env.DEPLOYMENT_EXIT_CODE = exitCodeLine.trim()
                    }
                }
            }
         
        stage('Check Deployment Status') {
            steps {
                script {
                    // Use the stored exit code to determine the deployment status
                   if (env.DEPLOYMENT_EXIT_CODE != null && env.DEPLOYMENT_EXIT_CODE.isInteger()) {
                    if (env.DEPLOYMENT_EXIT_CODE.toInteger() != 0) {
                        error("Deployment failed with exit code: ${env.DEPLOYMENT_EXIT_CODE}")
                    }
                } else {
                    error("Invalid deployment exit code: ${env.DEPLOYMENT_EXIT_CODE}")
                }

                }
            }
        }
         stage('Merge to Master') {
    when {
        // This stage is executed only if DEPLOYMENT_EXIT_CODE is 0
        expression { return env.DEPLOYMENT_EXIT_CODE.toInteger() == 0 }
    }
            steps {
                script {
                    withCredentials([string(credentialsId: 'git_cred', variable: 'GIT_TOKEN')]){
                        // Configure remote with access token for authentication
                        sh """
                            git remote set-url origin https://x-access-token:${GIT_TOKEN}@github.com/jobychacko2001/weather-app.git
                        """
        
                        // Merge main branch into master
                        sh """
                            git fetch --all
                            git checkout master
                            git pull origin master
                            git merge origin/main --no-ff -m "Merge main into master by Jenkins"
                        """
        
                        // Push the changes back to the master branch
                        sh """
                            git push origin master
                        """
                    }
                }
            }
        }

            stage('Deploy to PROD_EC2') {
                steps {
                    script {
                        // Execute the deployment command
                        sh(script: """
                            ssh -v -o StrictHostKeyChecking=no -i ${EC2_PROD_Key} ubuntu@${env.EC2_PROD_IP} '
                              sudo docker pull jobychacko/weather-app:latest
                              sudo docker run -d -p 8000:8000 jobychacko/weather-app:latest
                            '
                        """, returnStdout: true).trim()
                    }
                }
            }

         
    }
}

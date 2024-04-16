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
       
        stage('Deploy and Test on DEV_EC2') {
    steps {
        script {
            // Start the Docker container
            sh """
    ssh -v -o StrictHostKeyChecking=no -i ${privateKey} ubuntu@${env.EC2_IP} '
        # Get the container ID of any container running on port 8000
                        container_id=\$(docker ps --filter "publish=8000" -q)

                        # If a container is running on port 8000, stop and remove it
                        if [ ! -z "\$container_id" ]; then
                            echo "Stopping and removing container on port 8000..."
                            docker stop \$container_id
                            docker rm \$container_id
                            echo "Container \$container_id has been stopped and removed."
                        else
                            echo "No container is running on port 8000."
                        fi

                        # Pull the latest Docker image
                        docker pull jobychacko/weather-app:latest

                        # Start the Docker container on port 8000
                        docker run -d -p 8000:8000 jobychacko/weather-app:latest
    '
        """
            sh 'sleep 10'
            // Execute Selenium tests against the Docker container on the development server
            def testResult = sh (
                script: """
                    ssh -o StrictHostKeyChecking=no -i ${privateKey} ubuntu@${env.EC2_IP} 'bash -sx' << 'EOF'
                        containerId=\$(sudo docker ps -qf "ancestor=jobychacko/weather-app:latest")
                        sudo docker exec \$containerId python3 /app/selenium_test.py
                    EOF
                """,
                returnStatus: true
            )
            echo "Test Result: ${testResult}"
            // Store the test result
            env.TEST_RESULT = testResult
            
        }
    }
}

         stage('Merge to Master') {
    when {
        // This stage is executed only if DEPLOYMENT_EXIT_CODE is 0
        expression { return env.TEST_RESULT.toInteger() == 0 }
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
                              # Get the container ID of any container running on port 8000
                        container_id=\$(docker ps --filter "publish=8000" -q)

                        # If a container is running on port 8000, stop and remove it
                        if [ ! -z "\$container_id" ]; then
                            echo "Stopping and removing container on port 8000..."
                            docker stop \$container_id
                            docker rm \$container_id
                            echo "Container \$container_id has been stopped and removed."
                        else
                            echo "No container is running on port 8000."
                        fi

                        # Pull the latest Docker image
                        docker pull jobychacko/weather-app:latest

                        # Start the Docker container on port 8000
                        docker run -d -p 8000:8000 jobychacko/weather-app:latest
                            '
                        """)
                    }
                }
            }

         
    }
}

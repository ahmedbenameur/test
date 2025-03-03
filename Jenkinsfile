pipeline {
    agent any
    environment {
        SONAR_HOST_URL = 'http://sonarqube:9000'
        SONAR_TOKEN = 'sqp_b1467b24b33dd569eb9ebccb9d4e24f55680e096'
    }
    stages {
        stage('Checkout Code') {
            steps {
                script {
                    echo ":inbox_tray: Cloning repository: rsu_1"
                }
                git branch: 'rsu_1', url: 'https://github.com/ahmedbenameur/test.git'
            }
        }

       stage('Export Joget App as .jwa') {
            steps {
                script {
                    // Replace 'app_x' with the actual app folder name, e.g. 'rsu_1'
                    sh '''
                    # Navigate to the app folder and create the .jwa file manually
                    docker exec -it -u root jogetapp bash -c " cd /opt/joget/wflow/app_src/rsu/rsu_1 && zip -r /opt/joget/wflow/rsu_1.jwa *"
                    '''
                }
            }
        }

        stage('Copy .jwa to Host') {
            steps {
                script {
                    // Replace 'container_id' with the actual container ID or name
                    // Copy the .jwa file from the container to the host
                    sh '''
                    docker cp joget:/opt/joget/wflow/app_src/rsu/rsu_1.jwa .
                    '''
                }
            }
        }
    }
}

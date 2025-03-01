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

       stage('Prepare SonarQube Scanner') {
    steps {
        script {
            echo ":mag: Checking if SonarQube Scanner is installed..."
        }
        sh '''
            if [ ! -d "sonar-scanner" ]; then
                echo ":rocket: Installing SonarQube Scanner..."
                if ! command -v wget &> /dev/null; then
                    echo ":warning: wget not installed. Installing..."
                    sudo apt-get update && sudo apt-get install -y wget || exit 1
                fi
                wget --quiet https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip -O sonar-scanner.zip
                unzip -q sonar-scanner.zip
                mv sonar-scanner-5.0.1.3006-linux sonar-scanner
                chmod +x sonar-scanner/bin/sonar-scanner
            else
                echo ":white_check_mark: SonarQube Scanner is already installed."
            fi
        '''
    }
}

        stage('Create Folder') {
            steps {
                script {
                    echo ":open_file_folder: Setting up output directory..."
                }
                sh 'mkdir -p output'
            }
        }

        stage('Run Python Script') {
            steps {
                script {
                    echo ":snake: Executing Python script..."
                }
                sh 'python3 extract_code.py'
            }
        }

        stage('Verify Extracted Files in Jenkins') {
            steps {
                script {
                    echo ":open_file_folder: Listing extracted files in Jenkins workspace..."
                }
                sh 'ls -R ./output || echo ":rotating_light: No extracted files found!"'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    echo ":mag: Running SonarQube analysis on Java, SQL, and JS files..."
                }
                withEnv(["PATH+SCANNER=${WORKSPACE}/sonar-scanner/bin"]) {
                    sh '''
                        sonar-scanner \
                          -Dsonar.projectKey=testtest \
                          -Dsonar.projectName=testtest \
                          -Dsonar.host.url="${SONAR_HOST_URL}" \
                          -Dsonar.login="${SONAR_TOKEN}" \
                          -Dsonar.sources=./output \
                          -Dsonar.inclusions="**/*.java,**/*.sql,**/*.js" \
                          -Dsonar.java.binaries=. \
                          -Dsonar.scm.disabled=true \
                          -Dsonar.sourceEncoding=UTF-8 \
                          -Dsonar.verbose=true
                    '''
                }
            }
        }


        stage('Post Build Actions') {
            steps {
                archiveArtifacts artifacts: 'output/**', fingerprint: true
                echo ":white_check_mark: Pipeline execution completed successfully."
            }
        }
    }
}

pipeline {
   agent any
   environment {
        SONAR_HOST_URL = 'http://sonarqube:9000'
        SONAR_TOKEN = 'sqp_b1467b24b33dd569eb9ebccb9d4e24f55680e096'
        NEXUS_URL = "http://172.26.0.2:8081"
        NEXUS_USER = "admin"
        NEXUS_PASS = "adminADMIN123"
        REPO_NAME = "raw-joget"
      
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
           /*  stage('Export & Upload JWA to Nexus (joget-repo)') {
           steps {
               script {
                   echo ":package: Fetching application details from Joget..."
               }
               sh '''
               # Installer jq si absent
               if ! command -v jq &> /dev/null; then
                   echo ":wrench: Installing jq..."
                   apt-get update && apt-get install -y jq
               fi                # :one: Définition statique du nom et ID de l’application
               APP_NAME="rsu"
               APP_ID="5"                # :two: Générer un timestamp actuel (YYYYMMDDHHMMSS)
               TIMESTAMP=$(date +"%Y%m%d%H%M%S")                # :three: Construire le nom du fichier JWA avec le bon format
               JWA_FILE="APP_${APP_NAME}-${APP_ID}_${TIMESTAMP}.jwa"                echo ":package: Exporting application: Name=$APP_NAME, ID=$APP_ID, File=$JWA_FILE"                # :four: Créer le dossier d'export dans Joget et fixer les permissions
               docker exec -u root jogetapp bash -c "mkdir -p /opt/joget/export && chmod -R 777 /opt/joget/export"                # :five: Exporter l'application Joget en .jwa
               EXPORT_URL="http://192.168.193.128:8080/jw/web/json/apps/export?appId=${APP_ID}"
               echo ":outbox_tray: Exporting from: $EXPORT_URL"
               docker exec jogetapp bash -c "curl -u admin:admin -o /opt/joget/export/${JWA_FILE} '${EXPORT_URL}'"                # :six: Vérifier la taille du fichier exporté
               FILE_SIZE=$(docker exec jogetapp bash -c "stat -c %s /opt/joget/export/${JWA_FILE}")                if [ "$FILE_SIZE" -lt 1024 ]; then
                   echo ":x: ERREUR: Le fichier JWA exporté semble vide (taille: $FILE_SIZE octets)."
                   exit 1
               fi                echo ":straight_ruler: Taille du fichier exporté: $FILE_SIZE octets"                # :seven: Copier le fichier .jwa depuis Joget vers Jenkins
               docker cp jogetapp:/opt/joget/export/${JWA_FILE} .                # :eight: Vérifier que le fichier existe et a une taille correcte avant de l’uploader
               if [ ! -f "${JWA_FILE}" ]; then
                   echo ":x: ERREUR: Le fichier JWA n'a pas été exporté correctement."
                   exit 1
               fi                # :nine: Uploader le fichier sur Nexus (dans le repository joget-repo)
               echo ":outbox_tray: Uploading ${JWA_FILE} to Nexus (joget-repo)..."
               curl -u admin:Mouhamed2000** --upload-file ${JWA_FILE} \
               "http://192.168.193.128:8082/repository/joget-repo/com/wevioo/jwa/${APP_ID}/${JWA_FILE}"                echo ":white_check_mark: Upload completed successfully to joget-repo!"
               '''
           }
       }    */    stage('Prepare SonarQube Scanner') {
           steps {
               script {
                   echo ":mag: Checking if SonarQube Scanner is installed..."
               }
               sh '''
                   if [ ! -d "sonar-scanner" ]; then
                       echo ":rocket: Installing SonarQube Scanner..."
                       if ! command -v wget &> /dev/null; then
                           echo ":warning: wget non installed. Installing..."
                           apt-get update && apt-get install -y wget || exit 1
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
       stage('create folder ') {
           steps {
               script {
                   echo ":open_file_folder: Setting up output directory..."
               }
               sh '''
              echo output 
               '''
           }
       }
       stage('Run Python Script') {
           steps {
               script {
                   echo ":snake: Executing Python script..."
               }
               sh '''
                  python3 extract_code.py
               '''
           }
       }
  
       stage('Verify Extracted Files in Jenkins') {
           steps {
               script {
                   echo ":open_file_folder: Listing extracted files in Jenkins workspace..."
               }
               sh '''
               ls -R ./output || echo ":rotating_light: No extracted files found!"
               '''
           }
       }
       stage('SonarQube Analysis') {
           steps {
               script {
                   echo ":mag: Running SonarQube analysis on Java, SQL, and JS files..."
               }
               sh '''
                   if [ -d "./output/java" ] || [ -d "./output/sql" ] || [ -d "./output/js" ]; then
                       echo ":white_check_mark: Files found, proceeding with SonarQube analysis..."
                       sonar-scanner/bin/sonar-scanner \
                         -Dsonar.projectKey=yoyo1 \
                         -Dsonar.projectName=yoyo1 \
                         -Dsonar.host.url="${SONAR_HOST_URL}" \
                         -Dsonar.login="${SONAR_TOKEN}" \
                         -Dsonar.sources=./output \
                         -Dsonar.inclusions="**/*.java,**/*.sql,**/*.js" \
                         -Dsonar.java.binaries=. \
                         -Dsonar.scm.disabled=true \
                         -Dsonar.sourceEncoding=UTF-8 \
                         -Dsonar.verbose=true
                   else
                       echo ":rotating_light: ERROR: No Java, SQL, or JS files found in ./output!"
                       exit 1
                   fi
               '''
           }
       }       
           stage('Export Joget App as .jwa') {
            steps {
                script {
                    // Replace 'app_x' with the actual app folder name, e.g. 'rsu_1'
                    sh '''
                    # Navigate to the app folder and create the .jwa file manually
                    docker exec -u root jogetapp bash -c "cd /opt/joget/wflow/app_src/rsu/rsu_1 && zip -r rsu_1.jwa *"
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
                    docker cp jogetapp:/opt/joget/wflow/app_src/rsu/rsu_1.jwa .
                    '''
                }
            }
        }
            stage('Create Nexus Repository') {
            steps {
                script {
                    def createRepoJson = """
                    {
                        "name": "${REPO_NAME}",
                        "online": true,
                        "storage": {
                            "blobStoreName": "default",
                            "strictContentTypeValidation": true,
                            "writePolicy": "ALLOW"
                        }
                    }
                    """
                    sh """
                    curl -X POST -u ${NEXUS_USER}:${NEXUS_PASS} \\
                         -H "Content-Type: application/json" \\
                         -d '${createRepoJson}' \\
                         ${NEXUS_URL}/service/rest/v1/repositories/raw/hosted
                    """
                }
            }
        }

        stage('Upload File to Nexus') {
            steps {
                script {
                    sh """
                    curl -u ${NEXUS_USER}:${NEXUS_PASS} --upload-file ./rsu_1.jwa \\
                    ${NEXUS_URL}/repository/${REPO_NAME}/rsu_1.jwa
                    """
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

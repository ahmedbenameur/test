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

     /*   stage('Export Joget App as .jwa') {
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
        }*/
            stage('Export & Upload JWA to Nexus (joget-repo)') {
            steps {
                script {
                    echo ":colis: Fetching application details from Joget..."
                }
                sh '''
                # Installer jq si absent
                if ! command -v jq &> /dev/null; then
                    echo ":clé_anglaise: Installing jq..."
                    apt-get update && apt-get install -y jq
                fi
                # :un: Définition statique du nom et ID de l’application
                APP_NAME="rsu"
                APP_ID="rsu_5"
                # :deux: Générer un timestamp actuel (YYYYMMDDHHMMSS)
                TIMESTAMP=$(date +"%Y%m%d%H%M%S")
                # :trois: Construire le nom du fichier JWA avec le bon format
                JWA_FILE="APP_${APP_NAME}-${APP_ID}_${TIMESTAMP}.jwa"
                echo ":colis: Exporting application: Name=$APP_NAME, ID=$APP_ID, File=$JWA_FILE"
                # :quatre: Créer le dossier d'export dans Joget et fixer les permissions
                docker exec -u root jogetapp bash -c "mkdir -p /opt/joget/export && chmod -R 777 /opt/joget/export"
                # :cinq: Exporter l'application Joget en .jwa
                EXPORT_URL="http://localhost:8083/jw/web/json/apps/export?appId=${APP_ID}"
                echo ":outbox: Exporting from: $EXPORT_URL"
                docker exec jogetapp bash -c "curl -u admin:admin -o /opt/joget/export/${JWA_FILE} '${EXPORT_URL}'"
                # :six: Vérifier la taille du fichier exporté
                FILE_SIZE=$(docker exec jogetapp bash -c "stat -c %s /opt/joget/export/${JWA_FILE}")
                if [ "$FILE_SIZE" -lt 1024 ]; then
                    echo ":x: ERREUR: Le fichier JWA exporté semble vide (taille: $FILE_SIZE octets)."
                    exit 1
                fi
                echo ":règle: Taille du fichier exporté: $FILE_SIZE octets"
                # :sept: Copier le fichier .jwa depuis Joget vers Jenkins
                docker cp jogetapp:/opt/joget/export/${JWA_FILE} .
                # :huit: Vérifier que le fichier existe et a une taille correcte avant de l’uploader
                if [ ! -f "${JWA_FILE}" ]; then
                    echo ":x: ERREUR: Le fichier JWA n'a pas été exporté correctement."
                    exit 1
                fi
                # :neuf: Uploader le fichier sur Nexus (dans le repository joget-repo)
                echo ":outbox: Uploading ${JWA_FILE} to Nexus (joget-repo)..."
                curl -u admin:adminADMIN123 --upload-file ${JWA_FILE} \
                "http://localhost:8082/repository/joget/com/wevioo/jwa/${APP_ID}/${JWA_FILE}"
                echo ":coche_blanche: Upload completed successfully to joget-repo!"
                '''
            }
        }

    }
}

/*
 * (c) Copyright, Real-Time Innovations, 2024.  All rights reserved.
 * RTI grants Licensee a license to use, modify, compile, and create derivative
 * works of the software solely for use with RTI Connext DDS. Licensee may
 * redistribute copies of the software provided that all such copies are subject
 * to this license. The software is provided "as is", with no warranty of any
 * type, including any warranty for fitness for any purpose. RTI is under no
 * obligation to maintain or support the software. RTI shall not be liable for
 * any incidental or consequential damages arising out of the use or inability
 * to use the software.
 */

pipeline {
    agent {
        docker {
            image 'python:3.8'
            label 'docker'
        }
    }

    options {
        disableConcurrentBuilds()
        /*
            To avoid excessive resource usage in server, we limit the number
            of builds to keep in pull requests
        */
        buildDiscarder(
            logRotator(
                artifactDaysToKeepStr: '',
                artifactNumToKeepStr: '',
                daysToKeepStr: '',
                /*
                   For pull requests only keep the last 10 builds, for regular
                   branches keep up to 20 builds.
                */
                numToKeepStr: changeRequest() ? '10' : '20'
            )
        )
        // Set a timeout for the entire pipeline
        timeout(time: 30, unit: 'MINUTES')
    }

    stages {
        stage('Build doc') {
            steps {
                dir('docs') {
                    sh 'pip install -r requirements.txt --no-cache-dir'
                    sh 'make docs html'
                }
            }

            post {
                success {
                    publishHTML(
                        [
                            allowMissing: false,
                            alwaysLinkToLastBuild: false,
                            keepAll: false,
                            reportDir: 'docs/_build/html/',
                            reportFiles: 'index.html',
                            reportName: 'Connector Documentation',
                            reportTitles: 'Connector Documentation'
                        ]
                    )
                }
            }
        }

        stage('Publish doc') {
            when {
                tag pattern: /v\d+\.\d+\.\d+-doc/, comparator: "REGEXP"
            }

            steps {
                script {
                    def docVersion = env.TAG_NAME.split('-')[0]
                    docVersion = docVersion.replace('v', '')

                    withAWSCredentials {
                        withCredentials([
                            string(credentialsId: 's3-doc-bucket', variable: 'S3_DOC_BUCKET'),
                        ]) {
                            sh "aws s3 sync --acl public-read docs/_build/html/ s3://\$S3_DOC_BUCKET/documentation/connector/${docVersion}/api/python/"
                        }
                    }
                }
            }
        }
    }

    post {
        cleanup {
            cleanWs()
        }
    }
}

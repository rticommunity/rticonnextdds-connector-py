/*
 * (c) Copyright, Real-Time Innovations, 2023.  All rights reserved.
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
        dockerfile {
            additionalBuildArgs  "--build-arg USER_UID=789"
            dir 'resources/docker'
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
        stage('Test') {
            steps {
                sh "pip install tox"
                sh "tox"
            }

            post {
                always {
                    junit(testResults: 'tests-py*.xml')
                }
            }
        }

        stage('Publish') {
            when {
                beforeAgent true
                tag pattern: /v\d+\.\d+\.\d+-dev/, comparator: "REGEXP"
            }

            steps {
                echo "Nothing to be done!"
            }
        }
    }

    post {
        cleanup {
            cleanWs()
        }
    }
}

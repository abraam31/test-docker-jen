def MavenBuild() {
        // Doing the build first on the 
        def maven_image = docker.image('busybox:latest')
        maven_image.pull()
        maven_image.inside(-v /tmp/checking_script:/home/$HOME {
            sh ''' ./home/$HOME/hello.sh '''
            sh ''' sleep 60s '''
			}
}

pipeline {
agent any
stages {
    stage('build') {
        agent any
        steps {
            script {
                MavenBuild()
				}
			}
		}
	}
}
def MavenBuild() {
        // Doing the build first on the 
        def maven_image = docker.image('maven:3-jdk-8')
        maven_image.pull()
        maven_image.inside{
            echo "hello world !"
            sleep 60s
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
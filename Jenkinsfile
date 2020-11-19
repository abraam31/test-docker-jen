def MavenBuild() {
        // Doing the build first on the 
        def maven_image = docker.image('busybox:latest')
        maven_image.pull()
        maven_image.inside('-v /tmp/checking_script:/home') {
            sh ''' echo hello '''
            sh ''' sleep 60s '''
			}
}

pipeline {
agent any
stages {
    stage('build') {
        agent any
		environment {
				PROXY_CONF= '-Dhttp.proxyHost=isp-ceg.emea.cegedim.grp -Dhttp.proxyPort=3128 -Dhttp.nonProxyHosts=*.cegedim.clt -Dhttps.proxyHost=isp-ceg.emea.cegedim.grp -Dhttps.proxyPort=3128 -Dhttps.nonProxyHosts=*.cegedim.clt'
			  }
		steps {
			script {
				echo "$GIT_BRANCH"
			/*
				if(GIT_BRANCH =~ dev*) {
					echo "This is the dev branch"
					}
				else {
					echo "Fuckk off!"
					}
			*/
				MavenBuild()
				echo "$PROXY_CONF"
				}
			}
		}
	}
}
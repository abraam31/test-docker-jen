def MavenBuild() {
        // Doing the build first on the 
        def maven_image = docker.image('busybox:latest')
        maven_image.pull()
        maven_image.inside('-v /tmp/checking_script:/home') {
            sh ''' echo $MESSAGE '''
            sh ''' sleep 60s '''
			}
}

pipeline {
agent any
stages {
	stage('printenv'){
		steps {
			sh 'printenv'
			}
			}
			
    stage('DEV') {
		when {
			  $GIT_BRANCH comparator: 'REGEXP', pattern: '^[a-z].*master'
			  beforeAgent true
			}
		environment {
				PROXY_CONF= '-Dhttp.proxyHost=isp-ceg.emea.cegedim.grp -Dhttp.proxyPort=3128 -Dhttp.nonProxyHosts=*.cegedim.clt -Dhttps.proxyHost=isp-ceg.emea.cegedim.grp -Dhttps.proxyPort=3128 -Dhttps.nonProxyHosts=*.cegedim.clt'
				MESSAGE= 'HELLO FROM DEV'
			  }
		steps {
			script {
				MavenBuild($MESSAGE)
				echo "$PROXY_CONF"
				}
			}
		}
		
    stage('master') {
		when {
			  $GIT_BRANCH comparator: 'REGEXP', pattern: '^[a-z].*master'
			  beforeAgent true
			}
		environment {
				PROXY_CONF= '-Dhttp.proxyHost=isp-ceg.emea.cegedim.grp -Dhttp.proxyPort=3128 -Dhttp.nonProxyHosts=*.cegedim.clt -Dhttps.proxyHost=isp-ceg.emea.cegedim.grp -Dhttps.proxyPort=3128 -Dhttps.nonProxyHosts=*.cegedim.clt'
				MESSAGE= 'HELLO FROM PROD'
			  }
		steps {
			script {
				MavenBuild($MESSAGE)
				echo "$PROXY_CONF"
				}
			}
		}	
	}
}
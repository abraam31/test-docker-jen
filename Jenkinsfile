def MavenBuild(MESSAGE, COMMAND) {
// Doing the build first on the 
	stage("Pulling docker") {
		def maven_image = docker.image('busybox:latest')
		maven_image.pull()
		maven_image.inside('-v /tmp/checking_script:/home') {
			sh """ echo $MESSAGE """
			sh """ $COMMAND """
			sh ''' sleep 60s '''
			}
		}
}


pipeline {
	agent any
	stages {
	
		stage('DEV') {
			when {
				branch comparator: 'REGEXP', pattern: '^[(dev)]*'
				beforeAgent true
				}
			environment {
					PROXY_CONF= '-Dhttp.proxyHost=isp-ceg.emea.cegedim.grp -Dhttp.proxyPort=3128 -Dhttp.nonProxyHosts=*.cegedim.clt -Dhttps.proxyHost=isp-ceg.emea.cegedim.grp -Dhttps.proxyPort=3128 -Dhttps.nonProxyHosts=*.cegedim.clt'
					MESSAGE= 'HELLO FROM DEV'
					command = "echo Hello From DEEEEEEEEEEEEEEEEEEV"
				}
			steps {
				script {
					MavenBuild(env.MESSAGE, env.command)
					echo "$PROXY_CONF"
					sh """ env.command """
					}
				}
			}
			
		stage('master') {
			when {
				branch comparator: 'REGEXP', pattern: '^[(master)(release)]*'
				beforeAgent true
				}
			environment {
					PROXY_CONF= '-Dhttp.proxyHost=isp-ceg.emea.cegedim.grp -Dhttp.proxyPort=3128 -Dhttp.nonProxyHosts=*.cegedim.clt -Dhttps.proxyHost=isp-ceg.emea.cegedim.grp -Dhttps.proxyPort=3128 -Dhttps.nonProxyHosts=*.cegedim.clt'
					MESSAGE= 'HELLO FROM PROD'
					command = "echo Hello From PROOOOOOOOOOOOOOOD"
				}
			steps {
				script {
					MavenBuild(env.MESSAGE, env.command)
					echo "$PROXY_CONF"
					sh """ env.command """
					}
				}
			}	

		stage('ELSE') {
			when {
			  not {
				branch comparator: 'REGEXP', pattern: '^[(master)(release)(dev)]*'
			  }
}
			environment {
					PROXY_CONF= '-Dhttp.proxyHost=isp-ceg.emea.cegedim.grp -Dhttp.proxyPort=3128 -Dhttp.nonProxyHosts=*.cegedim.clt -Dhttps.proxyHost=isp-ceg.emea.cegedim.grp -Dhttps.proxyPort=3128 -Dhttps.nonProxyHosts=*.cegedim.clt'
					MESSAGE= 'HELLO FROM ELSEWHERE'
					command = "echo Hello From ELSEWHEEEEEEEEEEERE"
				}
			steps {
				script {
					MAVEN_COMMAND = "echo Hello From ELSEWHEEEEEEEEEEERE"
					MavenBuild(env.MESSAGE, MAVEN_COMMAND)
					// echo "$PROXY_CONF"
					// sh """ ${env.command} """
					}
				}
			}	
	}
}
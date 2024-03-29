from flask import Flask
import os
import subprocess

app = Flask(__name__)


@app.route('/launchpods/<string:namespace>', methods=['POST'])
def launchPods(namespace):
    print("In launchPods .. Checking to see if Namespace ,",namespace, "exists")
    namespaceExists = subprocess.Popen(["/bin/bash","/k8s-demo-deploy/scripts/namespaceExists.sh",namespace])
    print("Exit code:", namespaceExists.wait())
    if namespaceExists.returncode != 0:
        return 'Error: namespace already exists, aborting\n', 400

    print("Executing setup.sh for ",namespace)
    p = subprocess.Popen(["/bin/bash","/k8s-demo-deploy/scripts/setup.sh",namespace])
    print("Completed setup.sh for ",namespace)

    return "OK"


@app.route('/cleanpods/<string:namespace>', methods=['POST'])
def cleanPods(namespace):
    print("In cleanPods .. Checking to see if Namespace ,",namespace, "exists")
    namespaceExists = subprocess.Popen(["/bin/bash","/k8s-demo-deploy/scripts/namespaceExists.sh",namespace])
    print("Exit code:", namespaceExists.wait())
    if namespaceExists.returncode == 0:
        return 'Error: namespace does not exist, nothing to do\n', 200

    print("Executing setup.sh for ",namespace)
    p = subprocess.Popen(["/bin/bash","/k8s-demo-deploy/scripts/cleanup.sh",namespace])
    print("Completed cleanup.sh for ",namespace)

    return "OK"


@app.route('/deployworkload/<string:namespace>', methods=['POST'])
def deployWorkload(namespace):
    print("In deployWorkloads .. Checking to see if Namespace ,",namespace, "exists")
    namespaceExists = subprocess.Popen(["/bin/bash","/k8s-demo-deploy/scripts/namespaceExists.sh",namespace])
    print("Exit code:", namespaceExists.wait())
    if namespaceExists.returncode == 0:
        return 'Error: namespace does not exist, nothing to do\n', 400

    print("Executing createBrokenStuff.sh for ",namespace)
    p = subprocess.Popen(["/bin/bash","/k8s-demo-deploy/scripts/createBrokenStuff.sh",namespace])
    print("Completed createBrokenStuff.sh for ",namespace)

    return "OK"

@app.route('/deletenamespace/<string:namespace>', methods=['POST'])
def deleteNamespace(namespace):
    print("In deleteNamespace .. Deleting Namespace ,",namespace, "exists")
    namespaceDelete = subprocess.Popen(["kubectl","delete","namespace",namespace],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out, err = namespaceDelete.communicate()
    if (out.decode("utf-8") != ""):
        return out.decode("utf-8")
    else:
        return err.decode("utf-8")


if __name__ == '__main__':
    # default port is 6060
    port = 6060
    if 'SF_PORT' in os.environ:
        port = os.environ['SF_PORT']
    gcloud = subprocess.Popen(["/bin/bash","-c","gcloud container clusters get-credentials standard-cluster-1 --zone us-east1-b --project se-cicd-demo"])
    print("Exit code:", gcloud.wait())
    app.run(host='0.0.0.0', port=port)

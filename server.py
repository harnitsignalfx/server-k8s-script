from flask import Flask
import os
import subprocess

app = Flask(__name__)


@app.route('/launchpods/<string:namespace>', methods=['POST'])
def launchPods(namespace):
    print("In launchPods .. Checking to see if Namespace ,",namespace, "exists")
    namespaceExists = subprocess.Popen(["/home/harnitsingh/k8s-scripts/namespaceExists.sh",namespace])
    print("Exit code:", namespaceExists.wait())
    if namespaceExists.returncode != 0:
        return 'Error: namespace already exists, aborting\n', 400

    print("Executing setup.sh for ",namespace)
    p = subprocess.Popen(["/home/harnitsingh/k8s-scripts/setup.sh",namespace])
    print("Completed setup.sh for ",namespace)

    return "OK"


@app.route('/cleanpods/<string:namespace>', methods=['POST'])
def cleanPods(namespace):
    print("In cleanPods .. Checking to see if Namespace ,",namespace, "exists")
    namespaceExists = subprocess.Popen(["/home/harnitsingh/k8s-scripts/namespaceExists.sh",namespace])
    print("Exit code:", namespaceExists.wait())
    if namespaceExists.returncode == 0:
        return 'Error: namespace does not exist, nothing to do\n', 200

    print("Executing setup.sh for ",namespace)
    p = subprocess.Popen(["/home/harnitsingh/k8s-scripts/cleanup.sh",namespace])
    print("Completed cleanup.sh for ",namespace)

    return "OK"


@app.route('/deployworkload/<string:namespace>', methods=['POST'])
def deployWorkload(namespace):
    print("In deployWorkloads .. Checking to see if Namespace ,",namespace, "exists")
    namespaceExists = subprocess.Popen(["/home/harnitsingh/k8s-scripts/namespaceExists.sh",namespace])
    print("Exit code:", namespaceExists.wait())
    if namespaceExists.returncode == 0:
        return 'Error: namespace does not exist, nothing to do\n', 400

    print("Executing createBrokenStuff.sh for ",namespace)
    p = subprocess.Popen(["/home/harnitsingh/k8s-scripts/createBrokenStuff.sh",namespace])
    print("Completed createBrokenStuff.sh for ",namespace)

    return "OK"


if __name__ == '__main__':
    # default port is 6060
    port = 6060
    if 'SF_PORT' in os.environ:
        port = os.environ['SF_PORT']
    app.run(host='0.0.0.0', port=port)
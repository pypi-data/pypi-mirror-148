from polidoro_argument import Command

from polidoro_cli import CLI


class Kubectl(CLI):

    @staticmethod
    @Command(
        help='Return the pod name',
    )
    def pod_names(filter=''):
        pods, err = Kubectl.execute(
            'get pods -o=custom-columns=NAME:.metadata.name',
            capture_output=True,
            show_cmd=False,
            include_default_command=True
        )
        if filter:
            pods = '\n'.join(p for p in pods.split() if filter in p)
        return pods

    @staticmethod
    @Command(
        help='Run "exec" in the pod',
        aliases=['b']
    )
    def exec(pod_name, command):
        pod = Kubectl.pod_names(pod_name)
        if not pod:
            print('pod name not found!')
            return Kubectl.pod_names()
        pod = pod.split()[0]
        Kubectl.execute(f'exec -it {pod} -- {command}', include_default_command=True)


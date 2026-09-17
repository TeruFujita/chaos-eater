"""Fixed verify for nginx paper case: example-pod stays Running.

LLM is not used. After PodChaos, restartPolicy=Never should fail this check.
Do not treat controller self-heal as success; this Pod has no Deployment.
"""
from __future__ import annotations

import argparse
import os
import time

from kubernetes import client, config


def _load_kube() -> client.CoreV1Api:
    if os.getenv("KUBERNETES_SERVICE_HOST"):
        config.load_incluster_config()
    else:
        config.load_kube_config()
    return client.CoreV1Api()


def pod_running_ratio(namespace: str, pod_name: str, duration: int) -> float:
    v1 = _load_kube()
    running = 0
    for _ in range(duration):
        try:
            pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
            phase = pod.status.phase or ""
            print(f"pod={pod_name} phase={phase}")
            if phase == "Running":
                running += 1
        except client.ApiException as exc:
            print(f"read pod failed: {exc.status}")
        time.sleep(1)
    return (running / duration) * 100 if duration else 0.0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--namespace", default="default")
    parser.add_argument("--pod-name", default="example-pod")
    parser.add_argument("--duration", type=int, default=10)
    parser.add_argument("--threshold", type=float, default=90.0)
    args = parser.parse_args()

    ratio = pod_running_ratio(args.namespace, args.pod_name, args.duration)
    print(f"running_ratio={ratio:.1f}% threshold={args.threshold}%")
    if ratio < args.threshold:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

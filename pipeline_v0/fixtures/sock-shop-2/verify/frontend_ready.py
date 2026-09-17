"""Fixed verify for sock-shop-2 paper case: front-end Ready replicas.

replicas=1 is desired; K8s will recreate one Pod after kill (self-heal).
This check is still useful as a gate. Repair must change desired (e.g. replicas),
not re-create the same replica count.
"""
from __future__ import annotations

import argparse
import os
import time

from kubernetes import client, config


def _load_kube() -> client.AppsV1Api:
    if os.getenv("KUBERNETES_SERVICE_HOST"):
        config.load_incluster_config()
    else:
        config.load_kube_config()
    return client.AppsV1Api()


def ready_ratio(namespace: str, name: str, duration: int) -> tuple[float, int]:
    apps = _load_kube()
    ready_ok = 0
    spec_replicas = 0
    for _ in range(duration):
        dep = apps.read_namespaced_deployment(name=name, namespace=namespace)
        spec_replicas = dep.spec.replicas or 0
        ready = dep.status.ready_replicas or 0
        print(f"deployment={name} ready={ready}/{spec_replicas}")
        if spec_replicas > 0 and ready >= spec_replicas:
            ready_ok += 1
        time.sleep(1)
    ratio = (ready_ok / duration) * 100 if duration else 0.0
    return ratio, spec_replicas


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--namespace", default="sock-shop")
    parser.add_argument("--name", default="front-end")
    parser.add_argument("--duration", type=int, default=15)
    parser.add_argument("--threshold", type=float, default=90.0)
    args = parser.parse_args()

    ratio, spec_replicas = ready_ratio(args.namespace, args.name, args.duration)
    print(f"ready_ratio={ratio:.1f}% spec_replicas={spec_replicas} threshold={args.threshold}%")
    if ratio < args.threshold:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

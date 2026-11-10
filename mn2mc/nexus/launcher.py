"""Run Global 1.7.15 by default, optionally China 1.58 or both."""
from __future__ import annotations
import argparse
import asyncio
import subprocess
import sys
import time
from mn2mc.nexus.editions import apply_edition, plan_edition, validate_dual_ports

def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="MN2MC-Nexus game edition launcher")
    p.add_argument("--mode", choices=("global", "china", "both"))
    p.add_argument("--port", type=int, help="Override one edition's local UDP port")
    p.add_argument("--dry-run", action="store_true", help="Print plan without starting a listener")
    return p

def get_plans(mode, runtime, port_override=None):
    if mode not in ("global", "china", "both"):
        raise ValueError("Unknown execution mode")
    if port_override is not None and not 1 <= port_override <= 65535:
        raise ValueError("Port out of range")
    if mode == "both" and port_override is not None:
        raise ValueError("--port cannot be combined with --mode both")
    gp = port_override if mode == "global" and port_override is not None else runtime.global_port
    cp = port_override if mode == "china" and port_override is not None else runtime.china_port
    if mode == "both":
        validate_dual_ports(gp, cp)
    selected = ("global", "china") if mode == "both" else (mode,)
    return [plan_edition(edition, gp, cp, runtime.global_client_version_code) for edition in selected]

def run_both(plans) -> int:
    processes = []
    try:
        for edition in plans:
            processes.append(subprocess.Popen(
                [sys.executable, "-m", "mn2mc.nexus.launcher",
                 "--mode", edition.edition, "--port", str(edition.port)]
            ))
        while True:
            for child in processes:
                return_code = child.poll()
                if return_code is not None:
                    if return_code:
                        print("One edition stopped with an error; stopping all listeners.", file=sys.stderr)
                    return return_code
            time.sleep(0.25)
    except KeyboardInterrupt:
        return 130
    finally:
        for child in processes:
            if child.poll() is None:
                child.terminate()
        for child in processes:
            try:
                child.wait(timeout=8)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait()

def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    import mn2mc.config as config
    config.load()
    mode = args.mode or config.nexus.runtime.mode
    try:
        editions = get_plans(mode, config.nexus.runtime, args.port)
    except ValueError as exc:
        parser().error(str(exc))
    print("MN2MC-Nexus edition plan:", flush=True)
    for edition in editions:
        print(f"  {edition.edition}: Mini World {edition.mini_version}, "
              f"UDP {edition.port}, {edition.status}", flush=True)
    if any(edition.edition == "global" for edition in editions):
        print("WARNING: Global 1.7.15 is an experimental local listener reusing "
              "UNVERIFIED China 1.58 Protobuf handlers. This is NOT validated crossplay "
              "or regional login/room hosting.", flush=True)
    if args.dry_run:
        return 0
    if mode == "both":
        return run_both(editions)
    apply_edition(editions[0], config)
    # Import only after selecting edition: some modules build packets at import time.
    from mn2mc.nexus import bridge
    try:
        asyncio.run(bridge.main())
    except KeyboardInterrupt:
        return 130
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

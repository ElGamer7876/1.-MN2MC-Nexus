"""Run the proven China baseline by default; Global 1.7.15 is explicit BETA."""
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
    p.add_argument("--list-regions", action="store_true", help="List research-only Global endpoint candidates (offline)")
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
    selected = ("china", "global") if mode == "both" else (mode,)
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
    if args.list_regions:
        from mn2mc.nexus.regions import REGIONS
        print("Global 1.7.15 BETA: UNVERIFIED candidate hosts from community client XML")
        for code, region in REGIONS.items():
            print(f"  {code.upper():10s} room={region.room_host}:{region.room_port} "
                  f"account={region.auth_host}:{region.auth_port} "
                  f"source={region.source_file}")
        print("No connection or authentication was attempted.")
        return 0
    runtime = config.nexus.runtime
    # Old files may still contain mode=global; do NOT silently enable BETA.
    if args.mode is None and runtime.mode != "china" and not runtime.global_beta_enabled:
        print("Saved experimental mode is disabled. Starting China instead. "
              "Enable BETA in the setup wizard or pass --mode global/both.", flush=True)
    mode = args.mode or (runtime.mode if runtime.global_beta_enabled else "china")
    try:
        editions = get_plans(mode, config.nexus.runtime, args.port)
    except ValueError as exc:
        parser().error(str(exc))
    print("MN2MC-Nexus edition plan:", flush=True)
    for edition in editions:
        print(f"  {edition.edition}: Mini World {edition.mini_version}, "
              f"UDP {edition.port}, {edition.status}", flush=True)
    if any(edition.edition == "global" for edition in editions):
        print("WARNING: Global 1.7.15 is BETA and uses an experimental local listener reusing "
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

import argparse
import sys

from . import __version__, storage
from .authorization import (
    EXIT_ABORT,
    AuthorizationError,
    now_iso,
    record_authorization,
    require_authorization,
)
from .pipeline import PipelineError, run_scan_and_report
from .report import terminal_summary
from .scan import ScanError, validate_target


def build_parser():
    parser = argparse.ArgumentParser(
        prog="noobmap",
        description="Varredura de segurança guiada para redes de clientes (Kali Live).",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="noobmap " + __version__,
    )
    sub = parser.add_subparsers(dest="command")
    scan = sub.add_parser(
        "scan",
        help="Executa uma varredura guiada (requer autorização escrita).",
    )
    scan.add_argument(
        "--autorizado",
        action="store_true",
        help="Confirma que você tem autorização escrita (RoE) do cliente.",
    )
    scan.add_argument(
        "--cliente",
        help="Nome do cliente (registrado no relatório).",
    )
    scan.add_argument(
        "--rede",
        help="Rede alvo em CIDR privado, ex.: 192.168.1.0/24",
    )
    scan.add_argument(
        "--saida",
        default="noobmap-out",
        help="Pasta de saída (relatório + registro de autorização). Padrão: noobmap-out",
    )
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "scan":
        try:
            require_authorization(args.autorizado, args.cliente)
        except AuthorizationError as exc:
            print("noobmap: " + str(exc), file=sys.stderr)
            return EXIT_ABORT

        rede = None
        if args.rede:
            try:
                rede = validate_target(args.rede)
            except ScanError as exc:
                print("noobmap: " + str(exc), file=sys.stderr)
                return 2

        quando = now_iso()
        try:
            dest = storage.run_dir(args.saida, args.cliente, quando)
        except storage.StorageError as exc:
            print("noobmap: " + str(exc), file=sys.stderr)
            return 2
        path, record = record_authorization(dest, args.cliente, quando, rede)
        print(
            'Autorização registrada para "{cliente}" em {quando}.'.format(
                cliente=record["cliente"], quando=record["autorizado_em"]
            )
        )

        if not args.rede:
            print("Registro salvo em: {p}".format(p=path))
            print("Falta a rede alvo. Rode de novo com --rede 192.168.1.0/24 para escanear.")
            return 0

        try:
            findings, report_path = run_scan_and_report(
                args.cliente, quando, rede, dest
            )
        except (ScanError, PipelineError) as exc:
            print("noobmap: " + str(exc), file=sys.stderr)
            return 1

        print(terminal_summary(findings, report_path))
        print("Arquivos salvos em: {d}".format(d=dest))
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
